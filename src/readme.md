#### JADE version 0.0.2

JADE is a simple cross-platform dependency mapping tool written in Python 2.6 and using the library PyQt4.
It is available both as a standalone (ClientStandAlone.py) and as an additional panel in Maya
(ClientMaya.py called by the Python script MayaLauncherPythonScript from within Maya)

      Mostly still in progress.

To get started, please load the XML file relative to the available nodes, first.
Then, use the mouse right-button to create the tags, one by one, on the graphics view.
On hovering a tag, the mouse right-button will allow creating hooks to extend to any
other compatible tag.


ver 0.0.3 wish list:
- implement load/save XML maps.
- add props canvas to each tag (textfields to manually input info in)
