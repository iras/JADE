'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from xml.dom import minidom


class IO (object):
    '''
    This class manages graph importing and graph exporting to a file.
    '''
    
    def exportGraph (self, node_list, tag_position_dict):
        '''
        this method exports the graph in a XML-format file, dividing the graph into 2 blocks : nodes and links.
        
        @param node_list:
        @param tag_position_dict:
        @return string:
        '''
        macro_name = ''
        
        tmp = '<?xml version="1.0" encoding="UTF-8"?>\n<macro label="' + macro_name + '">\n'
        if len (node_list) > 0:
            
            tmp += '\t<nodes>\n'
            
            # (1) list out all the nodes and append them to the temp string.
            for node in node_list:
                tmp += '\t\t<' + node.getName() + ' id="' + str(node.getId()) + '" x="' + str(tag_position_dict[str(node.getId())].x()) + '" y="' + str(tag_position_dict[str(node.getId())].y()) + '"'
                # append props to the string if any.
                if len (node.getProps()) > 0:
                    for prop in node.getProps():
                        tmp += ' ' + str(prop[0]) + '="' + str(prop[2]) + '"'
                tmp += '/>\n'
            
            tmp += '\t</nodes>\n\t<links>\n'
            
            # (2) list out all the links and append them to the temp string. The InSockets will be only considered when
            #     going through the node_list since for each of them a correspondent OutSocket will be always found.
            if len (node_list) > 0:
                for node in node_list:
                    for socket in node.getIns():
                        for link in socket.getPluggedIns():
                            tmp += '\t\t<link>\n'
                            tmp += '\t\t\t<out id="' +  str(link.getNode().getId()) + '" connector="' + link.getSType()   + '"/>\n'
                            tmp += '\t\t\t<in id="' + str(socket.getNode().getId()) + '" connector="' + socket.getSType() + '"/>\n'
                            tmp += '\t\t</link>\n'
            
            tmp += '\t</links>\n'
        
        tmp += '</macro>\n'  
        
        return str(tmp)
    
    
    
    def importGraphData (self, XML_content):
        '''
        this method imports the graph from a XML-format file.
        
        @param string:
        @return list of 2 lists:
        '''
        
        def extractProperProps (xml_node):
            '''
            this closure returns the rest of the attributes (proper props) + relative values in a list of 2-lists.
            
            @param node a XML-format node.
            @return list list of 2-lists.
            '''
            tmp_list = []
            
            if len(xml_node.attributes.keys()) > 3:
                for a in xml_node.attributes.keys():
                    if str(a) != 'id' and str(a) != 'x' and str(a) != 'y':
                        tmp_list.append ([str(a), xml_node.attributes[str(a)].value])
            
            return tmp_list
        
        
        node_list = []
        link_list = []
        
        xml  = minidom.parseString (XML_content)
        self.nodes_XMLList = []
        self.link_XMLList  = []
        
        if xml != None:
            self.nodes_XMLList = xml.getElementsByTagName ('nodes')
            self.links_XMLList = xml.getElementsByTagName ('link')
        
        # (1) list out the nodes by tapping into the XML data.
        if len(self.nodes_XMLList) > 0:
            for i in range (0, len(self.nodes_XMLList[0].childNodes)):
                node = self.nodes_XMLList[0].childNodes[i]
                if node.nodeType == 1:  # the if-statement skips over the TEXT_NODEs and accepts only ELEMENT_NODEs, in other words the for-statement is running into nodes containing whitespace between the tags.
                    #print 'ATTR '+str(node.attributes.keys())+' ' + str(node.attributes.values())
                    node_list.append ([node.nodeName, node.attributes["id"].value, node.attributes["x"].value, node.attributes["y"].value, extractProperProps (node)])
        
        # (2) list out the links off the XML data.
        if len(self.links_XMLList) > 0:
            for i in range (0, len(self.links_XMLList)):
                
                for link in self.links_XMLList[i].childNodes:
                    
                    if link.nodeType == 1:  # skip the TEXT_NODEs
                        
                        if link.nodeName == 'out':
                            t = []
                            t.append(link.attributes["id"].value)
                            t.append(link.attributes["connector"].value)
                        elif link.nodeName == 'in':
                            t.append(link.attributes["id"].value)
                            t.append(link.attributes["connector"].value)
                            link_list.append (t)
        
        return [node_list, link_list]
