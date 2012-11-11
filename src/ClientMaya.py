'''
Copyright (c) 2012 Ivano Ras, ivano.ras@gmail.com

See the file license.txt for copying permission.

JADE mapping tool - Maya client
'''

import sip
import maya.OpenMayaUI as mui
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QMainWindow, qApp

import maya.cmds as cmds

import MainViewMaya as mv
import Graph as gr



def getMayaWindow ():
    ptr = mui.MQtUtil.mainWindow ()
    return sip.wrapinstance (long(ptr), QObject)

global app
global ui

app = qApp
#app.connect (app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))

mWindow = getMayaWindow ()

ui  = mv.MainMayaWindow (gr.Graph(), mWindow)
MainWindow = QMainWindow ()
ui.setupUi (MainWindow)

#MainWindow.show ()
if (cmds.dockControl('myDock', q=1, ex=1)): cmds.deleteUI ('myDock')
allowedAreas = ['right', 'left']
myDock = cmds.dockControl('myDock', aa=allowedAreas, a='right', content='MainWindow', label='JADE mapping tool panel', w=900)