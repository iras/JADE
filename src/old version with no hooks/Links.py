'''
Created on Feb 4, 2012

@author: ivanoras
'''

class Link ():

    def __init__(self, id, name, pnode_id, cnode_id, parent=None):
        
        self._id = id
        self._name = str(name)
        
        self.pnode_id = pnode_id
        self.cnode_id = cnode_id
        
    def dispose (self):
        pass
    
    def getId   (self): return self._id
    def getName (self): return self._name
    def get2NodesIds (self): return [self.pnode_id, self.cnode_id]
    
    def hasNodes (self, pnode_id, cnode_id):
        
        if (self.pnode_id==pnode_id and self.cnode_id==cnode_id) or (self.pnode_id==cnode_id and self.cnode_id==pnode_id):
            pass