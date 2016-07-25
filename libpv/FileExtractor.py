# -*- coding: utf-8 -*-
import multiprocessing
import threading
import os
from dfvfs.vfs.tsk_file_entry import TSKFileEntry

class FileExtractor(multiprocessing.Process):
    def __init__(self,**kwargs):
        super(FileExtractor, self).__init__()
        self.file_queue = multiprocessing.Queue()

        if 'out_path' not in kwargs:
            raise Exception(u'out_path is required argument for FileExtractor() class')

        self.out_path = kwargs['out_path']
        pass

    def run(self):
        print(u"Running File Extractor: (PID {})".format(
            os.getpid()
        ))

        # Read from the queue
        while True:
            file_item = self.file_queue.get()
            if isinstance(file_item,unicode):
                if (file_item == u'TERMINATE'):
                    break
            elif isinstance(file_item,TSKFileEntry):
                print(u"Extracting {} to location -> {}".format(
                    file_item.full_path,
                    self.out_path
                ))
            else:
                print(u"Item type unhandled for type: {}; {}".format(
                    unicode(type(file_item)),
                    unicode(file_item)
                ))

        print(u"Ending File Extractor: (PID {})".format(
            os.getpid()
        ))

    def AddFileToQueue(self,tsk_file_entry):
        self.file_queue.put(tsk_file_entry)

    def Finish(self):
        self.file_queue.put(u'TERMINATE')