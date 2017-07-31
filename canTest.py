#!/usr/bin/env python3
from threading import Timer
import threading

import os

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


'''def getFrame(fileName):

   with 
'''
def openCanListener(filename):
   
   os.system("candump can0 -tA > "+filename)


class MsgAnalysator():
   def __init__(self, filename):
      self.nextLine = 0
      self.filename = filename
      timer = RepeatedTimer(0.01, self.getNewMsgs)

   def getNewMsgs(self):
      newMsgsList = []
      with open(self.filename) as fn:
         for i, line in enumerate(fn):
            if i == self.nextLine:
               newMsgsList.append(line)
               self.nextLine = self.nextLine + 1
      return newMsgsList
            
    def analyseNewMesgs(self):
      newMsgsList = self.getNewMsgs()
      if newMsgsList:
         for i in newMsgsList:
            

      
       
if __name__ == "__main__":
   filename = "foo.log"
   canListener = threading.Thread(target = openCanListener, args = (filename,))
   canListener.deamon = True
   canListener.start()
   mA = MsgAnalysator(filename)

   
