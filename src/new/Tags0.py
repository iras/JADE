'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import Comm0
import Hook0 as hk


class Tag1 (QGraphicsItem):
    
    def __init__ (self, color, node_id, helper, parent=None):
        
        QGraphicsItem.__init__ (self)
        
        self.node_id = node_id
        self.helper  = helper
        self.node_model = self.helper.getGraph().getNode(self.node_id)
        
        self.inHooks  = []
        self.outHooks = []
        
        self.scene = self.helper.getScene ()
        
        self.harpoon = self.helper.getHarpoon()
        self.color = color
        
        self.tag_height_in_units = 0
        #self.in_socket_rail_y  = 0   # ANY USEFUL ?
        #self.out_socket_rail_y = 0   # ANY USEFUL ?
        
        self.comm = self.helper.getGraph().getComm()
        
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
        #self._text_item.setTextInteractionFlags (Qt.TextEditable)
        self._text_item.setPos (QPointF (20, 20))
        self._text_item.setFont (QFont ("Geneva", 10, QFont.Bold, False))
        self._text_item.setTextWidth(50)
        self._text_item.setToolTip(self._text_item.toPlainText ())
        #self._text_item.setHtml("<h2 align=\"center\">hello</h2><h2 align=\"center\">world 1234345345</h2>123");
        
        # init animation tweening
        self.tl = QtCore.QTimeLine (500)
        self.tl.setFrameRange (0, 100)
        self.anim = QtGui.QGraphicsItemAnimation ()
        self.anim.setTimeLine (self.tl)
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (0, 0, 82, self.tag_height_in_units*10 + 20)
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
            painter.drawRect (0, 0, 80, self.tag_height_in_units*10 + 20)
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
        painter.drawRect (QRect (0, 0, 80, self.tag_height_in_units*10 + 20))
    
    def remove (self): self.setVisible (False)
    
    # - - -  miscellanea  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    
    
    
    
    
    
    def appendInHook (self, node_id, inSocketId):
        
        if self.node_id==node_id:
            print 'appendInHook', node_id, inSocketId
            
            no_ins  = len (self.node_model.getIns ())
            no_outs = len (self.node_model.getOuts())
            
            if no_ins>1:
                
                # (1) if the rect isn't long enough then start an anim to make it long enough to host the new inSocket
                if no_ins > no_outs : self.tag_height_in_units+=1
                
                # (2) duplicate the inSocket on top of the last one and scroll it down until it reaches its place
                tmp = self.addInHook (inSocketId)
                # set off the animation
                self.anim.setItem (tmp)
                self.startOffAnim (tmp, no_ins)
            
            else:
                # generate the first inSocket and place it in the topmost place
                tmp = self.addInHook (inSocketId)
    
    def appendOutHook (self, node_id, outSocketId):
        
        if self.node_id==node_id:
            print 'appendOutHook',node_id, outSocketId
            
            no_ins  = len (self.node_model.getIns ())
            no_outs = len (self.node_model.getOuts())
            
            if no_outs>1:
                
                # (1) if the rect isn't long enough then start an anim to make it long enough to host the new inSocket
                if no_outs>no_ins : self.tag_height_in_units+=1
                
                # (2) duplicate the inSocket on top of the last one and scroll it down until it reaches its place
                tmp = self.addOutHook (outSocketId)
                # set off the animation
                self.anim.setItem (tmp)
                self.startOffAnim (tmp, no_outs)
            
            else:
                # generate the first inSocket and place it in the topmost place
                tmp = self.addOutHook (outSocketId)
    
    
    
    def startOffAnim (self, item, y):
        
        self.tl.stop ()
        self.height_hook_platform = (y-2)*10
        self.anim.setPosAt (0, QtCore.QPointF (item.x(), self.height_hook_platform))
        self.height_hook_platform += 10
        self.anim.setPosAt (1, QtCore.QPointF (item.x(), self.height_hook_platform))
        self.tl.start ()
        self.update ()
    
    
    
    
    
    def addInHook (self, socket_id):
        
        tmp_hook = hk.HookBox0 (self)
        tmp_hook.setSocketId (socket_id)
        tmp_hook.setHelper (self.helper)
        tmp_hook.setPos (QPointF (0,0))
        tmp_hook.setParentItem (self)
        
        self.inHooks.append (tmp_hook)
        
        return tmp_hook
    
    def addOutHook (self, socket_id):
        
        tmp_hook = hk.HookBox0 (self, socket_id)
        tmp_hook.setSocketId (socket_id)
        tmp_hook.setHelper (self.helper)
        tmp_hook.setPos (QPointF (70,0))
        tmp_hook.setParentItem (self)
        
        self.outHooks.append (tmp_hook)
        
        return tmp_hook
    
    def removeInHook  (self) : pass
    def removeOutHook (self) : pass
    
    
    
    
    
    
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def mousePressEvent (self, e):
        
        #self.setAcceptedMouseButtons(Qt.NoButton)
        self.previousMouseGrabberItem = self.scene.mouseGrabberItem()
        
        if e.button() == Qt.RightButton:
            pos = self.pos()
            self.comm.emitCtxMenuSignal (pos)
        
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
    
    def mouseReleaseEvent (self, e):
        
        self.update ()
        QGraphicsItem.mouseReleaseEvent (self, e)
    
    def hoverEnterEvent (self, e):
        
        # records the node_id in the helper's attribute.
        self.comm.setHoveredItemId (self.node_id)
        
        self._text_item.setToolTip (self._text_item.toPlainText ())
        
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e):
        
        # records the node_id in the helper's attribute.
        self.comm.setHoveredItemId (None)
    
    """
    # drag-n-drop behaviour : listeners
    
    def dragEnterEvent(self, event): 
        print "dragEnterEvent: %s (event type: %d)" % (type(event), event.type())
        event.acceptProposedAction() 
    
    def dragMoveEvent (self, e) : pass
    def dragLeaveEvent (self, e): pass
    
    def dropEvent (self, e):
        print e.type ()
        print 'caught '+str(self.node_id)
    """
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def getSId  (self): return self.node_id
    def getComm (self): return self.comm
    def getInHooks  (self): return self.inHooks
    def getOutHooks (self): return self.outHooks