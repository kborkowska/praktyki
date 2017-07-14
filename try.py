#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
from PyQt4.QtCore import Qt as pcq

from threading import Timer

from datetime import datetime as dt

from numpy import array, append
import numpy as np

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

def prT():
        print('lol')

if __name__ == "__main__":
        sys.settrace
        style = pq.QStyleFactory.create("motif")
        pq.QApplication.setStyle(style)
        app = pq.QApplication(sys.argv)
        win = pq.QWidget()
        win.setGeometry(100,100,500,500)
        timer = RepeatedTimer(0.1, prT)
        win.show()
        timer.stop()
        sys.exit(app.exec_())

