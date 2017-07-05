#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from numpy import array, append

import pyqtgraph as pg

import sys

class GUI(pq.QWidget):

	w = 100
	h = 100

	def __init__(self):
		super(GUI,self).__init__()
		self.setSize()
		self.createInitialData()
		self.createSlider(1, 0, 10)
		self.createGraph()
		self.show()

	def createGraph(self):
		global graph		
		graph = pg.PlotWidget(self)
		graph.plot(data)
		graph.setGeometry(0,0,self.w-40,self.h)

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
		#slider.setStyleSheet()

	def createInitialData(self):
		global data
		data = array([1,2,3,4,5])

	def appendData(x):
		data = append(data,x)

if __name__ == "__main__":
	style = pq.QStyleFactory.create("motif")
	pq.QApplication.setStyle(style)
	app = pq.QApplication(sys.argv)
	gui = GUI()
	print("lol dziala")
	sys.exit(app.exec_())


