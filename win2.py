#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq
from time import strftime
from numpy import array, append
import numpy as np
import pyqtgraph as pg

import sys

class timeAxisItem(pg.AxisItem):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print("jestem tu i nic nie pokzauje bo mam Cie w poważaniu")
		#super.setStyle(textFillLimits = [(2,0.3)])

	def tickStrings(self, values, scale, spacing):
		currTime = strftime("%H:%M:%S")
		strings = []
		
		for i in values:
			temp = len(values)-int(i)
			strings.append(self.timeRevind(temp,currTime))
		print(strings)
		return strings

	def timeRevind(self,initTime,currTime):
		self.strings = []
		secs = int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600
		secs -= initTime
		hurs = int(secs/3600)
		secs -= hurs*3600
		mins = int(secs/60)
		secs -= mins*60
		string = str(hurs)+":"+str(mins)+":"+str(secs)
		return string

class GUI(pq.QWidget):

	def __init__(self):
		super(GUI,self).__init__()
		self.setSize()
		self.createInitialdata()
		self.createSlider(1, 0, 10)
		self.createGraph()
		self.show()

	def createGraph(self):
		self.maxX = 100 #10 for debugging purposes
		self.graph = pg.PlotWidget(self,axisItems={'bottom': timeAxisItem(orientation='bottom')})
		#aI = pg.AxisItem(orientation='bottom')
		self.g = self.graph.plot(self.dataY)
		self.graph.setGeometry(0,0,self.w-40,self.h)

	def setSize(self):
		desktop = pq.QDesktopWidget()
		desktopGeometry = desktop.screenGeometry()
		self.w = desktopGeometry.width()*2/5
		self.h = desktopGeometry.height()*2/5
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(), self.w, self.h)

	def setAndShowSize(self):
		desktop = pq.QDesktopWidget()
		desktopGeometry = desktop.screenGeometry()
		self.w = desktopGeometry.width()*2/5
		self.h = desktopGeometry.height()*2/5
		#showSize used only for debugging purposes
		self.showSize(desktopGeometry.x(), desktopGeometry.y(), desktopGeometry.width(), desktopGeometry.height(), "desktop", 20,20)
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(), self.w, self.h)
		self.showSize(desktopGeometry.x(), desktopGeometry.y(), "app", 20,50)

	#showSize used only for debugging purposes
	def showSize(self, x,y, name, sx, sy):
		qStr = name+" geometry: x="+str(x)+", y="+str(y)+", w="+str(self.w)+", h="+str(self.h)
		print(qStr)
		geometryLabel = pq.QLabel(self)
		geometryLabel.setText(qStr)
		geometryLabel.move(sx,sy)

	def createSlider(self, tickInterval, minimum, maximum):
		slider = pq.QSlider(pcq.Vertical,self)
		slider.setTickInterval(tickInterval)
		slider.setMinimum(minimum)
		slider.setMaximum(maximum)
		#slider.setTrackig(True)
		slider.setTickPosition(pq.QSlider.TicksLeft)
		sw = 40
		slider.setGeometry(self.w-sw,0,sw,self.h)
		slider.valueChanged.connect(self.updateGraph)
		#slider.setStyleSheet()
	
	def updateGraph(self):
		self.appenddata(self.sender().value())
		#self.graph.clear()
		#self.graph.plot(self.dataY)
		self.g.setData(self.dataY)

	def createInitialdata(self):
		noOfFakeData = 5
		self.dataX = self.createInitialTimeData(noOfFakeData)
		self.dataY = np.zeros((noOfFakeData,), dtype=np.int)

	def appenddata(self, x):
		if self.dataY.size < self.maxX: 
			self.dataY = append(self.dataY,x)
			self.dataX = append(self.dataY,strftime("%H:%M:%S"))
		else:
			self.dataY = append(self.dataY[1:self.maxX],x)
			self.dataX = append(self.dataY[1:self.maxX],strftime("%H:%M:%S"))
		#print(self.dataY)

	def createInitialTimeData(self,initTime):
		currTime = strftime("%H:%M:%S")
		strings = []
		for i in range(initTime-1,0,-1):
			strings.append(self.timeRevind(i,currTime))
		return strings

	def timeRevind(self,offsetTime, currTime):
		self.strings = []
		secs = int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600
		secs -= offsetTime
		hurs = int(secs/3600)
		secs -= hurs*3600
		mins = int(secs/60)
		secs -= mins*60
		string = str(hurs)+":"+str(mins)+":"+str(secs)

if __name__ == "__main__":
	style = pq.QStyleFactory.create("motif")
	pq.QApplication.setStyle(style)
	app = pq.QApplication(sys.argv)
	gui = GUI()
	print("lol dziala")
	sys.exit(app.exec_())


