#!/usr/bin/env python3

from weakref import ref

class Member():
	def __init__(self, parent, memberType, memberName):
		self.memberType = memberType
		self.memberName = memberName

		self.parent = ref(parent)
		self.value = '0'

		if parent is None:
			self.lineage = None
		else:
			self.lineage = [parent.getLineage(), self.parent]


	def isTwoWay(self):
		return False

	def getName(self):
		try:
			return self.memberName
		except NameError:
			print('In Member.getName():\n'+\
				  '\t No name declared')

	def getType(self):
		try:
			return self.memberType
		except NameError:
			print('In Member.getType():\n'+\
				  '\t No type declared')

	def canHaveChildren(self):
		return False

	def setMsgAddress(self, msgAddress):
		self.msgAddress = int(msgAddress)

	def setMsgBytes(self, msgBytes):
		try:
			self.firstMsgByte = int(msgBytes[0])
			self.lastMsgByte = int(msgBytes[1])
		except IndexError:
			self.firstMsgByte = int(msgBytes)
			self.lastMsgByte = int(msgBytes)
			
	def setMsgBits(self, msgBits = [1,8]):
		try:
			self.firstMsgBit = int(msgBits[0])
			self.lastMsgBit = int(msgBits[1])
		except IndexError:
			self.firstMsgBit = int(msgBits)
			self.lastMsgBit = int(msgBits)

	def getMsgAddress(self, inOut):
		try:
			if self.isTwoWay() and inOut == 'out':
				return self.msgOutAddress
			else:
				return self.msgAddress
		except AttributeError:
			print('In Member:\n'+\
				  '\t Asked for message address but none has been declared')

	def getMsgBytes(self):
		try:
			if self.isTwoWay() and inOut == 'out':
				return self.getOutMsgBytes()
			else:
				return self.firstMsgByte, self.lastMsgByte
		except AttributeError:
			print('In Member:\n'+\
				  '\t Asked for message bytes but none have been declared')

	def getMsgBits(self):
		try:
			if self.isTwoWay() and inOut == 'out':
				return self.getOutMsgBits()
			else:
				return self.firstMsgBit, self.lastMsgBit
		except AttributeError:
			if self.isTwoWay() and inOut == 'out':
				first,last = self.getOutMsgBits()
				return 1, (last-first+1)*8
			else:
				return 1, (self.lastMsgByte-self.firstMsgByte+1)*8
			#print('In Member:\n'+\
				  #'\t Asked for message bits but none have been declared')

	def getOutMsgInfo(self):
		if self.isTwoWay():
			return self.getOutMsgBytes(), self.getOutMsgBits(), self.getOutData()
		else:
			return self.getMsgBytes(), self.getMsgBits(), self.getValue()

	def getInMsgInfo(self):
		if self.isTwoWay():
			return self.getInMsgBytes(), self.getInMsgBits()
		else:
			return self.getMsgBytes(), self.getMsgBits()

	def setValue(self, value):
		if value == self.value:
			return False
		else:
			self.value = value
			return True

	def getLineage(self):
		return self.lineage

	def getParent(self):
		return self.parent

	def setViewObject(self, object):
		self.viewObject = ref(object)

	def getViewObject(self):
		return self.viewObject

	def getValue(self):
		return self.value



