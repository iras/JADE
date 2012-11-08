## JADE Mapping Tool
ver 0.3

JADE is a simple cross-platform dependency mapping tool written in Python 2.6 and using the library PyQt4.
It is available both as a standalone version (through ClientStandAlone.py) and as Maya local dependency mapping tool
(through ClientMaya.py)

The codebase encompasses both the standalone and the Maya client. And, except for two initial view classes, all the rest of the
classes is shared between the clients. JADE is documented (EpyDoc, cfr. http://epydoc.sourceforge.net/) and the JADE model (graph.py, node.py, socket.py) is unit tested.

## How to use it
On running the client, please load the XML file description (available nodes) first, then mouse right-click
on the graphics view to create the tags, one by one. Right clicking on a tag (plus Ctrl or Alt pressed at once)
will allow hook creation and by click-and-dragging the dash line from a hook over to another one will allow link creation.
The buttons save and load are pretty self-explanatory.

Maya client : this client needs calling from within Maya by means of the additional Python script "MayaLauncherPythonScript" after
customising the physical path. Such script will reside in a Maya Script Editor's Python page and needs to be run from Maya.




## Known Issues
(1) two nodes can occasionally stay both selected after making a link. The workaround is to click on the background
to reset the selection.


## Version 0.4 wishlist:
(0) sorting the known issues.
(1) adding undo functionality.
(2) merging two imported graphs in a unique file.
(3) tube-like connections instead of straight lines.
(4) add unit tests for the props.


