'''
Created on Feb 5, 2012

@author: ivanoras
'''
import unittest

import Model


class TestModel (unittest.TestCase):


    def setUp (self):
        
        self.test_graph = Model.Model ()
        self.node1 = self.test_graph.addNode ()
    
    def tearDown (self):
        pass
    
    def testAddNode (self):
        
        self.assertTrue  (self.test_graph.addNode (), "error : something went wrong when adding the node")
        self.assertEqual (self.test_graph.getNode (self.node1.getId()), self.node1, "error : node not found")        
        self.assertEqual (len(self.test_graph.getNodesList ()), 2, "error : node_list items number mistaken")
    
    def testRemoveNode (self):
        
        self.assertTrue  (self.test_graph.removeNode (self.node1.getId()), "error while removing the node")
        self.assertEqual (len(self.test_graph.getNodesList ()), 0, "error : node_list items number mistaken")
    
    def testAddLink (self):
        
        parent_node = self.node1
        child_node  = self.test_graph.addNode ()
        
        test_link = self.test_graph.addLink (parent_node.getId(), child_node.getId())
        
        self.assertEqual (len(self.test_graph.getLinksList()), 1, "error : link_list items number mistaken")
        
        self.assertTrue (parent_node.hasChild (child_node )[0], "error : parent hasn't got the child")
        self.assertTrue (child_node.hasParent (parent_node)[0], "error : child hasn't got the parent")
    
    def testRemoveLink (self):
        
        parent_node = self.node1
        child_node  = self.test_graph.addNode ()
        
        test_link = self.test_graph.addLink (parent_node.getId(), child_node.getId())
        
        self.assertEqual (len(self.test_graph.getLinksList()), 1, "error : link_list items number mistaken")
        self.assertTrue (self.test_graph.removeLink (test_link.getId()), "error : link_list items number mistaken")
        
        self.assertFalse (parent_node.hasChild (child_node )[0], "error : parent has still got the child")
        self.assertFalse (child_node.hasParent (parent_node)[0], "error : child has still got the parent")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main ()