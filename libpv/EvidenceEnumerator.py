# -*- coding: utf-8 -*-
import wx
import os
import re
import logging
from dfvfs.credentials import manager as credentials_manager
from dfvfs.path import factory as path_spec_factory
from dfvfs.helpers import source_scanner
from dfvfs.analyzer import analyzer
from dfvfs.resolver import resolver
from dfvfs.lib import definitions
from dfvfs.path import factory
from dfvfs.vfs import ntfs_file_system
from dfvfs.volume import volume_system
from libpv import Properties


class EvidenceManager():
    def __init__(self,mainFrame):
        self.mainFrame = mainFrame

    def EnumerateEvidenceSource(self, filename):
        evidenceContainer = EvidenceContainer()
        evidenceContainer.OpenSourcePath(filename)

        match = re.match(r"^\\\\\.\\([a-zA-Z])\:$", filename)

        if match:
            os_path_spec = path_spec_factory.Factory.NewPathSpec(
                definitions.TYPE_INDICATOR_OS,
                location=filename
            )
            logical_path_spec = path_spec_factory.Factory.NewPathSpec(
                definitions.TYPE_INDICATOR_TSK,
                location=u'/',
                parent=os_path_spec
            )

            scan_path_spec = logical_path_spec
        else:
            scan_path_spec = None

        _source_scanner = source_scanner.SourceScanner()
        _source_scanner.Scan(
            evidenceContainer,
            auto_recurse=True,
            scan_path_spec=scan_path_spec
        )
        if match:
            evidenceContainer.AddScanNode(
                logical_path_spec,
                evidenceContainer.GetRootScanNode()
            )
        _root_node = evidenceContainer.GetRootScanNode()

        root = self.mainFrame.tree_fs.GetRootItem()

        evidenceContainer._EnumerateTree(
            self.mainFrame.tree_fs,
            root
        )

