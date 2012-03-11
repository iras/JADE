'''
Created on Feb 9, 2012

@author: macbookpro
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui


class HookBox0 (QGraphicsItem):


    def __init__(self, parent=None, scene=None):
        
        QGraphicsItem.__init__ (self)
        
        self.helper = None
        self.parent = parent
        
        self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents (True)
        
        self.pen_color = QPen (Qt.darkRed)
        
        self.socket_id = None
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (2, 2, 10, 10)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        painter.setBrush (QBrush (Qt.darkCyan))
        painter.setPen   (self.pen_color)
        
        painter.drawEllipse(1, 1, 8 ,8)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    
    def hoverEnterEvent (self, e):
        
        self.pen_color = QPen (Qt.red)
        self.update ()
        
        # records the node_id in the helper's attribute.
        self.comm.setHoveredSocketId (self.socket_id)
        
        # deal with the harpoon.
        if not self.helper.isTimerEnded():
            self.setSelected (True)
            self.helper.getGraphView().addLinkAndWirePressBtnListener ()
        
        #self._text_item.setToolTip (self._text_item.toPlainText ())
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e):
        
        self.pen_color = QPen (Qt.darkRed)
        self.update ()
        
        # records the node_id in the helper's attribute.
        self.comm.setHoveredSocketId (None)
        
        #QGraphicsItem.hoverLeaveEvent (self, e)
    
    def mousePressEvent (self, e):
        
        self.harpoon.setInitPos (self.pos()+self.parent.pos())
        self.harpoon.setVisible (True)
        self.harpoon.update ()
        
        QGraphicsItem.mousePressEvent (self, e)
        self.update ()
    
    def mouseMoveEvent (self, e):
        
        self.harpoon.setEndPos (self.pos()+e.pos()+self.parent.pos())
        self.harpoon.update ()
    
    def mouseReleaseEvent (self, e):
        
        self.harpoon.setVisible (False)
        self.update ()
        
        self.helper.initAndStartTimer ()
        
        QGraphicsItem.mouseReleaseEvent (self, e)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getAbsPos (self): return self.pos()+self.parent.pos()
    
    def setSocketId (self, socket_id) : self.socket_id = socket_id
    def getSocketId (self): return self.socket_id
    
    def setHelper (self, helper):
        
        self.helper  = helper
        self.comm    = self.helper.getGraph().getComm()
        self.harpoon = self.helper.getHarpoon()