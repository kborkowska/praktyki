#!/usr/bin/env python3

from Member import Member

class AlarmMemeber(Member):
    def __init__(self, memberType, memberName):
        Member.__init__(memberType, memberName)
            
    def setMsgAddress(self, msgAddress):
        self.msgAddress = msgAddress
                
    def serMsgBytes(self, msgBytes):
        try:
            self.firstMsgByte = msgBytes[0]
            self.lastMsgByte = msgBytes[1]
        except TypeError:
            self.firstMsgByte = msgBytes
            self.lastMsgByte = msgBytes

    def setMsgBits(self, msgBits = [1,8]):
        try:
            self.firstMsgBit = msgBits[0]
            self.lastMsgBit = msgBits[1]
        except TypeError:
            self.firstMsgBit = msgBits
            self.lastMsgBit = msgBitstry

    def setOnState(self,onState):
        self.onState = onState

    def setResetMsgAddress(self, resetMsgAddress):
        self.resetMsgAddress = resetMsgAddress

    def setResetMsgBytes(self, resetMsgBytes):
        try:
            self.firstResetMsgByte = resetMsgBytes[0]
            self.lastResetMsgByte = resetMsgBytes[1]
        except TypeError:
            self.firstResetMsgByte = resetMsgBytes
            self.lastResetMsgByte = resetMsgBytes 

    def setResetMsgBits(self, resetMsgBits = [1,8]):
        try:
            self.firstResetMsgBit = resetMsgBits[0]
            self.lastResetMsgBit = resetMsgBits[1]
        except TypeError:
            self.firstResetMsgBit = resetMsgBits
            self.lastRersetMsgBit = resetMsgBits
                
    def setResetOnState(self, resetOnState):
        self.resetOnState = resetOnState
            
    def getAlarmName(self):
        try:
            return self.AlarmName
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for alarm name but none has been declared')

    def getMsgAddress(self, msgAddress):
        try:
            return self.msgAddress
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for message address but none has been declared')
                
    def getMsgBytes(self, msgBytes):
        try:
            return self.firstMsgByte, self.lastMsgByte
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for message bytes but none have been declared')

    def getMsgBits(self, msgBits = [1,8]):
        try:
            return self.firstMsgBit, self.lastMsgBit
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for message bits but none have been declared')

    def getOnState(self):
        try:
            return self.onState
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for on state but none has been declared')

    def getResetMsgBytes(self):
        try:
            return self.rself.firstResetMsgByte, self.lastResetMsgByte
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for reset message bytes but none have been'+\
                  'declared')

    def getResetMsgBits(self):
        try:
            return self.firstResetMsgBit, self.lastResetMsgBit
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for reset message bits but none have been'+\
                  'declared')

    def getResetOnState(self):
        try:
            return self.resetOnState
        except NameError:
            print('In Alarm:\n'+\
                  '\t Asked for reset on state but none has been declared')
