'''
Created on Feb 18, 2012

@author: ivanoras
'''

import Nodes0 as nd
import Comm0


class Graph ():

    def __init__(self):
        
        # signal global operator
        self.comm = Comm0.Comm0 ()
        self.connections_map = {}
        
        self._node_list = []
        
    def getComm (self): return self.comm
    
    # - - -  nodes methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addNode (self):
        
        newId   = self.comm.getNewNodeId()
        newName = 'node_'+str(newId)
        
        newNode = nd.Node0 (newId, newName, self.comm)
        self._node_list.append (newNode)
        
        self.comm.emitAddNodeMSignal (newNode.getId())
        
        return newNode
    
    def removeNode (self, node0_id):
        
        # node removal code
        tmp = False
        for node in self._node_list:
            if node.getId()==node0_id:
                
                # unplug connections first
                for item in node.getIns() : node.removeIn (item)
                for item in node.getOuts(): node.removeOut(item)
                
                del self._node_list [self._node_list.index (node)]
                node.disposeNode ()
                tmp = True
                break
        
        # signal the Link0 instances that a node has gone so those connections need to go too.
        self.comm.emitDeleteNodeMSignal (node0_id)
        
        return tmp
    
    def duplicateNode (self, node0):
        
        node1 = self.addNode()
        
        node1.setName (node0.getName ())
        
        node1.setIns  (node0.getIns ())
        node1.setOuts (node0.getOuts())
        
        node1.setAttributes (node0.getAttributes ())
    
        return node1
    
    def getNodeList (self): return self._node_list
    
    def addInSocket (self, node_id, stype):
        
        node = self.getNode(node_id)
        if node!=None:
            node.addIn (stype)
    
    def addOutSocket (self, node_id, stype):
        
        node = self.getNode(node_id)
        if node!=None:
            node.addOut (stype)
    
    def getNode (self, node_id):
        
        tmp = None
        for item in self._node_list:
            if item.getId()==node_id:
                tmp = item
                break
        
        return tmp
    
    def getInsTypesLeft (self, node_id):
        
        tmp_list = []
        node = self.getNode (node_id)
        for socket in node.getIns ():
            tmp_list.append (socket.getSType())
        
        return list (set(self.connections_map[node.getName()][0]) - set(tmp_list))
    
    def getOutsTypesLeft (self, node_id):
        
        tmp_list = []
        node = self.getNode (node_id)
        for socket in node.getOuts ():
            tmp_list.append (socket.getSType())
        
        return list (set(self.connections_map[node.getName()][0]) - set(tmp_list))
    
    # - - -  links methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addLink (self, inSocket, outSocket):
        
        inSocket.addPluggedIn   (outSocket)
        outSocket.addPluggedOut (inSocket)
        
        self.comm.emitAddLinkMSignal (inSocket.getSId(), outSocket.getSId())
    
    def removeLink (self, inSocket, outSocket):
        
        inSocket.removePluggedIn   (outSocket)
        outSocket.removePluggedOut (inSocket)
        
        self.comm.emitDeleteLinkMSignal (inSocket.getSId(), outSocket.getSId())
    
    # - - -  miscellanea  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def setConnectionsMap (self, tmp):   self.connections_map=tmp