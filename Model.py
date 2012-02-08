'''
Created on Feb 1, 2012

@author: ivanoras
'''

import Nodes as nd
import Links as lk
import Comm

class Model ():
    
    def __init__(self):
        
        self.comm = Comm.Comm ()
        
        self._node_list = []
        self._link_list = []
        
        self.id_node_counter = 0
        self.id_link_counter = 0
    
    def getComm (self): return self.comm
    
    # - - -  node methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addNode (self, parent=None):
        
        newId   = self.__getNewNodeId()
        newName = 'node_'+str(newId)
        
        newNode = nd.Node (newId, newName)
        self._node_list.append (newNode)
        
        return newNode
    
    def removeNode (self, node_id):
        
        # signal the Link0 instances that a node has gone so those connections need to go too.
        self.comm.emitDeleteNodeMSignal (node_id)
        
        # node removal code
        tmp = False
        for node in self._node_list:
            if node.getId()==node_id:
                self.shootResizingMSignals (node.getChildren())
                self.shootResizingMSignals (node.getParents ())
                node.dispose ()
                del self._node_list [self._node_list.index (node)]
                tmp = True
                break
        
        return tmp
    
    # - - -  link methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addLink (self, parent_node_id, child_node_id):
        
        pnode = self.getNode (parent_node_id)
        cnode = self.getNode (child_node_id)
        pnode.addChild  (cnode)
        cnode.addParent (pnode)
        
        newId   = self.__getNewLinkId ()
        newName = 'link_'+str(newId)
        
        newLink = lk.Link (newId, newName, parent_node_id, child_node_id)
        self._link_list.append (newLink)
        
        self.comm.emitAddLinkMSignal (parent_node_id)
        self.comm.emitAddLinkMSignal (child_node_id)
        
        return newLink
    
    def removeLink (self, link_id):
        
        tmp = False
        for link in self._link_list:
            
            if link.getId()==link_id:
                nodes = link.get2NodesIds ()
                node1 = self.getNode(nodes[0])
                node2 = self.getNode(nodes[1])
                self.shootResizingMSignals ([node1, node2])
                
                if node1.hasParent (node2)[0]:
                    aa = node1.removeParent (node2)
                    bb = node2.removeChild  (node1)
                else:
                    aa = node2.removeParent (node1)
                    bb = node1.removeChild  (node2)
                link.dispose ()
                del self._link_list [self._link_list.index (link)]
                tmp = True
                break
        
        return tmp
    
    # - - -  misc methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def areNodesRelated (self, n1_id, n2_id):
        
        flag = False
        
        n1 = self.getNode (n1_id)
        n2 = self.getNode (n2_id)
        
        if n1.hasParent(n2)[0] or n2.hasParent(n1)[0]: flag=True
        
        return flag
        
    def shootResizingMSignals (self, ls):
        
        for item in ls:
            self.comm.emitDeleteLinkMSignal (item.getId())
    
    # - - -  getters/setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def getNode (self, node_id):
        
        tmp = None
        for node in self._node_list:
            if node.getId()==node_id:
                tmp = node
                break
        
        return tmp
    
    def getNodesList (self): return self._node_list
    def getLinksList (self): return self._link_list
    
    def __getNewNodeId (self):
        
        self.id_node_counter += 1
        return self.id_node_counter
    
    def __getNewLinkId (self):
        
        self.id_node_counter += 1
        return self.id_node_counter