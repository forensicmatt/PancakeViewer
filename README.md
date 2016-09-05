# Pancake Viewer
A DFVFS backed viewer project with a WxPython GUI.

Feedback, suggestions, help... its all welcome. With the right teamwork, we could make this a neat tool.

# Dependencies
- DFVFS
  - Homepage: https://github.com/log2timeline/dfvfs
  - Wiki: https://github.com/log2timeline/dfvfs/wiki
  - How to build: https://github.com/log2timeline/dfvfs/wiki/Building
- WxPython (v3.0)
  - Homepage: https://www.wxpython.org/
  - Compiled Binaries: https://www.wxpython.org/download.php
  
# Future Functionality
First priority is to allow extraction of files.
Other short term priorities include:
- Plugin viewer system to allow for better viewing of specific file types (mainly utilizing libyal):
  - Plists
  - Events (Evt,Evtx)
  - USN
  - etc

# Foreseen Shortcomings
Currently not sure how to implement a method for viewing objects (files, volumes, disk) in hex. I will soon remove the hex pane. I could always use help with this project and this is one of many areas that is beyond me. Because volumes, disk, and files can be very large in size, I dont think it would work to read the file to the hex pane. I believe what needs to be done is attach to the scroll and read sections of the I/O object that corresponds to viewer position. Not sure how to implement such a system.

# Example view
![Viewing VSS](https://github.com/forensicmatt/PancakeViewer/blob/master/resources/example001.png)
![Extraction Options](https://github.com/forensicmatt/PancakeViewer/blob/master/resources/example002.png)
![Extraction Results](https://github.com/forensicmatt/PancakeViewer/blob/master/resources/example003.png)

# More Talk
Forensic Lunch - 20160715

[![Pancake Talk on the Forensic Lunch](http://img.youtube.com/vi/3Hrz5QHwDwY/0.jpg)](https://youtu.be/3Hrz5QHwDwY?t=4m40sE)