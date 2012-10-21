'''
Created on Oct 19, 2012

@author: macbookpro
'''

class Exporter (object):
    '''
    This class manages graph exporting functionalities.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def export (self, node_list, tag_position_dict):
        '''
        this method exports the graph in an XML format, dividing the graph in nodes and links.
        '''
        macro_name = ''
        
        tmp = '<macro label="' + macro_name + '">\n'
        if len (node_list):
            
            tmp += '\t<nodes>\n'
            
            # (1) list out all the nodes.
            for node in node_list:
                tmp += '\t\t<' + node.getName() + ' id="' + str(node.getId()) + '" x ="' + str(tag_position_dict[str(node.getId())].x()) + '" y ="' + str(tag_position_dict[str(node.getId())].y()) + '" />\n'
            
            tmp += '\t</nodes>\n\t<links>\n'
            
            # (2) list out all the links. Only the InSockets will be considered since for each of them a correspondent OutSocket will be found.
            for node in node_list:
                for socket in node.getIns():
                    for link in socket.getPluggedIns():
                        tmp += '\t\t<link>\n'
                        tmp += '\t\t\t<out id="' +  str(link.getNode().getId()) + '" connector="' + link.getSType()   + '" />\n'
                        tmp += '\t\t\t<in id="' + str(socket.getNode().getId()) + '" connector="' + socket.getSType() + '" />\n'
                        tmp += '\t\t</link>\n'
                    
            tmp += '\t</links>\n'
        
        tmp += '</macro>\n'  
        
        return str(tmp)