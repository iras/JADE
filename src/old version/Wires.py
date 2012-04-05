'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import math

import Comm


class Wire (QGraphicsLineItem):
    
    def __init__ (self, s_in, s_out, link_id ,parent=None, scene=None):
        
        QGraphicsLineItem.__init__ (self)
        super (Wire, self).__init__(parent, scene)
        
        self.s_in = s_in
        self.s_out = s_out
        self.linkd_id = link_id
        
        self.comm = Comm.Comm ()
        
        self.xo = self.s_in.pos().x()
        self.yo = self.s_in.pos().y()
        self.xf = self.s_out.pos().x() + 5
        self.yf = self.s_out.pos().y() + 5
        
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
        
        path = super (Wire, self).shape()
        path.addPolygon (self.arrowHead)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        grayPen = QPen(Qt.gray, 2, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin) # Qt.SolidLine
        painter.setPen (grayPen)
        
        self.xo = self.s_in.pos().x() + 40
        self.yo = self.s_in.pos().y() + 20
        self.xf = self.s_out.pos().x() + 40
        self.yf = self.s_out.pos().y() + 20
        
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
    def getLinkId (self): return self.linkd_id
    def getComm   (self): return self.comm