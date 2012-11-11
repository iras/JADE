'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui



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

    def __init__ (self, name, graph_view, parent=None):
        
        QFrame.__init__(self, parent)
        
        self.graph_view = graph_view

        self.setFrameStyle (QFrame.Sunken | QFrame.StyledPanel)
        
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        
        
        self.graphicsView = CustomGraphicsView ()
        self.graphicsView.setRenderHint (QPainter.Antialiasing, True)
        self.graphicsView.setDragMode (QGraphicsView.RubberBandDrag)
        self.graphicsView.setViewportUpdateMode (QGraphicsView.SmartViewportUpdate)
        self.graphicsView.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(125, 125, 135, 255), stop:1 rgba(215, 215, 215, 255));\ncolor: rgb(255, 255, 255);')
        #self.graphicsView.setMouseTracking(True)
        
        # toolbox definition + group page definition
        sizePolicy = QtGui.QSizePolicy (QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.setObjectName ('Form')
        self.resize (900, 1000)
        self._toolBox = QtGui.QToolBox (self)
        self._toolBox.setGeometry(QtCore.QRect (0, 0, 131, 301))
        self._toolBox.setFont (self.font)
        self._toolBox.setObjectName ('_toolBox')
        self._toolBox.setCursor (Qt.PointingHandCursor)
        self.groupCluster = QtGui.QWidget ()
        self.groupCluster.setGeometry (QtCore.QRect(0, 0, 91, 241))
        self.groupCluster.setObjectName ('groupCluster')
        self.groupLineEdit = QtGui.QLineEdit (self.groupCluster)
        self.groupLineEdit.setGeometry (QtCore.QRect (2, 20, 60, 16))
        self.groupLineEdit.setObjectName ('groupLineEdit')
        self.label = QtGui.QLabel (self.groupCluster)
        self.label.setGeometry (QtCore.QRect (4, 6, 62, 16))
        self.label.setFont (self.font)
        self.label.setObjectName ('label')
        self.label_2 = QtGui.QLabel (self.groupCluster)
        self.label_2.setGeometry (QtCore.QRect (4, 40, 62, 16))
        self.label_2.setFont (self.font)
        self.label_2.setObjectName ('label_2')
        self.groupLineEdit_2 = QtGui.QLineEdit (self.groupCluster)
        self.groupLineEdit_2.setGeometry (QtCore.QRect(2, 54, 60, 16))
        self.groupLineEdit_2.setObjectName ('groupLineEdit_2')
        self.pushButton = QtGui.QPushButton (self.groupCluster)
        self.pushButton.setGeometry (QtCore.QRect (2, 90, 60, 16))
        self.pushButton.setFont (self.font)
        self.pushButton.setObjectName ('pushButton')
        self._toolBox.addItem (self.groupCluster, '')
        self._toolBox.setItemText (self._toolBox.indexOf (self.groupCluster), QtGui.QApplication.translate ("Form", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.setWindowTitle (QtGui.QApplication.translate ("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText (QtGui.QApplication.translate ("Form", "name group", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText (QtGui.QApplication.translate ("Form", "group id", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText (QtGui.QApplication.translate ("Form", "add cluster", None, QtGui.QApplication.UnicodeUTF8))
        self._toolBox.setSizePolicy (sizePolicy)
        
        # adding the first cluster - a cluster is always present.
        self._cluster_page_list = []
        self.connect (self.pushButton, SIGNAL ("clicked()"), self.addCluster)  # connect the 'add-cluster' button to the method that taps into the model for cluster addition.
        self.connect (self.graph_view.getComm(), SIGNAL ("addCluster_MSignal(int)"), self.addClusterPage)
        self.connect (self.graph_view.getComm(), SIGNAL ("deleteCluster_MSignal(int)"), self.removeClusterPage)
        self.addCluster () # add the first cluster. At least one cluster needs to be always present.
        self.disableAllClusterPagesDeleteButton() # since there's only one cluster page, the delete button is disabled.
        
        #size = self.style ().pixelMetric (QStyle.PM_ToolBarIconSize)
        iconSize = QSize (16, 16) #QSize (size, size)
        
        zoomInIcon = QToolButton ()
        zoomInIcon.setCursor (Qt.PointingHandCursor)
        zoomInIcon.setAutoRepeat (True)
        zoomInIcon.setAutoRepeatInterval (33)
        zoomInIcon.setAutoRepeatDelay (0)
        zoomInIcon.setIconSize (iconSize)
        
        zoomOutIcon = QToolButton ()
        zoomOutIcon.setCursor (Qt.PointingHandCursor)
        zoomOutIcon.setAutoRepeat (True)
        zoomOutIcon.setAutoRepeatInterval (33)
        zoomOutIcon.setAutoRepeatDelay (0)
        zoomOutIcon.setIconSize (iconSize)
        
        self.zoomSlider = QSlider ()
        self.zoomSlider.setCursor (Qt.PointingHandCursor)
        self.zoomSlider.setMinimum (200)
        self.zoomSlider.setMaximum (280)
        self.zoomSlider.setValue   (240)
        self.zoomSlider.setTickPosition (QSlider.TicksRight)
        
        # Zoom slider layout
        zoomSliderLayout = QVBoxLayout ()
        zoomSliderLayout.addWidget (zoomInIcon)
        zoomSliderLayout.addWidget (self.zoomSlider)
        zoomSliderLayout.addWidget (zoomOutIcon)
        
        self.printOutBtn = QPushButton()
        self.printOutBtn.setText ("print graph")
        self.printOutBtn.setFont (self.font)
        self.printOutBtn.setEnabled (True)
        
        self.loadNodesDescrpBtn = QPushButton()
        self.loadNodesDescrpBtn.setText ("load Nodes Description")
        self.loadNodesDescrpBtn.setFont (self.font)
        self.loadNodesDescrpBtn.setEnabled (True)
        
        self.graphLoadBtn = QPushButton()
        self.graphLoadBtn.setText ("load graph")
        self.graphLoadBtn.setFont (self.font)
        self.graphLoadBtn.setEnabled (True)
        
        self.graphSaveBtn = QPushButton()
        self.graphSaveBtn.setText ("save graph")
        self.graphSaveBtn.setFont (self.font)
        self.graphSaveBtn.setEnabled (True)
        
        self.resetButton = QToolButton ()
        self.resetButton.setText ("r")
        self.resetButton.setFont (self.font)
        self.resetButton.setEnabled (False)
        
        # Label layout
        labelLayout = QHBoxLayout ()
        self.label = QLabel (name)
        self.label.setFont (self.font)
        labelLayout.addWidget (self.loadNodesDescrpBtn)
        labelLayout.addWidget (self.graphLoadBtn)
        labelLayout.addWidget (self.graphSaveBtn)
        labelLayout.addWidget (self.printOutBtn)
        #labelLayout.addWidget (self.label)
        labelLayout.addStretch ()
        
        # top layout
        topLayout = QGridLayout ()
        topLayout.setHorizontalSpacing(0)
        topLayout.setVerticalSpacing(0)
        topLayout.addLayout (labelLayout, 0, 1)
        topLayout.addWidget (self._toolBox, 1, 0)
        topLayout.addWidget (self.resetButton, 0, 2)
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
    
    # - - -    cluster-specific methods   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addCluster (self):
        
        self.graph_view.delegateClusterAddition ()
    
    def addClusterPage (self, new_cluster_id):
        
        self.enableAllClusterPagesDeleteButton () # enable all the cluster page's delete buttons (as I can be bothered to go look for the one that got previously disabled) 
        
        tmp_w = QWidget ()
        tmp_l = QLabel (tmp_w)
        tmp_e = QLineEdit (tmp_w)
        tmp_b = QPushButton (tmp_w)
        self._cluster_page_list.append ([new_cluster_id, tmp_w, tmp_l, tmp_e, tmp_b])
        
        tmp_w.setGeometry (QtCore.QRect (0, 0, 131, 241))
        tmp_w.setObjectName ('Cluster_'+str(new_cluster_id))
        
        tmp_l.setGeometry (QtCore.QRect (4, 6, 62, 16))
        tmp_l.setFont (self.font)
        tmp_l.setObjectName ('label_'+str(new_cluster_id))
        
        tmp_e.setGeometry (QtCore.QRect (2, 20, 60, 16))
        tmp_e.setObjectName ('groupLineEdit_'+str(new_cluster_id))
        
        tmp_b.setGeometry(QtCore.QRect (2, 50, 60, 16))
        tmp_b.setFont (self.font)
        tmp_b.setObjectName ('pushButton_'+str(new_cluster_id))
        
        self._toolBox.addItem (tmp_w, 'cluster_page_'+str(new_cluster_id))
        self._toolBox.setItemText (self._toolBox.indexOf (tmp_w), QtGui.QApplication.translate ('Form', 'C_'+str(new_cluster_id), None, QtGui.QApplication.UnicodeUTF8))
        tmp_l.setText (QtGui.QApplication.translate ("Form", "name cluster", None, QtGui.QApplication.UnicodeUTF8))
        tmp_b.setText (QtGui.QApplication.translate ("Form", "delete", None, QtGui.QApplication.UnicodeUTF8))
        self._toolBox.setCurrentIndex (new_cluster_id)
        QtCore.QMetaObject.connectSlotsByName (self)
        
        # hook up the delete button (use a closure)
        receiver = lambda : self.removeCluster (new_cluster_id)
        self.connect (tmp_b, SIGNAL ("clicked()"), receiver)  # connect the 'add cluster' button to the method generating new cluster pages.
    
    def removeCluster (self, cluster_id):
        
        self.graph_view.delegateClusterRemoval (cluster_id)
    
    def removeClusterPage (self, cluster_id):
        
        qq = len(self._cluster_page_list)
        if qq > 1:
            for i in range (qq-1, -1, -1):
                if int(self._cluster_page_list[i][0]) == cluster_id:
                    self._toolBox.removeItem (self._toolBox.currentIndex())
                    del self._cluster_page_list[i]
                    break
        
        if len(self._cluster_page_list) == 1:
            self.disableAllClusterPagesDeleteButton ()
    
    def disableAllClusterPagesDeleteButton (self):
        
        if len(self._cluster_page_list) > 0:
            for item in self._cluster_page_list:
                item[4].setEnabled (False)
    
    def enableAllClusterPagesDeleteButton (self):
        
        if len(self._cluster_page_list) > 0:
            for item in self._cluster_page_list:
                item[4].setEnabled (True)
    
    # - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
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
            file0 = open (aa, 'w')
            file0.write (self.graph_view.delegateExport ())
            file0.close ()
            print '\n*** file exported.\n'
    
    def importGraph (self):
                
        aa = QFileDialog (self).getOpenFileName ()
        if aa != QString (u''): # it can be equal to QString(u'') when the user presses the Escape key, so in that circumstance, nothing is returned.
            file0 = open (aa, 'r')
            XML_content = file0.read()
            file0.close ()
            self.graph_view.delegateImport (XML_content)
            print '\n*** file imported.\n'
    
    # zoom slider
    def zoomIn  (self) : self.zoomSlider.setValue (self.zoomSlider.value() + 1)
    def zoomOut (self) : self.zoomSlider.setValue (self.zoomSlider.value() - 1)
    def getZoomSlider (self): return self.zoomSlider
    
    def setToolboxCSSColorScheme (self, css): self._toolBox.setStyleSheet (css)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def wireViewItemsUp (self):
                
        self.connect (self.printOutBtn,       SIGNAL ("clicked()"), self.printOutGraph)
        self.connect (self.loadNodesDescrpBtn,SIGNAL ("clicked()"), self.importNodesDescription)
        self.connect (self.graphSaveBtn,      SIGNAL ("clicked()"), self.exportGraph)
        self.connect (self.graphLoadBtn,      SIGNAL ("clicked()"), self.importGraph)
    
    def updateCurrentClusterNodeList (self, node):
        
        # fetch the current cluster's id.
        tmp_current_widget_id = None
        curr_widget = self._toolBox.currentWidget()
        for item in self._cluster_page_list:
            if item[1] == curr_widget:
                tmp_current_widget_id = item[0]
                break
        
        # delegate cluster node list update.
        self.graph_view.delegateClusterNodeListUpdate (tmp_current_widget_id, node)
