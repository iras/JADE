'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import QObject, SIGNAL, QString


class Comm0 (QObject):
    """
    This class allows QtGui.QGraphicsItem to send and receive signals besides being a utility helper.
    """
    
    def __init__(self, parent = None):
        
        super (Comm0, self).__init__ (parent)
        QObject.__init__ (self)
        
        self.initCounters ()
    
    def initCounters (self):
        
        self.id_cluster_counter= 0
        self.id_node_counter   = 0
        self.id_socket_counter = 0
        
        self.hovered_node_id   = None
        self.hovered_socket_id = None
    
    # cluster id counter
    def getNewClusterId (self):
        
        self.id_cluster_counter += 1
        return self.id_cluster_counter
    
    # node id counter
    def getNewNodeId (self):
        
        self.id_node_counter += 1
        return self.id_node_counter
    
    def updateNodeId (self, queried_node_id):
        
        if self.id_node_counter < queried_node_id:
            self.id_node_counter = queried_node_id
    
    # socket id counter
    def getNewSocketId (self):
        
        self.id_socket_counter += 1
        return self.id_socket_counter
    
    
    
    # Model signals
    
    def emitAddClusterMSignal (self, cluster_id):
        self.emit (SIGNAL ('addCluster_MSignal(int)'), cluster_id)
    
    def emitDeleteClusterMSignal (self, cluster_id):
        self.emit (SIGNAL ('deleteCluster_MSignal(int)'), cluster_id)
    
    def emitUpdateClusterNameMSignal (self, cluster_id, text):
        self.emit (SIGNAL ('updateClusterName_MSignal(int, QString)'), cluster_id, QString(text))
    
    def emitAddNodeToClusterMSignal (self, cluster_id, node_id):
        self.emit (SIGNAL ('addNodeToCluster_MSignal(int, int)'), cluster_id, node_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
     
    def emitAddNodeMSignal (self, node_id, node_x, node_y):
        self.emit (SIGNAL ('addNode_MSignal(int, float, float)'), node_id, node_x, node_y)
    
    def emitDeleteNodeMSignal (self, node_id):
        self.emit (SIGNAL ('deleteNode_MSignal(int)'), node_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def emitAddLinkMSignal (self, inSocket_id, outSocket_id):
        self.emit (SIGNAL ('addLink_MSignal(int, int)'), inSocket_id, outSocket_id)
        
    def emitDeleteLinkMSignal (self, inSocket_id, outSocket_id):
        self.emit (SIGNAL ('deleteLink_MSignal(int, int)'), inSocket_id, outSocket_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def emitAddInSocketMSignal (self, node_id, inSocket_id):
        self.emit (SIGNAL ('addInSocket_MSignal(int, int)'), node_id, inSocket_id)
    
    def emitAddOutSocketMSignal (self, node_id, outSocket_id):
        self.emit (SIGNAL ('addOutSocket_MSignal(int, int)'), node_id, outSocket_id)
    
    def emitDeleteInSocketMSignal (self, node_id, inSocket_id):
        self.emit (SIGNAL ('deleteInSocket_MSignal(int,int)'), node_id, inSocket_id)
    
    def emitDeleteOutSocketMSignal (self, node_id, outSocket_id):
        self.emit (SIGNAL ('deleteOutSocket_MSignal(int,int)'), node_id, outSocket_id)
    

    
    # View Signals
    
    #def emitSelectVSignal (self, node_id):
        
        #self.emit (SIGNAL ('SelectTag_VSignal(int)'), node_id)
    
    def emitCtxMenuSignal (self, pos):
        self.emit (SIGNAL ('customContextMenuRequested(QPoint)'), pos)
    
    # misc
    
    def setHoveredSocketId (self, socket_id):
        self.hovered_socket_id = socket_id
    
    def setHoveredItemId (self, node_id):
        self.hovered_node_id = node_id
    
    def getHoveredItemId (self):
        return self.hovered_node_id