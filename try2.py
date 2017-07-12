#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from threading import Timer

from datetime import datetime as dt

from numpy import array, append
import numpy as np

import pyqtgraph as pg

import random

import sys

'''

Prototyp GUI do oprogramowania panelu operatorskiego do zadawania
i odbierania sygnałów układów przeksztaltnikowych.

Wesja do wprowadzania zmian i nowych funkcjonalności.

Wesja różowa.

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
		super().__init__(*args, **kwargs)

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

	def __init__(self):
		super(GUI,self).__init__()

		self.setSize()

		self.insidePane = pq.QWidget(self)

		self.layout = pq.QGridLayout()
		self.insideLayout = pq.QHBoxLayout()

		self.insidePane.setLayout(self.insideLayout)

		self.maxX = 100
		self.createInitialdata()

		self.createGraph()
		self.createSlider(1, 0, 10)
		self.createLabeledInputBoxes(self.insidePane)

		self.layout.addWidget(self.graph, 1, 1)
		self.layout.addWidget(self.slider, 1 , 2)
		self.layout.addWidget(self.insidePane, 2 , 1)

		self.setLayout(self.layout)

		self.openDataFile()

		self.show()



	def __del__(self):
		self.closeDataFile()

	
	def closeDataFile(self):
		self.file.close()



	def openDataFile(self):
		currTime = dt.now()
		self.file = open('Dane_{when}.txt'.format(when=currTime.strftime('%d_%b_%y_%H:%M')), 'w')


	def createLabeledInputBoxes(self, parent):
		self.firstLine = pq.QLineEdit(parent)
		firstLabel = pq.QLabel("first:",parent)
		parent.layout().addWidget(firstLabel)
		parent.layout().addWidget(self.firstLine)
		#self.firstLine.resize((self.width()-self.sw)*0.4,self.height()*0.15)

		self.secondLine = pq.QLineEdit(parent)
		secondLabel = pq.QLabel("second:",parent)
		self.insideLayout.addWidget(secondLabel)
		self.insideLayout.addWidget(self.secondLine)
		#self.secondLine.resize((self.width()-self.sw)*0.4,self.height()*0.15)


	def setSize(self):
		self.sw = 40

		desktopGeometry = pq.QDesktopWidget().screenGeometry()
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
				desktopGeometry.width()*2/5, desktopGeometry.height()*2/5)



	def createGraph(self):
		self.graph = pg.PlotWidget(self, background =(217,217,222,255),\
					axisItems={'bottom': TimeAxisItem(orientation='bottom',\
					                     pen=pg.mkPen(color = (255,9,215,255),\
							     width=2)),\
					    	    'left': pg.AxisItem(orientation='left',\
					    		    pen=pg.mkPen(color = (255,9,215,255),\
							    width=2))})
		self.g = self.graph.plot(list(self.dataX),list(self.dataY),\
				pen=pg.mkPen(color = (255,9,215,255),width=3.5))
		self.graph.resize(self.width()-self.sw,self.height()-self.height()*0.15)



	def createSlider(self, tickInterval, minimum, maximum):
		self.slider = pq.QSlider(pcq.Vertical,self)

		self.slider.setTickInterval(tickInterval)
		self.slider.setMinimum(minimum)
		self.slider.setMaximum(maximum)

		self.slider.setTickPosition(pq.QSlider.TicksLeft)

		self.slider.valueChanged.connect(self.updateGraph)

		self.slider.resize(self.sw,self.height()-self.height()*0.15)
	


	def updateGraph(self):
		self.appendData(self.sender().value())
		self.g.setData(list(self.dataX),list(self.dataY))
	


	def updateGraphExternaly(self):
		self.appendData()
		self.g.setData(list(self.dataX),list(self.dataY))



	def createInitialdata(self):
		self.dataX = self.createInitialTimeData(self.maxX)
		self.dataY = np.zeros((self.maxX,), dtype=np.int)



	def appendData(self, y):
		currTime = dt.now()

		if self.dataY.size < self.maxX: 
			self.dataY = append(self.dataY,y)
			self.dataX = append(self.dataX,(currTime.hour*3600+\
						currTime.minute*60+currTime.second)*1000+\
						int(currTime.microsecond/1000))
		else:
			self.dataY = append(self.dataY[1:self.maxX],y)
			self.dataX = append(self.dataX[1:self.maxX],(currTime.hour*3600+\
						currTime.minute*60+currTime.second)*1000+\
						int(currTime.microsecond/1000))

		self.saveData(currTime, y)



	def appendData(self):
		currTime = dt.now()
		y=random.randint(0,100)

		if self.dataY.size < self.maxX: 
			self.dataY = append(self.dataY,y)
			self.dataX = append(self.dataX,(currTime.hour*3600+\
						currTime.minute*60+currTime.second)*1000+\
						int(currTime.microsecond/1000))
		else:
			self.dataY = append(self.dataY[1:self.maxX],y)
			self.dataX = append(self.dataX[1:self.maxX],(currTime.hour*3600+\
						currTime.minute*60+currTime.second)*1000+\
						int(currTime.microsecond/1000))

		self.saveData(currTime, y)



	def saveData(self, currTime, dataY):
		self.file.write('time: {time}\t data: {data}\n'.format(\
				time = currTime.strftime('%H:%M:%S.%f')[:-3], data = dataY))


	def createInitialTimeData(self,initTime):
		currTime = dt.now()
		times = []

		for i in range(initTime-1,-1,-1):
			times.append(self.timeRevind(i,currTime))

		return times



	def timeRevind(self,offsetTime, currTime):
		tim = currTime.hour*3600+currTime.minute*60+currTime.second
		tim -= offsetTime
		tim = tim*1000+int(currTime.microsecond/1000)
		return tim



	def timeRevindFromString(self,offsetTime, currTime):
		secs = int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600
		secs -= offsetTime
		return secs
		


if __name__ == "__main__":
	style = pq.QStyleFactory.create("motif")
	pq.QApplication.setStyle(style)
	app = pq.QApplication(sys.argv)
	gui = GUI()
	timer = RepeatedTimer(0.1, gui.updateGraphExternaly)
	app.exec_()
	timer.stop()
	del gui
	sys.exit()

