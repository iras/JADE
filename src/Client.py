'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import Utility

import Tags
import Wires
import View
import Model as md
import Harpoon as hp


class MainWindow (QWidget):
    
    def __init__ (self, graph, parent=None):
        
        QWidget.__init__ (self, parent)
        
        self.graph = graph
        
        #self.setMouseTracking (True)
        #self.setAttribute(Qt.WA_Hover)
        
        self.scene = QGraphicsScene()
        self.populateScene ()
        
        self.hSplit = QSplitter ()
        
        vSplit = QSplitter ()
        vSplit.setOrientation (Qt.Vertical)
        vSplit.addWidget (self.hSplit)
        
        view = View.View ("Main view")
        view.setClientAndWireViewItems (self)
        view.view().setScene (self.scene)
        self.hSplit.addWidget (view)
        
        layout = QHBoxLayout ()
        layout.addWidget (vSplit)
        self.setLayout (layout)
        
        self.setWindowTitle("Just Another DEpendency mapping tool")
    
    def populateScene (self):
        
        self.utility = Utility.Helper (self, self.scene)
        
        # init harpoon and make it invisible
        self.harpoon = hp.Harpoon (0, 0, 0, 0)
        self.harpoon.setVisible (False)
        self.scene.addItem (self.harpoon)
        
        self._tag_list  = []
        self._wire_list = []
        
        # Populate scene
        t1 = self.addNodeAndTag (-100, -100)
        t2 = self.addNodeAndTag (0, 0)
        t3 = self.addNodeAndTag (-100, 100)
        t4 = self.addNodeAndTag (100, -100)
        t5 = self.addNodeAndTag (100, 100)
        
        #l11 = self.addLinkAndWire (t1, t1) # implement self-referencing
        self.addLinkAndWire (t1, t2)
        self.addLinkAndWire (t1, t3)
        self.addLinkAndWire (t1, t4)
        self.addLinkAndWire (t1, t5)
        self.addLinkAndWire (t2, t3)
        self.addLinkAndWire (t2, t4)
        self.addLinkAndWire (t2, t5)
        self.addLinkAndWire (t3, t4)
        self.addLinkAndWire (t3, t5)
        self.addLinkAndWire (t4, t5)
    
    def addNodeAndTagButtonHook (self): self.addNodeAndTag (20, 20)
    def addNodeAndTag (self, x, y):
        
        node = model.addNode ()
        
        color = QColor (Qt.white).dark (120)
        tag = Tags.Tag0 (self.harpoon, color, node.getId(), self.utility)
        tag.setPos (QPointF (x, y))
        self.scene.addItem (tag)
        self.connect (model.getComm (), SIGNAL('addLink_MSignal(int)'),    tag.addedLinkSignal)
        self.connect (model.getComm (), SIGNAL('deleteLink_MSignal(int)'), tag.deletedLinkSignal)
        self._tag_list.append (tag)
        
        return tag
    
    def removeNodeAndTagButtonHook (self):
        
        self.removeNodeAndTag (self.getListSelectedTags ())
    
    def removeNodeAndTag (self, tmp_list):
        
        for i in tmp_list:
            nid = i.getNodeId ()
            model.removeNode (nid)
            self.removeTag   (nid)
    
    def addLinkAndWireButtonHook (self):
        
        ls = self.getListSelectedTags ()
        if len(ls)==2 and not model.areNodesRelated (ls[0].getNodeId(), ls[1].getNodeId()):
            self.addLinkAndWire (ls[0], ls[1])
        
            # take the focus away from the nodes
            ls[0].setSelected (False)
            ls[1].setSelected (False)
    
    def addLinkAndWire (self, tag1, tag2):
        
        link = model.addLink (tag1.getNodeId(), tag2.getNodeId ())
        
        link_tag1_tag2 = Wires.Wire (tag1, tag2, link.getId ())
        self.scene.addItem (link_tag1_tag2)
        self.connect (model.getComm(), SIGNAL ('deleteNode_MSignal(int)'), link_tag1_tag2.switchOffLink)
        self._wire_list.append (link_tag1_tag2)
        
        # update the two tags in order to draw the link's line.
        tag1.update ()
        tag2.update ()
        
        return link_tag1_tag2
    
    def removeLinkAndWireButtonHook (self):
        
        ls = self.getListSelectedTags ()
        tmp = self.findTheWireBetweenTwoTags (ls)
        if tmp!=None:
            self.removeLinkAndWire ([tmp])
        
            # take the focus away from the nodes
            ls[0].setSelected(False)
            ls[1].setSelected(False)
    
    def removeLinkAndWire (self, tmp_list):
        
        for i in tmp_list:
            lid = i.getLinkId()
            flag = model.removeLink (lid)
            if flag:
                self.removeWire  (lid)
    
    def removeTag (self, node_id):
        
        for tag in self._tag_list:
            if tag.getNodeId()==node_id:
                tag.remove ()
                del self._tag_list [self._tag_list.index (tag)]
                break
    
    def removeWire (self, link_id):
        
        for wire in self._wire_list:
            if wire.getLinkId()==link_id:
                wire.remove ()
                del self._wire_list [self._wire_list.index (wire)]
                break
    
    def findTheWireBetweenTwoTags (self, ls):
        
        tmp = None
        if len(ls)==2:
            n1_id = ls[0].getNodeId ()
            n2_id = ls[1].getNodeId ()
            
            for item in self._wire_list:
                wls = item.get2NodesIds ()
                if (wls[0]==n1_id and wls[1]==n2_id) or (wls[1]==n1_id and wls[0]==n2_id):
                    tmp = item
                    break
        return tmp
    
    def getListSelectedTags (self):
        
        ls = []
        [ls.append (item) for item in self._tag_list if item.isSelected ()]
        return ls
    
    def getListSelectedWires (self):
        
        ls = []
        [ls.append (item) for item in self._wire_list if item.isSelected ()]
        return ls

def main (argv):
    
    app = QApplication(argv)
    
    window = MainWindow   (model)
    window.setWindowFlags (Qt.WindowStaysOnTopHint)
    window.show ()
    
    return app.exec_()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

model = md.Model ()

if __name__ == "__main__":
    import sys
    sys.exit (main (sys.argv))