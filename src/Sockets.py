'''
Created on Feb 18, 2012

@author: ivanoras
'''

class Socket ():
    """
        Abstract Socket class
    """
    def __init__(self, sid, type0, node):
        
        self._sid   = sid     # socket's id
        self._node  = node # id of the node this socket belongs to.
        self._stype = str(type0)
        
        self._attributes = []
    
    def isPluggedWith (self, socket):
        raise Exception ("*** Method isPluggedWith (...) needs implementing.")
    
    def isEmpty (self):
        raise Exception ("*** Method isEmpty () needs implementing.")
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getSId   (self): return self._sid
    def getNode  (self): return self._node
    def getSType (self): return self._stype
    
    def getAttributes (self): return self._attributes
    





# ---------------------------------------------------------------------------

class InSocket (Socket):
    
    def __init__(self, sid, type0, node):
        
        Socket.__init__(self, sid, type0, node)
        
        # lists of all the sockets plugged into this InSocket 
        self._plugged_ins = []
    
    
    def addPluggedIn (self, outSocket):
        
        tmp = True
        for item in self._plugged_ins:
            if outSocket.getSId()==item.getSId():
                tmp = False
                break
        
        if tmp:
            self._plugged_ins.append (outSocket)
        
        return tmp
    
    def removePluggedIn (self, outSocket):
        
        tmp = False
        for item in self._plugged_ins:
            if item.getSId()==outSocket.getSId():
                
                del self._plugged_ins [self._plugged_ins.index (outSocket)]
                tmp = True
                break
        
        return tmp
    
    def isPluggedWith (self, socket):
        
        try:
            tmp = self._plugged_ins.index (socket)
        except ValueError:
            tmp = -1
        
        return False if tmp==-1 else True
    
    def isEmpty (self):
        
        flag = False
        
        if len(self._plugged_ins)==0:
            flag=True
        
        return flag
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getPluggedIns (self): return self._plugged_ins


# ---------------------------------------------------------------------------

class OutSocket (Socket):
    
    def __init__(self, sid, type0, node):
        
        Socket.__init__(self, sid, type0, node)
        
        # lists of connected sockets 
        self._plugged_outs = []
    
    
    def addPluggedOut (self, inSocket):
        
        tmp = True
        for item in self._plugged_outs:
            if inSocket.getSId()==item.getSId():
                tmp = False
                break
        
        if tmp:
            self._plugged_outs.append (inSocket)
        
        return tmp
    
    def removePluggedOut (self, inSocket):
        
        tmp = False
        for item in self._plugged_outs:
            if item.getSId()==inSocket.getSId():
                
                del self._plugged_outs [self._plugged_outs.index (inSocket)]
                tmp = True
                break
        
        return tmp
    
    def isPluggedWith (self, socket):
        
        try:
            tmp = self._plugged_outs.index (socket)
        except ValueError:
            tmp = -1
        
        return False if tmp==-1 else True
    
    def isEmpty (self):
        
        flag = False
        
        if len(self._plugged_outs)==0:
            flag=True
        
        return flag
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getPluggedOuts (self): return self._plugged_outs