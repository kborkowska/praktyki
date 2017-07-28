#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from threading import Timer

from datetime import datetime as dt

from numpy import array, append
import numpy as np

import pyqtgraph as pg

from random import randint

from smbus import SMBus

from weakref import ref

import sys

'''

Prototyp GUI do oprogramowania panelu operatorskiego do zadawania
i odbierania sygnalow ukladow przeksztaltnikowych.

Wesja do wprowadzania zmian i nowych funkcjonalnosci.

Wesja rozowa.

'''


class RepeatedTimer():

        def __init__(self, interval, function, *args, **kwargs):
                self._timer     = None
                self.interval   = interval
                self.function   = function
                self.args       = args
                self.kwargs     = kwargs
                self.is_running = False
                self.start()

        def _run(self):
                self.is_running = False
                self.start()
                self.function(*self.args, **self.kwargs)

        def start(self):
                if not self.is_running:
                        self._timer = Timer(self.interval, self._run)
                        self._timer.start()
                        self.is_running = True

        def stop(self):
                self._timer.cancel()
                self.is_running = False

class TimeAxisItem(pg.AxisItem):

        def __init__(self, *args, **kwargs):
                super(TimeAxisItem,self).__init__(*args, **kwargs)

        def tickStrings(self, values, scale, spacing):
                strings = []
                for i in values:
                        strings.append(self.timeToString(i))
                return strings

        def timeToString(self,milsecs):
                hurs = int(milsecs/3600000)
                milsecs -= hurs*3600000
                mins = int(milsecs/60000)
                milsecs -= mins*60000
                secs = int(milsecs/1000)
                milsecs -= secs*1000

                string = str(hurs)+":"+str(mins)+":"+str(secs)#+"."+str(int(milsecs/100))

                return string

class GUI(pq.QWidget):

        def __init__(self, controler):
                super(GUI,self).__init__()

                self.controlerRef = ref(controler)

                self.setSize()

                self.insidePane = ref(pq.QWidget(self))

                layout = pq.QGridLayout()
                insideLayout = pq.QHBoxLayout()

                self.insidePane().setLayout(insideLayout)
                self.setLayout(layout)

                self.maxX = 100
                #self.createInitialdata()

                self.createGraph()
                self.createSlider(1, 0, 10)
                self.createLabeledInputBoxes(self.insidePane())

                layout.addWidget(self.slider(), 1 , 2)
                layout.addWidget(self.insidePane(), 2 , 1)

                self.show()



        def finish(self):
                print('out. for. a. walk.')


        def getMaxX(self):
                return self.maxX


        def createLabeledInputBoxes(self, parent):
                firstLine = pq.QLineEdit(parent)
                firstLabel = pq.QLabel("first:",parent)
                parent.layout().addWidget(firstLabel)
                parent.layout().addWidget(firstLine)
                #self.firstLine.resize((self.width()-self.sliderWidth)*0.4,self.height()*0.15)

                secondLine = pq.QLineEdit(parent)
                secondLabel = pq.QLabel("second:",parent)
                parent.layout().addWidget(secondLabel)
                parent.layout().addWidget(secondLine)
                #self.secondLine.resize((self.width()-self.sliderWidth)*0.4,self.height()*0.15)


        def setSize(self):
                self.sliderWidth = 40

                desktopGeometry = pq.QDesktopWidget().screenGeometry()
                self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
				desktopGeometry.width()*2/5,\
                                 desktopGeometry.height()*2/5)



        def createGraph(self):
                graph = pg.PlotWidget(self, background =(217,217,222,255),\
					axisItems={'bottom': TimeAxisItem(\
                                                        orientation='bottom',\
                                                        pen=pg.mkPen(color = \
                                                        (255,9,215,255),\
                                                        width=2)),
					    	    'left': pg.AxisItem(\
                                                        orientation='left',\
                                                        pen=pg.mkPen(color = \
                                                        (255,9,215,255),\
                                                        width=2))})
                dataX,dataY = self.controlerRef().createInitialdata(self.maxX)
                self.g = ref(graph.plot(dataX,dataY,\
				pen=pg.mkPen(color = \
                                (255,9,215,255),width=3.5)))
                graph.resize(self.width()-self.sliderWidth,\
                             self.height()-self.height()*0.15)
                self.layout().addWidget(graph, 1, 1)



        def createSlider(self, tickInterval, minimum, maximum):
                self.slider = ref(pq.QSlider(pcq.Vertical,self))

                self.slider().setTickInterval(tickInterval)
                self.slider().setMinimum(minimum)
                self.slider().setMaximum(maximum)

                self.slider().setTickPosition(pq.QSlider.TicksLeft)

                #self.slider.valueChanged.connect(self.updateGraph)

                self.slider().resize(self.sliderWidth,\
                                   self.height()-self.height()*0.15)



        def updateGraph(self):
                dataX,dataY = self.appendData(self.sender().value())
                self.g().setData(dataX,dataY)



        def updateGraphExternally(self,x,y):
                dataX,dataY = self.appendData(x,y)
                self.g().setData(dataX,dataY)


        def appendData(self, x, y):

                dataX,dataY = self.g().getData()

                if dataY.size < self.maxX:
                        dataY = append(dataY,y)
                        dataX = append(dataX,x)
                else:
                        dataY = append(dataY[1:self.maxX],y)
                        dataX = append(dataX[1:self.maxX],x)

                return list(dataX),list(dataY)


