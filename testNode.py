'''
Created on Feb 5, 2012

@author: ivanoras
'''
import unittest

import Model
import Nodes


class TestNode (unittest.TestCase):


    def setUp (self):
        
        self.test_model = Model.Model ()
        self.node1 = self.test_model.addNode ()

    def tearDown (self):
        pass
    
    def testAddParent (self):
        
        node2 = self.test_model.addNode ()
        self.node1.addParent (node2)
        
        self.assertEqual (len(self.node1.getParents()), 1, "error : something went wrong when adding the parent")

    def testGetChild (self):
        
        node2 = Nodes.Node (115, 'hey_its_me')
        node3 = Nodes.Node (221, 'child')
        node4 = Nodes.Node (111, 'another_child')
        
        node2.addChild (node3)
        
        self.assertEqual (node2.getChild('child'), node3, "error : something went wrong when getting the child")

    def testGetParent (self):
        
        node2 = Nodes.Node (115, 'hey_its_me')
        node3 = Nodes.Node (221, 'parent')
        node4 = Nodes.Node (111, 'another_parent')
        
        node2.addParent (node3)
        
        self.assertEqual (node2.getParent('parent'), node3, "error : something went wrong when getting the parent")
    
    def testAddChild (self):
        
        node2 = self.test_model.addNode ()
        self.node1.addChild (node2)
        
        self.assertEqual (len(self.node1.getChildren()), 1, "error : something went wrong when adding the child")
    
    def testRemoveChild (self):
        
        node2 = self.test_model.addNode ()
        node3 = self.test_model.addNode ()
        self.node1.addChild (node2)
        
        self.assertTrue  (self.node1.removeChild (node2), "error while removing the child")
        self.assertEqual (len(self.node1.getChildren()), 0, "error : something went wrong when removing the child")
    
    def testAddParent (self):
        
        node2 = self.test_model.addNode ()
        self.node1.addParent (node2)
        
        self.assertEqual (len(self.node1.getParents()), 1, "error : something went wrong when adding the parent")
    
    def testRemoveParent (self):
        
        node2 = self.test_model.addNode ()
        node3 = self.test_model.addNode ()
        node2.addParent (node3)
        
        self.assertTrue  (node2.removeParent (node3), "error while removing the parent")
        self.assertEqual (len(node2.getParents()), 0, "error : something went wrong when removing the parent")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()