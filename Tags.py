'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import Comm

class Tag0 (QGraphicsItem):
    
    def __init__ (self, color, node_id, parent=None, scene=None):
        
        QGraphicsItem.__init__ (self)
        
        self.node_id = node_id
        
        self.color = color
        self.stuff = []
        
        self.comm = Comm.Comm ()
        
        self.setFlags (QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptsHoverEvents (True)
        
        self.setZValue (1.0)
        
        self.height = 5
        
        self._text_item = QGraphicsTextItem ('text '+str(self.node_id), self)
        self._text_item.setTextInteractionFlags (Qt.TextEditable)
        self._text_item.setPos (QPointF (20, 20))
        self._text_item.setFont (QFont ("Geneva", 10, QFont.Bold, False))
        self._text_item.setTextWidth(50)
        self._text_item.setToolTip(self._text_item.toPlainText ())
        #self._text_item.setHtml("<h2 align=\"center\">hello</h2><h2 align=\"center\">world 12334345354444444444444444444444444</h2>123");
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (0, 0, 82, 42)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        if option.state & QStyle.State_Selected:
            fillColor = self.color.dark (150)
        else:
            fillColor = self.color
        
        if option.state & QStyle.State_MouseOver:
            fillColor = fillColor.light (125)
        
        if option.levelOfDetail < 0.2:
            
            if option.levelOfDetail < 0.125:
                painter.fillRect (QRectF (0, 0, 110, 70), fillColor)
                return
            
            painter.setPen   (QPen (Qt.black, 0))
            painter.setBrush (fillColor)
            painter.drawRect (0, 0, 80, 40)
            return
        
        oldPen = painter.pen ()
        pen = oldPen
        width = 0
        if option.state & QStyle.State_Selected:
            width += 2
        
        pen.setWidth (width)
        if option.state & QStyle.State_Sunken:
            level = 120
        else:
            level = 100
        painter.setBrush (QBrush (fillColor.dark (level)))
        
        painter.drawRoundRect (QRect (0, 0, 80, 34+self.height), 20)
    
    def remove (self): self.setVisible (False)
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addedLinkSignal (self, node_id):
        
        if node_id==self.node_id:
            self.height += 5
            self.update ()
    
    def deletedLinkSignal (self, node_id):
        
        if node_id==self.node_id:
            self.height -= 5
            self.update ()
    
    def mousePressEvent (self, e):
        
        QGraphicsItem.mousePressEvent (self, e)
        self.update ()
    
    def mouseMoveEvent (self, e):
        
        if e.modifiers () & Qt.ShiftModifier:
            self.stuff.append (e.pos ())
            self.update ()
            return
        QGraphicsItem.mouseMoveEvent (self, e)
    
    def hoverEnterEvent (self, e): self._text_item.setToolTip (self._text_item.toPlainText ())
    def hoverLeaveEvent (self, e): pass
    
    def mouseReleaseEvent (self, e):
        
        QGraphicsItem.mouseReleaseEvent (self, e)
        self.update ()
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def getNodeId (self): return self.node_id
    def getComm   (self): return self.comm