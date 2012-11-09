'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import View0

import GraphView as grv
import Utility0 as utility


class MainWindow (QWidget):
    '''
    Base widget for the JADE standalone app.
    Notice the difference with the MainMayaWindow. This class is subclassing QWidget while the Maya one subclasses QObject.
    
    This class handles the Qt contextual menu.
    '''
    def __init__ (self, graph, parent=None):
        '''constructor
        
        @param graph the model
        @param parent a parent QWidget, or None for root window.
        '''
        QWidget.__init__ (self, parent)
        
        # define scene and constrain its workspace
        self.scene = QGraphicsScene()
        qrect = QRectF(-1000, -1000, 2000, 2000)
        self.scene.setSceneRect(qrect)
        
        self.graph_model = graph
        self.helper = utility.Helper (self, self.scene, self.graph_model)
        self.graph_view  = grv.GraphView (self.graph_model, self.helper)
        self.helper.setGraphView (self.graph_view)
        
        # wiring Contextual Menu
        self.menu = QMenu ()
        self.setContextMenuPolicy (Qt.CustomContextMenu)
        self.connect (self, SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
        
        # wirings
        comm = self.graph_model.getComm ()
        self.connect (comm, SIGNAL('addNode_MSignal(int, float, float)'), self.graph_view.addTag)
        self.connect (comm, SIGNAL('deleteNode_MSignal(int)'), self.graph_view.removeTag)
        self.connect (comm, SIGNAL('addLink_MSignal(int,int)'), self.graph_view.addWire)
        self.connect (comm, SIGNAL('deleteLink_MSignal(int,int)'), self.graph_view.checkIfEmpty)
        
        view = View0.View ('Main view', self.graph_view)
        view.wireViewItemsUp ()
        view.getGraphicsView().setScene (self.scene)
        
        self.graphicsView = view.getGraphicsView ()
        self.node_coords = QPoint (0,0)
        
        layout = QHBoxLayout ()
        layout.setContentsMargins(QMargins(0,0,0,0));
        layout.addWidget (view)
        self.setLayout (layout)
        
        self.setWindowTitle("Just Another DEpendency mapping tool")
        
        self.scene.addItem (self.helper.getHarpoon ())
        
        self.alt_pressed = False
        self.ctl_pressed = False
                
        self.hovered_tag_id = None
    
    def mousePressEvent (self, e):
        '''Callback function dealing with pressing a mouse button.
        
        @param e event
        '''
        modif = int (e.modifiers())
        ctrl  = (modif&0x04000000) != 0
        alt   = (modif&0x08000000) != 0
        #shift = (modif&0x02000000) != 0
        
        if alt:  self.alt_pressed = True
        else:    self.alt_pressed = False
        
        if ctrl: self.ctl_pressed = True
        else:    self.ctl_pressed = False
        
        QWidget.mousePressEvent (self, e)
    
    def keyPressEvent (self, e):
        '''Callback function dealing with pressing a keyboard key.
        
        @param e event
        '''
        if e.key() == Qt.Key_Backspace:
            self.graph_view.removeSelectedItems ()
    
    # - - -    context menu methods   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def ctxMenu (self, pos):
        '''Callback function dealing with invoking the contextual menu.
        
        @param pos position
        '''
        self.hovered_tag_id = self.graph_model.getComm().getHoveredItemId()
        
        self.menu.clear()
        
        if self.hovered_tag_id!=None:
            if self.ctl_pressed == True:
                left_list = self.graph_model.getInsTypesLeft (self.hovered_tag_id)
                if len(left_list)!=0:
                    
                    self.prepareNodeCtxMenu (left_list)
                    self.menu.popup (self.mapToGlobal (pos))
            
            elif self.alt_pressed == True:
                right_list = self.graph_model.getOutsTypesLeft (self.hovered_tag_id)
                if len(right_list)!=0:
                    
                    self.prepareNodeCtxMenu (right_list)
                    self.menu.popup (self.mapToGlobal (pos))
        else:
            # ctx menu to establish what node is going to be retrieved
            tmp_ls = []
            [tmp_ls.append(key) for key in self.graph_model.getNodesDecription()]
            self.prepareGeneralCtxMenu (tmp_ls)
            self.menu.popup (self.mapToGlobal (pos))
            self.node_coords = self.graphicsView.mapToScene (pos)
    
    def prepareGeneralCtxMenu (self, list0):
        '''populates the QMenu dynamically with available node infos and pass the menu string name to the receiver.
        
        @param list0 list of menu items
        '''
        for i in list0:
            
            tmp = self.menu.addAction(i)
            receiver = lambda value=i: self.addTag (value)
            self.connect (tmp, QtCore.SIGNAL('triggered()'), receiver)
    
    def addTag (self, name0):
        '''adds a Tag0 instance by name. the constants added to the are needed to make the tag pop up near the mouse pointer.
        
        @param name0 string
        '''
        self.graph_model.addNode (name0, self.node_coords.x() - 50, self.node_coords.y() - 80)
    
    def prepareNodeCtxMenu (self, list0):
        '''populates the QMenu dynamically with available socket names and pass the menu string name to the receiver. Also, it generates closures as callbacks for each item.
        
        @param list0 list of menu items.
        '''
        for i in list0:
            tmp = self.menu.addAction(i)
            receiver = lambda value=i: self.addSocketAction (value)
            self.connect (tmp, QtCore.SIGNAL('triggered()'), receiver)
    
    def addSocketAction (self, value):
        '''adds a socket name based on the key modifier pressed.
        
        @param value
        '''
        if self.ctl_pressed == True:
            
            tag = self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            # the event released by adding an InSocket signal will trigger the Tag0's method appendInHook() as a result.
            self.graph_model.addInSocket (self.hovered_tag_id, value)
        
        elif self.alt_pressed == True:
            
            tag = self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            # the event released by adding an InSocket signal will trigger the Tag0's method appendOutHook as a result.
            self.graph_model.addOutSocket (self.hovered_tag_id, value)
