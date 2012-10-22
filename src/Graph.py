"""
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
"""

from xml.dom import minidom
from xml.dom.minidom import parseString

import Nodes0 as nd
import Comm0
import GraphIO as gio



class Graph ():

    def __init__(self):
        
        # signal global operator
        self.comm = Comm0.Comm0 ()
        self.connections_map = {}
        
        self._node_list = []
        
        self.graph_io = gio.IO()
        
    def getComm (self): return self.comm
    
    # - - -  nodes methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addNode (self):
        
        newId   = self.comm.getNewNodeId()
        newName = 'node_'+str(newId)
        
        newNode = nd.Node0 (newId, newName, self.comm)
        self._node_list.append (newNode)
        
        self.comm.emitAddNodeMSignal (newNode.getId())
        
        return newNode
    
    def importNode (self, node_id, node_name):
        
        importedNode = nd.Node0 (node_id, node_name, self.comm)
        self._node_list.append (importedNode)
        
        self.comm.emitAddNodeMSignal (importedNode.getId())
        
        return importedNode
    
    def removeNode (self, node0_id):
        
        # node removal code
        tmp = False
        for node in self._node_list:
            if node.getId()==node0_id:
                
                # unplug connections first
                
                for item in reversed(node.getIns()) : node.removeIn (item)
                for item in reversed(node.getOuts()): node.removeOut(item)
                
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
        
        node = self.getNode (node_id)
        if node!=None:
            node.addIn (stype)
    
    def addOutSocket (self, node_id, stype):
        
        node = self.getNode (node_id)
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
        
        return list (set(self.connections_map[node.getName()][1]) - set(tmp_list))
    
    # - - -  links methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addLink (self, inSocket, outSocket):
        
        inSocket.addPluggedIn   (outSocket)
        outSocket.addPluggedOut (inSocket)
        
        self.comm.emitAddLinkMSignal (inSocket.getSId(), outSocket.getSId())
    
    def removeLink (self, s_in_id, s_out_id):
        
        if self.areSocketsRelated (s_in_id, s_out_id) == True:
            
            flag1 = False
            flag2 = False
            
            s_in  = self.getSocket (s_in_id)
            s_out = self.getSocket (s_out_id)
            
            if s_in.isPluggedWith (s_out):
                flag1 = s_in.removePluggedIn   (s_out)
                flag2 = s_out.removePluggedOut (s_in)
            
            if flag1==True and flag2==True:
                self.comm.emitDeleteLinkMSignal (s_in_id, s_out_id)
    
    # - - -  miscellanea  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def areSocketsRelated (self, s1_id, s2_id):
        
        flag = False
        
        s1 = self.getSocket (s1_id)
        s2 = self.getSocket (s2_id)
        
        if s1.isPluggedWith(s2) or s2.isPluggedWith(s1): flag=True
        
        return flag
    
    def getSocket (self, sid):
        
        s = None
        
        for node in self._node_list:
            
            if s==None:
                
                for socket in node.getIns ():
                    if socket.getSId()==sid:
                        s = socket
                        break
                
                for socket in node.getOuts ():
                    if socket.getSId()==sid:
                        s = socket
                        break
            else:
                break
        
        return s
    
    # graph rules
    
    def setRules (self, text_xml):
        
        self.xml_rules_table = parseString(text_xml)
        
        self.node_rules_XMLList = self.xml_rules_table.getElementsByTagName ('node')
        
        for item in self.node_rules_XMLList:
                        
            node_name = item.getElementsByTagName ('class')[0].firstChild.data
            tmp_ls = node_name.split('.')
            node_name = str(tmp_ls[-1])
            
            inputs_ls = []
            self.inputs_XMLList  = item.getElementsByTagName ('input')
            for item_input in self.inputs_XMLList:
                if item_input.getElementsByTagName ('type')[0].firstChild.data == 'Connector':
                    inputs_ls.append (str(item_input.getElementsByTagName ('name')[0].firstChild.data))
            
            outputs_ls = []
            self.outputs_XMLList  = item.getElementsByTagName ('output')
            for item_output in self.outputs_XMLList:
                if item_output.getElementsByTagName ('type')[0].firstChild.data == 'Connector':
                    outputs_ls.append (str(item_output.getElementsByTagName ('name')[0].firstChild.data))
            
            self.connections_map[node_name] = [list(inputs_ls), list(outputs_ls)]
        
        # print map
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint (self.connections_map)
    
    def getRules (self): return self.connections_map
    
    # i/o
    
    def exportGraph (self, tag_position_dict):
        return self.graph_io.exportGraph (self._node_list, tag_position_dict)
    
    def importGraph (self, XML_content):
        self.graph_io.importGraph (XML_content)
