'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import CustomView as cvw


class View (QFrame):

    def __init__ (self, name, parent=None):
        
        QFrame.__init__(self, parent)
        
        self.setFrameStyle (QFrame.Sunken | QFrame.StyledPanel)
        
        self.graphicsView = cvw.CustomView ()
        self.graphicsView.setRenderHint (QPainter.Antialiasing, True)
        self.graphicsView.setDragMode (QGraphicsView.RubberBandDrag)
        self.graphicsView.setViewportUpdateMode (QGraphicsView.SmartViewportUpdate)
        
        #self.graphicsView.setMouseTracking(True)
        
        size = self.style ().pixelMetric (QStyle.PM_ToolBarIconSize)
        iconSize = QSize (size, size)
        
        zoomInIcon = QToolButton ()
        zoomInIcon.setAutoRepeat (True)
        zoomInIcon.setAutoRepeatInterval (33)
        zoomInIcon.setAutoRepeatDelay (0)
        zoomInIcon.setIconSize (iconSize)
        
        zoomOutIcon = QToolButton ()
        zoomOutIcon.setAutoRepeat (True)
        zoomOutIcon.setAutoRepeatInterval (33)
        zoomOutIcon.setAutoRepeatDelay (0)
        zoomOutIcon.setIconSize (iconSize)
        
        self.zoomSlider = QSlider ()
        self.zoomSlider.setMinimum (200)
        self.zoomSlider.setMaximum (280)
        self.zoomSlider.setValue (240)
        self.zoomSlider.setTickPosition (QSlider.TicksRight)
        
        # Zoom slider layout
        zoomSliderLayout = QVBoxLayout ()
        zoomSliderLayout.addWidget (zoomInIcon)
        zoomSliderLayout.addWidget (self.zoomSlider)
        zoomSliderLayout.addWidget (zoomOutIcon)
        
        #self.addNodeBtn = QPushButton ()
        #self.addNodeBtn.setText ("add node")
        #self.addNodeBtn.setEnabled (True)
        
        #self.removeNodeBtn = QPushButton ()
        #self.removeNodeBtn.setText ("remove node")
        #self.removeNodeBtn.setEnabled (True)
        
        self.printOutBtn = QPushButton()
        self.printOutBtn.setText ("print graph")
        self.printOutBtn.setEnabled (True)
        
        self.loadNodesDescrpBtn = QPushButton()
        self.loadNodesDescrpBtn.setText ("load Nodes Description")
        self.loadNodesDescrpBtn.setEnabled (True)
        
        self.graphSaveBtn = QPushButton()
        self.graphSaveBtn.setText ("save graph")
        self.graphSaveBtn.setEnabled (True)
        
        self.graphLoadBtn = QPushButton()
        self.graphLoadBtn.setText ("load graph")
        self.graphLoadBtn.setEnabled (True)
        
        self.resetButton = QToolButton ()
        self.resetButton.setText ("0")
        self.resetButton.setEnabled (False)
        
        # Label layout
        labelLayout = QHBoxLayout ()
        self.label = QLabel (name)
        #labelLayout.addWidget (self.addNodeBtn)
        #labelLayout.addWidget (self.removeNodeBtn)
        labelLayout.addWidget (self.printOutBtn)
        labelLayout.addWidget (self.loadNodesDescrpBtn)
        labelLayout.addWidget (self.graphSaveBtn)
        labelLayout.addWidget (self.graphLoadBtn)
        
        labelLayout.addWidget (self.label)
        labelLayout.addStretch ()
        
        topLayout = QGridLayout ()
        topLayout.addLayout (labelLayout, 0, 0)
        topLayout.addWidget (self.graphicsView, 1, 0)
        topLayout.addLayout (zoomSliderLayout, 1, 1)
        topLayout.addWidget (self.resetButton, 2, 1)
        self.setLayout (topLayout)
        
        self.connect (self.resetButton, SIGNAL ("clicked()"), self.resetView)
        self.connect (self.zoomSlider,  SIGNAL ("valueChanged(int)"), self.setupMatrix)
        self.connect (self.graphicsView.verticalScrollBar (),   SIGNAL ("valueChanged(int)"), self.setResetButtonEnabled)
        self.connect (self.graphicsView.horizontalScrollBar (), SIGNAL ("valueChanged(int)"), self.setResetButtonEnabled)
        
        self.connect (zoomInIcon,  SIGNAL ("clicked()"), self.zoomIn)
        self.connect (zoomOutIcon, SIGNAL ("clicked()"), self.zoomOut)
        
        self.setupMatrix ()
        
        self.printer = QPrinter (QPrinter.HighResolution)
    
    def view (self): return self.graphicsView
    
    def resetView (self):
        
        self.zoomSlider.setValue (250)
        self.setupMatrix ()
        self.graphicsView.ensureVisible (QRectF (0, 0, 0, 0))
        
        self.resetButton.setEnabled (False)
    
    def setResetButtonEnabled (self) : self.resetButton.setEnabled (True)
    
    def setupMatrix (self):
        
        scale = pow (2.0, (self.zoomSlider.value () - 250) / 50.0)
        
        matrix = QMatrix ()
        matrix.scale (scale, scale)
        
        self.graphicsView.setMatrix (matrix)
        self.setResetButtonEnabled ()
    
    def printOutGraph (self):
        
        qqq = QPainter (self.printer)
        self.graphicsView.render(qqq)
    
    def importNodesDescription (self):
                
        aa = QFileDialog (self).getOpenFileName()
        if aa != QString (u''): # it can be equal to QString(u'') when the user presses the Escape key, so in that circumstance, nothing is returned.
            self.graph_view.setNodesDescription (open(aa).read())
    
    def exportGraph (self):
        
        aa = QFileDialog (self).getSaveFileName ()
        if aa != QString (u''): # it can be equal to QString(u'') when the user presses the Escape key, so in that circumstance, nothing is returned.
            file = open (aa, 'w')
            file.write (self.graph_view.delegateExport ())
            file.close ()
            print '\n*** file exported.\n'
    
    def importGraph (self):
                
        aa = QFileDialog (self).getOpenFileName ()
        if aa != QString (u''): # it can be equal to QString(u'') when the user presses the Escape key, so in that circumstance, nothing is returned.
            file = open (aa, 'r')
            XML_content = file.read()
            file.close ()
            self.graph_view.delegateImport (XML_content)
            print '\n*** file imported.\n'
    
    def zoomIn  (self) : self.zoomSlider.setValue (self.zoomSlider.value() + 1)
    def zoomOut (self) : self.zoomSlider.setValue (self.zoomSlider.value() - 1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setClientAndWireViewItems (self, graph_view):
        
        self.graph_view = graph_view
        
        #self.connect (self.addNodeBtn,       SIGNAL ("clicked()"), self.graph_view.addNodeAndTagPressBtnListener)
        #self.connect (self.removeNodeBtn,    SIGNAL ("clicked()"), self.graph_view.removeNodeAndTagPressBtnListener)
        self.connect (self.printOutBtn,       SIGNAL ("clicked()"), self.printOutGraph)
        self.connect (self.loadNodesDescrpBtn,SIGNAL ("clicked()"), self.importNodesDescription)
        self.connect (self.graphSaveBtn,      SIGNAL ("clicked()"), self.exportGraph)
        self.connect (self.graphLoadBtn,      SIGNAL ("clicked()"), self.importGraph)
        