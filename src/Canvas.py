"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

#import GText as gt


class Canvas (QGraphicsItem):


    def __init__(self, parent=None, scene=None):
        
        QGraphicsItem.__init__ (self)
        
        self.helper = None
        self.parent = parent
        
        #self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents (True)
        
        self.pen_color = QPen (Qt.black, 2)
        
        self.color = QColor (Qt.white).dark (120)
        
        # init Canvas Animation Tweening
        self.timeline = QtCore.QTimeLine (200)
        self.timeline.setFrameRange (0, 100)
        self.anim = QtGui.QGraphicsItemAnimation ()
        self.anim.setItem (self)
        self.anim.setTimeLine (self.timeline)
        self.parent.helper.connect (self.timeline, QtCore.SIGNAL("finished()"), self.makeFurtherThinner)
        self.anim_active = False
        
        self.SCALING = 0.25
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (0, 0, 122, 20)
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
            painter.drawRect (0, 0, 120, 20)
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
        
        #painter.drawRoundRect (QRect (0, 0, 80, 34+self.height), 20)
        painter.drawRect (QRect (0, 0, 120, 20))
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def makeThicker (self, canvas_height_in_units):
        
        print " --- make thicker ---"
        
        self.anim_active   = True
        self.thinning_flag = False
        
        self.canvas_height = canvas_height_in_units
        
        self.timeline.stop ()
        
        self.anim.setScaleAt (0, 1, 1+(self.canvas_height+1)*self.SCALING)
        self.anim.setScaleAt (1, 1, 1+(self.canvas_height+2)*self.SCALING)
        
        self.timeline.start ()
        self.update ()
    
    def makeThinner (self, canvas_height_in_units):
        
        print " --- make thinner ---"
        
        if self.anim_active == False:
            
            self.anim_active   = True
            self.thinning_flag = True
            
            self.canvas_height = canvas_height_in_units
            
            self.timeline.stop ()
            
            self.anim.setScaleAt (0, 1, 1+(self.canvas_height+1)*self.SCALING)
            self.anim.setScaleAt (1, 1, 1+(self.canvas_height)  *self.SCALING)
            
            self.timeline.start ()
            self.update ()
    
    # this method double-checks whether the canvas needs to be further thinner as a
    # result of receiving other asynchronous "delete link" SIGNALs while moving up.
    def makeFurtherThinner (self):
        
        self.anim_active = False
        
        if self.thinning_flag==True:
            
            if self.parent.getMaxLen() < self.canvas_height:
                self.makeThinner (self.canvas_height-1)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def hoverEnterEvent (self, e):
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e):
        
        QGraphicsItem.hoverLeaveEvent (self, e)
    
    def mousePressEvent (self, e):
        
        QGraphicsItem.mousePressEvent (self, e)
        #self.update ()
    
    def mouseMoveEvent (self, e):
        
        QGraphicsItem.mouseMoveEvent (self, e)
    
    def mouseReleaseEvent (self, e):
        
        QGraphicsItem.mouseReleaseEvent (self, e)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def setMaxPosInLists (self, pos): self.max_pos_in_list=pos