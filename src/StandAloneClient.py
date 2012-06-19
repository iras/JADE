'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.
'''

'''
JADE mapping tool - Stand-alone client
'''
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication

import MainView
import Graph as gr



def main (argv):
    
    app = QApplication (argv)
    
    window = MainView.MainWindow (gr.Graph())
    window.setWindowFlags (Qt.WindowStaysOnTopHint)
    window.show ()
    
    return app.exec_()



if __name__ == "__main__":
    import sys
    sys.exit (main (sys.argv))