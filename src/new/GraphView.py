'''
Created on Feb 23, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import Tags0


class GraphView ():


    def __init__(self, graph, utility, parent = None):
        
        self._tag_list  = []
        self._wire_list = []
        
        self.graph   = graph
        self.utility = utility
        
    # - Listeners from key pressing - - - - - - - - - - - - - - - - - - - - - - - - - -

    def addNodeAndTagPressBtnListener (self): self.addNodeAndTag()
    
    def removeNodeAndTagPressBtnListener (self):
        
        # pop-up window
        
        self.removeNodeAndTag (self.getListSelectedTags ())
    
    def addLinkAndWirePressBtnListener (self):
        # self.addLinkAndWire (tag_out, tag_in)
        pass
    
    def removeLinkAndWirePressBtnListener (self):
        
        # pop-up window
        
        # self.removeLinkAndWire (self.getListSelectedWires ())
        pass
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addNodeAndTag (self):
        tmp = self.graph.addNode ()
        tmp.setName ('stateBegun')
    
    def addTag (self, node_id):
        
        color = QColor (Qt.white).dark (120)
        tag = Tags0.Tag1 (color, node_id, self.utility)
        tag.setPos (QPointF (20, 20))
        self.utility.getScene().addItem (tag)
        """
        self.connect (self.graph.getComm (), SIGNAL('addLink_MSignal(int)'),    tag.addedLinkSignal)
        self.connect (self.graph.getComm (), SIGNAL('deleteLink_MSignal(int)'), tag.deletedLinkSignal)
        """
        self._tag_list.append (tag)
        
        return tag
    
    
    
    def removeNodeAndTag (self, selected_tags):
        pass
    
    def addLinkAndWire (self, tag_out, tag_in):
        pass
    
    def removeLinkAndWire (self, selected_wires):
        pass
    
    # - - Getters - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getTag (self, node_id):
        
        seeked_tag = None
        for tag in self._tag_list:
            print '2222 '+str(tag.getSId())+' '+str(node_id)
            if tag.getSId()==node_id:
                seeked_tag = tag
                break
        
        return seeked_tag
    
    def getListSelectedTags (self):
        
        ls = []
        [ls.append (item) for item in self._tag_list if item.isSelected ()]
        return ls
    
    def getListSelectedWires (self):
        
        ls = []
        [ls.append (item) for item in self._wire_list if item.isSelected ()]
        return ls