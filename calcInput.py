#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc

from smbus import SMBus

from weakref import ref

import sys


class View(object):
    def __init__(self):
        print('initiate View')
        self.gui = GUI()

class GUI(pq.QWidget):
    def __init__(self):
        super(GUI,self).__init__()
        print('initiate window')
        self.setSize()

        self.bus = SMBus(1)
        self.add = 0x48
        
        self.vref = 3.3
        
        btnWidth = 0.3
        btnHight = 0.4
        labelWidth = 0.2
        labelHight = 0.3
        xStartPtn = 0.05
        yStartPtn = 0.05
        
        self.createInputBtn(self,[xStartPtn,yStartPtn,btnWidth,btnHight],\
                            'Podaj napięcie',self.gatherData)
        self.createInputBtn(self,[xStartPtn+btnWidth,\
                                  yStartPtn,btnWidth,btnHight],\
                            'Wyślij sterowanie',self.sendControlVal)
        self.createInputBtn(self,[xStartPtn+btnWidth*2,\
                                  yStartPtn,btnWidth,btnHight],\
                            'Ustawienia',self.settings)

        self.createLabel(self,[xStartPtn,yStartPtn+btnHight,\
                                    labelWidth,labelHight],\
                              'textLabel',None,'Zadane napięcie:')
        self.inputLabel=self.createLabel(self,[xStartPtn+labelWidth,\
                                                    yStartPtn+btnHight,\
                                                    labelWidth,labelHight],\
                                        'inputLabel',self.gatherData,'','white')
                            
        self.createLabel(self,[0.5+xStartPtn,yStartPtn+btnHight,\
                                    labelWidth,labelHight],\
                              'vrefLabel',None,'Vref:')
        self.vrefLabel=self.createLabel(self,[0.5+xStartPtn+labelWidth,\
                                                    yStartPtn+btnHight,\
                                                   labelWidth,labelHight],\
                                          'vrefLabel',None,'3.3V','white')

        self.createInputBtn(self,[xStartPtn,yStartPtn+btnHight+labelHight,\
                                  btnWidth*3,btnHight/3],\
                            'Zakończ',self.close)
        
        self.show()

    def setSize(self):
        print('set size of a window')
        dG = pq.QDesktopWidget().screenGeometry()
        self.setGeometry(dG.width()*0.15, dG.height()*0.15,\
                         dG.width()*0.7,dG.height()*0.7)

    def createLabel(self,parent,normlizedSize,name,function = None,\
                    text='Podaj wartosc zadana',backColor = 'none'):
        inputLabel = pq.QLabel(parent)
        inputLabel.setObjectName(name)
        inputLabel.setGeometry(parent.width()*normlizedSize[0],\
                             parent.height()*normlizedSize[1],\
                             parent.width()*normlizedSize[2],\
                             parent.height()*normlizedSize[3])
        inputLabel.setText(text)
        inputLabel.setStyleSheet('background-color: '+backColor)
        if function is not None:
            inputLabel.linkActivated.connect(function)
        return ref(inputLabel)

    def createInputBtn(self,parent,normlizedSize,txt,function):
        inputBtn = pq.QPushButton(parent)
        inputBtn.setGeometry(parent.width()*normlizedSize[0],\
                             parent.height()*normlizedSize[1],\
                             parent.width()*normlizedSize[2],\
                             parent.height()*normlizedSize[3])
        inputBtn.setText(txt)
        inputBtn.released.connect(function)

    def gatherData(self):
        #ch = self.findChildren(pq.QLabel,"inputLabel")
        #ch[0].setText('yolo')
        self.createCalcPanel()

    def sendControlVal(self):
        try:
            tmp = round(self.dataToSend*256/self.vref)
            self.bus.write_byte_data(self.add,0x40,tmp)
        except:
            print('Najpierw wprowadź zadane sterowanie')

    def settings(self):
        self.settingWin = pq.QWidget()
        self.settingWin.setWindowModality(pc.Qt.ApplicationModal)
        self.settingWin.setGeometry(dG.width()*0.4, dG.height()*0.4,\
                         dG.width()*0.2,dG.height()*0.2)
        xStartPtn = 0.05
        yStartPtn = 0.1
        labelWidth = 0.4
        labelHeight = 0.8
        self.createLabel(self.settingWin,[xStartPtn,yStartPtn,\
                                          labelWidth,labelHight],'none',\
                                          None,'Vref: ')
        self.createInputBtn(self.calcWin,[xStartPtn+labelWidth,\
                                          yStartPtn,\
                                          labelWidth,labelHight],'3.3V',\
                                          self.changeVref)

    def changeVref(self):
        self.createCalcPanel()

    def createCalcPanel(self):
        self.calcWin = pq.QWidget()
        self.calcWin.setWindowModality(pc.Qt.ApplicationModal)
        dG = pq.QDesktopWidget().screenGeometry()
        btnWidth = 0.3
        btnHight = 0.15
        btnXStartPtn = 0.05
        btnYStartPtn = 0.05
        self.calcWin.setGeometry(dG.width()*0.5, dG.height()*0.10,\
                         dG.width()*0.46,dG.height()*0.46)
        self.calcInput=self.createLabel(self.calcWin,\
                                            [btnXStartPtn,btnYStartPtn,\
                                            btnWidth*3,btnHight],'calcInput',\
                                        backColor = 'white')
        
        self.createInputBtn(self.calcWin,[btnXStartPtn,btnYStartPtn+btnHight,\
                                          btnWidth,btnHight],'7',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
                                          btnYStartPtn+btnHight,\
                                          btnWidth,btnHight],'8',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
                                          btnYStartPtn+btnHight,\
                                          btnWidth,btnHight],'9',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn,\
                                          btnYStartPtn+btnHight*2,\
                                          btnWidth,btnHight],'4',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
                                          btnYStartPtn+btnHight*2,\
                                          btnWidth,btnHight],'5',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
                                          btnYStartPtn+btnHight*2,\
                                          btnWidth,btnHight],'6',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn,\
                                          btnYStartPtn+btnHight*3,
                                          btnWidth,btnHight],'1',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
                                          btnYStartPtn+btnHight*3,\
                                          btnWidth,btnHight],'2',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
                                          btnYStartPtn+btnHight*3,\
                                          btnWidth,btnHight],'3',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn,\
                                          btnYStartPtn+btnHight*4,\
                                          btnWidth,btnHight],'0',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
                                          btnYStartPtn+btnHight*4,\
                                          btnWidth,btnHight],'.',\
                                          self.addANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
                                          btnYStartPtn+btnHight*4,\
                                          btnWidth,btnHight],'del',\
                                          self.deleteANumber)
        self.createInputBtn(self.calcWin,[btnXStartPtn,\
                                          btnYStartPtn+btnHight*5,\
                                          btnWidth*3,btnHight],'Zatwierdz',\
                                          self.closeCalcWin)
        self.calcWin.show()


    def deleteANumber(self):
        if self.calcInput().text() != 'Podaj wartosc zadana':
            self.calcInput().setText(self.calcInput().text()\
                                     [0:len(self.calcInput().text())-1])

    def addANumber(self):
        if self.calcInput().text() != 'Podaj wartosc zadana':
            self.calcInput().setText(self.calcInput().text()+self.sender().text())
        else:
            self.calcInput().setText(self.sender().text())

    def closeCalcWin(self):
        self.dataToSend = float(self.calcInput().text())
        self.calcWin.close()
        self.inputLabel().setText(str(self.dataToSend))


if __name__=="__main__":
    print('change app style')
    pq.QApplication.setStyle(pq.QStyleFactory.create("motif"))
    print('create app')
    app = pq.QApplication(sys.argv)
    view = View()
    print('start main app loop')
    app.exec_()
    print('close app')
    sys.exit()
