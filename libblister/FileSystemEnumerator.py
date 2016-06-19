# -*- coding: utf-8 -*-
from dfvfs.helpers import source_scanner
from dfvfs.lib import definitions

def EnumerateNode(mainFrame,tree_item,node):
    if isinstance(node, source_scanner.SourceScanNode):
        if node.type_indicator == definitions.TYPE_INDICATOR_TSK:
            # Open File System here if not already opened
            pass
    pass

class FileSystemManager():
    def __init__(self,mainFrame):
        self.mainFrame = mainFrame