"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Harpoon0 (QGraphicsLineItem):
    
    def __init__(self, x0, y0, x1, y1):
        '''
        Constructor
        '''
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
    
    def setEndPos (self, pos):
        
        self.x1 = pos.x()
        self.y1 = pos.y()



class Helper (QObject):
    '''
    This class is a utility helper and deals with the harpoon and its timing-related stuff,
    additionally it provides a common place where to fish for globals.
    '''
    def __init__(self, MainWindow, scene, graph, parent = None):
        '''
        Constructor
        '''
        super (Helper, self).__init__ (parent)
        QObject.__init__ (self)
        
        self.main  = MainWindow
        self.scene = scene
        self.graph = graph
        self.graph_view = None
        
        self.ctimer = QTimer()
        
        #self.connect (self.ctimer, SIGNAL("timeout()"), self.singleUpdate)
        
        #self.ctimer.singleShot (500, self.singleUpdate)
        self.timer_flag = False
        
        # init harpoon and make it invisible
        self.harpoon = Harpoon0 (0, 0, 0, 0)
        self.harpoon.setVisible (False)
        
        self.menu = None
    
    # - - - - - - - - - - - - - - - - - - - - 
    
    def initAndStartTimer (self):
        
        self.timer_flag = False
        
        if not self.ctimer.isActive():
            
            self.ctimer.singleShot (30, self.singleUpdate)
            #self.ctimer.start (500)
    
    def singleUpdate (self):
        
        self.timer_flag = True
    
    # - - - - - - - - - - - - - - - - - - - - 
    
    def getScene (self): return self.scene
    def getGraph (self): return self.graph
    def getHarpoon (self): return self.harpoon
    def getMain  (self): return self.main
    def getTimer (self): return self.ctimer
    def isTimerEnded (self): return self.timer_flag
    def getGraphView (self): return self.graph_view
    
    def setGraphView (self, gv): self.graph_view = gv
    
    # menu
    def setMenu (self, mn): self.menu = mn
    def getMenu (self): return self.menu