#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
#from PyQt4.QtCore import Qt as pcq

from numpy import array
from numpy import ndarray

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

        self.chosenModule = 1

        self.secondaryLayouts = self.createInsideLayouts(self, grid = True,\
                                                         gridIdx = 1)

        self.createBasicStatisticPanel(self.secondaryLayouts[0])
        self.createModulePanel(self.secondaryLayouts[1])
        self.createModuleTabs(self.secondaryLayouts[2])

    def createModuleTabs(self,pane):
        numberOfModules = self.controler().getNumberOfModules()
        for i in range(numberOfModules):
            moduleTabBtn = pq.QPushButton('Modol '+str(i+1))
            if i == self.chosenModule-1:
                moduleTabBtn.setStyleSheet('background-color:'+\
                                                'rgb(204,253,139)')
            else:
                moduleTabBtn.setStyleSheet('background-color:'+\
                                                 'rgb(233,255,202)')
            moduleTabBtn.setFlat(True)
            moduleTabBtn.setObjectName('Modol_'+str(i+1)+'_Btn')
            moduleTabBtn.clicked.connect(self.changeModuleTab)
            pane().addWidget(moduleTabBtn)

    def changeModuleTab(self):
        sender = self.sender()
        senderName = sender.objectName()
        senderNumber = senderName.split('_')[1]

        if self.chosenModule != senderNumber:
            self.findChild(pq.QPushButton,\
                           'Modol_'+str(self.chosenModule)+'_Btn').\
                        setStyleSheet('background-color:rgb(233,255,202)')
            self.findChild(pq.QPushButton,\
                           'Modol_'+str(senderNumber)+'_Btn').\
                        setStyleSheet('background-color:rgb(204,253,139)')
            self.changeModulePanelInfo(senderNumber)
            self.chosenModule = senderNumber
    

    def changeModulePanelInfo(self,senderNumber):
        self.findChild(pq.QLabel,'chosenModelLabel').setText('Modol nr. '+\
                                                   str(senderNumber))

                
        

    def createModulePanel(self, pane): 
        label = pq.QLabel('Modol nr. '+str(self.chosenModule))
        label.setObjectName('chosenModelLabel')
        pane().addWidget(label,1,1)

        moduleOnOffBtn = pq.QPushButton('On')
        moduleOnOffBtn.setStyleSheet('background-color:rgb(136,255,67)')
        moduleOnOffBtn.setObjectName('moduleOnOffBtn')
        moduleOnOffBtn.clicked.connect(self.toggleOnOffBtn)
        pane().addWidget(moduleOnOffBtn,1,2)

        labels = self.labelsIn, self.labelsOut
        pane().addLayout(self.createInfoGrid(labels,True),2,1)

        labels = 'Awarie:'
        pane().addLayout(self.createInfoGrid(labels),2,2)

        labels = 'Temperatura:','Temp1', 'Temp2', 'Temp3'
        pane().addLayout(self.createInfoGrid(labels),3,1)

        labels = 'Zadane:','U', 'I'
        pane().addLayout(self.createInfoGrid(labels),3,2)

        pane().addWidget(pq.QLabel('Tryb pracy:'),4,1)
        value = pq.QLabel('napieciowy')
        #value.setStyleSheet('background-color:rgb(255,255,255)')
        value.setMargin(4)
        value.setObjectName = 'Tryb pracy'
        pane().addWidget(value,4,2)


    def createBasicStatisticPanel(self, pane):
        mainOnOffBtn = pq.QPushButton('On')
        mainOnOffBtn.setStyleSheet('background-color:rgb(136,255,67)')
        mainOnOffBtn.setObjectName('mainOnOffBtn')
        mainOnOffBtn.clicked.connect(self.toggleOnOffBtn)

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
                value.setStyleSheet('background-color:rgb(255,255,255)')
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
                    value.setStyleSheet('background-color:rgb(255,255,255)')
                    value.setMargin(4)
                    value.setObjectName = labelsArray[int((j-1)/2)][i-1]\
                                          +moduleStr
                    layout.addWidget(value,i,j+1)

        return layout

    def createInsideLayouts(self,parent,numberOfPanes = 3, grid = False,\
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
                else:
                    newLayout = pq.QGridLayout()
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
            elif sender.objectName() == 'moduleOnOffBtn':
                try:
                    self.controler().toggleModulePower('Off',self.chosenModule)
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
            elif sender.objectName() == 'moduleOnOffBtn':
                try:
                    self.controler().toggleModulePower('On',self.chosenModule)
                except NoneType:
                    print('controler object not defined')

        else:
            print('error in view.toggleOnOffBtn wrong sender text')


class Model():

    def __init__(self):
        self.configureModules()

    def configureModules(self):
        self.numberOfModules = 4

    def getNumberOfModules(self):
        return self.numberOfModules
    
    def turnOffModulePwrMsg(self,chosenModule):
        self.sendOffModulePwrMsg(chosenModule)

    def turnOnModulePwrMsg(self,chosenModule):
        self.sendOnModulePwrMsg(chosenModule)

    def turnOffMainPwrMsg(self):
        self.sendOffMainPwrMsg()

    def turnOnMainPwrMsg(self):
        self.sendOnMainPwrMsg()

    def sendOffModulePwrMsg(self,chosenModule):
        print('turned module no.'+str(chosenModule)+' off')

    def sendOnModulePwrMsg(self,chosenModule):
        print('turned module no.'+str(chosenModule)+' on')

    def sendOffMainPwrMsg(self):
        print('turned charger off')

    def sendOnMainPwrMsg(self):
        print('turned charger on')

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

    def toggleModulePower(self, toggleString, chosenModule):
        if toggleString is 'On':
            self.model.turnOnModulePwrMsg(chosenModule)
        elif toggleString is 'Off':
            self.model.turnOffModulePwrMsg(chosenModule)
        else:
            print('error in controler.toggleMainPower wrong toggleString')

    def toggleMainPower(self, toggleString):
        if toggleString is 'On':
            self.model.turnOnMainPwrMsg()
        elif toggleString is 'Off':
            self.model.turnOffMainPwrMsg()
        else:
            print('error in controler.toggleMainPower wrong toggleString')

if __name__ == "__main__":
        sys.settrace
        con = Controler()
