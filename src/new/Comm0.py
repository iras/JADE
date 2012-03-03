'''
Created on Jan 18, 2012

@author: ivanoras
'''
import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui  import *


class Comm0 (QObject):
    """
    This class allows QtGui.QGraphicsItem to send and receive signals (like a mediator)
    besides being a utility helper.
    """
    
    def __init__(self, parent = None):
        
        super (Comm0, self).__init__ (parent)
        QObject.__init__ (self)
        
        self.id_node_counter   = 0
        self.id_socket_counter = 0
        
        self.hovered_item_id = None
    
    def getNewNodeId (self):
        
        self.id_node_counter += 1
        return self.id_node_counter
    
    def getNewSocketId (self):
        
        self.id_socket_counter += 1
        return self.id_socket_counter
    
    
    
    # Model signals
    
    def emitAddNodeMSignal (self, node_id):
        self.emit (SIGNAL ('addNode_MSignal(int)'), node_id)
    
    def emitDeleteNodeMSignal (self, node_id):
        self.emit (SIGNAL ('deleteNode_MSignal(int)'), node_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def emitAddLinkMSignal (self, inSocket_id, outSocket_id):
        self.emit (SIGNAL ('addLink_MSignal(int, int)'), inSocket_id, outSocket_id)
        
    def emitDeleteLinkMSignal (self, inSocket_id, outSocket_id):
        self.emit (SIGNAL ('deleteLink_MSignal(int, int)'), inSocket_id, outSocket_id)
    
    def emitAddInSocketMSignal (self, inSocket_id):
        self.emit (SIGNAL ('addInSocket_MSignal(int)'), inSocket_id)
    
    def emitDeleteInSocketMSignal (self, inSocket_id):
        self.emit (SIGNAL ('deleteInSocket_MSignal(int)'), inSocket_id)
    
    def emitAddOutSocketMSignal (self, outSocket_id):
        self.emit (SIGNAL ('addOutSocket_MSignal(int)'), outSocket_id)
    
    def emitDeleteOutSocketMSignal (self, outSocket_id):
        self.emit (SIGNAL ('deleteOutSocket_MSignal(int)'), outSocket_id)
    
    def emitCtxMenuSignal (self, pos):
        self.emit (SIGNAL ('customContextMenuRequested(QPoint)'), pos)
    
    
    # View Signals
    
    #def emitSelectVSignal (self, node_id):
        
        #self.emit (SIGNAL ('SelectTag_VSignal(int)'), node_id)
    
    
    # misc
    
    def setHoveredItemId (self, node_id):
        
        print 'hovered '+str(node_id)
        self.hovered_item_id = node_id
    
    def getHoveredItemId (self): return self.hovered_item_id