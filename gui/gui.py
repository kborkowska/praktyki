#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
#from PyQt4.QtCore import Qt as pcq

from numpy import array
from numpy import ndarray
from numpy import append

from weakref import ref

import sys    

class Controler():

    def __init__(self):
        #style = pq.QStyleFactory.create('motif')
        #pq.QApplication.setStyle(style)
        app = pq.QApplication(sys.argv)
        self.model = Model()
        self.view = View(self)
        app.exec_()
        self.execteShutdown()

    def getNumberOfModules(self):
        return self.model.getNumberOfModules()

    def execteShutdown(self):
        sys.exit()

    def getComponentMemebers(self, component):
        

    def toggleModulePower(self, toggleString, selectedModule):
        if toggleString is 'On':
            self.model.turnOnModulePwr(selectedModule)
        elif toggleString is 'Off':
            self.model.turnOffModulePwr(selectedModule)
        else:
            print('error in controler.toggleMainPower wrong toggleString')

    def toggleMainPower(self, toggleString):
        if toggleString is 'On':
            self.model.turnOnMainPwr()
        elif toggleString is 'Off':
            self.model.turnOffMainPwr()
        else:
            print('error in controler.toggleMainPower wrong toggleString')

if __name__ == "__main__":
        #sys.settrace
        con = Controler()
