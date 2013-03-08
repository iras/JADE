# JADE Mapping Tool
### ver 0.3

A brief Introductory Video can be found [here](http://vimeo.com/54445956)

JADE is a simple cross-platform data-driven dependency mapping tool written in Python 2.6 and using the PyQt framework.
It is both available as a standalone app and as Maya scripted-plugin (tested on Maya 2012 and 2013).

JADE mapping tool allows handling clusters of customisable nodes which means that the user can set up different tools by simply changing
the nodes description in the XML file node_description. A mock-up version of a graphics scripting tool - useful for linking components in an component-based entity system - is given as example.
By changing the XML nodes description, any other specific mapping tool can be easily achieved from JADE with no additional code, e.g. dialogue mapping tool, mind mapping tool, etc.

The code base encompasses both the standalone and the Maya client. And, except for two initial view classes, all the rest of the
classes is shared between the two clients. JADE is (mostly) documented ([EpyDoc](http://epydoc.sourceforge.net/)) and the JADE mapping
tool's model (graph.py, node.py, socket.py) is unit tested. An approximated class structure for the JADE mapping tool
is shown right below.

![JADE mapping tool - overall approximated class structure](http://www.stc0.co.uk/JADE_classes_rough_structure.jpg)

The JADE floating tags are self-resizing depending on the number of connections, the reason for that is to avoid big tags with many unused hooks to clutter the working space.

## How to use it
After running the client, please load the XML file relative to the node description, then to start adding tags (nodes), 
mouse right-click on the graphics view and then choose what node-type from the contextual menu. Right clicking on a tag (plus Ctrl or Alt
pressed at once) will allow hook creation and by click-and-dragging the dash line from a hook over to another one will allow link creation.
The functionalities for the buttons new, save and load are pretty self-explanatory.

## Installation
 * Maya scripted-plugin : ClientMaya.py needs calling from within Maya by means of the additional Python script "MayaLauncherPythonScript" after
customising the physical path in it. Such script needs to run from the Maya Script Editor.
 * Standalone app : use py2app on Mac OS X, py2exe on Windows or PyInstaller on Linux, the python file to target is always ClientStandAlone.py.
On a Mac, some more installation notes are available [here](http://stc0.wordpress.com/2012/11/16/installing-py2app-for-python-2-6-8-macports-on-mac-os-lion/)

## Some Definitions
> ### Cluster
> A cluster can be imagined as a self-contained graph. More specifically, a cluster (in JADE) is a collection of nodes and links.
> Any two clusters never share nodes/links.
> ### Nodes and Links
> Nodes/Links are the basic elements that make up a graph. The Node can have a number of plugs (in-plugs, and out-plugs).
> Two nodes can be connected by a link, that means that the in-plug of the 1st node and the out-plug of the 2nd node reference each other.

## Issues + Bug Fixes + Feature Requests
[here](https://github.com/iras/JADE/issues?sort=created&state=open)


