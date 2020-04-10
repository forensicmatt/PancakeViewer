# -*- coding: utf-8 -*-
import wx.propgrid

from dfvfs.helpers import source_scanner
from dfvfs.lib import definitions
from dfvfs.volume import volume_system
from dfvfs.volume import vshadow_volume_system
from dfvfs.resolver import resolver

from dfvfs.vfs import ntfs_file_system
from dfvfs.vfs import tsk_file_entry

def EnumerateProperties(property_grid_1, node):
    # Clear previous properties
    property_grid_1.Clear()
    properties = []

    if isinstance(node, source_scanner.SourceScanNode):
        if node.type_indicator == definitions.TYPE_INDICATOR_OS:
            properties = OsProperties(node)
        elif node.type_indicator == definitions.TYPE_INDICATOR_EWF:
            properties = EwfProperties(node)
        elif node.type_indicator == definitions.TYPE_INDICATOR_TSK_PARTITION:
            properties = TskPartitionProperties(node)
        elif node.type_indicator == definitions.TYPE_INDICATOR_TSK:
            properties = TskProperties(node)
        elif node.type_indicator == definitions.TYPE_INDICATOR_VSHADOW:
            properties = VshadowProperties(node)
        else:
            raise Exception(u'Unhandled type enumeration. type: {}'.format(node.type_indicator))
    elif isinstance(node, tsk_file_entry.TSKFileEntry):
            properties = TskFileEntryProperties(node)
    else:
        raise Exception(u'Unhandled Class in Property Enumeration. type: {}'.format(str(type(node))))

    for prop in properties:
        property_grid_1.Append(prop)

class OsProperties(list):
    def __init__(self, node):
        self.append(wx.propgrid.PropertyCategory("OS Path Spec"))
        self.append(wx.propgrid.StringProperty("Location", value=getattr(node.path_spec, 'location', None)))

class TskFileEntryProperties(list):
    def __init__(self, node):
        self.append(wx.propgrid.StringProperty("Full Path",
            value=u'{}'.format(node.full_path.encode('utf-8', u'replace'))))
        self.append(wx.propgrid.PropertyCategory("TSK File Meta Info"))
        meta = node._tsk_file.info.meta

        self.append(wx.propgrid.StringProperty(
            "Type", value=u'{}'.format(meta.type)))
        self.append(wx.propgrid.StringProperty(
            "Flags", value=u'{}'.format(meta.flags)))
        self.append(wx.propgrid.UIntProperty(
            "Address", value=meta.addr))
        self.append(wx.propgrid.IntProperty(
            "Sequence", value=meta.seq))
        self.append(wx.propgrid.UIntProperty(
            "Creation Time", value=meta.crtime))
        self.append(wx.propgrid.UIntProperty(
            "MFT Change Time", value=meta.ctime))
        self.append(wx.propgrid.UIntProperty(
            "Modified Time", value=meta.mtime))
        self.append(wx.propgrid.UIntProperty(
            "Access Time", value=meta.atime))
        self.append(wx.propgrid.UIntProperty(
            "Size", value=meta.size))

class EwfProperties(list):
    def __init__(self, node):
        ewf = resolver.Resolver.OpenFileObject(node.path_spec)

        self.append(wx.propgrid.PropertyCategory("EWF Information"))
        self.append(wx.propgrid.StringProperty("Header Codepage",
            value=u'{}'.format(getattr(ewf._file_object, 'header_codepage', None))))
        self.append(wx.propgrid.StringProperty("Media Size",
             value=u'{}'.format(getattr(ewf._file_object, 'media_size', None))))

        dict_hash = ewf._file_object.get_hash_values()
        for key in dict_hash:
            value = dict_hash[key]
            self.append(wx.propgrid.StringProperty(key, value=u'{}'.format(value)))

        header_values = ewf._file_object.get_header_values()
        for key in header_values:
            value = header_values[key]
            self.append(wx.propgrid.StringProperty(key, value=u'{}'.format(value)))

class TskPartitionProperties(list):
    def __init__(self, node):
        file_system = resolver.Resolver.OpenFileSystem(node.path_spec)

        for volume in file_system._tsk_volume:
            if volume.addr == node.path_spec.part_index:
                # TSK Partition Info
                self.append(wx.propgrid.PropertyCategory("TSK Partition Info"))
                self.append(wx.propgrid.StringProperty("Partition Address",
                                                       value=u'{}'.format(getattr(volume, 'addr', None))))
                self.append(wx.propgrid.StringProperty("Description",
                                                       value=getattr(volume, 'desc', None)))
                self.append(wx.propgrid.StringProperty("Size",
                                                       value=u'{}'.format(getattr(volume, 'len', None))))
                self.append(wx.propgrid.StringProperty("Slot Number",
                                                       value=u'{}'.format(getattr(volume, 'slot_num', None))))
                self.append(wx.propgrid.StringProperty("Starting Offset",
                                                       value=u'{}'.format(getattr(volume, 'start', ''))))
                self.append(wx.propgrid.StringProperty("Table Number",
                                                       value=u'{}'.format(getattr(volume, 'table_num', None))))
                self.append(wx.propgrid.StringProperty("Tag",
                                                       value=u'{}'.format(getattr(volume, 'tag', None))))

