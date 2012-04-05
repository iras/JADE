'''
Created on Feb 21, 2012

@author: ivanoras
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import unittest

import Graph as gf
import Nodes0 as nd
import Sockets as sk


class TestSocket (unittest.TestCase):


    def setUp (self):
        
        self.test_graph = gf.Graph ()
        self.node1 = self.test_graph.addNode ()
        self.node2 = self.test_graph.addNode ()
        self.node3 = self.test_graph.addNode ()
        
        self.i1 = self.node1.addIn  ('type1')
        self.i2 = self.node1.addIn  ('type2')
        self.o1 = self.node2.addOut ('type1')
        self.o2 = self.node3.addOut ('type2')
    
    def tearDown (self):
        pass
    
    
    # InSocket tests - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    
    def testAddPluggedInBasic (self):
        
        self.assertTrue (self.i1.addPluggedIn (self.o1), 'unexpectedly it didn''t return True')
        self.assertTrue (self.i1.addPluggedIn (self.o2), 'unexpectedly it didn''t return True')
        self.assertEqual (len(self.i1.getPluggedIns()), 2, 'Unexpected no. of pluggedIns')
    
    def testAddPluggedInLessBasic (self):
        
        self.i3 = self.node1.addIn  ('type3')
        self.o3 = self.node2.addOut ('type3')
        self.o4 = self.node3.addOut ('type4')
        self.o5 = self.node2.addOut ('type5')
        self.o6 = self.node3.addOut ('type6')
        
        self.i1.addPluggedIn (self.o1)
        self.i1.addPluggedIn (self.o2)
        self.assertTrue (self.i1.addPluggedIn (self.o3), 'unexpectedly it didn''t return True')
        self.assertTrue (self.i3.addPluggedIn (self.o4), 'unexpectedly it didn''t return True')
        self.assertTrue (self.i3.addPluggedIn (self.o5), 'unexpectedly it didn''t return True')
        self.assertTrue (self.i2.addPluggedIn (self.o6), 'unexpectedly it didn''t return True')
        self.assertEqual (len(self.i1.getPluggedIns()), 3, 'Unexpected no. of pluggedIns')
        self.assertEqual (len(self.i2.getPluggedIns()), 1, 'Unexpected no. of pluggedIns')
        self.assertEqual (len(self.i3.getPluggedIns()), 2, 'Unexpected no. of pluggedIns')
    
    def testRemovePluggedInBasic (self):
        
        self.assertTrue  (self.i1.addPluggedIn (self.o1), 'unexpectedly it didn''t return True')
        self.i1.removePluggedIn (self.o1)
        self.assertEqual (len(self.i1.getPluggedIns()), 0, 'wrong no. of pluggedIns achieved')
        self.assertFalse (self.i1.removePluggedIn (self.o1), 'unexpected removal of empty stack happened')
    
    def testRemovePluggedInLessBasic (self):
        
        self.i3 = self.node1.addIn  ('type3')
        self.o3 = self.node2.addOut ('type3')
        self.o4 = self.node3.addOut ('type4')
        self.o5 = self.node2.addOut ('type5')
        self.o6 = self.node3.addOut ('type6')
        
        self.i1.addPluggedIn (self.o1)
        self.i1.addPluggedIn (self.o2)
        self.i3.addPluggedIn (self.o4)
        self.i3.addPluggedIn (self.o5)
        self.i2.addPluggedIn (self.o6)
        
        self.assertTrue (self.i1.removePluggedIn (self.o2), 'received wrong boolean')
        self.assertEqual (len(self.i1.getPluggedIns()), 1, 'unexpected no. of items returned.')
        self.assertTrue (self.i2.removePluggedIn (self.o6), 'received wrong boolean')
        self.assertEqual (len(self.i2.getPluggedIns()), 0, 'unexpected no. of items returned.')
        
        self.i1.addPluggedIn (self.o3)
        self.assertTrue (self.i1.removePluggedIn (self.o1), 'received wrong boolean')
        self.assertEqual (len(self.i1.getPluggedIns()), 1, 'unexpected no. of items returned.')
    
    def testIsPluggedWith_In (self):
        
        self.i1.addPluggedIn (self.o1)
        self.assertTrue (self.i1.isPluggedWith(self.o1), 'unexpectedly not plugged in with the specified socket')
        self.i1.removePluggedIn (self.o1)
        self.assertFalse (self.i1.isPluggedWith(self.o1), 'unexpectedly still plugged in with the specified socket')
    
    # OutSocket tests - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def testAddPluggedOutBasic (self):
        
        self.assertTrue (self.o1.addPluggedOut (self.i1), 'unexpectedly it didn''t return True')
        self.assertTrue (self.o1.addPluggedOut (self.i2), 'unexpectedly it didn''t return True')
        self.assertEqual (len(self.o1.getPluggedOuts()), 2, 'Unexpected no. of pluggedOuts')

    def testAddPluggedOutLessBasic (self):
        
        self.o3 = self.node1.addOut ('type3')
        self.i3 = self.node2.addIn  ('type3')
        self.i4 = self.node3.addIn  ('type4')
        self.i5 = self.node2.addIn  ('type5')
        self.i6 = self.node3.addIn  ('type6')
        
        self.o1.addPluggedOut (self.i1)
        self.o1.addPluggedOut (self.i2)
        self.assertTrue (self.o1.addPluggedOut (self.i3), 'unexpectedly it didn''t return True')
        self.assertTrue (self.o3.addPluggedOut (self.i4), 'unexpectedly it didn''t return True')
        self.assertTrue (self.o3.addPluggedOut (self.i5), 'unexpectedly it didn''t return True')
        self.assertTrue (self.o2.addPluggedOut (self.i6), 'unexpectedly it didn''t return True')
        self.assertEqual (len(self.o1.getPluggedOuts()), 3, 'Unexpected no. of pluggedOuts')
        self.assertEqual (len(self.o2.getPluggedOuts()), 1, 'Unexpected no. of pluggedOuts')
        self.assertEqual (len(self.o3.getPluggedOuts()), 2, 'Unexpected no. of pluggedOuts')
    
    def testRemovePluggedOutBasic (self):
        
        self.assertTrue  (self.o1.addPluggedOut (self.i1), 'unexpectedly it didn''t return True')
        self.o1.removePluggedOut (self.i1)
        self.assertEqual (len(self.o1.getPluggedOuts()), 0, 'wrong no. of pluggedIns achieved')
        self.assertFalse (self.o1.removePluggedOut (self.i1), 'unexpected removal of empty stack happened')
    
    def testRemovePluggedOutLessBasic (self):
        
        self.o3 = self.node1.addOut ('type3')
        self.i3 = self.node2.addIn  ('type3')
        self.i4 = self.node3.addIn  ('type4')
        self.i5 = self.node2.addIn  ('type5')
        self.i6 = self.node3.addIn  ('type6')
        
        self.o1.addPluggedOut (self.i1)
        self.o1.addPluggedOut (self.i2)
        self.o3.addPluggedOut (self.i4)
        self.o3.addPluggedOut (self.i5)
        self.o2.addPluggedOut (self.i6)
        
        self.assertTrue (self.o1.removePluggedOut (self.i2), 'received wrong boolean')
        self.assertEqual (len(self.o1.getPluggedOuts()), 1, 'unexpected no. of items returned.')
        self.assertTrue (self.o2.removePluggedOut (self.i6), 'received wrong boolean')
        self.assertEqual (len(self.o2.getPluggedOuts()), 0, 'unexpected no. of items returned.')
        
        self.o1.addPluggedOut (self.i3)
        self.assertTrue (self.o1.removePluggedOut (self.i1), 'received wrong boolean')
        self.assertEqual (len(self.o1.getPluggedOuts()), 1, 'unexpected no. of items returned.')
    
    def testIsPluggedWith_Out (self):
        
        self.o1.addPluggedOut (self.i1)
        self.assertTrue (self.o1.isPluggedWith(self.i1), 'unexpectedly not plugged in with the specified socket')
        self.o1.removePluggedOut (self.i1)
        self.assertFalse (self.o1.isPluggedWith(self.i1), 'unexpectedly still plugged in with the specified socket')

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()