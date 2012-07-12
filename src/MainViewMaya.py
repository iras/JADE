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
        QObject.__init__(self) # initialisation indispensable for sending and receiving signals !!
                
        self.scene = QGraphicsScene()
        
        self.graph_model = graph
        self.helper = utility.Helper (self, self.scene, self.graph_model)
        self.graph_view  = grv.GraphView (self.graph_model, self.helper)
        self.helper.setGraphView (self.graph_view)
        
        # wirings
        comm = self.graph_model.getComm ()
        self.connect (comm, SIGNAL('addNode_MSignal(int)'),        self.graph_view.addTag)
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
        view.setObjectName(_fromUtf8("JADEview"))
        view.graphicsView.setObjectName(_fromUtf8("JADE2"))
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
        #layout.setObjectName ("Just Another DEpendency mapping tool")1
        #self.setLayout (layout)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        print
        cmds.control('JADE2', edit=True, ebg=True, bgc=[.5,.5,.9])
        print cmds.control('JADE2', query=True, p=True)
        print
    
        # wiring Contextual Menu
        self.menu = cmds.popupMenu ('JADEmenu', parent='JADEview', button=3, pmc = 'MayaClient.ui.ctxMenu()', aob=True)
        #self.menu = cmds.popupMenu ('JADEmenu', parent='viewPanes', alt=True, button=3, pmc = 'MayaClient.ui.ctxMenu()', aob=True)
    
    def retranslateUi (self, MainWindow):
        pass
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def keyPressEvent (self, e):
        
        if e.key() == Qt.Key_Backspace:
            self.graph_view.removeSelectedItems ()
    
    # - - -    context menu methods   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def ctxMenu (self):
        
        print 'CTXMENU'
        print cmds.getPanel (vis=True)
        print cmds.getPanel (wf=True)
        
        self.hovered_tag_id = self.graph_model.getComm().getHoveredItemId()
        
        if self.hovered_tag_id!=None:
            if self.first_click==True:
                left_list = self.graph_model.getInsTypesLeft (self.hovered_tag_id)
                if len(left_list)!=0:
                    
                    self.prepareNodeCtxMenu (left_list)
            else:
                left_list = self.graph_model.getOutsTypesLeft (self.hovered_tag_id)
                if len(left_list)!=0:
                    
                    self.prepareNodeCtxMenu (left_list)
        else:
            # ctx menu to establish what node is going to be retrieved
            tmp_ls = []
            [tmp_ls.append(key) for key in self.graph_model.getRules()]
            self.prepareGeneralCtxMenu (tmp_ls)
    
    def prepareGeneralCtxMenu (self, list0):
        
        # clear all the menu items out.
        cmds.popupMenu ('JADEmenu', edit=True, dai=True)
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            tmp = cmds.menuItem (parent=self.menu, label=str(i), c='MayaClient.ui.addTag ("'+str(i)+'")')
    
    def addTag (self, name0):
        
        tmp = self.graph_model.addNode ()
        tmp.setName (name0)
    
    def prepareNodeCtxMenu (self, list0):
        
        #self.menu.clear()
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            tmp = cmds.menuItem (parent=self.menu, label=str(i), c='MayaClient.ui.addSocketAction ("'+str(i)+'")')
    
    def addSocketAction (self, value):
        
        if self.first_click==True:
            
            self.first_click=False
            tag = self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            
            # the event released by adding an InSocket signal will trigger the Tag0's method appendInHook() as a result.
            self.graph_model.addInSocket (self.hovered_tag_id, value)
        else:
            
            self.first_click=True
            tag = self.graph_view.getTag (self.hovered_tag_id) # retrieve the tag the ctx menu was open above.
            
            # the event released by adding an InSocket signal will trigger the Tag0's method appendOutHook as a result.
            self.graph_model.addOutSocket (self.hovered_tag_id, value)
