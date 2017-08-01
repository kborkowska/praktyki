#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from weakref import ref

import sys

class View(pq.QWidget):

    def __init__(self, controler = None):
        super(View,self).__init__()
        
        self.controler = ref(controler)

        self.setSize()

        self.createMainView()

        self.show()


    def createMainView(self):
        self.setLayout(pq.QHBoxLayout())

        self.secondaryLayouts = self.createInsideLayouts(self)

        self.fillBasicStatisticPanel(self.secondaryLayouts[0])


    def fillBasicStatisticPanel(self, pane):
        mainOnOffBtn = pq.QPushButton('On')
        mainOnOffBtn.setStyleSheet('background-color:rgb(136,255,67)')
        mainOnOffBtn.setObjectName('mainOnOffBtn')
        mainOnOffBtn.clicked.connect(self.toggleOnOffBtn)

        pane().addWidget(mainOnOffBtn)

        middleLayout = pq.QGridLayout()
        labelsIn = 'Wejście','U<sub>in</sub>','I<sub>in</sub>','P<sub>in</sub>'
        labelsOut = 'Wyjście','U<sub>out</sub>','I<sub>out</sub>',\
                    'P<sub>out</sub>'
        labels = labelsIn, labelsOut
        for i in range(1,len(labels[0])+1):
            for j in range(1,len(labels[0][0])*2,2):
                print(i,j)
                middleLayout.addWidget(pq.QLabel(labels[int((j-1)/2)][i-1]),i,j)
                middleLayout.addWidget(pq.QLabel('  '),i,j+1)
        pane().addLayout(middleLayout)

        lowerLayout = pq.QGridLayout()
        labels = []
        labels = 'Info z baterii'
        for i in range(1,len(labels[0])+1):

    def createInsideLayouts(self,parent,numberOfPanes = 3):
        newLayouts = []

        for i in range(numberOfPanes):
            newLayout = pq.QVBoxLayout()
            newLayouts.append(ref(newLayout))
            parent.layout().insertLayout(i,newLayout)

        return newLayouts


    def setSize(self):
        desktopGeometry = pq.QDesktopWidget().screenGeometry()
        self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
			 desktopGeometry.width()*2/5,\
                         desktopGeometry.height()*2/5)


    def toggleOnOffBtn(self):
        sender = self.sender()

        if sender.text() == 'On':
            sender.setText('Off')
            sender.setStyleSheet('background-color:rgb(192,196,198)')
            if sender.objectName() == 'mainOnOffBtn':
                try:
                    self.controler().toggleMainPower('Off')
                except NoneType:
                    print('controler object not defined')

        elif sender.text() == 'Off':
            sender.setText('On')
            sender.setStyleSheet('background-color:rgb(136,255,67)')
            if sender.objectName() == 'mainOnOffBtn':
                try:
                    self.controler().toggleMainPower('On')
                except NoneType:
                    print('controler object not defined')

        else:
            print('error in view.toggleOnOffBtn wrong sender text')




class Controler():

    def __init__(self):
        style = pq.QStyleFactory.create('motif')
        pq.QApplication.setStyle(style)
        app = pq.QApplication(sys.argv)
        #model = Model()
        view = View(self)
        app.exec_()
        self.execteShutdown()

    def execteShutdown(self):
        sys.exit()

    def toggleMainPower(self, toggleString):
        if toggleString is 'On':
            print('turned charger on')
            #model.sendOffMainPwrMsg()
        elif toggleString is 'Off':
            print('turned charger off')
            #model.sendOnMainPwrMsg()
        else:
            print('error in controler.toggleMainPower wrong toggleString')

if __name__ == "__main__":
        sys.settrace
        con = Controler()
        sys.exit()
