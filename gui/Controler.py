#!/usr/bin/env python3

from PyQt4.QtGui import QApplication

from numpy import array
from numpy import ndarray
from numpy import append

from weakref import ref

import sys

from Model import Model
from View import View

class Controler():

    def __init__(self):
        #style = pq.QStyleFactory.create('motif')
        #pq.QApplication.setStyle(style)
        app = QApplication(sys.argv)
        self.model = Model()
        self.view = View(self)
        app.exec_()
        self.execteShutdown()

    def execteShutdown(self):
        sys.exit()

if __name__ == "__main__":
        #sys.settrace
        con = Controler()
