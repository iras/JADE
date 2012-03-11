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
        super (Wire0, self).__init__(parent, scene)
        
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
    
    def boundingRect (self): return QtCore.QRectF (-1000, -1000, 2000, 2000)
        
        #extra = (self.pen().width() + 20) * 0.5
        #p1 = self.line().p1()
        #p2 = self.line().p2()    
        #return QtCore.QRectF (p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)
    
    def shape (self):
        
        path = super (Wire0, self).shape()
        path.addPolygon (self.arrowHead)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        grayPen = QPen(Qt.gray, 2, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin) # Qt.SolidLine
        painter.setPen (grayPen)
        
        self.xo = self.s_in.getAbsPos().x() + 3
        self.yo = self.s_in.getAbsPos().y() + 3
        self.xf = self.s_out.getAbsPos().x() + 3
        self.yf = self.s_out.getAbsPos().y() + 3
        
        lines=[]
        if option.levelOfDetail>=0.4: lines=[QLine (self.xo, self.yo, self.xf, self.yf)]
        painter.drawLines(lines)
    
    def remove (self): self.setVisible (False)
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def mousePressEvent (self, e):
        QGraphicsItem.mousePressEvent (self, e)
        self.update ()
    
    def mouseMoveEvent (self, e):
        QGraphicsItem.mouseMoveEvent (self, e)
    
    def mouseReleaseEvent (self, e):
        QGraphicsItem.mouseReleaseEvent (self, e)
        self.update ()
    
    def switchOffLink (self, nodeid):
        if self.s_in.getNodeId()==nodeid or self.s_out.getNodeId()==nodeid:
            self.setVisible (False)
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
     
    def get2NodesIds (self): return [self.s_in.getNodeId(), self.s_out.getNodeId()]
    def getComm   (self): return self.comm