class TskProperties(list):
    def __init__(self, node):
        try:
            file_system = resolver.Resolver.OpenFileSystem(node.path_spec)
        except Exception as error:
            self.append(wx.propgrid.PropertyCategory("Info"))
            self.append(wx.propgrid.StringProperty("Description",
                                                   value=u'Cannot open filesystem.'))
            self.append(wx.propgrid.StringProperty("Error",
                                                   value=u'{}'.format(error)))
            return

        if file_system is not None:
            tsk_fs_info = file_system._tsk_file_system.info

            self.append(wx.propgrid.PropertyCategory("TSK File System Info"))
            self.append(wx.propgrid.StringProperty(
                "Block Count", value=u'{}'.format(getattr(tsk_fs_info, 'block_count', None))))
            self.append(wx.propgrid.StringProperty(
                "Block Post Size", value=u'{}'.format(getattr(tsk_fs_info, 'block_post_size', None))))
            self.append(wx.propgrid.StringProperty(
                "Block Pre Size", value=u'{}'.format(getattr(tsk_fs_info, 'block_pre_size', None))))
            self.append(wx.propgrid.StringProperty(
                "Block Size", value=u'{}'.format(getattr(tsk_fs_info, 'block_size', None))))
            self.append(wx.propgrid.StringProperty(
                "Dev Block Size", value=u'{}'.format(getattr(tsk_fs_info, 'dev_bsize', None))))
            self.append(wx.propgrid.StringProperty(
                "Endian", value=u'{}'.format(getattr(tsk_fs_info, 'endian', None))))
            self.append(wx.propgrid.StringProperty(
                "First Block", value=u'{}'.format(getattr(tsk_fs_info, 'first_block', None))))
            self.append(wx.propgrid.StringProperty(
                "First Inode", value=u'{}'.format(getattr(tsk_fs_info, 'first_inode', None))))
            self.append(wx.propgrid.StringProperty(
                "Flags", value=u'{}'.format(getattr(tsk_fs_info, 'flags', None))))
            self.append(wx.propgrid.StringProperty(
                "File System ID Used", value=u'{}'.format(getattr(tsk_fs_info, 'fs_id_used', None))))
            self.append(wx.propgrid.StringProperty(
                "File System Type", value=u'{}'.format(getattr(tsk_fs_info, 'ftype', None))))
            self.append(wx.propgrid.StringProperty(
                "Inode Count", value=u'{}'.format(getattr(tsk_fs_info, 'inum_count', None))))
            self.append(wx.propgrid.StringProperty(
                "Journal Inode", value=u'{}'.format(getattr(tsk_fs_info, 'journ_inum', None))))
            self.append(wx.propgrid.StringProperty(
                "Last Block", value=u'{}'.format(getattr(tsk_fs_info, 'last_block', None))))
            self.append(wx.propgrid.StringProperty(
                "Last Block Actual", value=u'{}'.format(getattr(tsk_fs_info, 'last_block_act', None))))
            self.append(wx.propgrid.StringProperty(
                "Last Inode", value=u'{}'.format(getattr(tsk_fs_info, 'last_inum', None))))
            self.append(wx.propgrid.StringProperty(
                "Offset", value=u'{}'.format(getattr(tsk_fs_info, 'offset', None))))
            self.append(wx.propgrid.StringProperty(
                "Orphan Dir", value=u'{}'.format(getattr(tsk_fs_info, 'orphan_dir', None))))
            self.append(wx.propgrid.StringProperty(
                "Root Inode", value=u'{}'.format(getattr(tsk_fs_info, 'root_inum', None))))
            self.append(wx.propgrid.StringProperty(
                "Tag", value=u'{}'.format(getattr(tsk_fs_info, 'tag', None))))

class VshadowProperties(list):
    def __init__(self, node):
        if node.path_spec.store_index is None:
            # VSS Root
            vss = vshadow_volume_system.VShadowVolumeSystem()
            vss.Open(node.path_spec)

            for shadow_volume in vss.volumes:
                self.append(
                    wx.propgrid.PropertyCategory(
                        u'{}'.format(shadow_volume.identifier)
                    )
                )
                for attribute in shadow_volume.attributes:
                    self.append(
                        wx.propgrid.StringProperty(
                            u'{} {}'.format(shadow_volume.identifier, attribute.identifier),
                            value=u'{}'.format(attribute.value)
                        )
                    )
        else:
            # VSS Index
            vss = vshadow_volume_system.VShadowVolumeSystem()
            vss.Open(node.path_spec)

            vss_index = node.path_spec.store_index
            vss_label = node.path_spec.location[1:]

            _vss_cnt = 0
            for shadow_volume in vss.volumes:
                if vss_label == shadow_volume.identifier:
                    self.append(
                        wx.propgrid.PropertyCategory(
                            u'{}'.format(shadow_volume.identifier)
                        )
                    )
                    for attribute in shadow_volume.attributes:
                        self.append(
                            wx.propgrid.StringProperty(
                                u'{} {}'.format(shadow_volume.identifier, attribute.identifier),
                                value=u'{}'.format(attribute.value)
                            )
                        )
                    _vss_cnt += 1
