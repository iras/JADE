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
        '''constructor
        '''
        super (Comm0, self).__init__ (parent)
        QObject.__init__ (self)
        
        self.initCounters ()
    
    def initCounters (self):
        '''This init method is decoupled out from the constructor as it is reused to clean up the Comm0 instance from previously used data.
        '''
        self.id_cluster_counter = 0
        self.id_node_counter    = 0
        self.id_socket_counter  = 0
        
        self.hovered_node_id    = None
        self.hovered_socket_id  = None
    
    def getNewClusterId (self):
        '''This method increments the self.id_cluster_counter by one and returns it.
        
        @return self.id_cluster_counter int
        '''
        self.id_cluster_counter += 1
        return self.id_cluster_counter
    
    def getNewNodeId (self):
        '''This method increments the self.id_node_counter by one and returns it.
        
        @return self.id_node_counter int
        '''
        self.id_node_counter += 1
        return self.id_node_counter
    
    def updateNodeId (self, queried_node_id):
        '''This method updates the self.id_node_counter with the given value if the value is bigger than the stored self.id_node_counter.
        '''
        if self.id_node_counter < queried_node_id:
            self.id_node_counter = queried_node_id
    
    def getNewSocketId (self):
        '''This method increments the self.id_socket_counter by one and returns it.
        
        @return self.id_socket_counter int
        '''
        self.id_socket_counter += 1
        return self.id_socket_counter
    
    
    
    # - - -  Model signals  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def emitAddClusterMSignal (self, cluster_id):
        '''This method shoots a "addCluster_MSignal" signal.
        
        @param cluster_id int
        '''
        self.emit (SIGNAL ('addCluster_MSignal(int)'), cluster_id)
    
    def emitDeleteClusterMSignal (self, cluster_id):
        '''This method shoots a "deleteCluster_MSignal" signal.
        
        @param cluster_id int
        '''
        self.emit (SIGNAL ('deleteCluster_MSignal(int)'), cluster_id)
    
    def emitUpdateClusterNameMSignal (self, cluster_id, text):
        '''This method shoots a "updateClusterName_MSignal" signal.
        
        @param cluster_id int
        @param text string
        '''
        self.emit (SIGNAL ('updateClusterName_MSignal(int, QString)'), cluster_id, QString(text))
    
    def emitAddNodeToClusterMSignal (self, cluster_id, node_id):
        '''This method shoots a "addNodeToCluster_MSignal" signal.
        
        @param cluster_id int
        @param node_id int
        '''
        self.emit (SIGNAL ('addNodeToCluster_MSignal(int, int)'), cluster_id, node_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
     
    def emitAddNodeMSignal (self, node_id, node_x, node_y):
        '''This method shoots a "addNode_MSignal" signal.
        
        @param node_id int
        @param node_x int
        @param node_y int
        '''
        self.emit (SIGNAL ('addNode_MSignal(int, float, float)'), node_id, node_x, node_y)
    
    def emitDeleteNodeMSignal (self, node_id):
        '''This method shoots a "deleteNode_MSignal" signal.
        
        @param node_id int
        '''
        self.emit (SIGNAL ('deleteNode_MSignal(int)'), node_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def emitAddLinkMSignal (self, inSocket_id, outSocket_id):
        '''This method shoots a "addLink_MSignal" signal.
        
        @param inSocket_id int
        @param outSocket_id int
        '''
        self.emit (SIGNAL ('addLink_MSignal(int, int)'), inSocket_id, outSocket_id)
        
    def emitDeleteLinkMSignal (self, inSocket_id, outSocket_id):
        '''This method shoots a "deleteLink_MSignal" signal.
        
        @param inSocket_id int
        @param outSocket_id int
        '''
        self.emit (SIGNAL ('deleteLink_MSignal(int, int)'), inSocket_id, outSocket_id)
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def emitAddInSocketMSignal (self, node_id, inSocket_id):
        '''This method shoots a "addInSocket_MSignal" signal.
        
        @param node_id int
        @param inSocket_id int
        '''
        self.emit (SIGNAL ('addInSocket_MSignal(int, int)'), node_id, inSocket_id)
    
    def emitAddOutSocketMSignal (self, node_id, outSocket_id):
        '''This method shoots a "addOutSocket_MSignal" signal.
        
        @param node_id int
        @param outSocket_id int
        '''
        self.emit (SIGNAL ('addOutSocket_MSignal(int, int)'), node_id, outSocket_id)
    
    def emitDeleteInSocketMSignal (self, node_id, inSocket_id):
        '''This method shoots a "deleteInSocket_MSignal" signal.
        
        @param node_id int
        @param inSocket_id int
        '''
        self.emit (SIGNAL ('deleteInSocket_MSignal(int,int)'), node_id, inSocket_id)
    
    def emitDeleteOutSocketMSignal (self, node_id, outSocket_id):
        '''This method shoots a "deleteOutSocket_MSignal" signal.
        
        @param node_id int
        @param outSocket_id int
        '''
        self.emit (SIGNAL ('deleteOutSocket_MSignal(int,int)'), node_id, outSocket_id)
    

    # - - -  View signals  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def emitCtxMenuSignal (self, pos):
        '''This method shoots a "customContextMenuRequested" signal.
        
        @param pos QPoint
        '''
        self.emit (SIGNAL ('customContextMenuRequested(QPoint)'), pos)
    
    # - - -  misc  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def setHoveredSocketId (self, socket_id):
        '''This method sets the self.hovered_socket_id.
        
        @param socket_id int
        '''
        self.hovered_socket_id = socket_id
    
    def setHoveredItemId (self, node_id):
        '''This method sets the value of the self.hovered_node_id.
        
        @param socnode_idket_id int
        '''
        self.hovered_node_id = node_id
    
    def getHoveredItemId (self):
        '''This method returns the self.hovered_node_id.
        
        @return self.hovered_node_id int
        '''
        return self.hovered_node_id
