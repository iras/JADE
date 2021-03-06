'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import Qt, QLineF, QLine
from PyQt4.QtGui import QGraphicsLineItem, QColor, QPolygonF, QGraphicsItem, QPen

import JADEmisc.Comm0 as c0



class Wire0 (QGraphicsLineItem):
    
    def __init__ (self, s_in, s_out ,parent=None, scene=None):
        
        QGraphicsLineItem.__init__ (self)
        
        self.s_in  = s_in
        self.s_out = s_out
        
        self.comm = c0.Comm0 ()
        
        self.xo = self.s_in.getAbsPos().x()
        self.yo = self.s_in.getAbsPos().y()
        self.xf = self.s_out.getAbsPos().x()
        self.yf = self.s_out.getAbsPos().y()
        
        self.color  = QColor (Qt.green).dark(120)
        
        #self.setFlags (QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        #self.setAcceptsHoverEvents (True)
        
        self.setZValue (-1)
        
        self.arrowSize = 5
        self.arrowHead = QPolygonF()
        
        self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents (True)
        self.setActive(True)
        
        self.wire_pen = QPen (Qt.white, 3, Qt.DotLine) # Qt.SolidLine
        
        self.const = 3
        
    def paint (self, painter, option, unused_widget):
        
        painter.setPen (self.wire_pen)
        
        self.xo = self.s_in.getAbsPos().x()  + self.const
        self.yo = self.s_in.getAbsPos().y()  + self.const
        self.xf = self.s_out.getAbsPos().x() + self.const
        self.yf = self.s_out.getAbsPos().y() + self.const
        
        # QGraphicsLineItem uses the line and the pen width to provide a reasonable implementation of
        # QGraphicsLineItem.boundingRect(), QGraphicsLineItem.shape() and QGraphicsLineItem.contains()
        self.setLine (QLineF (self.xo, self.yo, self.xf, self.yf))
        
        lines=[]
        if option.levelOfDetail>=0.4: lines=[QLine (self.xo, self.yo, self.xf, self.yf)]
        painter.drawLines (lines)
    
    def remove (self):
        
        self.setVisible (False)
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def hoverEnterEvent (self, e):
        
        self.wire_pen.setColor (Qt.red)
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent(self, e):
        
        self.wire_pen.setColor (Qt.white)
        
        QGraphicsItem.hoverLeaveEvent(self,e)
    
    '''
    def mousePressEvent (self, e):
        QGraphicsItem.mousePressEvent (self, e)
        self.update()
    
    def mouseMoveEvent (self, e):
        QGraphicsItem.mouseMoveEvent (self, e)
    
    def mouseReleaseEvent (self, e):
        QGraphicsItem.mouseReleaseEvent (self, e)
        self.update ()
    '''
    
    def switchOffLink (self, s_in_id, s_out_id):
        
        if self.s_in.getSocketId()==s_in_id and self.s_out.getSocketId()==s_out_id:
            self.setVisible (False)
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
     
    def get2HooksIds (self): return [self.s_in.getSocketId(), self.s_out.getSocketId()]
    def getComm   (self): return self.comm