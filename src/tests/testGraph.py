'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import QObject, SIGNAL

import unittest

import Graph as gf
import Nodes0 as nd


class TestGraph (unittest.TestCase):


    def setUp (self):
        
        self.test_graph = gf.Graph ()
        
        QObject.connect (self.test_graph.getComm (), SIGNAL('addNode_MSignal(int, float, float)'), self.addNode_MSignalListener)
        QObject.connect (self.test_graph.getComm (), SIGNAL('deleteNode_MSignal(int)'), self.addInSocket_MSignalListener)
        QObject.connect (self.test_graph.getComm (), SIGNAL('addLink_MSignal(int,int)'), self.addLink_MSignalListener)
        QObject.connect (self.test_graph.getComm (), SIGNAL('deleteLink_MSignal(int,int)'), self.removeLink_MSignalListener)
        
        self.receivedNId = 0
        self.isAddNode_MSignalReceived    = False
        self.isRemoveNode_MSignalReceived = False
        self.isAddLink_MSignalReceived    = False
        self.isRemoveLink_MSignalReceived = False
        
        map0 = {'stateBegun'    :[['type0_s', 'type1_s', 'type2_s', 'type3_s'],['type1_s'],[],[]],
               'triggerFire'   :[['type0_s', 'type4_s'],['type1_s', 'type2_s', 'type3_s'],[],[]],
               'stopAction'    :[['type1_s', 'type2_s'],[],[],[]],
               'restoreAction' :[[],['type1_s', 'type2_s'],[],[]]}
        self.test_graph.node_details_map = map0
    
    def tearDown(self):
        pass
    
    def addNode_MSignalListener (self,e):
        
        self.isAddNode_MSignalReceived = True
        self.receivedNId = e
    
    def addInSocket_MSignalListener (self,e):
        
        self.isRemoveNode_MSignalReceived = True
        self.receivedNId = e
    
    def addLink_MSignalListener (self,e):
        
        self.isAddLink_MSignalReceived = True
        self.receivedNId = e
    
    def removeLink_MSignalListener (self,e):
        
        self.isRemoveLink_MSignalReceived = True
        self.receivedNId = e
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    def testAddNode (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.assertEqual (len(self.test_graph.getNodeList ()), 1, 'Wrong no. of nodes in the list.')
        self.assertTrue  (isinstance (self.node1, nd.Node0), 'Not the right type returned.')
        self.assertEqual (self.isAddNode_MSignalReceived, True, 'Didn''t get SIGNAL addInSocket_MSignal(int)')
    
    def testAddMultipleNodes (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        self.node3 = self.test_graph.addNode ('stateBegun', 200.0, 0.0)
        self.assertEqual (len(self.test_graph.getNodeList ()), 3, 'Wrong no. of nodes in the list.')
    
    def testRemoveNode (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        result = self.test_graph.removeNode (self.node1.getId())
        self.assertEqual (len(self.test_graph.getNodeList ()), 0, 'Wrong no. of nodes in the list.')
        self.assertTrue  (result, 'The returned value isn''t True')
        self.assertEqual (self.isRemoveNode_MSignalReceived, True, 'Didn''t get SIGNAL addInSocket_MSignal(int)')
        
        self.assertFalse (self.test_graph.removeNode (self.node1.getId()), 'The returned value isn''t False')
    
    def testRemoveMultipleNodes (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        self.node3 = self.test_graph.addNode ('stateBegun', 200.0, 0.0)
        
        self.test_graph.removeNode (self.node2.getId())
        self.assertEqual (len(self.test_graph.getNodeList ()), 2, 'Wrong no. of nodes in the list.')
        self.assertEqual (self.isRemoveNode_MSignalReceived, True, 'Didn''t get SIGNAL addInSocket_MSignal(int)')
        
        self.isRemoveNode_MSignalReceived = False
        self.test_graph.removeNode (self.node1.getId())
        self.assertEqual (len(self.test_graph.getNodeList ()), 1, 'Wrong no. of nodes in the list.')
        self.assertEqual (self.isRemoveNode_MSignalReceived, True, 'Didn''t get SIGNAL addInSocket_MSignal(int)')
    
    def testDuplicateNode (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 200.0, 0.0)
        self.node3 = self.test_graph.addNode ('stateBegun', 300.0, 0.0)
        self.node4 = self.test_graph.addNode ('stateBegun', 400.0, 0.0)
        self.node5 = self.test_graph.addNode ('stateBegun', 500.0, 0.0)
        
        # going to duplicate node1
        # add sockets - in and out
        n1sin1  = self.node1.addIn ('type0')
        n1sin2  = self.node1.addIn ('type1')
        n1sout1 = self.node1.addOut('type0')
        
        # add other nodes' sockets
        n2sout1 = self.node2.addOut('type0')
        n3sout1 = self.node3.addOut('type1')
        n4sin1  = self.node4.addIn ('type0')
        n5sin1  = self.node5.addIn ('type0')
        
        self.test_graph.addLink (n1sin1, n2sout1)
        self.test_graph.addLink (n1sin1, n3sout1)
        self.test_graph.addLink (n4sin1, n1sout1)
        self.test_graph.addLink (n5sin1, n1sout1)
        
        duplicate = self.test_graph.duplicateNode (self.node1)
        self.assertTrue (isinstance (duplicate, nd.Node0), 'unexpected type received')
        self.assertEquals (len(self.test_graph.getNodeList()), 6, 'unexpected length of list received')
        self.assertTrue (duplicate.hasIn (n1sin1)[0], 'duplicate In test failed')
        self.assertTrue (duplicate.hasIn (n1sin2)[0], 'duplicate In test failed')
        self.assertTrue (duplicate.hasOut(n1sout1)[0],'duplicate Out test failed')
        self.assertFalse(duplicate.hasOut(n3sout1)[0],'duplicate Out test failed')
        
    def testAddLink (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 200.0, 0.0)
        
        n1sin1  = self.node1.addIn ('type0')
        n2sout1 = self.node2.addOut('type0')
        
        self.test_graph.addLink (n1sin1, n2sout1)
        self.assertTrue (self.isAddLink_MSignalReceived, 'not as true as it should be.')
    
    def testRemoveLink (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        
        n1sin1  = self.node1.addIn ('type0')
        n2sout1 = self.node2.addOut('type0')
        
        self.test_graph.addLink (n1sin1, n2sout1)
        
        self.test_graph.removeLink (n1sin1.getSId(), n2sout1.getSId())
        self.assertTrue (self.isRemoveLink_MSignalReceived, 'not as true as it was expected to be.')
    
    def testGetNode (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        
        self.assertEqual (self.test_graph.getNode(self.node2.getId()), self.node2, 'didn''t get the right node')
        self.assertEqual (self.test_graph.getNode(self.node1.getId()), self.node1, 'didn''t get the right node')
        self.assertEqual (self.test_graph.getNode(3), None, 'didn''t get None')
    
    def testGetInsTypesLeft (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.node1.setName ('stateBegun')
        
        n1sin1  = self.node1.addIn ('type3_s')
        n1sin2  = self.node1.addIn ('type1_s')
        
        result = self.test_graph.getInsTypesLeft (self.node1.getId())

        self.assertEqual (result[0], 'type0_s', 'received wrong ins type left.')
        self.assertEqual (result[1], 'type2_s', 'received wrong ins type left.')
        self.assertEqual (len(result), 2, 'received wrong amount of ins type left.')

    def testGetOutsTypesLeft (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 0.0, 0.0)
        self.node1.setName ('triggerFire')
        
        n1sout1  = self.node1.addOut ('type3_s')
        n1sout2  = self.node1.addOut ('type1_s')
        
        result = self.test_graph.getOutsTypesLeft (self.node1.getId())
        
        self.assertEqual (result[0], 'type2_s', 'received wrong outs type left.')
        self.assertEqual (len(result), 1, 'received wrong amount of outs type left.')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def testGetSocket (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 200.0, 0.0)
        self.node3 = self.test_graph.addNode ('stateBegun', 300.0, 0.0)
        self.node4 = self.test_graph.addNode ('stateBegun', 400.0, 0.0)
        self.node5 = self.test_graph.addNode ('stateBegun', 500.0, 0.0)
        
        # going to duplicate node1
        # add sockets - in and out
        n1sin1  = self.node1.addIn ('type0')
        n1sin2  = self.node1.addIn ('type1')
        n1sout1 = self.node1.addOut('type0')
        
        # add other nodes' sockets
        n2sout1 = self.node2.addOut('type0')
        n3sout1 = self.node3.addOut('type1')
        n4sin1  = self.node4.addIn ('type0')
        n5sin1  = self.node5.addIn ('type0')
        
        self.assertEqual (self.test_graph.getSocket (n4sin1.getSId()),  n4sin1, 'socket not found')
        self.assertEqual (self.test_graph.getSocket (n1sin2.getSId()),  n1sin2, 'socket not found')
        self.assertEqual (self.test_graph.getSocket (n5sin1.getSId()),  n5sin1, 'socket not found')
        self.assertEqual (self.test_graph.getSocket (n3sout1.getSId()), n3sout1,'socket not found')
    
    def testAreSocketsRelated (self):
        
        self.node1 = self.test_graph.addNode ('stateBegun', 100.0, 0.0)
        self.node2 = self.test_graph.addNode ('stateBegun', 200.0, 0.0)
        self.node3 = self.test_graph.addNode ('stateBegun', 300.0, 0.0)
        self.node4 = self.test_graph.addNode ('stateBegun', 400.0, 0.0)
        self.node5 = self.test_graph.addNode ('stateBegun', 500.0, 0.0)
        
        # going to duplicate node1
        # add sockets - in and out
        n1sin1  = self.node1.addIn ('type0')
        n1sin2  = self.node1.addIn ('type1')
        n1sout1 = self.node1.addOut('type0')
        
        # add other nodes' sockets
        n2sout1 = self.node2.addOut('type0')
        n3sout1 = self.node3.addOut('type1')
        n4sin1  = self.node4.addIn ('type0')
        n5sin1  = self.node5.addIn ('type0')
        
        self.test_graph.addLink(n5sin1, n1sout1)
        self.test_graph.addLink(n1sin2, n3sout1)
        
        self.assertTrue (self.test_graph.areSocketsRelated (n1sout1.getSId(), n5sin1.getSId()), 'unexpectedly unrelated.')
        self.assertTrue (self.test_graph.areSocketsRelated (n1sin2.getSId(), n3sout1.getSId()), 'unexpectedly unrelated.')
        self.assertFalse(self.test_graph.areSocketsRelated (n1sin2.getSId(), n1sout1.getSId()), 'unexpectedly unrelated.')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
