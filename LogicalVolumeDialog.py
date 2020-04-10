# -*- coding: CP1252 -*-
#
# generated by wxGlade 0.7.2 on Tue Jun 21 00:40:16 2016
#
import sys
import wx

if sys.platform == 'win32':
    import win32api

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class LogicalVolumeDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: LogicalVolumeDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((400, 115))
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_4 = wx.Panel(self, wx.ID_ANY)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Select Logical Volume: "))
        self.panel_7 = wx.Panel(self, wx.ID_ANY)
        self.combo_logical_volumes = wx.ComboBox(self, wx.ID_ANY, choices=[], style=0)
        self.panel_8 = wx.Panel(self, wx.ID_ANY)
        self.panel_3 = wx.Panel(self, wx.ID_ANY)
        self.panel_5 = wx.Panel(self, wx.ID_ANY)
        self.button_select = wx.Button(self, wx.ID_OK, _("Select"))
        self.panel_9 = wx.Panel(self, wx.ID_ANY)
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
        self.panel_6 = wx.Panel(self, wx.ID_ANY)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.button_select_click, self.button_select)
        self.Bind(wx.EVT_BUTTON, self.button_cancel_click, self.button_cancel)
        # end wxGlade

        self.PopulateVolumes()

    def __set_properties(self):
        # begin wxGlade: LogicalVolumeDialog.__set_properties
        self.SetTitle(_("Select Logical Volume"))
        self.SetSize((400, 115))
        self.panel_1.SetMinSize((379, 5))
        self.panel_4.SetMinSize((5, 25))
        self.panel_7.SetMinSize((5, 25))
        self.panel_3.SetMinSize((379, 10))
        self.panel_5.SetMinSize((5, 26))
        self.panel_9.SetMinSize((5, 26))
        self.panel_6.SetMinSize((93, 20))
        self.panel_2.SetMinSize((379, 5))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: LogicalVolumeDialog.__do_layout
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12.Add(self.panel_1, 0, wx.EXPAND, 0)
        sizer_13.Add(self.panel_4, 0, 0, 0)
        sizer_13.Add(self.label_1, 0, wx.EXPAND, 0)
        sizer_13.Add(self.panel_7, 0, 0, 0)
        sizer_13.Add(self.combo_logical_volumes, 1, wx.EXPAND, 0)
        sizer_13.Add(self.panel_8, 0, 0, 0)
        sizer_12.Add(sizer_13, 0, 0, 0)
        sizer_12.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_14.Add(self.panel_5, 0, 0, 0)
        sizer_14.Add(self.button_select, 0, wx.EXPAND, 0)
        sizer_14.Add(self.panel_9, 0, wx.EXPAND, 0)
        sizer_14.Add(self.button_cancel, 0, wx.EXPAND, 0)
        sizer_14.Add(self.panel_6, 1, 0, 0)
        sizer_12.Add(sizer_14, 0, 0, 0)
        sizer_12.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_11.Add(sizer_12, 1, 0, 0)
        self.SetSizer(sizer_11)
        self.Layout()
        # end wxGlade

    def button_select_click(self, event):  # wxGlade: LogicalVolumeDialog.<event_handler>
        print("Event handler 'button_select_click' not implemented!")
        event.Skip()

    def button_cancel_click(self, event):  # wxGlade: LogicalVolumeDialog.<event_handler>
        print("Event handler 'button_cancel_click' not implemented!")
        event.Skip()

    def PopulateVolumes(self):
        if sys.platform == 'win32':
            volume_list_string = win32api.GetLogicalDriveStrings()
            volume_list = volume_list_string.split('\x00')
            for volume_name in volume_list:
                if volume_name != '':
                    self.combo_logical_volumes.Append('\\\\.\\{}'.format(volume_name[:-1]))
        elif sys.platform == 'linux':
            # Parse /proc/partitions for connected partitions
            with open('/proc/partitions', 'r') as proc_file:
                raw_parts = proc_file.readlines()
            parts = [i.split()[-1] for i in raw_parts[2:]]

            for part in parts:
                self.combo_logical_volumes.Append(f"/dev/{part}")
        else:
            print("Platform not supported")

# end of class LogicalVolumeDialog
