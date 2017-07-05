#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq
from numpy import array, append
import sys

class GUI(pq.QWidget):
	def __init__(self):
		super(GUI,self).__init__()
		self.createInitialData()
		self.createSlider(1, 0, 10)
		self.setSize()
		self.show()

	def setSize(self):
		desktop = pq.QDesktopWidget()
		desktopGeometry = desktop.screenGeometry()
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
		self.showSize(desktopGeometry.x(), desktopGeometry.y(), w, h, "app", 20,50)

	#showSize used only for debugging purposes
	def showSize(self, x,y,w,h, name, sx, sy):
		qStr = name+" geometry: x="+str(x)+", y="+str(y)+", w="+str(w)+", h="+str(h)
		print(qStr)
		geometryLabel = pq.QLabel(self)
		geometryLabel.setText(qStr)
		geometryLabel.move(sx,sy)

	def createSlider(self, tickInterval, minimum, maximum):
		slider = pq.QSlider(pcq.Vertical,self)
		slider.setTickInterval(tickInterval)
		slider.setMinimum(minimum)
		slider.setMaximum(maximum)
		
#		slider.setGeeometry()

	def createInitialData(self):
		global data
		data = array([1,2,3,4,5])

	def appendData(x):
		data = append(data,x)

if __name__ == "__main__":
	app = pq.QApplication(sys.argv)
	gui = GUI()
	print("lol dziala")
	sys.exit(app.exec_())
