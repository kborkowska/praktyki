from Member import Member

class OutputMember(Member):
	def __init__(self, parent, memberType, memberName):
		Member.__init__(self, parent, memberType, memberName)

	def isTwoWay(self):
		return False

	def isInput(self):
		return True
