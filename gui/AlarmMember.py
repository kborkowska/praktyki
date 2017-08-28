#!/usr/bin/env python3

from Member import Member

from weakref import ref

class AlarmMember(Member):
	def __init__(self, parent, memberType, memberName):
		Member.__init__(self, parent, memberType, memberName)
		self.value = '0'
		self.dataToSend = '0'

	def isTwoWay(self):
		return True

	def isInput(self):
		return True

	def setOnState(self,onState):
		self.onState = onState
		self.offState = ''
		for w,q in enumerate(self.onState):
			if q == '1':
				self.offState += '0'
			else:
				self.offState += '1'
		self.value = self.offState

	def setResetMsgAddress(self, resetMsgAddress):
 		self.resetMsgAddress = int(resetMsgAddress)

	def setResetMsgBytes(self, resetMsgBytes):
		try:
			self.firstResetMsgByte = int(resetMsgBytes[0])
			self.lastResetMsgByte = int(resetMsgBytes[1])
		except IndexError:
			self.firstResetMsgByte = int(resetMsgBytes)
			self.lastResetMsgByte = int(resetMsgBytes)

	def setResetMsgBits(self, resetMsgBits = [1,8]):
		try:
			self.firstResetMsgBit = int(resetMsgBits[0])
			self.lastResetMsgBit = int(resetMsgBits[1])
		except IndexError:
			self.firstResetMsgBit = int(resetMsgBits)
			self.lastResetMsgBit = int(resetMsgBits)

	def setResetOnState(self, resetOnState):
		self.resetOnState = resetOnState
		self.resetOffState = ''
		for w,q in enumerate(self.resetOnState):
			if q == '1':
				self.resetOffState += '0'
			else:
				self.resetOffState += '1'
		self.dataToSend = self.resetOffState

	def getAlarmName(self):
		try:
			return self.AlarmName
		except NameError:
			print('In Alarm:\n'+\
				  '\t Asked for alarm name but none has been declared')

	def getOnState(self):
		try:
			return self.onState
		except NameError:
			print('In Alarm:\n'+\
				  '\t Asked for on state but none has been declared')

	def getResetMsgAddress(self):
		try:
			return self.resetMsgAddress
		except NameError:
			print('In Alarm:\n'+\
				  '\t Asked for message address but none has been declared')

	def getResetMsgBytes(self):
		try:
			return self.firstResetMsgByte, self.lastResetMsgByte
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

	def reset(self):
		self.value = 'not'
		self.dataToSend = self.resetOnState


	def setValue(self, value):
		if value == self.value:
			return False
		else:
			self.value = value
			return True

	def getOutMsgBytes(self):
		return self.firstResetMsgByte, self.lastResetMsgByte

	def getOutMsgBits(self):
		return self.firstResetMsgBit, self.lastResetMsgBit

	def getOutData(self):
		tmp = self.dataToSend
		if self.dataToSend == self.resetOnState:
			self.dataToSend = self.resetOffState
		return tmp

	def getInMsgBytes(self):
		return self.firstMsgByte, self.lastMsgByte

	def getInMsgBits(self):
		return self.firstMsgBit, self.lastMsgBit

	def isOn(self):
		print(self.value)
		if self.value == self.onState:
			return True
		else:
			return False




