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
		self.createPixelMap()
		self.show()

	def createPixelMap(self):
		#after debug remove globals
		global graph
		graph = pq.QPixmap(self.w,self.h)
		col = pq.QColor()
		col.setHsv(307,0.57*255,0.969*255,255)
		graph.fill(col)
		global gLabel
		gLabel = pq.QLabel(self)
		gLabel.setPixmap(graph)

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

if __name__ == "__main__":
	style = pq.QStyleFactory.create("motif")
	pq.QApplication.setStyle(style)
	app = pq.QApplication(sys.argv)
	gui = GUI()
	print("lol dziala")
	sys.exit(app.exec_())


