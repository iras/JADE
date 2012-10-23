'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
'''

'''
JADE mapping tool
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import maya.cmds as cmds

import View0

import GraphView as grv
import Utility0 as utility


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class MainMayaWindow (QObject):
    
    def __init__ (self, graph, parent=None):
        
        super (MainMayaWindow, self).__init__(parent)
        QObject.__init__(self) # initiation indispensable for sending and receiving signals!
        
        self.scene = QGraphicsScene()
        
        self.graph_model = graph
        self.helper = utility.Helper (self, self.scene, self.graph_model)
        self.graph_view  = grv.GraphView (self.graph_model, self.helper)
        self.helper.setGraphView (self.graph_view)
        
        # wirings
        comm = self.graph_model.getComm ()
        self.connect (comm, SIGNAL('addNode_MSignal(int, float, float)'), self.graph_view.addTag)
        self.connect (comm, SIGNAL('deleteNode_MSignal(int)'),     self.graph_view.removeTag)
        self.connect (comm, SIGNAL('addLink_MSignal(int,int)'),    self.graph_view.addWire)
        self.connect (comm, SIGNAL('deleteLink_MSignal(int,int)'), self.graph_view.checkIfEmpty)
        
        self.scene.addItem (self.helper.getHarpoon ())
        
        self.hovered_tag_id = None
        self.first_click = False
    
    def setupUi (self, MainWindow):
        
        MainWindow.setObjectName(_fromUtf8 ("MainWindow"))
        MainWindow.resize(494, 1396)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Location Tool", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        
        self.verticalLayoutWidget = QtGui.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 600, 1000))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 350, 350))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        view = View0.View ("JADEview", self.scrollAreaWidgetContents_3)
        view.setObjectName(_fromUtf8("JADEview"))  # real ui name
        view.graphicsView.setObjectName(_fromUtf8("JADEInnerView"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout.addWidget(self.scrollArea)
        
        self.hSplit = QSplitter (self.scrollAreaWidgetContents_3)
        
        vSplit = QSplitter (self.scrollAreaWidgetContents_3)
        vSplit.setOrientation (Qt.Vertical)
        vSplit.addWidget (self.hSplit)
        
        view.setClientAndWireViewItems (self.graph_view)
        view.view().setScene (self.scene)
        self.hSplit.addWidget (view)
        
        layout = QHBoxLayout (self.scrollAreaWidgetContents_3)
        layout.addWidget (vSplit)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        """
        cmds.control('JADEInnerView', edit=True, ebg=True, bgc=[.5,.5,.9])
        print cmds.control('JADEInnerView', query=True, p=True)
        """
        
        # wiring the Maya Contextual pop-up Menu
        self.menu        = cmds.popupMenu ('JADEmenu',        parent='JADEInnerView', button=3, pmc = 'ClientMaya.ui.ctxMenu()', aob=True)
        self.menuAddOuts = cmds.popupMenu ('JADEmenuAddOuts', parent='JADEInnerView', button=3, pmc = 'ClientMaya.ui.ctxMenuAddOuts()', aob=True, alt=True)
        self.menuAddIns  = cmds.popupMenu ('JADEmenuAddIns',  parent='JADEInnerView', button=3, pmc = 'ClientMaya.ui.ctxMenuAddIns()',  aob=True, ctl=True)
    
    def retranslateUi (self, MainWindow):
        pass
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def keyPressEvent (self, e):    # ...can't use this one within Maya : REMOVE it.
        
        if e.key() == Qt.Key_Backspace:
            self.graph_view.removeSelectedItems ()
    
    # - - -    context menus methods   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def ctxMenu (self):
        
        self.hovered_tag_id = self.graph_model.getComm().getHoveredItemId()
        
        cmds.popupMenu ('JADEmenu', edit=True, dai=True) # clear all the menu items out.
        
        if self.hovered_tag_id==None:
            # ctx menu to establish what node is going to be retrieved
            tmp_ls = []
            [tmp_ls.append(key) for key in self.graph_model.getRules()]
            self.prepareGeneralCtxMenu (tmp_ls)
    
    def prepareGeneralCtxMenu (self, list0):
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            cmds.menuItem (parent=self.menu, label=str(i), c='ClientMaya.ui.addTag ("'+str(i)+'")')
    
    def addTag (self, name0):
        
        tmp = self.graph_model.addNode ()
        tmp.setName (name0)
    
    def ctxMenuAddOuts (self):
        
        self.hovered_tag_id = self.graph_model.getComm().getHoveredItemId()
        
        cmds.popupMenu ('JADEmenuAddOuts', edit=True, dai=True) # clear all the menu items out.
        
        if self.hovered_tag_id!=None:
            
            right_list = self.graph_model.getOutsTypesLeft (self.hovered_tag_id)
            if len(right_list)!=0:
                self.prepareNodeCtxMenuOnAddingOuts (right_list)
    
    def ctxMenuAddIns (self):
        
        self.hovered_tag_id = self.graph_model.getComm().getHoveredItemId()
        
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
        
        self.helper.setMenu(self.menuAddIns)
    
    def addOutSocketAction (self, value):
        
            self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            
            # the event released by adding an InSocket signal will trigger the Tag0's method appendOutHook as a result.
            self.graph_model.addOutSocket (self.hovered_tag_id, value)
    
    def addInSocketAction (self, value):
        
        self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            
        # the event released by adding an InSocket signal will trigger the Tag0's method appendInHook() as a result.
        self.graph_model.addInSocket (self.hovered_tag_id, value)
