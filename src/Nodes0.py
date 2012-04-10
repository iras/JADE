'''
Created on Feb 18, 2012

@author: ivanoras
'''
import Sockets as sk

class Node0 ():

    def __init__(self, id, name, comm):
        
        self._id   = id
        self._name = str(name)
        self.comm  = comm
        
        # lists of input/output sockets 
        self._ins  = []
        self._outs = []
        
        self._attributes = []
        
    def disposeNode (self):   # SURPLUS - WHAT TO DO WITH THIS ?
        pass
    
    # - - -  sockets methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addIn  (self, stype):
        
        inSocket = None
        
        # check out that it's not already there as there can only be one type of inSocket down an in_rail.
        tmp = True
        for item in self._ins:
            if item.getSType ()==stype:
                tmp = False
                break
        
        if tmp:
            newId = self.comm.getNewSocketId()
            inSocket = sk.InSocket (newId, stype, self)
        
            self._ins.append (inSocket)
            self.comm.emitAddInSocketMSignal (self._id, inSocket.getSId())
        
        return inSocket
    
    def addOut (self, stype):
        
        outSocket = None
        
        # check out that it's not already there as there can only be one type of outSocket down an out_rail.
        tmp = True
        for item in self._outs:
            if item.getSType ()==stype:
                tmp = False
                break
        
        if tmp:
            newId = self.comm.getNewSocketId()
            outSocket = sk.OutSocket (newId, stype, self)
        
            self._outs.append (outSocket)
            self.comm.emitAddOutSocketMSignal (self._id, outSocket.getSId())
        
        return outSocket
    
    # removeIn (InSocket) : Boolean
    def removeIn (self, inSocket):
        
        for socket in self._ins:
            if socket==inSocket:
                
                # (1) clear all the references to the current inSocket
                for outSocket in inSocket.getPluggedIns():
                    outSocket.removePluggedOut (inSocket)
                    self.comm.emitDeleteLinkMSignal (inSocket.getSId(), outSocket.getSId())
                
                # (1b) clear the references to all the outSockets
                pluggedInList = inSocket.getPluggedIns ()
                qq = len (pluggedInList)
                for i in range(qq-1, 0, -1):
                    del pluggedInList[i]
                
                # (2) signal deletion of the inSocket
                self.comm.emitDeleteInSocketMSignal (self._id, inSocket.getSId())
                
                # (3) delete the inSocket reference from this node
                del self._ins [self._ins.index (inSocket)]
                
                break
    
    # removeOut (OutSocket) : Boolean
    def removeOut (self, outSocket):
        
        for socket in self._outs:
            if socket==outSocket:
                
                # (1) clear all the references to the current outSocket.
                for inSocket in outSocket.getPluggedOuts():
                    inSocket.removePluggedIn (outSocket)
                    self.comm.emitDeleteLinkMSignal (inSocket.getSId(), outSocket.getSId())
                
                # (1b) clear the references to all the inSockets
                pluggedOutList = outSocket.getPluggedOuts ()
                qq = len (pluggedOutList)
                for i in range(qq-1, 0, -1):
                    del pluggedOutList[i]
                
                # (2) signal deletion of the outSocket
                self.comm.emitDeleteOutSocketMSignal (self._id, outSocket.getSId())
                
                # (3) delete the outSocket reference from this node
                del self._outs [self._outs.index (outSocket)]
                
                break
    
    def getInByType (self, stype):    # VERIFY ITS USEFULLNESS
        
        tmp = None
        for item in self._ins:
            if item.getSType()==stype:
                tmp = item
                break
        
        return tmp
    
    def getAllInsTypes (self):         # VERIFY ITS USEFULLNESS
        
        tmp = []
        for item in self._ins:
            if item.getSType() not in tmp:
                tmp.append (item.getSType())
        
        return tmp
    
    def getOutByType (self, stype):    # VERIFY ITS USEFULLNESS
        
        tmp = None
        for item in self._outs:
            if item.getSType()==stype:
                tmp = item
                break
        
        return tmp
    
    def getAllOutsTypes (self):        # VERIFY ITS USEFULLNESS
        
        tmp = []
        for item in self._outs:
            if item.getSType() not in tmp:
                tmp.append (item.getSType())
        
        return tmp
    
    # hasIn (inSocket) : 2-list [Boolean, int]
    def hasIn (self, inSocket):
        
        try:
            tmp = self._ins.index (inSocket)
        except ValueError:
            tmp = -1
        
        list0 = [False, tmp]
        if list0[1]!=-1: list0[0]=True
        return list0
    
    # hasOut (outSocket) : 2-list [Boolean, int]
    def hasOut (self, outSocket):
        
        try:
            tmp = self._outs.index (outSocket)
        except ValueError:
            tmp = -1
        
        list0 = [False, tmp]
        if list0[1]!=-1: list0[0]=True
        return list0
    
    # - - getters / setters - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getId   (self): return self._id
    def getName (self): return self._name
    
    def getIns  (self): return self._ins
    def getOuts (self): return self._outs
    
    def getAttributes (self): return self._attributes
    
    
    def setName (self, name0): self._name = name0
    
    def setIns  (self, ls):
        self._ins = []
        self._ins.extend (ls)
    
    def setOuts (self, ls):
        self._outs = []
        self._outs.extend (ls)
    
    def setAttributes (self, ls):
        self._attributes = []
        self._attributes.extend (ls)