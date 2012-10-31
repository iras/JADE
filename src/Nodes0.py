"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

import Sockets as sk

class Node0 ():

    def __init__(self, id0, name, comm):
        
        self._id   = id0 # id0 has been used instead of id since the latter is a built-in variable.
        self._name = str(name)
        self.comm  = comm
        
        # lists of input/output sockets 
        self._ins  = []
        self._outs = []
        
        # list of props. Each element of the list is a 3-list. [prop name, prop type, prop value]
        self._props_list = []
    
    def disposeNode (self):   # SURPLUS - WHAT TO DO WITH THIS ?
        pass
    
    def updateProp (self, name_prop, value_prop):
        
        print 'update node '+str(self._id)
        if len(self._props_list) > 0:
            for prop in self._props_list:
                if prop[0] == name_prop:
                    prop[2] = value_prop
                    break
    
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
                for i in range (qq-1, -1, -1):
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
                for i in range (qq-1, -1, -1):
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
    
    def getProps (self): return self._props_list
    
    def setName (self, name0): self._name = name0
    
    # the following lists are copied, not just referenced.
    
    def setIns  (self, ls):
        self._ins = []
        self._ins.extend (ls)
    
    def setOuts (self, ls):
        self._outs = []
        self._outs.extend (ls)
    
    def setProps (self, ls):
        # ls is a list of lists in this case. So, copying a list of lists is slightly different,
        self._props_list = []
        
        if len(ls) > 0:
            for item in ls:
                self._props_list.append ([item[0], item[1], item[2]])
