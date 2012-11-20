'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import Qt, SIGNAL, QString, QTimeLine, QPointF, QRectF, QRect
from PyQt4.QtGui  import QGraphicsTextItem, QGraphicsItem, QPen, QColor, QGraphicsItemAnimation, QFont, QPainterPath, QStyle, QBrush



class CustomFloatingText (QGraphicsTextItem):
    '''
    Re-implementation of the class QGraphicsTextItem in order to provide it with convenient the QLineEdit's textChanged Event.
    '''
    def __init__(self, text, parent=None):
        
        QGraphicsTextItem.__init__ (self, text, parent)
    
    def keyPressEvent (self, event):
        '''Re-implementation of the QGraphicsTextItem's method  keyPressEvent in order to provide QGraphicsTextItem with the QLineEdit's textChanged Event.
        
        @param event event
        '''
        self.emit (SIGNAL ('textChanged(QString)'), QString(self.toPlainText()))
        QGraphicsTextItem.keyPressEvent(self, event)
    
    def focusOutEvent (self, event):
        '''Re-implementation of the QGraphicsTextItem's method focusOutEvent in order to provide QGraphicsTextItem with the QLineEdit's textChanged Event.
        
        @param event event
        '''
        self.emit (SIGNAL ('textChanged(QString)'), QString(self.toPlainText()))
        self.setDefaultTextColor (QColor (Qt.white).light (255))
        QGraphicsTextItem.focusOutEvent(self, event)
    
    def focusInEvent (self, event):
        '''Re-implementation of the QGraphicsTextItem's method focusOInEvent in order to change the text colour to red.
        
        @param event event
        '''
        self.setDefaultTextColor (Qt.red)
        QGraphicsTextItem.focusOutEvent(self, event)



