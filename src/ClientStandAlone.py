'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool - Standalone client
'''

from PyQt4.QtCore import Qt, QCoreApplication
from PyQt4.QtGui import QApplication

import MainView
import Graph as gr


# PyQt automatically swaps the key Ctrl with the Meta (Command) key when in Mac OS X. The line below should stop the swapping BUT it doesn't seem to work on the MacBookPro (Lion) although the attribute gets set to True correctly.
QCoreApplication.setAttribute (Qt.AA_MacDontSwapCtrlAndMeta, True)
#print QCoreApplication.testAttribute (Qt.AA_MacDontSwapCtrlAndMeta) # test the line above.


def main (argv):
    
    app = QApplication (argv)
    app.setAttribute (Qt.AA_DontUseNativeMenuBar)
    app.setAttribute (Qt.AA_MacDontSwapCtrlAndMeta) # this one doesn't seem to work, at least on the MacBookPro (Lion)
    
    window = MainView.MainWindow (gr.Graph())
    window.setWindowFlags (Qt.WindowStaysOnTopHint)
    window.show ()
    
    return app.exec_()


if __name__ == "__main__":
    import sys
    sys.exit (main (sys.argv))