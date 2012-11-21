'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import QObject, QRectF, SIGNAL, QRect, QPoint, QMargins, QMetaObject
from PyQt4.QtGui import QGraphicsScene, QSizePolicy, QFont, QHBoxLayout, QCursor, QMainWindow, QTabWidget, QApplication, QWidget

import maya.cmds as cmds

import GraphView as grv
import JADEmisc.Utility0 as utility
import View0



class MainMayaWindow (QObject):
    '''
    Base QObject for the JADE Maya scripted plugin.
    Notice the difference with the MainMWindow. This class is subclassing QObject while the Standalone one subclasses QWidget.
    
    This class handles the Maya way to deal with the contextual pop-up menu. Additionally, this class shares some of the responsibilities with graph.py.
    '''
    def __init__ (self, graph, parent=None):
        '''constructor
        
        @param graph the model
        @param parent a parent QObject, or None for root window.
        '''
        super (MainMayaWindow, self).__init__(parent)
        QObject.__init__(self) # initiation indispensable for sending and receiving signals!
        
        # define scene and constrain its workspace
        self.scene = QGraphicsScene ()
        self.scene.setSceneRect (QRectF (-1000, -1000, 2000, 2000))
        
        self.graph_model = graph
        self.helper = utility.Helper (self, self.scene, self.graph_model)
        self.graph_view  = grv.GraphView (self.graph_model, self.helper)
        self.helper.setGraphView (self.graph_view)
        
        # wirings
        self.comm = self.graph_model.getComm ()
        self.connect (self.comm, SIGNAL ('deleteNode_MSignal(int)'), self.graph_view.removeTag)
        self.connect (self.comm, SIGNAL ('addLink_MSignal(int,int)'), self.graph_view.addWire)
        self.connect (self.comm, SIGNAL ('deleteLink_MSignal(int,int)'), self.graph_view.checkIfEmpty)
        self.connect (self.comm, SIGNAL ('addNode_MSignal(int, float, float)'), self.graph_view.addTag)
        
        self.scene.addItem (self.helper.getHarpoon ())
        
        self.hovered_tag_id = None
    
    def setupUi (self, MainWindow):
        
        MainWindow.setObjectName ('MainWindow')
        MainWindow.resize (800, 1396)
        sizePolicy = QSizePolicy (QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch (0)
        sizePolicy.setVerticalStretch (0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont ()
        font.setPointSize (11)
        MainWindow.setFont (font)
        MainWindow.setWindowTitle (QApplication.translate("MainWindow", "Location Tool", None, QApplication.UnicodeUTF8))
        MainWindow.setTabShape (QTabWidget.Rounded)
        MainWindow.setDockOptions (QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        
        self.scrollAreaWidgetContents_3 = QWidget (MainWindow)
        self.scrollAreaWidgetContents_3.setGeometry (QRect(10, 10, 900, 1000))
        self.scrollAreaWidgetContents_3.setObjectName ('scrollAreaWidgetContents_3')
        self._view = View0.View ("JADEview", self.graph_view, self.scene, self.scrollAreaWidgetContents_3)
        self._view.setObjectName ('JADEview')  # real ui name
        self._view.graphicsView.setObjectName ('JADEInnerView')
        self.connect (self.scene, SIGNAL("selectionChanged()"), self._view.selectionChanged)
        
        self._view.wireViewItemsUp ()
        self._view.getGraphicsView().setScene (self.scene)
        self._view.setToolboxCSSColorScheme ('background-color: rgb(68,68,68);color: rgb(200,200,200)') # this needs to be done since the toolbox's background didn't have a uniform colour otherwise.
        #self._view.setGraphicsViewCSSBackground () # the CSS background doesn't seem to work in Maya as there seems to be a problem with cleaning QGraphicsLineItems when they move, that doesn't happen when there's no CSS applied to the background.

        self.graphicsView = self._view.getGraphicsView ()
        self.node_coords = QPoint (0,0)
        
        layout = QHBoxLayout (self.scrollAreaWidgetContents_3)
        layout.setContentsMargins (QMargins(0,0,0,0));
        layout.addWidget (self._view)
        
        self.retranslateUi (MainWindow)
        QMetaObject.connectSlotsByName (MainWindow)
        
        """
        cmds.control('JADEInnerView', edit=True, ebg=True, bgc=[.5,.5,.9])
        print cmds.control('JADEInnerView', query=True, p=True)
        """
        
        # wiring the Maya Contextual pop-up Menu
        self.menu        = cmds.popupMenu ('JADEmenu',        parent='JADEInnerView', button=3, pmc = 'ClientMaya.ui.ctxMenu()',        aob=True)
        self.menuAddOuts = cmds.popupMenu ('JADEmenuAddOuts', parent='JADEInnerView', button=3, pmc = 'ClientMaya.ui.ctxMenuAddOuts()', aob=True, alt=True)
        self.menuAddIns  = cmds.popupMenu ('JADEmenuAddIns',  parent='JADEInnerView', button=3, pmc = 'ClientMaya.ui.ctxMenuAddIns()',  aob=True, ctl=True)
        
        # this class property is used to keep track of the mouse position.
        self._mouse = QCursor
        
        # self._view's zoom slider (we need this to correct the bias added to sort the mouse position when the zoom changes - ONLY in Maya)
        self._zoom_slider = self._view.getZoomSlider()
    
    def retranslateUi (self, MainWindow):
        pass
    
    # - - -    context menus methods   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def ctxMenu (self):
        
        self.hovered_tag_id = self.comm.getHoveredItemId()
        
        cmds.popupMenu ('JADEmenu', edit=True, dai=True) # clear all the menu items out.
        
        if self.hovered_tag_id==None:
            # ctx menu to establish what node is going to be retrieved
            tmp_ls = []
            [tmp_ls.append(key) for key in self.graph_model.getNodesDecription()]
            self.prepareGeneralCtxMenu (tmp_ls)
    
    def prepareGeneralCtxMenu (self, list0):
        
        self.node_coords = self.graphicsView.mapToScene (self._mouse.pos())
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            cmds.menuItem (parent=self.menu, label=str(i), c='ClientMaya.ui.addTag ("'+str(i)+'")')
    
    def addTag (self, name0):
        
        # the piece-wise linear interpolation below is a workaround only present in the Maya JADE mapping tool since the self.graphicsView.mapToScene() doesn't seem to work as the standalone's one.
        if self._zoom_slider.value() > 199 and self._zoom_slider.value() < 241:
            x_bias = -22.5*(self._zoom_slider.value()-200) + 2100
            y_bias = -3.75*(self._zoom_slider.value()-200) + 400
        elif self._zoom_slider.value() > 240 and self._zoom_slider.value() < 281:
            x_bias = -12.5*(self._zoom_slider.value()-240) + 1200
            y_bias = -2.5* (self._zoom_slider.value()-240) + 250
        
        new_node = self.graph_model.addNode (name0, self.node_coords.x() - x_bias, self.node_coords.y() - y_bias)
        self._view.updateCurrentClusterNodeList (new_node)
    
    def ctxMenuAddOuts (self):
        
        self.hovered_tag_id = self.comm.getHoveredItemId()
        
        cmds.popupMenu ('JADEmenuAddOuts', edit=True, dai=True) # clear all the menu items out.
        
        if self.hovered_tag_id!=None:
            
            right_list = self.graph_model.getOutsTypesLeft (self.hovered_tag_id)
            if len(right_list)!=0:
                self.prepareNodeCtxMenuOnAddingOuts (right_list)
    
    def ctxMenuAddIns (self):
        
        self.hovered_tag_id = self.comm.getHoveredItemId()
        
        cmds.popupMenu ('JADEmenuAddIns', edit=True, dai=True) # clear all the menu items out.
        
        if self.hovered_tag_id!=None:
            
            left_list = self.graph_model.getInsTypesLeft (self.hovered_tag_id)
            if len(left_list)!=0:
                self.prepareNodeCtxMenuOnAddingIns (left_list)
    
    def prepareNodeCtxMenuOnAddingOuts (self, list0):
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            cmds.menuItem (parent=self.menuAddOuts, label=str(i), c='ClientMaya.ui.addOutSocketAction ("'+str(i)+'")')
        
        self.helper.setMenu(self.menuAddOuts)
    
    def prepareNodeCtxMenuOnAddingIns (self, list0):
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            cmds.menuItem (parent=self.menuAddIns, label=str(i), c='ClientMaya.ui.addInSocketAction ("'+str(i)+'")')
        
        self.helper.setMenu (self.menuAddIns)
    
    def addOutSocketAction (self, value):
        
            self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            
            # the event released by adding an InSocket signal will trigger the Tag0's method appendOutHook as a result.
            self.graph_model.addOutSocket (self.hovered_tag_id, value)
    
    def addInSocketAction (self, value):
        
        self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            
        # the event released by adding an InSocket signal will trigger the Tag0's method appendInHook() as a result.
        self.graph_model.addInSocket (self.hovered_tag_id, value)