class CanvasProps (QGraphicsItem):


    def __init__(self, parent=None, scene=None):
        
        QGraphicsItem.__init__ (self)
        
        self.parent = parent
        self.helper = self.parent.getHelper()
        
        #self.setFlags (QGraphicsItem.ItemIsSelectable)
        self.setAcceptsHoverEvents (True)
        
        self.pen_color = QPen (Qt.black, 2)
        
        self.color = QColor (Qt.white).dark (150)
        
        # init Canvas Animation Tweening
        self.timeline = QTimeLine (200)
        self.timeline.setFrameRange (0, 100)
        self.anim = QGraphicsItemAnimation ()
        self.anim.setItem (self)
        self.anim.setTimeLine (self.timeline)
        self.helper.connect (self.timeline, SIGNAL("finished()"), self.moveFurtherUp)
        self.anim_active = False
        
        #self._nodename = QGraphicsTextItem ('text '+str(self.node_id), self)
        self._nodename = QGraphicsTextItem ('', self)
        self._nodename.setPos (QPointF (18, 20))
        self._nodename.setDefaultTextColor (QColor (Qt.white).light (255))
        self._nodename.setFont (QFont ("Helvetica", 11, QFont.Bold, False))
        self._nodename.setTextWidth(120)
        self._nodename.setToolTip (self._nodename.toPlainText ())
        #self._nodename.setHtml("<h2 align=\"center\">hello</h2><h2 align=\"center\">world 1234345345</h2>123");
        
        self.props_list = []
        self.props_textItem_value_list = []
        
        self.FACTOR = 4.0
        
        self._canvas_height = 0
    
    def boundingRect (self): return QRectF (-1000, -1000, 2000, 2000)
    
    def shape (self):
        
        path = QPainterPath ()
        path.addRect (0, 0, 122, 20)
        return path
    
    def paint (self, painter, option, unused_widget):
        
        if option.state & QStyle.State_Selected:
            fillColor = self.color.dark (100)
        else:
            fillColor = self.color
        
        if option.state & QStyle.State_MouseOver:
            fillColor = fillColor.light (120)
        
        if option.levelOfDetail < 0.2:
            
            if option.levelOfDetail < 0.125:
                painter.fillRect (QRectF (0, 0, 110, 70), fillColor)
                return
            
            painter.setPen   (QPen (Qt.black, 0))
            painter.setBrush (fillColor)
            painter.drawRect (0, 0, 120, 20)
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
        painter.drawRect (QRect (0, 20, 120, 30+9*self._canvas_height))
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addProp (self, prop_name, prop_value):
        
        i = len (self.props_list)
        self.props_list.append  (QGraphicsTextItem (prop_name + ' : ', self))
        self.props_textItem_value_list.append (CustomFloatingText (prop_value, self))
        
        # (1) adding the prop's name.
        self.props_list[i].setPos (QPointF (7, 35+i*10))
        self.props_list[i].setDefaultTextColor (QColor (Qt.white).light (255))
        self.props_list[i].setFont (QFont ("Helvetica", 9, QFont.StyleItalic, False))
        self.props_list[i].setTextWidth (55)
        self.props_list[i].setToolTip (self.props_list[i].toPlainText ())
        
        # (2) adding the prop's value.
        self.props_textItem_value_list[i].setTextInteractionFlags (Qt.TextEditable)
        self.props_textItem_value_list[i].setPos (QPointF (55, 35+i*10))
        self.props_textItem_value_list[i].setDefaultTextColor (QColor (Qt.white).light (255))
        self.props_textItem_value_list[i].setFont (QFont ("Helvetica", 9, QFont.StyleNormal, False))
        self.props_textItem_value_list[i].setTextWidth (55)
        
        receiver = lambda value: self.parent.listenToChangedPropsValues (prop_name, value)
        self.helper.connect (self.props_textItem_value_list[i], SIGNAL ("textChanged(QString)"), receiver)
    
    def getProps (self):
        
        tmp_list = []
        
        l = len (self.props_list)
        for i in range (0, l):
            tmp_list[i] = [self.props_list[i].toPlainText(), self.props_textItem_value_list[i].toPlainText()]
        
        return tmp_list
    
    def setTitle (self, title): self._nodename.setPlainText (title)
    
    def setCanvasHeightInUnits (self, ch): self._canvas_height = ch
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def moveDown (self, canvas_height_in_units):
        
        self.anim_active  = True
        self.upwards_flag = False
        
        self.canvas_height = canvas_height_in_units
        
        self.timeline.stop ()
        
        self.anim.setPosAt (0, QPointF(0, 1+(self.canvas_height+1)*self.FACTOR))
        self.anim.setPosAt (1, QPointF(0, 1+(self.canvas_height+2)*self.FACTOR))
        
        self.timeline.start ()
        self.update ()
    
    def moveUp (self, canvas_height_in_units):
        
        if self.anim_active == False:
            
            self.anim_active  = True
            self.upwards_flag = True
            
            self.canvas_height = canvas_height_in_units
            
            self.timeline.stop ()
            
            self.anim.setPosAt (0, QPointF(0, 1+(self.canvas_height+1)*self.FACTOR))
            self.anim.setPosAt (1, QPointF(0, 1+(self.canvas_height)  *self.FACTOR))
            
            self.timeline.start ()
            self.update ()
    
    # this method double-checks whether the canvas needs to be further up as a
    # result of receiving other asynchronous "delete link" SIGNALs while moving up.
    def moveFurtherUp (self):
        
        self.anim_active = False
        
        if self.upwards_flag==True:
            
            if self.parent.getMaxLen() < self.canvas_height:
                self.moveUp (self.canvas_height-1)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def hoverEnterEvent (self, e):
        
        self._nodename.setToolTip (self._nodename.toPlainText ())
        QGraphicsItem.hoverEnterEvent (self, e)
    
    def hoverLeaveEvent (self, e):
        
        QGraphicsItem.hoverLeaveEvent (self, e)
    
    def mousePressEvent (self, e):
        
        QGraphicsItem.mousePressEvent (self, e)
        #self.update ()
    
    def mouseMoveEvent (self, e):
        
        QGraphicsItem.mouseMoveEvent (self, e)
    
    def mouseReleaseEvent (self, e):
        
        QGraphicsItem.mouseReleaseEvent (self, e)