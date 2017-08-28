#!/usr/bin/env python3

from weakref import ref

class Main():
	def __init__(self, parent, moduleName):
		self.moduleName = moduleName
		if parent is None:
			self.parent = None
		else:
			self.parent = ref(parent)

		if parent is None:
			self.lineage = None
		else:
			self.lineage = [parent.getLineage(), self.parent]

	def addMember(self, member):
		try:
			self.members = append(self.members, member)
		except AttributeError:
			self.members = array(member)

	def getMemberArray(self):
		try:
			return self.members
		except AttributeError:
			print('In Module:\n'+\
				  '\t Asked for member array but none has been declared')
			return None

	def getName(self):
		return self.moduleName

	def canHaveChildren(self):
		return True

	def getParent(self):
		return self.parent

	def getLineage(self):
		return self.lineage
