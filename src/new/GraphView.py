'''
Created on Feb 23, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import Tags0
import Wires0
import Sockets


class GraphView ():


    def __init__(self, graph, utility, parent = None):
        
        self._tag_list  = []
        self._wire_list = []
        
        self.graph   = graph
        self.utility = utility
    
    def removeSelectedItems (self):
        
        # wires
        tmp_ls = self.getListSelectedWires()
        for wire in tmp_ls:
            tmp_ls = wire.get2HooksIds ()
            self.graph.removeLink (tmp_ls[0], tmp_ls[1])
    
    # - Listeners from key pressing - - - - - - - - - - - - - - - - - - - - - - - - - -

    def addNodeAndTagPressBtnListener (self): self.addNodeAndTag()
    
    def removeNodeAndTagPressBtnListener (self):
        
        # pop-up window
        
        #self.removeNodeAndTag (self.getListSelectedHooks ())
        pass
    
    def addLinkAndWirePressBtnListener (self):
        
        lh = self.getListSelectedHooks ()
        if len(lh)==2 and not self.graph.areSocketsRelated (lh[0].getSocketId(), lh[1].getSocketId()):
            self.addLinkAndWire (lh[0].getSocketId(), lh[1].getSocketId())
            
            # take the focus away from the nodes
            lh[0].setSelected (False)
            lh[1].setSelected (False)
    
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
        
        comm = self.graph.getComm ()
        self.utility.connect (comm, SIGNAL('addInSocket_MSignal(int,int)'),  tag.appendInHook)
        self.utility.connect (comm, SIGNAL('addOutSocket_MSignal(int,int)'), tag.appendOutHook)
        
        self._tag_list.append (tag)
        
        return tag
    
    def removeNodeAndTag (self, selected_tags):
        pass
    
    
    
    
    def addLinkAndWire (self, s_out_id, s_in_id):
        
        s1 = self.graph.getSocket (s_in_id)
        s2 = self.graph.getSocket (s_out_id)
        
        is1 = isinstance (s1, Sockets.InSocket)
        os1 = isinstance (s1, Sockets.OutSocket)
        
        is2 = isinstance (s2, Sockets.InSocket)
        os2 = isinstance (s2, Sockets.OutSocket)
        
        if (is1 and os2) or (os1 and is2):
            if is1==True:
                self.graph.addLink (s1, s2)
            else:
                self.graph.addLink (s2, s1)
        else:
            print 'Sockets must be one of each kind. No connection will be made now.'
    
    def addWire (self, s_in_id, s_out_id):
        
        print 'will extend the wire between ',s_in_id,' and ',s_out_id
        
        hook_in  = self.getHook (s_in_id)
        hook_out = self.getHook (s_out_id)
        wire_sin_sout = Wires0.Wire0 (hook_in, hook_out)
        self.utility.getScene().addItem (wire_sin_sout)
        self.utility.connect (self.graph.getComm(), SIGNAL ('deleteLink_MSignal(int,int)'), wire_sin_sout.switchOffLink)
        self._wire_list.append (wire_sin_sout)
        
        # update the two tags in order to draw the link's line.
        hook_in.update ()
        hook_out.update ()
        
        return wire_sin_sout
    
    def removeLinkAndWire (self, selected_wires):
        pass
    
    # - - Getters - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getTag (self, node_id):
        
        seeked_tag = None
        for tag in self._tag_list:
            if tag.getSId()==node_id:
                seeked_tag = tag
                break
        
        return seeked_tag
    
    def getListSelectedHooks (self):
        
        ls = []
        for tag in self._tag_list:
            [ls.append (hook) for hook in tag.getInHooks () if hook.isSelected ()]
            [ls.append (hook) for hook in tag.getOutHooks() if hook.isSelected ()]
        return ls
    
    def getHook (self, socked_id):
        
        hook = None
        
        for tag in self._tag_list:
            
            if hook==None:
            
                for h in tag.getInHooks ():
                    if h.getSocketId()==socked_id:
                        hook = h
                        break
                
                for h in tag.getOutHooks ():
                    if h.getSocketId()==socked_id:
                        hook = h
                        break
            else:
                break
        
        return hook
        
    
    def getListSelectedWires (self):
        
        ls = []
        [ls.append (item) for item in self._wire_list if item.isSelected ()]
        return ls