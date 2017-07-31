#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from weakref import ref

class View(pq.QWidget):

    def __init__(self, controlerRef = None):
        super(GUI,self).__init__()
        
        self.controlerRef = controlerRef

        self.setSize()

        self.createMainLayout()


    def createMainLayout():
        self.mainLayout = pq.QHBoxLayout()

        self.createInsidePanes(3)

    def createInsidePanes(numberOfPanes = 3)
        for in range(numberOfPanes)

    def setSize(self):
        desktopGeometry = pq.QDesktopWidget().screenGeometry()
        self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
			 desktopGeometry.width()*2/5,\
                         desktopGeometry.height()*2/5)

class Controler():

    def __init__(self):
        style = pq.QStyleFactory.create("motif")
        pq.QApplication.setStyle(style)
        app = pq.QApplication(sys.argv)
        view = View()
        app.exec_()
        self.execteShutdown()

    def execteShutdown(self):
        sys.exit()

if __name__ == "__main__":
        sys.settrace
        con = Controler()
        sys.exit()
