#### JADE version 0.0.2

      Mostly still work in progress.

JADE is a simple cross-platform dependency mapping tool written in Python 2.6 and using the library PyQt4.
It is available both as a standalone version (ClientStandAlone.py) and as an additional Maya panel
(ClientMaya.py needs to be called by the Python script MayaLauncherPythonScript from within Maya).

When the window (panel) appears, please load the XML file relative to the available nodes first, then right-click
on the graphics view to create the tags, one by one. Right clicking on a tag will allow hooks creation and, clicking
and dragging the dash line from a hook over to another one will allow link creation.


ver 0.0.3 wish list:
- implement load/save XML maps.
- add props canvas to each tag (textfields to manually input info in)
