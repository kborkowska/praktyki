#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq
from time import strftime
from datetime import datetime as dt
from numpy import array, append
import numpy as np
import pyqtgraph as pg

import sys

class timeAxisItem(pg.AxisItem):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#print("jestem tu i nic nie pokzauje bo mam Cie w poważaniu")
		#super.setStyle(textFillLimits = [(2,0.3)])

	def tickStrings(self, values, scale, spacing):
		strings = []
		#print("values:")
		#print(values)
		for i in values:
			strings.append(self.timeToString(i))
		#print("strings:")
		#print(strings)
		return strings

	def timeToString(self,milsecs):
		hurs = int(milsecs/3600000)
		milsecs -= hurs*3600000
		mins = int(milsecs/60000)
		milsecs -= mins*60000
		secs = int(milsecs/1000)
		milsecs -= secs*1000
		string = str(hurs)+":"+str(mins)+":"+str(secs)+":"+str(int(milsecs))
		return string

class GUI(pq.QWidget):

	def __init__(self):
		super(GUI,self).__init__()
		self.setSize()
		self.layout = pq.QHBoxLayout()
		#self.layout.addStretch(0)
		self.createInitialdata()
		self.createSlider(1, 0, 10)
		self.createGraph()
		self.layout.addWidget(self.graph)
		self.layout.addWidget(self.slider)
		self.setLayout(self.layout)
		self.show()

	def createGraph(self):
		self.maxX = 10 #10 for debugging purposes
		self.graph = pg.PlotWidget(self,axisItems={'bottom': timeAxisItem(orientation='bottom',pen=pg.mkPen(color = (255,9,215,255),width=2)), 'left': pg.AxisItem(orientation='left',pen=pg.mkPen(color = (255,9,215,255),width=2))}, background =(217,217,222,255))
		
		#aI = pg.AxisItem(orientation='bottom')
		self.g = self.graph.plot(list(self.dataX),list(self.dataY), pen=pg.mkPen(color = (255,9,215,255),width=3.5))
		#self.graph.setGeometry(0,0,self.width()-self.sw,self.height())
		self.graph.resize(self.width()-self.sw,self.height())

	def setSize(self):
		desktop = pq.QDesktopWidget()
		desktopGeometry = desktop.screenGeometry()
		self.sw = 40
		w = desktopGeometry.width()*2/5
		h = desktopGeometry.height()*2/5
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(), w, h)

	def setAndShowSize(self):
		desktop = pq.QDesktopWidget()
		desktopGeometry = desktop.screenGeometry()
		w = desktopGeometry.width()*2/5
		h = desktopGeometry.height()*2/5
		#showSize used only for debugging purposes
		self.showSize(desktopGeometry.x(), desktopGeometry.y(), desktopGeometry.width(), desktopGeometry.height(), "desktop", 20,20)
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(), w, h)
		self.showSize(desktopGeometry.x(), desktopGeometry.y(), "app", 20,50)

	#showSize used only for debugging purposes
	def showSize(self, x,y, name, sx, sy):
		qStr = name+" geometry: x="+str(x)+", y="+str(y)+", w="+str(self.w)+", h="+str(self.h)
		print(qStr)
		geometryLabel = pq.QLabel(self)
		geometryLabel.setText(qStr)
		geometryLabel.move(sx,sy)

	def createSlider(self, tickInterval, minimum, maximum):
		self.slider = pq.QSlider(pcq.Vertical,self)
		self.slider.setTickInterval(tickInterval)
		self.slider.setMinimum(minimum)
		self.slider.setMaximum(maximum)
		#slider.setTrackig(True)
		self.slider.setTickPosition(pq.QSlider.TicksLeft)
		#self.slider.setGeometry(self.width()-self.sw+self.geometry().x(),self.geometry().y(),self.sw,self.height())
		self.slider.valueChanged.connect(self.updateGraph)
		#slider.setStyleSheet()
		self.slider.resize(self.sw,self.height())
	
	def updateGraph(self):
		self.appenddata(self.sender().value())
		#self.graph.clear()
		#self.graph.plot(self.dataY)
		self.g.setData(list(self.dataX),list(self.dataY))

	def createInitialdata(self):
		noOfFakeData = 5
		self.dataX = self.createInitialTimeData(noOfFakeData)
		self.dataY = np.zeros((noOfFakeData,), dtype=np.int)

	def appenddata(self, x):
		#currTime = strftime("%H:%M:%S.%f")
		currTime = dt.now()
		if self.dataY.size < self.maxX: 
			self.dataY = append(self.dataY,x)
			#self.dataX = append(self.dataX,int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600)
			self.dataX = append(self.dataX,(currTime.hour*3600+currTime.minute*60+currTime.second)*1000+int(currTime.microsecond/1000))
		else:
			self.dataY = append(self.dataY[1:self.maxX],x)
			#self.dataX = append(self.dataX[1:self.maxX],int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600)
			self.dataX = append(self.dataX[1:self.maxX],(currTime.hour*3600+currTime.minute*60+currTime.second)*1000+int(currTime.microsecond/1000))
		#print(self.dataY)

	def createInitialTimeData(self,initTime):
		#currTime = strftime("%H:%M:%S.%f")
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
		#self.strings = []
		secs = int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600
		secs -= offsetTime
		return secs
		

if __name__ == "__main__":
	style = pq.QStyleFactory.create("motif")
	pq.QApplication.setStyle(style)
	app = pq.QApplication(sys.argv)
	gui = GUI()
	app.exec_()
	del gui
	sys.exit()

