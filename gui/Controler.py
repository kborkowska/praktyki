#!/usr/bin/env python3

from datetime import datetime as dt

from PyQt4.QtGui import QApplication

from numpy import array
from numpy import ndarray
from numpy import append

from weakref import ref

import sys

from threading import Timer
import threading

from Model import Model
from View import View

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
			self._timer.daemon = True
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

class Controler():

	def __init__(self):
		#style = pq.QStyleFactory.create('motif')
		#pq.QApplication.setStyle(style)
		app = QApplication(sys.argv)
		self.model = Model(self)
		self.view = View(self)
		self.nextLine = 0
		self.createAndStartCanListener()
		timer = RepeatedTimer(2, self.getAndSendMsgs)
		app.exec_()
		self.execteShutdown()

	def getAndSendMsgs(self):
		self.getNewMsgs()
		self.sendNewMsg()

	def updateView(self, mem):
		self.view.update(mem)

	def sendNewMsg(self):
		msg = self.model.getMsgToSend()
		#os.system("cansend can0 "+msg)
		print("cansend can0 "+msg)

	def getNewMsgs(self):
		with open(self.filename) as fn:
			for i, line in enumerate(fn):
				if i == self.nextLine:
					self.model.setRecievedValues(line)
					self.nextLine = self.nextLine + 1
					print('tu')

	def execteShutdown(self):
		sys.exit()

	def getModuleNumber(self):
		return self.module.getModuleNumber()

	def getModule(self, moduleIndex = None, moduleName = None):
		if isinstance(moduleIndex, int):
			return self.model.getModuleDueIndex(moduleIndex)
		elif isinstance(moduleName, str):
			return self.model.getModuleDueName(moduleName)
		else:
			return None

	def getModel(self):
		return self.model

	def openCanListener(self):
		#os.system("candump can0 -tA > "+filename)
		f = open(self.filename,'w')
		for i in ['003', '004', '007', '010', '011', '014', '017', '018', '021', '024', '025', '028']:
			f.write('(2017-07-31 14:55:44.889417)  can0  '+i+'   [8]  FF EE DD CC BB AA 99 88\n')
		f.close()

	def createAndStartCanListener(self):
		currTime = dt.now()
		self.filename = 'CanLogs_{when}.txt'.format(when=currTime.strftime('%d_%b_%y_%H:%M'))
		self.canListener = threading.Thread(target = self.openCanListener)#, args = (filename,))
		self.canListener.deamon = True
		self.canListener.start()


if __name__ == "__main__":
	#sys.settrace
	con = Controler()





