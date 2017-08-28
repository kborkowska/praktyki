from numpy import array,append

from weakref import ref

class Group():
	def __init__(self, parent, groupName):
		self.groupName = groupName
		self.parent = ref(parent)

		if parent is None:
			self.lineage = None
		else:
			self.lineage = [parent.getLineage(), self.parent]


	def getGroupName(self):
		try:
			return self.groupName
		except NameError:
			print('In Group:\n'+\
				  '\t Asked for group name but none has been declared')

	def addMember(self, member):
		try:
			self.members = append(self.members, member)
		except AttributeError:
			self.members = array(member)

	def getMemberArray(self):
		try:
			return self.members
		except NameError:
			print('In Module:\n'+\
				  '\t Asked for member array but none has been declared')
			return None

	def canHaveChildren(self):
		return True

	def getName(self):
		try:
			return self.groupName
		except NameError:
			print('In Module:\n'+\
				  '\t Asked for group name but none has been declared')
			return None

	def getLineage(self):
		return self.lineage

	def getParent(self):
		return self.parent


