#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq
from time import strftime
from numpy import array, append

import pyqtgraph as pg

import sys

class timeAxisItem():

	def timeRevind(self,initTime):
		self.strings = []
		currTime = strftime("%H:%M:%S")
		secs = int(currTime[6:8])+int(currTime[3:5])*60+int(currTime[0:2])*3600
		secs -= initTime
		hurs = int(secs/3600)
		secs -= hurs*3600
		mins = int(secs/60)
		secs -= mins*60
		string = str(hurs)+":"+str(mins)+":"+str(secs)

	def __init__(self, initTime,orientation="bottom"):
		#super(timeAxisItem,self).__init__(orientation)
		#super.setStyle(textFillLimits = [(2,0.3)])
		'''		
		self.strings = []
		currTime = strftime("%H:%M:%S")
		for i in range(initTime,0,-1):
			secs = int(currTime[6:8])
			mins = int(currTime[3:5])
			hurs = int(currTime[0:2])
			secs -= initTime
			if i == initTime:
				print(currTime)
				print(str(secs))
			if secs<0:
				mins += int(secs/60)
				if i == initTime:
					print(str(int(secs/60)))
					print(str(mins))
				if mins < 0:
					hurs += int(mins/60)
					if hurs < 0:
						hurs = 24+hurs
					mins = 60+mins
				secs = 60+secs%60
			string = str(hurs)+":"+str(mins)+":"+str(secs)
			self.strings.append(string)
		print(self.strings[0])
		'''
if __name__ == "__main__":
	tAI = timeAxisItem(3800)
	tAI.timeRevind(3661)

