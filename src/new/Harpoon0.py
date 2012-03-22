'''
Created on Feb 11, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui


class Harpoon0 (QGraphicsLineItem):

    def __init__(self, x0, y0, x1, y1):
        
        QGraphicsLineItem.__init__ (self)
        
        self.setZValue (2000)
        
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        
        self.cx = 2
        self.cy = 2
        
    def boundingRect (self):
        
        return QtCore.QRectF (-1000, -1000, 2000, 2000)
    
    def shape(self):
        
        path = super (Harpoon0, self).shape()
        return path
    
    def paint (self, painter, option, unused_widget):
        
        grayPen = QPen(Qt.black, 4, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen (grayPen)
        
        lines=[]
        if option.levelOfDetail>=0.4: lines=[QLine (self.x0+self.cx, self.y0+self.cy, self.x1, self.y1)]
        painter.drawLines(lines)
    
    def setInitPos (self, pos):
        
        self.x0 = pos.x()+self.cx
        self.y0 = pos.y()+self.cy
        self.x1 = pos.x()
        self.y1 = pos.y()
        
    def setEndPos   (self, pos):
        
        self.x1 = pos.x()
        self.y1 = pos.y()