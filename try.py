#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from threading import Timer

from datetime import datetime as dt

from numpy import array, append
import numpy as np

import pyqtgraph as pg

import sys

'''

Prototyp GUI do oprogramowania panelu operatorskiego do zadawania
i odbierania sygnałów układów przeksztaltnikowych.

Wesja do wprowadzania zmian i nowych funkcjonalności.

Wesja różowa.

'''

class RepeatedTimer(object):

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


class GUI(pq.QWidget):

        def __init__(self):
                super(GUI,self).__init__()

                self.setSize()

                self.layout = pq.QHBoxLayout()

                self.maxX = 100
                self.createInitialdata()
                self.createGraph()

                self.setLayout(self.layout)

                self.show()

        def __del__(self):
                del self.g
                del self.graph

        def setSize(self):
                self.sw = 40

                desktopGeometry = pq.QDesktopWidget().screenGeometry()
                self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
				desktopGeometry.width()*2/5, desktopGeometry.height()*2/5)
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

        def createInitialdata(self):
                self.dataX = self.createInitialTimeData(self.maxX)
                self.dataY = np.zeros((self.maxX,), dtype=np.int)

        def createGraph(self):
                self.graph = pg.PlotWidget(self, background =(217,217,222,255))
                self.g = self.graph.plot(list(self.dataX),list(self.dataY),\
				pen=pg.mkPen(color = (255,9,215,255),width=3.5))
                self.graph.resize(self.width()-self.sw,self.height())


def prT():
        print(' ')

if __name__ == "__main__":
	sys.settrace
	style = pq.QStyleFactory.create("motif")
	pq.QApplication.setStyle(style)
	app = pq.QApplication(sys.argv)
	gui = GUI()
	timer = RepeatedTimer(0.1, prT)
	app.exec_()
	timer.stop()
	sys.exit()

