'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

class Socket ():
    '''
    sub-model abstract class.
    
    This class (and its subclasses) is unit tested, cfr. textSockets.py
    '''
    def __init__(self, sid, type0, node):
        '''constructor
        
        @param sid int
        @param type0 string
        @param node instance of class Node0
        '''
        self._sid   = sid   # socket's id
        self._node  = node  # id of the node this socket belongs to.
        self._stype = str(type0)
        
        self._attributes = []
    
    def isPluggedWith (self, socket):
        '''abstract method that queries whether a given socket is plugged in with the current socket or it is still loose.
        
        @param socket socket
        '''
        raise Exception ("*** Method isPluggedWith (...) needs implementing.")
    
    def isEmpty (self):
        '''abstract method that queries whether the current socket is plugged in with any other socket.        
        '''
        raise Exception ("*** Method isEmpty () needs implementing.")
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getSId (self):
        '''Getter.
                
        @return self._sid int
        '''
        return self._sid
    
    def getNode (self):
        '''Getter.
                
        @return self._node instance of class Node0.
        '''
        return self._node
    
    def getSType (self):
        '''Getter.
                
        @return self._stype string
        '''
        return self._stype
    
    def getAttributes (self):
        '''Getter.
                
        @return self._attributes list
        '''
        return self._attributes
    

# ---------------------------------------------------------------------------


class InSocket (Socket):
    '''
    sub-model implemented class.
    
    This class is unit tested, cfr. textSockets.py
    '''
    def __init__(self, sid, type0, node):
        '''constructor
        
        @param sid int
        @param type0 string
        @param node instance of class Node0
        '''
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
        '''implemented method that queries whether the given outSocket is plugged in with the current InSocket's instance or it is still loose.
        
        @param socket outSocket's instance.
        '''
        try:
            tmp = self._plugged_ins.index (socket)
        except ValueError:
            tmp = -1
        
        return False if tmp==-1 else True
    
    def isEmpty (self):
        '''implemented method that queries whether the current socket is plugged in with any other socket.        
        '''
        flag = False
        
        if len(self._plugged_ins)==0:
            flag=True
        
        return flag
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getPluggedIns (self):
        '''Getter.
                
        @return self._plugged_outs list of InSocket's instances.
        '''
        return self._plugged_ins


# ---------------------------------------------------------------------------

class OutSocket (Socket):
    '''
    sub-model implemented class.
    
    This class is unit tested, cfr. textSockets.py
    '''
    def __init__(self, sid, type0, node):
        '''constructor
        
        @param sid int
        @param type0 string
        @param node instance of class Node0
        '''
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
        '''implemented method that queries whether the given inSocket is plugged in with the current OutSocket's instance or it is still loose.
        
        @param socket inSocket's instance.
        '''
        try:
            tmp = self._plugged_outs.index (socket)
        except ValueError:
            tmp = -1
        
        return False if tmp==-1 else True
    
    def isEmpty (self):
        '''implemented method that queries whether the current socket is plugged in with any other socket.        
        '''
        flag = False
        
        if len(self._plugged_outs)==0:
            flag=True
        
        return flag
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getPluggedOuts (self):
        '''Getter.
                
        @return self._plugged_outs list of OutSocket's instances.
        '''
        return self._plugged_outs