class Model(object):
        def __init__(self):
                self.bus = SMBus(1)
                self.addr = 0x48
                self.bus.write_byte(self.addr,0x00)

        def gatherData(self):
                return self.bus.read_byte(self.addr)


class Controler(object):

        def __init__(self):
                style = pq.QStyleFactory.create("motif")
                pq.QApplication.setStyle(style)
                app = pq.QApplication(sys.argv)
                self.openDataFile()
                self.model = Model()
                self.gui = GUI(self)
                #print(gc.get_objects())
                self.timer = RepeatedTimer(0.1, self.updateView)
                #timer = RepeatedTimer(0.1,prT)
                app.exec_()
                self.execteShutdown()


        def execteShutdown(self):
                self.gui.finish()
                self.timer.stop()
                self.closeDataFile()
                del self.gui



        def updateView(self):
                currTime = dt.now()

                x = (currTime.hour*3600+currTime.minute*60+\
                     currTime.second)*1000+int(currTime.microsecond/1000)
                y = self.model.gatherData()

                self.gui.updateGraphExternally(x,y)

                self.saveData(currTime,y)


        def openDataFile(self):
                currTime = dt.now()
                self.file = open('Dane_{when}.txt'.\
                                format(when=currTime.\
                                strftime('%d_%b_%y_%H:%M')), 'w')

        def closeDataFile(self):
                self.file.close()


        def saveData(self, currTime, dataY):
                self.file.write('time: {time}\t data: {data}\n'.\
                                format(time = currTime.\
                                strftime('%H:%M:%S.%f')[:-3], data = dataY))

        def createInitialTimeData(self,initTime):
                currTime = dt.now()
                times = []

                for i in range(initTime-1,-1,-1):
                        times.append(self.timeRevind(i,currTime))

                return times

        def createInitialdata(self,maxX):
                dataX = self.createInitialTimeData(maxX)
                dataY = np.zeros((maxX,), dtype=np.int)
                return list(dataX),list(dataY)


        def timeRevind(self,offsetTime, currTime):
                tim = currTime.hour*3600+currTime.minute*60+currTime.second
                tim -= offsetTime
                tim = tim*1000+int(currTime.microsecond/1000)
                return tim

        def timeRevindFromString(self,offsetTime, currTime):
                secs = int(currTime[6:8])+int(currTime[3:5])*60+\
                       int(currTime[0:2])*3600
                secs -= offsetTime
                return secs


def prT():
        print(' ')

if __name__ == "__main__":
        sys.settrace
        con = Controler()
        sys.exit()

