'''
Created on Jan 18, 2012

@author: ivanoras
'''
import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui  import *


class Comm (QObject):
    """
    This class allows QtGui.QGraphicsItem to send and receive signals (like a mediator)
    """
    
    def __init__(self, parent = None):
        
        super (Comm, self).__init__ (parent)
        QObject.__init__ (self)
    
    
    
    # Model signals
    def emitDeleteNodeMSignal (self, node_id):
        self.emit (SIGNAL ('deleteNode_MSignal(int)'), node_id)
    
    
    def emitDeleteLinkMSignal (self, node_id):
        self.emit (SIGNAL ('deleteLink_MSignal(int)'), node_id)
    
    def emitAddLinkMSignal (self, node_id):
        self.emit (SIGNAL ('addLink_MSignal(int)'), node_id)
    
    # View Signals
    
    #def emitSelectVSignal (self, node_id):
        
        #self.emit (SIGNAL ('SelectTag_VSignal(int)'), node_id)