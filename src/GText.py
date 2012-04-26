"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui


class GText (QGraphicsTextItem):


    def __init__(self, str0='', parent=None, scene=None):
        
        QGraphicsTextItem.__init__ (self, str0, parent, scene)
    
    def boundingRect (self):
        
        # this is needed as the QGraphicsTextItem could catch its hook's signal otherwise.
        return QRectF (0, 0, 0, 0)