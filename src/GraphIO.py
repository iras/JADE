'''
Created on Oct 19, 2012

@author: macbookpro
'''
from xml.dom import minidom


class IO (object):
    '''
    This class manages graph importing and exporting a JADE graph to a file.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
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
                    node_list.append ([node.nodeName, node.attributes["id"].value, node.attributes["x"].value, node.attributes["y"].value])
        
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
