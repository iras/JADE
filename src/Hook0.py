'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui


class GText (QGraphicsTextItem):
    
    def __init__(self, str0='', parent=None, scene=None):
        
        QGraphicsTextItem.__init__ (self, str0, parent, scene)
    
    def boundingRect (self):
        
        # this is needed as the QGraphicsTextItem couldn't catch its hook's signal otherwise.
        return QRectF (0, 0, 0, 0)


class HookBox0 (QGraphicsItem):


    def __init__(self, parent=None, scene=None):
        
        QGraphicsItem.__init__ (self)
        
        self.helper = None
        self.parent = parent
        
        self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents (True)
        
        self.pen_color = QPen (Qt.black, 2)
        
        self.socket_id = None
        self.hookType  = None
        self.hookName  = ''
        
        # init Hook Animation Tweening
        self.timeline = QtCore.QTimeLine (200)
        self.timeline.setFrameRange (0, 100)
        self.anim = QtGui.QGraphicsItemAnimation ()
        self.anim.setItem (self)
        self.anim.setTimeLine (self.timeline)
        self.parent.helper.connect (self.timeline, QtCore.SIGNAL("finished()"), self.moveFurtherUp)
        self.anim_active = False
    
    def setTextfield (self):
        
        tx = 8
        
        self._text_item = GText (self.hookName, self)
        self._text_item.setEnabled (False)
        
        if self.hookType=='out' :
            tx=-50
            tmp0 = QTextBlockFormat ()
            tmp0.setAlignment (Qt.AlignRight)
            tmp = QTextCursor ()
            tmp.setBlockFormat(tmp0)
            self._text_item.setTextCursor (tmp)
        
        self._text_item.setPos (QPointF (tx, -5))
        self._text_item.setFont(QFont ("Geneva", 8, QFont.AllLowercase, False))
        self._text_item.setTextWidth (65)
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (2, 2, 10, 10)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        painter.setBrush (QBrush (Qt.white))
        painter.setPen   (self.pen_color)
        
        painter.drawEllipse (1, 1, 8 ,8)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def moveDown (self):
        
        self.anim_active = True
        self.up_flag=False
        
        self.timeline.stop ()
        self.hook_height = (self.pos_in_list-2)*10
        self.anim.setPosAt (0, QtCore.QPointF (self.x(), self.hook_height))
        self.hook_height += 10
        self.anim.setPosAt (1, QtCore.QPointF (self.x(), self.hook_height))
        self.timeline.start ()
        self.update ()
    
    def moveUp (self):
        
        if self.anim_active == False:
            
            if (self.parent.getHookPos(self)+1) < self.pos_in_list: # this check is to prevent the hooks with unchanged position from moving up.
            
                self.anim_active = True
                self.up_flag=True
                
                self.timeline.stop ()
                self.pos_in_list -= 1
                self.hook_height = float(self.y())
                self.anim.setPosAt (0, QtCore.QPointF (self.x(), self.hook_height))
                self.hook_height -= 10
                self.anim.setPosAt (1, QtCore.QPointF (self.x(), self.hook_height))
                self.timeline.start ()
                self.update ()
    
    # this method double-checks whether the hook needs to move up again as a result
    # of receiving other asynchronous "delete link" SIGNALs while moving up.
    def moveFurtherUp (self):
        
        self.anim_active = False
        
        if self.up_flag==True and self.parent.getHookPos(self)!=None: # it can happen to be None in the case the Hook gets only switched off instead of properly erased.
                        
            if (self.parent.getHookPos(self)+1) < self.pos_in_list:
                self.moveUp ()
    
    def switchOffHook (self, node_id, socket_id):
        
        if self.socket_id==socket_id:
                        
            self.parent.scrollRestOfHooksUp (self.hookType)
            self.setVisible (False)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def hoverEnterEvent (self, e):
        
        self.pen_color = QPen (Qt.red, 2)
        self.update ()
        
        # records the node_id in the helper's attribute.
        self.comm.setHoveredSocketId (self.socket_id)
        
        # deal with the harpoon.
        if not self.helper.isTimerEnded():
            self.setSelected (True)
            self.helper.getGraphView().addLinkAndWirePressBtnListener ()
        
        #self._text_item.setToolTip (self._text_item.toPlainText ())
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e):
        
        self.pen_color = QPen (Qt.black, 2)
        self.update ()
        
        # records the node_id in the helper's attribute.
        self.comm.setHoveredSocketId (None)
        
        #QGraphicsItem.hoverLeaveEvent (self, e)
    
    def mousePressEvent (self, e):
        
        self.harpoon.setInitPos (self.pos()+self.parent.pos())
        self.harpoon.setVisible (True)
        self.harpoon.update ()
        
        QGraphicsItem.mousePressEvent (self, e)
        self.update ()
    
    def mouseMoveEvent (self, e):
        
        self.harpoon.setEndPos (self.pos()+e.pos()+self.parent.pos())
        self.harpoon.update ()
    
    def mouseReleaseEvent (self, e):
        
        self.harpoon.setVisible (False)
        self.update ()
        
        self.helper.initAndStartTimer ()
        
        QGraphicsItem.mouseReleaseEvent (self, e)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getAbsPos (self): return self.pos()+self.parent.pos()
    
    def setSocketId (self, socket_id) : self.socket_id = socket_id
    def getSocketId (self): return self.socket_id
    
    def getHookType (self): return self.hookType
    def setHookType (self, htype): self.hookType = htype
    
    def setHelper (self, helper):
        
        self.helper  = helper
        self.comm    = self.helper.getGraph().getComm()
        self.harpoon = self.helper.getHarpoon()
    
    def setHookName (self, name0):
        
        self.hookName = name0
        self.setTextfield()
    
    def setPosInList (self, pos): self.pos_in_list=pos