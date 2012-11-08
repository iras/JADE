'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from xml.dom import minidom
from xml.dom.minidom import parseString

import Comm0
import Nodes0 as nd
import GraphIO as gio



class Graph ():
    '''
    Base model class for the JADE app. The other specific sub-models are the class: Nodes0 and Socket which sub-classes into InSocket and OutSocket.
    
    This class is unit tested, cfr. textGraph.py
    '''
    def __init__(self):
        '''constructor
        '''
        # signal global operator
        self.comm = Comm0.Comm0 ()
        self.node_details_map = {}
        
        self._node_list = []
        
        self.graph_io = gio.IO()
        
    def getComm (self):
        '''Getter.
                
        @return self.comm instance of class Comm0
        '''
        return self.comm
    
    # - - -  node methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addNode (self, node_name, node_x, node_y):
        '''This method creates a generic node.
        
        @param node_name string
        
        @return node instance of class Node0
        '''
        newNode = nd.Node0 (self.comm.getNewNodeId(), node_name, self.comm)
        self.initProps (newNode)
        self._node_list.append (newNode)
        
        self.comm.emitAddNodeMSignal (newNode.getId(), node_x, node_y)
        
        return newNode
    
    def importNode (self, node_id, node_name, node_x, node_y, props_list):
        '''This method creates a node from given data and it's used exclusively when importing a file.
        
        @param node_id int
        @param node_name string
        @param x float
        @param y float
        @param props_list list of props, each entry is a 2-list [prop_name, prop_value]
        
        @return node instance of class Node0
        '''
        self.comm.updateNodeId (node_id) # keep the node id counter up to date.
        
        importedNode = nd.Node0 (node_id, node_name, self.comm)
        self.initProps   (importedNode)
        self.importProps (importedNode, props_list)
        
        self._node_list.append (importedNode)
        
        self.comm.emitAddNodeMSignal (importedNode.getId(), node_x, node_y)
        
        return importedNode
    
    def removeNode (self, node0_id):
        '''This method removes a specific node.
        
        @param node0_id int
        
        @return tmp boolean
        '''
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
        '''This method duplicates a specific node.
        
        @param node0 instance of class Node0
        
        @return node1 instance of class Node0
        '''
        node1 = self.addNode (node0.getName (), 0.0, 0.0)
                
        node1.setIns  (node0.getIns ())
        node1.setOuts (node0.getOuts())
        
        node1.setProps (node0.getProps ())
        
        return node1
    
    def getNodeList (self):
        '''Getter.
                
        @return self._node_list list
        '''
        return self._node_list
    
    def addInSocket (self, node_id, stype):
        '''This method adds a new InSocket's instance given the node id and the socket type.
        
        @param node_id int
        @param stype string
        
        @return socket instance of class InSocket
        '''
        tmp_socket = None
        
        node = self.getNode (node_id)
        if node!=None:
            tmp_socket = node.addIn (stype)
        
        return tmp_socket
    
    def addOutSocket (self, node_id, stype):
        '''This method adds a new OutSocket's instance given the node id and the socket type.
        
        @param node_id int
        @param stype string
        
        @return socket instance of class OutSocket
        '''
        tmp_socket = None
        
        node = self.getNode (node_id)
        if node!=None:
            tmp_socket = node.addOut (stype)
        
        return tmp_socket
    
    def getNode (self, node_id):
        '''This method retrieves a specific instance of the class Node0 given the node_id.
        
        @param node_id int
        
        @return node1 instance of class Node0
        '''
        tmp = None
        for item in self._node_list:
            if item.getId()==node_id:
                tmp = item
                break
        
        return tmp
    
    def getInsTypesLeft (self, node_id):
        '''This method retrieves lists out the types of InSocket still available for a specific node, given the node id.
        
        @param node_id int
        
        @return list list of string
        '''
        tmp_list = []
        node = self.getNode (node_id)
        for socket in node.getIns ():
            tmp_list.append (socket.getSType())
        
        return list (set(self.node_details_map[node.getName()][0]) - set(tmp_list))
    
    def getOutsTypesLeft (self, node_id):
        '''This method retrieves lists out the types of OutSocket still available for a specific node, given the node id.
        
        @param node_id int
        
        @return list list of string
        '''
        tmp_list = []
        node = self.getNode (node_id)
        for socket in node.getOuts ():
            tmp_list.append (socket.getSType())
        
        return list (set(self.node_details_map[node.getName()][1]) - set(tmp_list))
    
    # - - -  links methods  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def addLink (self, inSocket, outSocket):
        '''This method adds a link between a pair of Sockets (an InSocket and an OutSocket). A signal 'addLink_MSignal' is consequently given off.
        
        @param inSocket instance of the class InSocket
        @param outSocket instance of the class OutSocket
        '''
        inSocket.addPluggedIn   (outSocket)
        outSocket.addPluggedOut (inSocket)
        
        self.comm.emitAddLinkMSignal (inSocket.getSId(), outSocket.getSId())
    
    def importLink (self, id_out_node, type_out_socket, id_in_node, type_in_socket):
        '''This method imports a link between a pair of Sockets (an InSocket and an OutSocket).
        
        @param id_out_node int
        @param type_out_socket string
        @param id_in_node int
        @param type_in_socket string
        '''
        inSocket = self.getSocketFromNode (id_in_node, type_in_socket) # try n retrieve the appropriate inSocket for the node with id=id_in_node
        if inSocket == None: inSocket = self.addInSocket (id_in_node, type_in_socket) # if not, add it.
        
        outSocket = self.getSocketFromNode (id_out_node, type_out_socket) # try n retrieve the appropriate outSocket for the node with id=id_out_node
        if outSocket == None: outSocket = self.addOutSocket (id_out_node, type_out_socket) # if not, add it.
        
        self.addLink (inSocket, outSocket)
    
    def removeLink (self, s_in_id, s_out_id):
        '''This method removes an existing link between a pair of Sockets (an InSocket and an OutSocket). A signal 'deleteLink_MSignal' is consequently given off.
        
        @param s_in_id int
        @param s_out_id int
        '''
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
    
    def areSocketsRelated (self, s1_id, s2_id):
        '''This method queries whether two sockets are related (a link between them is already in place).
        
        @param s1_id int
        @param s2_id int
        
        @return flag boolean
        '''
        flag = False
        
        s1 = self.getSocket (s1_id)
        s2 = self.getSocket (s2_id)
        
        if s1.isPluggedWith(s2) or s2.isPluggedWith(s1): flag=True
        
        return flag
    
    # - - -  misc props  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def initProps (self, node):
        '''This method initiates the node's props values to the default values found in the dictionary self.node_details_map.
        
        @param node XML-format node
        '''
        node.setProps (self.node_details_map [node.getName()][2])
    
    def importProps (self, node, new_props_list):
        '''This method updates the node's props values to the ones found in the given new_props_list.
        
        @param node XML-format node
        @param new_props_list list of 2_lists [prop_name, prop_value]
        '''
        if len (new_props_list) > 0:
            for prop in new_props_list:
                node.updateProp (str(prop[0]), str(prop[1]))
    
    # - - -  misc sockets  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getSocket (self, sid):
        '''This method retrieves an instance of the class Socket given its socket id.
        
        @param sid int
        
        @return s instance of class Socket (either InSocket or OutSocket)
        '''
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
    
    def getSocketFromNode (self, node_id, socket_type):
        '''This method retrieves an instance of the class Socket given the id of the node it belongs to and the socket type.
        
        @param node_id int
        @param socket_type string
        
        @return s instance of class Socket (either InSocket or OutSocket)
        '''
        node = self.getNode (node_id)
        s = None
        
        for socket in node.getIns ():
            if socket.getSType()==socket_type:
                s = socket
                break
        
        for socket in node.getOuts ():
            if socket.getSType()==socket_type:
                s = socket
                break
        
        return s
    
    # graph nodes description  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def setNodesDescription (self, text_xml):
        '''This method configures the types of nodes the user is able to handle in the JADE editor.
        That means that modifying the node types is possible. The nodes description can be found in
        the XML file "available_nodes.xml"
        
        @param text_xml string
        '''
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
            
            props_ls = []
            self.props_XMLList  = item.getElementsByTagName ('prop')
            for item_prop in self.props_XMLList:
                props_ls.append ([str(item_prop.getElementsByTagName ('name')[0].firstChild.data),
                                  str(item_prop.getElementsByTagName ('type')[0].firstChild.data),
                                  str(item_prop.getElementsByTagName ('default')[0].firstChild.data)])
            
            self.node_details_map [node_name] = [list(inputs_ls), list(outputs_ls), list(props_ls)]
        
        # print map
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint (self.node_details_map)
    
    def getNodesDecription (self):
        '''Getter.
        
        @return self.node_details_map dictionary
        '''
        return self.node_details_map
    
    # i/o - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def exportGraph (self, tag_position_dict):
        '''This method exports the graph given the dictionary of tag's positions.
        
        @param tag_position_dict dictionary
        
        @return graph_XML_string string 
        '''
        return self.graph_io.exportGraph (self._node_list, tag_position_dict)
    
    def importGraph (self, XML_content):
        '''This method imports a graph given the string XML_content passed in.
        
        @param XML_content string 
        '''
        tmp_list = self.graph_io.importGraphData (XML_content)
        
        node_list = tmp_list[0]
        link_list = tmp_list[1]
        
        print '\n\nImport Nodes'
        for item in node_list:
            print item[0], item[1], item[2], item[3]
            self.importNode (int(item[1]), item[0], float(item[2]), float(item[3]), item[4])
        
        print '\n\nImport Links'
        for item in link_list:
            self.importLink (int(item[0]), item[1], int(item[2]), item[3])
            print item[0], item[1], item[2], item[3]
