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
        
        self.scene   = QGraphicsScene()
        
        self.graph_model = graph
        self.graph_model.setConnectionsMap (self.initConnectionsMap())
        self.utility = utility.Helper (self, self.scene, self.graph_model)
        self.graph_view  = grv.GraphView (self.graph_model, self.utility)
        
        # wiring Contextual Menu
        self.menu = QMenu ()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self ,SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
        
        # wiring buttons
        self.connect (self.graph_model.getComm (), SIGNAL('addNode_MSignal(int)'), self.graph_view.addTag)
        
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
        
        self.scene.addItem (self.utility.getHarpoon ())
        
        self.temp_hovered_item_id = None
        self.first_click  = False
    
    
    def ctxMenu (self, pos):
        
        self.temp_hovered_item_id = self.graph_model.getComm().getHoveredItemId()
        
        if self.temp_hovered_item_id!=None:
            
            if self.first_click==True:
                left_list = self.graph_model.getInsTypesLeft (self.temp_hovered_item_id)
                if len(left_list)!=0:
                    
                    for i in left_list:
                        self.menu.addAction (i, self.action1) #it is just a regular QMenu
                    
                    self.menu.popup (self.mapToGlobal (pos))
            else:
                left_list = self.graph_model.getOutsTypesLeft (self.temp_hovered_item_id)
                if len(left_list)!=0:
                    
                    for i in left_list:
                        self.menu.addAction (i, self.action1) #it is just a regular QMenu
                    
                    self.menu.popup (self.mapToGlobal (pos))
                
    
    def action1 (self):
        
        tag = self.graph_view.getTag (self.temp_hovered_item_id)
        print 'hi action '+str(tag) + ' '+str(self.graph_model.getComm().getHoveredItemId())
        tag.makeRectBigger ()
    
    def populateScene (self):
        
        self.graph_view.addNodeAndTag ()
    
    def addLinkAndWirePressBtnListener (self):
        
        print 'this needs to go.'
    
    def initConnectionsMap (self):
        
        tmp_map = {
                   'stateBegun'    :[['type0_s', 'type1_s', 'type2_s'],['type1_s']],
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