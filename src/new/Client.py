'''
JADE mapping tool

Created on Feb 23, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import View0

import Graph as gr
import GraphView as grv
import Utility0 as utility



class MainWindow (QWidget):
    
    def __init__ (self, graph, parent=None):
        
        QWidget.__init__ (self, parent)
        
        self.scene = QGraphicsScene()
        
        self.graph_model = graph
        self.graph_model.setConnectionsMap (self.initConnectionsMap())
        self.helper = utility.Helper (self, self.scene, self.graph_model)
        self.graph_view  = grv.GraphView (self.graph_model, self.helper)
        self.helper.setGraphView (self.graph_view)
        
        # wiring Contextual Menu
        self.menu = QMenu ()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect (self, SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
        
        # wirings
        comm = self.graph_model.getComm ()
        self.connect (comm, SIGNAL('addNode_MSignal(int)'),        self.graph_view.addTag)
        self.connect (comm, SIGNAL('addLink_MSignal(int,int)'),    self.graph_view.addWire)
        self.connect (comm, SIGNAL('deleteLink_MSignal(int,int)'), self.graph_view.checkIfEmpty)
        
        #self.setMouseTracking (True)
        #self.setAttribute(Qt.WA_Hover)
        
        self.populateScene ()
        
        self.hSplit = QSplitter ()
        
        vSplit = QSplitter ()
        vSplit.setOrientation (Qt.Vertical)
        vSplit.addWidget (self.hSplit)
        
        view = View0.View ("Main view")
        view.setClientAndWireViewItems (self.graph_view)
        view.view().setScene (self.scene)
        self.hSplit.addWidget (view)
        
        layout = QHBoxLayout ()
        layout.addWidget (vSplit)
        self.setLayout (layout)
        
        self.setWindowTitle("Just Another DEpendency mapping tool")
        
        self.scene.addItem (self.helper.getHarpoon ())
        
        self.hovered_tag_id = None
        self.first_click = False
    
    def keyPressEvent (self, e):
        
        if e.key() == Qt.Key_Backspace:
            self.graph_view.removeSelectedItems ()
    
    def populateScene (self):
        
        self.graph_view.addNodeAndTag ()
    
    # - - -    context menu methods   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def ctxMenu (self, pos):
        
        self.hovered_tag_id = self.graph_model.getComm().getHoveredItemId()
        
        if self.hovered_tag_id!=None:
            if self.first_click==True:
                left_list = self.graph_model.getInsTypesLeft (self.hovered_tag_id)
                if len(left_list)!=0:
                    
                    self.prepareCtxMenu (left_list)
                    self.menu.popup (self.mapToGlobal (pos))
            else:
                left_list = self.graph_model.getOutsTypesLeft (self.hovered_tag_id)
                if len(left_list)!=0:
                    
                    self.prepareCtxMenu (left_list)
                    self.menu.popup (self.mapToGlobal (pos))
    
    def prepareCtxMenu (self, list0):
        
        self.menu.clear()
        
        # populate the QMenu dynamically and pass the menu string name to the receiver
        for i in list0:
            tmp = self.menu.addAction(i)
            receiver = lambda value=i: self.addSocketAction (value)
            self.connect (tmp, QtCore.SIGNAL('triggered()'), receiver)
    
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
    
    def initConnectionsMap (self):
        
        tmp_map = {
                   'stateBegun'    :[['type0_s', 'type1_s', 'type2_s', 'type3_s'],['type1_s', 'type3_s']],
                   'triggerFire'   :[['type0_s', 'type4_s'],['type1_s', 'type2_s']],
                   'stopAction'    :[['type1_s', 'type2_s'],[]],
                   'restoreAction' :[[],['type1_s', 'type2_s']]
                   }
        
        return tmp_map

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def main (argv):
    
    app = QApplication(argv)
    
    window = MainWindow   (gr.Graph())
    window.setWindowFlags (Qt.WindowStaysOnTopHint)
    window.show ()
    
    return app.exec_()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    import sys
    sys.exit (main (sys.argv))