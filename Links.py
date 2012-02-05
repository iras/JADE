'''
Created on Feb 4, 2012

@author: ivanoras
'''


class Link ():

    def __init__(self, id, name, pnode_id, cnode_id, parent=None):
        
        self._id = id
        self._name = str(name)
        
        self.parent_node_id = pnode_id
        self.child_node_id  = cnode_id
        
    def destroy (self):
        pass
    
    def getId   (self): return self._id
    def getName (self): return self._name
    def get2NodesIds (self): return [self.parent_node_id, self.child_node_id]