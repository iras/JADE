'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import math

import Comm0


class Wire0 (QGraphicsLineItem):
    
    def __init__ (self, s_in, s_out ,parent=None, scene=None):
        
        QGraphicsLineItem.__init__ (self)
        
        self.s_in  = s_in
        self.s_out = s_out
        
        self.comm = Comm0.Comm0 ()
        
        self.xo = self.s_in.getAbsPos().x()
        self.yo = self.s_in.getAbsPos().y()
        self.xf = self.s_out.getAbsPos().x()
        self.yf = self.s_out.getAbsPos().y()
        
        self.color  = QColor(Qt.green).dark(120)
        
        #self.setFlags (QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        #self.setAcceptsHoverEvents (True)
        
        self.setZValue (-1.0)
        
        self.arrowSize = 5
        self.arrowHead = QtGui.QPolygonF()
        
        self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents (True)
        self.setActive(True)
        
        self.wire_pen = QPen(Qt.gray, 2, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin) # Qt.SolidLine
    
    def paint (self, painter, option, unused_widget):
        
        painter.setPen (self.wire_pen)
        
        self.xo = self.s_in.getAbsPos().x()  + 3
        self.yo = self.s_in.getAbsPos().y()  + 3
        self.xf = self.s_out.getAbsPos().x() + 3
        self.yf = self.s_out.getAbsPos().y() + 3
        
        # QGraphicsLineItem uses the line and the pen width to provide a reasonable implementation of
        # QGraphicsLineItem.boundingRect(), QGraphicsLineItem.shape() and QGraphicsLineItem.contains()
        self.setLine (QLineF(self.xo, self.yo, self.xf, self.yf))
        
        lines=[]
        if option.levelOfDetail>=0.4: lines=[QLine (self.xo, self.yo, self.xf, self.yf)]
        painter.drawLines(lines)
    
    def remove (self): self.setVisible (False)
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def hoverEnterEvent (self, e):
        
        self.wire_pen.setColor (Qt.red)
        self.update()
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent(self, e):
        
        self.wire_pen.setColor (Qt.gray)
        self.update()
        
        QGraphicsItem.hoverLeaveEvent(self,e)
    
    def mousePressEvent (self, e):
        QGraphicsItem.mousePressEvent (self, e)
        self.update()
    
    def mouseMoveEvent (self, e):
        QGraphicsItem.mouseMoveEvent (self, e)
    
    def mouseReleaseEvent (self, e):
        QGraphicsItem.mouseReleaseEvent (self, e)
        self.update ()
    
    def switchOffLink (self, s_in_id, s_out_id):
        
        print 'switchOffLink !'
        if self.s_in.getSocketId()==s_in_id or self.s_out.getSocketId()==s_out_id:
            self.setVisible (False)
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
     
    def get2HooksIds (self): return [self.s_in.getSocketId(), self.s_out.getSocketId()]
    def getComm   (self): return self.comm