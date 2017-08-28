from Member import Member

class InputMember(Member):
	def __init__(self, parent, memberType, memberName):
		Member.__init__(self, parent, memberType, memberName)

	def isTwoWay(self):
		return False

	def isInput(self):
		return False
