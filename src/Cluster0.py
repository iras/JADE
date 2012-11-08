'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

class Cluster0 ():
    '''
    sub-model class.
    '''
    def __init__(self, id0, name, parent, comm):
        '''constructor
        
        @param id0 int
        @param name string
        @param comm instance of class Comm0
        '''
        self._id   = id0  # id0 has been used instead of id since the latter is a built-in variable.
        self._name = str(name)
        self.graph = parent
        self.comm  = comm
        
        self._cluster_node_list = []
    
    def addNodeToCluster (self, node):  # TODO : unit test
        
        self._cluster_node_list.append (node)
    
    def removeNodeFromCluster (self, node):  # TODO : unit test
        
        qq = len (self._cluster_node_list)
        for i in range (qq-1, -1, -1):
            if self._cluster_node_list[i] == node:
                self.graph.removeNode (self._cluster_node_list[i].getId()) # remove the node.
                del self._cluster_node_list[i] # remove the list item referencing the node.
                break    
    
    def removeAllNodesFromCluster (self):  # TODO : unit test
        
        qq = len (self._cluster_node_list)
        for i in range (qq-1, -1, -1):
            self.graph.removeNode (self._cluster_node_list[i].getId()) # remove the node.
            del self._cluster_node_list[i] # remove the list item referencing the node.
    
    # - - -   getters / setters  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getId (self):
        
        return self._id
    
    def getName (self):
        
        return self._name
    
    
    
    def setId (self, id0): self._id = id0
    
    def setName (self, name0): self._name = name0
    
