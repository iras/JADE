'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import Comm
import Harpoon as hp
import Hook as hk

class Tag0 (QGraphicsItem):
    
    def __init__ (self, harpoon, color, node_id, helper, parent=None):
        
        QGraphicsItem.__init__ (self)
        
        self.node_id = node_id
        self.helper  = helper
        
        self.scene = self.helper.getScene ()
        
        self.harpoon = harpoon
        self.color = color
        
        self.comm = Comm.Comm ()
        
        self.setFlags (QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents (True)
        self.previousMouseGrabberItem = None
        
        """
        # drag-n-drop behaviour : init
        self.setAcceptDrops (True)
        """
        
        self.setZValue (1.0)
        
        self.height = 0
        self.height_hook_platform = 0
        
        self._text_item = QGraphicsTextItem ('text '+str(self.node_id), self)
        self._text_item.setTextInteractionFlags (Qt.TextEditable)
        self._text_item.setPos (QPointF (20, 20))
        self._text_item.setFont (QFont ("Geneva", 10, QFont.Bold, False))
        self._text_item.setTextWidth(50)
        self._text_item.setToolTip(self._text_item.toPlainText ())
        #self._text_item.setHtml("<h2 align=\"center\">hello</h2><h2 align=\"center\">world 12334345354444444444444444444444444</h2>123");
        
        self._box = hk.HookBox (self)
        self._box.setParentItem (self)
        
        self.tl = QtCore.QTimeLine (500)
        self.tl.setFrameRange (0, 100)
        self.a = QtGui.QGraphicsItemAnimation ()
        self.a.setItem (self._box)
        self.a.setTimeLine (self.tl)
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (0, 0, 82, 42)
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
            painter.drawRect (0, 0, 80, 40)
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
        
        painter.drawRoundRect (QRect (0, 0, 80, 34+self.height), 20)
    
    def remove (self): self.setVisible (False)
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addedLinkSignal (self, node_id):
        
        if node_id==self.node_id:
            
            self.tl.stop ()
            self.a.setPosAt (0, QtCore.QPointF(1, self.height_hook_platform))
            self.height_hook_platform += 5
            self.a.setPosAt (1, QtCore.QPointF(1, self.height_hook_platform))
            self.tl.start ()
            self.update ()
    
    def deletedLinkSignal (self, node_id):
        
        if node_id==self.node_id:
            
            self.tl.stop ()
            self.a.setPosAt (0, QtCore.QPointF(1, self.height_hook_platform))
            self.height_hook_platform -= 5
            self.a.setPosAt (1, QtCore.QPointF(1, self.height_hook_platform))
            self.tl.start ()
            self.update ()
    
    def mousePressEvent (self, e):
        
        #self.setAcceptedMouseButtons(Qt.NoButton)
        self.previousMouseGrabberItem = self.scene.mouseGrabberItem()
        
        if e.button() == Qt.RightButton:
            pass
        
        if e.modifiers() & Qt.ShiftModifier:
            #e.ignore()
            self.harpoon.setInitPos (self.pos())
            self.harpoon.setVisible (True)
            self.harpoon.update ()
        """
        # drag-n-drop behaviour : action
        
        if e.modifiers() & Qt.ShiftModifier:
            md = QMimeData () 
            md.setText ("test") 
            drag = QDrag (e.widget()) 
            drag.setMimeData (md) 
            drag.start (Qt.MoveAction)
        """
        QGraphicsItem.mousePressEvent (self, e)
        self.update ()
    
    def mouseMoveEvent (self, e):
        
        if e.modifiers () & Qt.ShiftModifier:
            
            self.harpoon.setEndPos (e.pos()+self.pos())
            self.harpoon.update ()
        
        else:
            QGraphicsItem.mouseMoveEvent (self, e)
    
    def mouseReleaseEvent (self, e):
        
        self.harpoon.setVisible (False)
        self.update ()
        
        self.helper.initAndStartTimer ()
        
        QGraphicsItem.mouseReleaseEvent (self, e)
        
    
    def hoverEnterEvent (self, e):
        
        # deal with the harpoon.
        if not self.helper.isTimerEnded():
            self.setSelected (True)
            self.helper.getMain().addLinkAndWireButtonHook ()
            
                
        self._text_item.setToolTip (self._text_item.toPlainText ())
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e): pass
    
    """
    # drag-n-drop behaviour : listeners
    
    def dragEnterEvent(self, event): 
        print "dragEnterEvent: %s (event type: %d)" % (type(event), event.type())
        event.acceptProposedAction() 
    
    def dragMoveEvent (self. e) : pass
    def dragLeaveEvent (self. e): pass
    
    def dropEvent (self, e):
        print e.type ()
        print 'caught '+str(self.node_id)
    """
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def getNodeId (self): return self.node_id
    def getComm   (self): return self.comm