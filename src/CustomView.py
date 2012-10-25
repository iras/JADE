"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import GText as gt


class CustomView (QGraphicsView):
    
    def __init__(self, scene=None):
        
        QGraphicsView.__init__ (self)
    
    def mousePressEvent(self, event):
        
        # this distinction with events needs to be done for the Maya integration,
        # otherwise the cmds.popupmenu wouldn't work in the QGraphicsView as it
        # would override the Maya cmds.popupmenu's signals.
        if (event.button()==Qt.RightButton): 
            event.ignore()
        else:
            QGraphicsView.mousePressEvent (self, event) # <-- added this line.