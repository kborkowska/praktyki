#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
#from PyQt4.QtCore import Qt as pcq

from numpy import array
from numpy import ndarray
from numpy import append

from weakref import ref


class View(pq.QWidget):

    def __init__(self, controler):
        super(View,self).__init__()

        self.controler = ref(controler)

        self.setSize()

        self.initiateColours()

        self.createAndShowGUI()



    def createAndShowGUI(self):
        self.setLayout(pq.QHBoxLayout())

        self.secondaryLayouts = self.createInsideLayouts(self, grid = True,\
                                                               gridIdx = 1)

        self.createBasicStatisticPanel(self.secondaryLayouts[0])

        self.show()

    def createBasicStatisticPanel(self, pane):
        mainOnOffBtn = pq.QPushButton('On')
        mainOnOffBtn.setStyleSheet('background-color:'+self.onBtnColor)
        mainOnOffBtn.setObjectName('mainOnOffBtn')
        #mainOnOffBtn.clicked.connect(self.toggleOnOffBtn)

        pane().addWidget(mainOnOffBtn)

        self.labelsIn = 'Wejście','U<sub>in</sub>','I<sub>in</sub>','P<sub>in</sub>'
        self.labelsOut = 'Wyjście','U<sub>out</sub>','I<sub>out</sub>',\
                    'P<sub>out</sub>'
        labels = self.labelsIn, self.labelsOut
        pane().addLayout(self.createInfoGrid(labels))

        labels = []
        labels = 'Info z baterii'
        pane().addLayout(self.createInfoGrid(labels))


    def createInfoGrid(self, labels, module = False):
        labelsArray = array(labels)
        layout = pq.QGridLayout()

        #print(labelsArray.shape)
        
        try:
            numberOfCollumns = labelsArray.shape[0]
            if numberOfCollumns < 1:
                print('no labels to add')
                return -1
        except IndexError:
            labelsArray = array([labels])
            numberOfCollumns = 1

        try:
            numberOfRows = labelsArray.shape[1]
        except IndexError:
            numberOfRows = 1

        moduleStr = ''
        if module:
            moduleStr = '_module'

        if numberOfRows == 1 and numberOfCollumns == 1:
            layout.addWidget(pq.QLabel(labelsArray[0]),1,1)
        elif numberOfRows == 1:
            layout.addWidget(pq.QLabel(labelsArray[0]),1,1)
            for i in range(2,numberOfCollumns+1):
                #print(i,j)
                layout.addWidget(pq.QLabel(labelsArray[i-1]),i,1)
                value = pq.QLabel('  ')
                value.setStyleSheet('background-color:'+self.valueLabel)
                value.setMargin(4)
                value.setObjectName = labelsArray[i-1]+moduleStr
                layout.addWidget(value,i,2)
        else:
            for i in range(1,numberOfCollumns*2,2):
                layout.addWidget(pq.QLabel(labelsArray[int((i-1)/2)][0]),1,i)

            for i in range(2,numberOfRows+1):
                for j in range(1,numberOfCollumns*2,2):
                    #print(i,j)
                    layout.addWidget(pq.QLabel(labelsArray[int((j-1)/2)][i-1]),\
                                     i,j)
                    value = pq.QLabel('  ')
                    value.setStyleSheet('background-color:'+self.valueLabel)
                    value.setMargin(4)
                    value.setObjectName = labelsArray[int((j-1)/2)][i-1]\
                                          +moduleStr
                    layout.addWidget(value,i,j+1)

        return layout

    def createInsideLayouts(self, parent, numberOfPanes = 3, grid = False,\
                            gridIdx = -1):
        newLayouts = []

        if not isinstance(gridIdx,(list,int)):
            print('wrong type of gridIdx')
            return -1

        if type(gridIdx) is int:
            gridIdx = [gridIdx]

        if not grid:
            for i in range(numberOfPanes):
                newLayout = pq.QVBoxLayout()
                newLayouts.append(ref(newLayout))
                parent.layout().insertLayout(i,newLayout)
        else:
            for i in range(numberOfPanes):
                if not i in gridIdx:
                    newLayout = pq.QVBoxLayout()
                    parent.layout().insertLayout(i,newLayout)
                else:
                    newLayout = pq.QGridLayout()
                    colorWidget = pq.QWidget()
                    parent.layout().insertWidget(i,colorWidget)
                    colorWidget.setStyleSheet(\
                        'background-color:'+self.selectedComponentColor)
                    colorWidget.setLayout(newLayout)
                newLayouts.append(ref(newLayout))

        return newLayouts

    def initiateColours(self):
        
        self.selectedComponentColor = 'rgb(255,255,247)'
        self.workingComponentColor = 'rgb(233,255,202)'
        self.shutoffComponentColor = 'rgb(233,255,202)'
        self.alarmComponentColor = 'rgb(252,77,42)'

        self.onBtnColor = 'rgb(136,255,67)'
        self.offBtnColor = 'rgb(192,196,198)'

        self.valueLabel = 'rgb(255,255,255)'
        
        
    def setSize(self):
        desktopGeometry = pq.QDesktopWidget().screenGeometry()
        self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
			 desktopGeometry.width()*3/5,\
                         desktopGeometry.height()*3/5)
