"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

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
        
        self.tag_height_in_units = 0.0
        #self.in_socket_rail_y  = 0   # ANY USEFUL ?
        #self.out_socket_rail_y = 0   # ANY USEFUL ?
        
        self.comm = self.helper.getGraph().getComm()
        
        self.setFlags (QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents (True)
        self.previousMouseGrabberItem = None
        
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
        
        # init Tag's Animation Tweening
        self.timeline = QtCore.QTimeLine (200)
        self.timeline.setFrameRange (0, 100)
        self.anim = QtGui.QGraphicsItemAnimation ()
        self.anim.setItem (self)
        self.anim.setTimeLine (self.timeline)
        
        #self.qproperty = QPropertyAnimation(box, 'geometry', state1)
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (0, 0, 122, self.tag_height_in_units*10 + 20)
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
            painter.drawRect (0, 0, 120, self.tag_height_in_units*10 + 20)
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
        painter.drawRect (QRect (0, 0, 120, self.tag_height_in_units*10 + 20))
    
    def remove (self): self.setVisible (False)
    
    def scrollRestOfHooksUp (self, rail):
        
        marker = False
        tmp_index = None
        
        if rail=='in':
            
            ilen = len (self.inHooks)
            for i in range (0, ilen):
                self.inHooks[i].moveUp ()
        
        elif rail=='out':
            
            olen = len (self.outHooks)
            for i in range (0, olen):
                self.outHooks[i].moveUp ()
        else:
            print 'ERROR : there''s no more than two rails per socket'
        
        return [marker, tmp_index]
    
    def getHookPos (self, hk):
        
        pos = None
        
        if hk.getHookType()=='in':
            
            s_id = hk.getSocketId()
            ilen = len (self.inHooks)
            for i in range (0, ilen):
                if self.inHooks[i].getSocketId()==s_id:
                    pos = i
                    break
        
        elif hk.getHookType()=='out':
            
            s_id = hk.getSocketId()
            olen = len (self.outHooks)
            for i in range (0, olen):
                if self.outHooks[i].getSocketId()==s_id:
                    pos = i
                    break
        
        return pos
    
    # - - -  hook-related  methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def removeInHook  (self, node_id, inSocketId):
        
        if self.node_id==node_id:
            print 'RemoveInHook', node_id, inSocketId
            
            l = len (self.inHooks)
            for i in range(0, l):
                if self.inHooks[i].getSocketId()==inSocketId:
                    del self.inHooks[i]
                    break
            
            if self.isInsLessThanOuts()==True : self.reduceTagsHeight()
            
    def removeOutHook (self, node_id, outSocketId):
        
        if self.node_id==node_id:
            print 'RemoveOutHook', node_id, outSocketId
            
            l = len (self.outHooks)
            for i in range(0, l):
                if self.outHooks[i].getSocketId()==outSocketId:
                    del self.outHooks[i]
                    break
            
            if self.isOutsLessThanIns()==True : self.reduceTagsHeight()
    
    def reduceTagsHeight (self): self.tag_height_in_units-=1
    
    def isInsLessThanOuts (self):        
        flag=False
        if len (self.node_model.getIns())>=len (self.node_model.getOuts()):
            flag=True

        return flag
    
    def isOutsLessThanIns (self):
        flag=False
        if len (self.node_model.getIns())<=len (self.node_model.getOuts()):
            flag=True
        
        return flag
            
    
    def appendInHook (self, node_id, inSocketId):
        
        if self.node_id==node_id:
            print 'appendInHook', node_id, inSocketId
            
            no_ins  = len (self.node_model.getIns ())
            no_outs = len (self.node_model.getOuts())
            
            if no_ins>1:
                
                # (1) if the rect isn't long enough then start an anim to make it long enough to host the new inSocket
                if no_ins > no_outs : self.tag_height_in_units+=1
                
                # (2) duplicate the inSocket on top of the last one and scroll it down until it reaches its place
                tmp = self.addInHook (inSocketId, no_ins)
                # set off the animation
                tmp.moveDown ()
            
            else:
                # generate the first inSocket and place it in the topmost place
                tmp = self.addInHook (inSocketId, no_ins)
    
    def appendOutHook (self, node_id, outSocketId):
        
        if self.node_id==node_id:
            print 'appendOutHook',node_id, outSocketId
            
            no_ins  = len (self.node_model.getIns ())
            no_outs = len (self.node_model.getOuts())
            
            if no_outs>1:
                
                # (1) if the rect isn't long enough then start an anim to make it long enough to host the new inSocket
                if no_outs>no_ins : self.tag_height_in_units+=1
                
                # (2) duplicate the inSocket on top of the last one and scroll it down until it reaches its place
                tmp = self.addOutHook (outSocketId, no_outs)
                # set off the animation
                tmp.moveDown ()
            
            else:
                # generate the first inSocket and place it in the topmost place
                tmp = self.addOutHook (outSocketId, no_outs)
    
    def makeTagTaller (self):
                        
        self.timeline.stop ()
        self.anim.setPosAt (0, self.tag_height_in_units, self.tag_height_in_units)
        self.anim.setPosAt (1, self.tag_height_in_units, self.tag_height_in_units+1)
        self.timeline.start ()
        self.update ()
    
    def addInHook (self, socket_id, pos):
        
        hook = hk.HookBox0 (self)
        hook.setSocketId (socket_id)
        hook.setPosInList (pos)
        hook.setHookType ('in')
        hook.setHookName (self.helper.getGraph().getSocket(socket_id).getSType())
        hook.setHelper (self.helper)
        self.helper.connect (self.comm, SIGNAL ('deleteInSocket_MSignal (int,int)'), hook.switchOffHook)
        hook.setPos (QPointF (0,0))
        hook.setParentItem (self)
        
        self.inHooks.append (hook)
        
        return hook
    
    def addOutHook (self, socket_id, pos):
        
        hook = hk.HookBox0 (self)
        hook.setSocketId (socket_id)
        hook.setPosInList (pos)
        hook.setHookType ('out')
        hook.setHookName (self.helper.getGraph().getSocket(socket_id).getSType())
        hook.setHelper (self.helper)
        self.helper.connect (self.comm, SIGNAL ('deleteOutSocket_MSignal (int,int)'), hook.switchOffHook)
        hook.setPos (QPointF (110,0))
        hook.setParentItem (self)
        
        self.outHooks.append (hook)
        
        return hook
    
    # - - -  listeners  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def mousePressEvent (self, e):
        
        #self.setAcceptedMouseButtons(Qt.NoButton)
        self.previousMouseGrabberItem = self.scene.mouseGrabberItem()
        
        if e.button() == Qt.RightButton:
            pos = self.pos()
            self.comm.emitCtxMenuSignal (pos)
        
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
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def getSId  (self): return self.node_id
    def getComm (self): return self.comm
    def getInHooks  (self): return self.inHooks
    def getOutHooks (self): return self.outHooks