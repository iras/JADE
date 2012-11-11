# JADE Mapping Tool
ver 0.3

JADE is a simple cross-platform data-driven dependency mapping tool written in Python 2.6 and using the library PyQt4.
It is available both as a standalone app (through ClientStandAlone.py) and as Maya local dependency mapping tool
(through ClientMaya.py)

This tool allows handling of cluster of customisable graphs. That allows the user to have different tools by just changing
the node definitions in the XML file available_nodes. A kismet©-like editor is already given as example by having a set of
specific nodes. By changing the node definition, a dialogue mapping tool can be easily achieved too.

The codebase encompasses both the standalone and the Maya client. And, except for two initial view classes, all the rest of the
classes is shared between the clients. JADE is documented (EpyDoc, cfr. http://epydoc.sourceforge.net/) and the JADE model (graph.py, node.py, socket.py) is unit tested.

## how to use it
On running the client, please load the XML file description (available nodes) first, then mouse right-click
on the graphics view to create the tags, one by one. Right clicking on a tag (plus Ctrl or Alt pressed at once)
will allow hook creation and by click-and-dragging the dash line from a hook over to another one will allow link creation.
The buttons save and load are pretty self-explanatory.

Maya client : this client needs calling from within Maya by means of the additional Python script "MayaLauncherPythonScript" after
customising the physical path in it. Such script will reside in a Maya Script Editor's Python page and needs to be run from Maya.

## Some Definitions
# Cluster
A cluster can be imagined as a self-contained graph. More specifically, a cluster (in JADE) is a collection of nodes and links.
Any two clusters never share nodes/links.
# Nodes and Links
Nodes/Links are the basic elements that make up a graph. The Node can have a number of plugs (in-plugs, and out-plugs).
Two nodes can be connected by a link. That means that the in-plug of the 1st node and the out-plug of the 2nd node reference each other.



## known Issues
(1) two nodes can occasionally stay both selected after making a link. The workaround is to click on the background
to reset the selection.


## version 0.4 wishlist:
(0) sorting the known issues.
(1) adding undo functionality.
(2) merging two imported graphs in a unique file.
(3) tube-like connections instead of straight lines.
(4) add unit tests for the props.


