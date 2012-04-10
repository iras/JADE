'''
Created on Feb 1, 2012

@author: ivanoras
'''

class Node ():
    
    def __init__(self, id, name, parent=None):
        
        self._id = id
        self._name = str(name)
        self._children = []
        self._parents  = []
        
        if parent!=None:
            parent.addChild (self)
            self.addParent (parent)
    
    def addChild  (self, child ): self._children.append (child)
    def addParent (self, parent): self._parents.append (parent)
    
    # removeChild (Node) : Boolean
    def removeChild (self, node):
        
        tmp = False
        for i in self._children:
            if i.getId()==node.getId():
                del self._children[self._children.index(node)]
                tmp = True
                break
        return tmp
    
    # removeParent (Node) : Boolean
    def removeParent (self, node):
        
        tmp = False
        for i in self._parents:
            if i.getId()==node.getId():
                del self._parents[self._parents.index(node)]
                tmp = True
                break
        return tmp
    
    def dispose (self):
        pass
    
    def noChildren (self): return len(self._children)
    def noParents  (self): return len(self._parents)
    
    # hasChild (Node) : 2-list [Boolean, int]
    def hasChild (self, child):
        try:
            tmp = self._children.index (child)
        except ValueError:
            tmp = -1
        
        list0 = [False, tmp]
        if list0[1]!=-1: list0[0]=True
        return list0
    
    # hasParent (Node) : 2-list [Boolean, int]
    def hasParent (self, parent):
        try:
            tmp = self._parents.index (parent)
        except ValueError:
            tmp = -1
            
        list0 = [False, tmp]
        if list0[1]!=-1: list0[0]=True
        return list0
    
    def getParent (self, name0):
        tmp = None
        for i in self._parents:
            if i.getName()==name0:
                tmp=i
                break
        return tmp
    
    def getChild  (self, name0):
        tmp = None
        for i in self._children:
            if i.getName()==name0:
                tmp=i
                break
        return tmp
    
    # getChildrenList () : list
    def getChildren (self): return self._children
    def getParents  (self): return self._parents
        
    def getId   (self) : return self._id
    def getName (self) : return self._name