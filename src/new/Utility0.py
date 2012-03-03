'''
Created on Feb 15, 2012

@author: ivanoras
'''
from PyQt4 import QtCore
from PyQt4.QtCore import *

import Harpoon0 as hp


class Helper (QObject):

    def __init__(self, MainWindow, scene, graph, parent = None):
        
        super (Helper, self).__init__ (parent)
        QObject.__init__ (self)
        
        self.main  = MainWindow
        self.scene = scene
        self.graph = graph
        
        self.ctimer = QTimer()
        
        #self.connect (self.ctimer, SIGNAL("timeout()"), self.singleUpdate)
        
        #self.ctimer.singleShot (500, self.singleUpdate)
        self.timer_flag = False
        
        # init harpoon and make it invisible
        self.harpoon = hp.Harpoon0 (0, 0, 0, 0)
        self.harpoon.setVisible (False)
    
    # - - - - - - - - - - - - - - - - - - - - 
        
    def initAndStartTimer (self):
        
        self.timer_flag = False
        
        if not self.ctimer.isActive():
            
            self.ctimer.singleShot (50, self.singleUpdate)
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