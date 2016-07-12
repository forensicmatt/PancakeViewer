# -*- coding: utf-8 -*-
import wx
from dfvfs.helpers import source_scanner
from dfvfs.lib import definitions
from dfvfs.resolver import resolver
from dfvfs.volume import volume_system,vshadow_volume_system
from dfvfs.path import factory as path_spec_factory

def EnumerateNode(mainFrame,tree_item,node):
    if isinstance(node, source_scanner.SourceScanNode):
        if (node.type_indicator == definitions.TYPE_INDICATOR_TSK or
            node.type_indicator == definitions.TYPE_INDICATOR_VSHADOW):
            if mainFrame.tree_fs.GetChildrenCount(tree_item) < 1:
                if node.type_indicator == definitions.TYPE_INDICATOR_VSHADOW:
                    location = getattr(node.path_spec, 'location', None)
                    if location == u'/':
                        return
                    identifier = location[1:]
                try:
                    path_spec = node.path_spec
                    if node.type_indicator == definitions.TYPE_INDICATOR_VSHADOW:
                        path_spec = path_spec_factory.Factory.NewPathSpec(
                            definitions.TYPE_INDICATOR_TSK, location=u'/',
                            parent=node.path_spec)
                    file_system = resolver.Resolver.OpenFileSystem(path_spec)
                except Exception as error:
                    file_system = None
                    print str(error)

                if file_system is not None:
                    #file_entry = resolver.Resolver.OpenFileEntry(node.path_spec)
                    file_entry = file_system.GetRootFileEntry()

                    ProcessFolder(
                        file_system,
                        file_entry,
                        u'',
                        tree_fs=mainFrame.tree_fs,
                        tree_item=tree_item
                )
    pass

def ProcessFolder(file_system, file_entry, parent_full_path,tree_fs=None,tree_item=None):
    full_path = parent_full_path + u'/' + file_entry.name
    file_entry.full_path = full_path
    if file_entry.IsDirectory():
        #print full_path.encode('utf-8', u'replace')
        if tree_item:
            entry_name = file_entry.name

            if file_entry.IsRoot():
                entry_name = '[root]'

            folder_tree_item = tree_fs.AppendItem(
                tree_item,
                entry_name
            )
            item_data = wx.TreeItemData(
                file_entry
            )
            # Set Client Data
            tree_fs.SetItemData(
                folder_tree_item,
                item_data
            )
            # Set Icons for this node
            SetNodeIcons(file_entry, tree_fs, folder_tree_item)
        else:
            folder_tree_item = None

    for sub_file_entry in file_entry.sub_file_entries:
        ProcessFolder(file_system, sub_file_entry, full_path,tree_fs=tree_fs,tree_item=folder_tree_item)

def SetNodeIcons(file_entry, tree_fs, tree_item):
    icon_list = GetIcons(
        tree_fs,
        file_entry
    )
    for icon in icon_list:
        tree_fs.SetItemImage(tree_item, icon[0], icon[1])

def GetIcons(tree_fs, file_entry):
    icon_list = []
    if file_entry.type_indicator == definitions.TYPE_INDICATOR_TSK:
        icon_list.append([tree_fs.icon_fldridx, wx.TreeItemIcon_Normal])
        icon_list.append([tree_fs.icon_fldropenidx, wx.TreeItemIcon_Expanded])
    else:
        icon_list.append([tree_fs.icon_fldridx, wx.TreeItemIcon_Normal])
        icon_list.append([tree_fs.icon_fldropenidx, wx.TreeItemIcon_Expanded])

    return icon_list

class FileSystemManager():
    def __init__(self,mainFrame):
        self.mainFrame = mainFrame
        self.opened_fs = {}