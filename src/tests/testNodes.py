'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool
'''

from PyQt4.QtCore import QObject, SIGNAL

import unittest

import Graph as gf


class TestNode (unittest.TestCase):
    
    def setUp (self):
        
        self.test_graph = gf.Graph ()
        self.test_graph.node_details_map ['node_1'] = [[], [], []]
        self.test_graph.node_details_map ['node_2'] = [[], [], []]
        self.test_graph.node_details_map ['node_3'] = [[], [], []]
        
        self.node1 = self.test_graph.addNode ('node_1', 0.0, 0.0)
        self.node2 = self.test_graph.addNode ('node_2', 100.0, 0.0)
        self.node3 = self.test_graph.addNode ('node_3', 200.0, 0.0)
        
        self.receivedNId = 0
        self.receivedSId = 0
        self.isAddInSocket_MSignalReceived     = False
        self.isAddOutSocket_MSignalReceived    = False
        self.isRemoveInSocket_MSignalReceived  = False
        self.isRemoveOutSocket_MSignalReceived = False
        
        comm=self.test_graph.getComm ()
        QObject.connect (comm, SIGNAL('addInSocket_MSignal(int,int)'),  self.addInSocket_MSignalListener)
        QObject.connect (comm, SIGNAL('addOutSocket_MSignal(int,int)'),  self.addOutSocket_MSignalListener)
        QObject.connect (comm, SIGNAL('deleteInSocket_MSignal(int,int)'), self.removeInSocket_MSignalListener)
        QObject.connect (comm, SIGNAL('deleteOutSocket_MSignal(int,int)'), self.removeOutSocket_MSignalListener)
    
    def tearDown (self):
        pass
    
    def addInSocket_MSignalListener (self, nid, sid):
        
        self.isAddInSocket_MSignalReceived = True
        self.receivedNId = nid
        self.receivedSId = sid
    
    def addOutSocket_MSignalListener (self, nid, sid):
        
        self.isAddOutSocket_MSignalReceived = True
        self.receivedNId = nid
        self.receivedSId = sid
    
    def removeInSocket_MSignalListener (self, nid, sid):
        
        self.isRemoveInSocket_MSignalReceived = True
        self.receivedNId = nid
        self.receivedSId = sid
    
    def removeOutSocket_MSignalListener (self, nid, sid):
        
        self.isRemoveOutSocket_MSignalReceived = True
        self.receivedNId = nid
        self.receivedSId = sid
    
    
    # In tests - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    
    def testAddInSimple (self):
        
        self.node1.addIn ('type0')
        self.assertEqual (len(self.node1.getIns()), 1, "error : something went wrong when adding the In socket")
        self.assertEqual (self.isAddInSocket_MSignalReceived, True, 'Didn''t get SIGNAL addInSocket_MSignal(int,int)')
        self.assertEqual (self.receivedSId, 1, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testAddInWithDifferentTypes (self):
        
        self.node1.addIn ('type0')
        self.node1.addIn ('type1')
        self.node1.addIn ('type2')
        self.assertEqual (len(self.node1.getIns()), 3, "error : something went wrong when adding the In socket")
        self.assertEqual (self.receivedSId, 3, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testAddInWithOneRepeatedType (self):
        
        self.node1.addIn ('type0')
        self.node1.addIn ('type1')
        self.assertEqual (self.node1.addIn ('type1'), None, 'The last addIn hasn''t be rejected as instead it was expected.')
        self.node1.addIn ('type2')
        self.assertEqual (len(self.node1.getIns()), 3, "error : something went wrong when adding the In socket")
        self.assertEqual (self.receivedSId, 3, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testRemoveInSimple (self):
        
        tmpInSocket = self.node1.addIn ('type0')
        self.node1.removeIn (tmpInSocket)
        self.assertEqual (len(self.node1.getIns()), 0, "error : something went wrong when adding the In socket")
        
        self.assertEqual (self.isRemoveInSocket_MSignalReceived, True, 'Didn''t get SIGNAL removeInSocket_MSignal(int,int)')
        self.assertEqual (self.receivedSId, 1, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testRemoveInWithDifferentTypes (self):
        
        self.node1.addIn ('type0')
        tmpInSocket = self.node1.addIn ('type1')
        self.node1.addIn ('type2')
        self.node1.removeIn (tmpInSocket) # remove the middle one
        self.assertEqual (len(self.node1.getIns()), 2, "error : something went wrong when adding the In socket")
        
        tmp_list = self.node1.getIns()
        self.assertEqual (tmp_list[0].getSType(), 'type0', 'Not the right one has been found.')
        self.assertEqual (tmp_list[1].getSType(), 'type2', 'Not the right one has been found.')
        
        self.assertEqual (self.isRemoveInSocket_MSignalReceived, True, 'Didn''t get SIGNAL removeInSocket_MSignal(int,int)')
        self.assertEqual (self.receivedSId, 2, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testGetInByType (self):
        
        self.i1 = self.node1.addIn ('type1')
        self.i2 = self.node1.addIn ('type2')
        
        self.assertTrue (self.node1.getInByType('type1'), 'unexpectedly returned False')
        self.assertTrue (self.node1.getInByType('type2'), 'unexpectedly returned False')
        self.assertFalse(self.node1.getInByType('type0'), 'unexpectedly returned True')
    
    def testGetAllInsTypes (self):
        
        self.i1 = self.node1.addIn ('type1')
        self.i2 = self.node1.addIn ('type2')
        self.i3 = self.node1.addIn ('type3')
        
        self.assertEqual (len(self.node1.getAllInsTypes()), 3, 'unexpected number of types returned')
        
    # Out tests - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    
    def testAddOutSimple (self):
        
        self.node1.addOut ('type0')
        self.assertEqual (len(self.node1.getOuts()), 1, "error : something went wrong when adding the Out socket")
        self.assertEqual (self.isAddOutSocket_MSignalReceived, True, 'Didn''t get SIGNAL addOutSocket_MSignal(int,int)')
        self.assertEqual (self.receivedSId, 1, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testAddOutWithDifferentTypes (self):
        
        self.node1.addOut ('type0')
        self.node1.addOut ('type1')
        self.node1.addOut ('type2')
        self.assertEqual (len(self.node1.getOuts()), 3, "error : something went wrong when adding the Out socket")
        self.assertEqual (self.receivedSId, 3, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testAddOutWithOneRepeatedType (self):
        
        self.node1.addOut ('type0')
        self.node1.addOut ('type1')
        self.assertEqual (self.node1.addOut ('type1'), None, 'The last addOut hasn''t be rejected as instead it was expected.')
        self.node1.addOut ('type2')
        self.assertEqual (len(self.node1.getOuts()), 3, "error : something went wrong when adding the Out socket")
        self.assertEqual (self.receivedSId, 3, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testRemoveOutSimple (self):
        
        tmpOutSocket = self.node1.addOut ('type0')
        self.node1.removeOut (tmpOutSocket)
        self.assertEqual (len(self.node1.getOuts()), 0, "error : something went wrong when adding the Out socket")
        
        self.assertEqual (self.isRemoveOutSocket_MSignalReceived, True, 'Didn''t get SIGNAL removeOutSocket_MSignal(int,int)')
        self.assertEqual (self.receivedSId, 1, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testRemoveOutWithDifferentTypes (self):
        
        self.node1.addOut ('type0')
        tmpOutSocket = self.node1.addOut ('type1')
        self.node1.addOut ('type2')
        self.node1.removeOut (tmpOutSocket) # remove the middle one
        self.assertEqual (len(self.node1.getOuts()), 2, "error : something went wrong when adding the Out socket")
        
        tmp_list = self.node1.getOuts()
        self.assertEqual (tmp_list[0].getSType(), 'type0', 'Not the right one has been found.')
        self.assertEqual (tmp_list[1].getSType(), 'type2', 'Not the right one has been found.')
        
        self.assertEqual (self.isRemoveOutSocket_MSignalReceived, True, 'Didn''t get SIGNAL removeOutSocket_MSignal(int,int)')
        self.assertEqual (self.receivedSId, 2, 'SocketId hasn''t been updated correctly')
        self.assertEqual (self.receivedNId, self.node1.getId(), 'NodeId hasn''t been updated correctly')
    
    def testGetOutByType (self):
        
        self.i1 = self.node1.addOut ('type1')
        self.i2 = self.node1.addOut ('type2')
        
        self.assertTrue (self.node1.getOutByType('type1'), 'unexpectedly returned False')
        self.assertTrue (self.node1.getOutByType('type2'), 'unexpectedly returned False')
        self.assertFalse(self.node1.getOutByType('type0'), 'unexpectedly returned True')
    
    def testGetAllOutsTypes (self):
        
        self.i1 = self.node1.addOut ('type1')
        self.i2 = self.node1.addOut ('type2')
        self.i3 = self.node1.addOut ('type3')
        
        self.assertEqual (len(self.node1.getAllOutsTypes()), 3, 'unexpected number of types returned')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
