'''
Created on Jan 18, 2012

@author: ivanoras
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



class CustomGraphicsView (QGraphicsView):
    '''
    Re-implementation of the class QGraphicsView in order to deal with differences in how Qt and Maya deal with pop-up menus.
    '''
    def __init__(self, scene=None):
        
        QGraphicsView.__init__ (self)
    
    def mousePressEvent(self, event):
        '''Re-implementation of the QGraphicsView's method mousePressEvent in order to differentiate how the pop-up menu is dealt with by Maya and by Qt.
        More specifically, this distinction with events needs to be made for the Maya integration, otherwise the cmds.popupmenu wouldn't work in the
        QGraphicsView as it would override the Maya cmds.popupmenu's signals.
        
        @param event event
        '''
        if (event.button()==Qt.RightButton): 
            event.ignore()
        else:
            QGraphicsView.mousePressEvent (self, event) # <-- added this line.



class View (QFrame):

    def __init__ (self, name, parent=None):
        
        QFrame.__init__(self, parent)
        
        self.setFrameStyle (QFrame.Sunken | QFrame.StyledPanel)
        
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        
        self.graphicsView = CustomGraphicsView ()
        self.graphicsView.setRenderHint (QPainter.Antialiasing, True)
        self.graphicsView.setDragMode (QGraphicsView.RubberBandDrag)
        self.graphicsView.setViewportUpdateMode (QGraphicsView.SmartViewportUpdate)
        #self.graphicsView.setMouseTracking(True)
        
        # toolbox definition
        sizePolicy = QtGui.QSizePolicy (QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.setObjectName (_fromUtf8 ("Form"))
        self.resize (400, 300)
        self._toolBox = QtGui.QToolBox (self)
        self._toolBox.setGeometry(QtCore.QRect (0, 0, 131, 301))
        self._toolBox.setFont (self.font)
        self._toolBox.setObjectName (_fromUtf8("_toolBox"))
        self.groupCluster = QtGui.QWidget ()
        self.groupCluster.setGeometry (QtCore.QRect(0, 0, 91, 241))
        self.groupCluster.setObjectName (_fromUtf8 ("groupCluster"))
        self.groupLineEdit = QtGui.QLineEdit (self.groupCluster)
        self.groupLineEdit.setGeometry (QtCore.QRect (2, 20, 71, 16))
        self.groupLineEdit.setObjectName (_fromUtf8 ("groupLineEdit"))
        self.label = QtGui.QLabel (self.groupCluster)
        self.label.setGeometry (QtCore.QRect (4, 6, 62, 16))
        self.label.setFont (self.font)
        self.label.setObjectName (_fromUtf8("label"))
        self.label_2 = QtGui.QLabel (self.groupCluster)
        self.label_2.setGeometry (QtCore.QRect (4, 40, 62, 16))
        self.label_2.setFont (self.font)
        self.label_2.setObjectName (_fromUtf8 ("label_2"))
        self.groupLineEdit_2 = QtGui.QLineEdit (self.groupCluster)
        self.groupLineEdit_2.setGeometry (QtCore.QRect(2, 54, 71, 16))
        self.groupLineEdit_2.setObjectName (_fromUtf8("groupLineEdit_2"))
        self.pushButton = QtGui.QPushButton (self.groupCluster)
        self.pushButton.setGeometry (QtCore.QRect (2, 90, 71, 16))
        self.pushButton.setFont (self.font)
        self.pushButton.setObjectName (_fromUtf8 ("pushButton"))
        self._toolBox.addItem (self.groupCluster, _fromUtf8 (""))
        self._toolBox.setItemText (self._toolBox.indexOf (self.groupCluster), QtGui.QApplication.translate ("Form", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.setWindowTitle (QtGui.QApplication.translate ("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText (QtGui.QApplication.translate ("Form", "name group", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText (QtGui.QApplication.translate ("Form", "group id", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText (QtGui.QApplication.translate ("Form", "add cluster", None, QtGui.QApplication.UnicodeUTF8))
        self._toolBox.setSizePolicy (sizePolicy)
        self.connect (self.pushButton, SIGNAL ("clicked()"), self.addclusterPage)
        
        # adding the first cluster - a cluster is always present.
        self._cluster_page = []
        self.addclusterPage ()
        
        size = self.style ().pixelMetric (QStyle.PM_ToolBarIconSize)
        iconSize = QSize (16, 16) #QSize (size, size)
        
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
        self.zoomSlider.setValue   (240)
        self.zoomSlider.setTickPosition (QSlider.TicksRight)
        
        # Zoom slider layout
        zoomSliderLayout = QVBoxLayout ()
        zoomSliderLayout.addWidget (zoomInIcon)
        zoomSliderLayout.addWidget (self.zoomSlider)
        zoomSliderLayout.addWidget (zoomOutIcon)
        
        #self.addNodeBtn = QPushButton ()
        #self.addNodeBtn.setText ("add node")
        #self.addNodeBtn.setFont(font)
        #self.addNodeBtn.setEnabled (True)
        
        #self.removeNodeBtn = QPushButton ()
        #self.removeNodeBtn.setText ("remove node")
        #self.addNodeBtn.setFont(font)
        #self.removeNodeBtn.setEnabled (True)
        
        self.printOutBtn = QPushButton()
        self.printOutBtn.setText ("print graph")
        self.printOutBtn.setFont (self.font)
        self.printOutBtn.setEnabled (True)
        
        self.loadNodesDescrpBtn = QPushButton()
        self.loadNodesDescrpBtn.setText ("load Nodes Description")
        self.loadNodesDescrpBtn.setFont (self.font)
        self.loadNodesDescrpBtn.setEnabled (True)
        
        self.graphSaveBtn = QPushButton()
        self.graphSaveBtn.setText ("save graph")
        self.graphSaveBtn.setFont (self.font)
        self.graphSaveBtn.setEnabled (True)
        
        self.graphLoadBtn = QPushButton()
        self.graphLoadBtn.setText ("load graph")
        self.graphLoadBtn.setFont (self.font)
        self.graphLoadBtn.setEnabled (True)
        
        self.resetButton = QToolButton ()
        self.resetButton.setText ("0")
        self.resetButton.setFont (self.font)
        self.resetButton.setEnabled (False)
        
        # Label layout
        labelLayout = QHBoxLayout ()
        self.label = QLabel (name)
        self.label.setFont (self.font)
        #labelLayout.addWidget (self.addNodeBtn)
        #labelLayout.addWidget (self.removeNodeBtn)
        labelLayout.addWidget (self.loadNodesDescrpBtn)
        labelLayout.addWidget (self.graphSaveBtn)
        labelLayout.addWidget (self.graphLoadBtn)
        labelLayout.addWidget (self.printOutBtn)
        labelLayout.addWidget (self.resetButton)
        
        labelLayout.addWidget (self.label)
        labelLayout.addStretch ()
        
        topLayout = QGridLayout ()
        topLayout.addLayout (labelLayout, 0, 1)
        topLayout.addWidget (self._toolBox, 1, 0)
        topLayout.addWidget (self.graphicsView, 1, 1)
        topLayout.addLayout (zoomSliderLayout, 1, 2)
        self.setLayout (topLayout)
        
        self.connect (self.resetButton, SIGNAL ("clicked()"), self.resetView)
        self.connect (self.zoomSlider,  SIGNAL ("valueChanged(int)"), self.setupMatrix)
        self.connect (self.graphicsView.verticalScrollBar (),   SIGNAL ("valueChanged(int)"), self.setResetButtonEnabled)
        self.connect (self.graphicsView.horizontalScrollBar (), SIGNAL ("valueChanged(int)"), self.setResetButtonEnabled)
        
        self.connect (zoomInIcon,  SIGNAL ("clicked()"), self.zoomIn)
        self.connect (zoomOutIcon, SIGNAL ("clicked()"), self.zoomOut)
        
        self.setupMatrix ()
        
        self.printer = QPrinter (QPrinter.HighResolution)
    
    def addclusterPage (self, event=None):
        
        tmp_w = QWidget ()
        tmp_l = QLabel (tmp_w)
        tmp_e = QLineEdit (tmp_w)
        tmp_b = QPushButton (tmp_w)
        self._cluster_page.append ([tmp_w, tmp_l, tmp_e, tmp_b])
        tmp_index = len (self._cluster_page)
        
        tmp_w.setGeometry (QtCore.QRect (0, 0, 131, 241))
        tmp_w.setObjectName (_fromUtf8 ('Cluster_'+str(tmp_index)))
        
        tmp_l.setGeometry (QtCore.QRect (4, 6, 62, 16))
        tmp_l.setFont (self.font)
        tmp_l.setObjectName (_fromUtf8('label_'+str(tmp_index)))
        
        tmp_e.setGeometry (QtCore.QRect (2, 20, 71, 16))
        tmp_e.setObjectName (_fromUtf8 ('groupLineEdit_'+str(tmp_index)))
        
        tmp_b.setGeometry(QtCore.QRect (2, 50, 71, 16))
        tmp_b.setFont (self.font)
        tmp_b.setObjectName (_fromUtf8 ('pushButton_'+str(tmp_index)))
        
        self._toolBox.addItem (tmp_w, _fromUtf8 ('cluster_page_'+str(tmp_index)))
        self._toolBox.setItemText (self._toolBox.indexOf (tmp_w), QtGui.QApplication.translate ('Form', 'C_'+str(tmp_index), None, QtGui.QApplication.UnicodeUTF8))
        tmp_l.setText (QtGui.QApplication.translate ("Form", "name cluster", None, QtGui.QApplication.UnicodeUTF8))
        tmp_b.setText (QtGui.QApplication.translate ("Form", "delete", None, QtGui.QApplication.UnicodeUTF8))
        self._toolBox.setCurrentIndex (tmp_index)
        QtCore.QMetaObject.connectSlotsByName (self)
    
    def getGraphicsView (self): return self.graphicsView
    
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
    
    # zoom slider
    def zoomIn  (self) : self.zoomSlider.setValue (self.zoomSlider.value() + 1)
    def zoomOut (self) : self.zoomSlider.setValue (self.zoomSlider.value() - 1)
    def getZoomSlider (self): return self.zoomSlider
    
    def setToolboxCSSColorScheme (self, css): self._toolBox.setStyleSheet (css)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setClientAndWireViewItems (self, graph_view):
        
        self.graph_view = graph_view
        
        #self.connect (self.addNodeBtn,       SIGNAL ("clicked()"), self.graph_view.addNodeAndTagPressBtnListener)
        #self.connect (self.removeNodeBtn,    SIGNAL ("clicked()"), self.graph_view.removeNodeAndTagPressBtnListener)
        self.connect (self.printOutBtn,       SIGNAL ("clicked()"), self.printOutGraph)
        self.connect (self.loadNodesDescrpBtn,SIGNAL ("clicked()"), self.importNodesDescription)
        self.connect (self.graphSaveBtn,      SIGNAL ("clicked()"), self.exportGraph)
        self.connect (self.graphLoadBtn,      SIGNAL ("clicked()"), self.importGraph)
        