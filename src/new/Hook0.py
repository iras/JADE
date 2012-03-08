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
        
        self.parent = parent
        
        self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents (True)
        
        self.pen_color = QPen (Qt.darkRed)
        
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (2, 2, 10, 10)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        painter.setBrush (QBrush (Qt.darkCyan))
        painter.setPen   (self.pen_color)
        
        painter.drawEllipse(1, 1, 8 ,8)
    
    def hoverEnterEvent (self, e):
        
        self.pen_color = QPen (Qt.red)
        self.update ()
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e):
        
        self.pen_color = QPen (Qt.darkRed)
        self.update ()
        
        QGraphicsItem.hoverLeaveEvent (self, e)