class EvidenceContainer(source_scanner.SourceScannerContext):
    def __init__(self):
        source_scanner.SourceScannerContext.__init__(self)

    def _EnumerateTree(self,tree_fs,tree_item):
        _root_node = self.GetRootScanNode()
        self._ProcessNode(
            tree_fs,
            tree_item,
            _root_node
        )

    def PrintDriveLayout(self):
        #Get Root node#
        _root_node = self.GetRootScanNode()

        self._ProcessNode(_root_node)

    def _ProcessFs(self,file_system_path_spec):
        try:
            file_system = resolver.Resolver.OpenFileSystem(file_system_path_spec)
        except Exception as error:
            file_system = None

        if file_system:
            file_entry = resolver.Resolver.OpenFileEntry(file_system_path_spec)
            if file_entry is None:
                logging.warning(
                    u'Unable to open base path specification:\n{0:s}'.format(
                        file_system_path_spec.comparable)
                )
                return
            self._ProcessFile(file_entry,file_entry,u'')

        pass

    def _ProcessFile(self,file_system, file_entry, parent_full_path):
        full_path = parent_full_path + u'/' + file_entry.name

        print(full_path.encode('utf-8',u'replace'))

        for data_stream in file_entry.data_streams:
            if data_stream.name:
                print(u'{}:{}'.format(full_path, data_stream.name).encode('utf-8',u'replace'))

        for sub_file_entry in file_entry.sub_file_entries:
            self._ProcessFile(file_system, sub_file_entry, full_path)

    def _SetNodeIcons(self,scan_node,tree_fs,tree_item):
        icon_list = self._GetIcons(
            tree_fs,
            scan_node
        )
        for icon in icon_list:
            tree_fs.SetItemImage(tree_item, icon[0], icon[1])

    def _GetAlias(self,scan_node):
        """Generate a string alias for a given node to represent it by in the tree view.

        :param scan_node: <SourceScanNode> The scan node to create an alias for.
        :return: <str> The name to represent this item on the tree naviagter
        """
        alias = scan_node.type_indicator

        if scan_node.type_indicator == definitions.TYPE_INDICATOR_OS:
            alias = getattr(scan_node.path_spec, 'location', None)

            match = re.match(r"^\\\\\.\\([a-zA-Z])\:$",alias)
            if match:
                alias = alias[4:6]
            else:
                alias = os.path.basename(alias)
        elif scan_node.type_indicator == definitions.TYPE_INDICATOR_TSK_PARTITION:
            if scan_node.path_spec.part_index is not None:
                alias = u'Partition Index - {}'.format(scan_node.path_spec.part_index)
                file_system = resolver.Resolver.OpenFileSystem(scan_node.path_spec)
                for volume in file_system._tsk_volume:
                    if volume.addr == scan_node.path_spec.part_index:
                        alias = u'{}'.format(volume.desc)
                        break
            else:
                return None
        elif scan_node.type_indicator == definitions.TYPE_INDICATOR_TSK:
            file_system = None

            try:
                file_system = resolver.Resolver.OpenFileSystem(scan_node.path_spec)
            except Exception as error:
                print(
                    u"Cannot open file system. [comparable]({})".format(
                        scan_node.path_spec.comparable)
                )

            if file_system is not None:
                if file_system.IsNTFS():
                    # Get File System Label
                    ntfs = ntfs_file_system.NTFSFileSystem(None)
                    ntfs._Open(scan_node.path_spec)
                    if ntfs._fsntfs_volume.name is not None:
                        alias = ntfs._fsntfs_volume.name
                    else:
                        #alias = unicode(file_system._tsk_fs_type)
                        alias = u'NONAME'
                else:
                    alias = getattr(scan_node.path_spec, 'location', None)
                    alias = os.path.basename(alias)

        elif scan_node.type_indicator == definitions.TYPE_INDICATOR_VSHADOW:
            alias = getattr(scan_node.path_spec, 'location', None)

            # Remove preceding '/'
            if alias is not None:
                alias = alias[1:]
            # If no location, then set as 'VSHADOW' (for a vss root)
            if alias == '':
                alias = 'Volume Shadow Stores'
            else:
                alias = os.path.basename(alias)

        return alias

    def _ProcessNode(self,tree_fs,parent_item,scan_node):
        print('{}'.format(scan_node.type_indicator))

        # Get alias
        alias = self._GetAlias(scan_node)

        if alias is not None:
            # Set GUI Tree Item
            tree_item = tree_fs.AppendItem(
                parent_item,
                alias
            )
            item_data = wx.TreeItemData(
                scan_node
            )
            # Set Client Data
            tree_fs.SetItemData(
                tree_item,
                item_data
            )

            # Set Icons for this node
            self._SetNodeIcons(scan_node,tree_fs,tree_item)
        else:
            tree_item = parent_item

        if (scan_node.type_indicator == definitions.TYPE_INDICATOR_TSK):
            print('FILESYSTEM')
            #self._ProcessFs(scan_node.path_spec)
        elif (scan_node.type_indicator == definitions.TYPE_INDICATOR_VSHADOW):
            print('FILESYSTEM [VSS]')
            path_spec = factory.Factory.NewPathSpec(
                definitions.TYPE_INDICATOR_TSK,
                location=u'/',
                parent=scan_node.path_spec
            )
            #self._ProcessFs(path_spec)

        for sub_scan_node in scan_node.sub_nodes:
            self._ProcessNode(tree_fs,tree_item,sub_scan_node)

    def _GetIcons(self,tree_fs,sub_scan_node):
        icon_list = []
        if sub_scan_node.type_indicator == definitions.TYPE_INDICATOR_TSK:
            icon_list.append([tree_fs.icon_fldridx, wx.TreeItemIcon_Normal])
            icon_list.append([tree_fs.icon_fldropenidx, wx.TreeItemIcon_Expanded])
        else:
            icon_list.append([tree_fs.icon_fldridx, wx.TreeItemIcon_Normal])
            icon_list.append([tree_fs.icon_fldropenidx, wx.TreeItemIcon_Expanded])

        return icon_list
