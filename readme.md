#### JADE version 0.3


JADE is a simple cross-platform dependency mapping tool written in Python 2.6 and using the library PyQt4.
It is available both as a standalone version (ClientStandAlone.py) and as an additional Maya panel
(ClientMaya.py needs to be called by the Python script MayaLauncherPythonScript from within Maya, with the amended path).
The model (graph.py, node.py, socket.py) is unit tested.

On starting, please load the XML file description relative to the available nodes first, then mouse right-click
on the graphics view to create the tags, one by one. Right clicking on a tag (plus Ctrl or Alt pressed at once)
will allow hooks creation and by click-and-dragging the dash line from a hook over to another one will allow link creation.
The buttons save and load are pretty self-explanatory.

The codebase encompasses both the standalone and the Maya client. and, except for two initial classes, all the rest of the
classes is shared between the clients.

The code is documented and EpyDoc (cfr. http://epydoc.sourceforge.net/)




Known Issues:
(1) two nodes can occasionally stay both selected after making a link. The workaround is to click on the background
to reset the selection.


Version 0.4 wish list:
(0) sorting the known issues.
(1) adding undo functionality.
(2) merging two imported graphs in a unique file.
(3) tube-like connections instead of straight lines.
(4) add unit tests for the props.


