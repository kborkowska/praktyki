from Member import Member

class ToggleMember(Member):
	def __init__(self, parent, memberType, memberName):
		Member.__init__(self, parent,memberType, memberName)
		self.isOn = False
	
	def isTwoWay(self):
		return False

	def isInput(self):
		return False

	def setOnState(self,onState):
		self.onState = onState

	def setOnMsg(self,msg):
		self.onMsg = msg

	def setOffMsg(self,msg):
		self.offMsg = msg

	def setOnText(self,text):
		self.onText = text

	def setOffText(self,text):
		self.offText = text

	def getOnMsg(self):
		try:
			return self.onMsg
		except NameError:
			print('In ToggleMember: \n \
				  \t Asked for on message but none has been declared')

	def getOffMsg(self):
		try:
			return self.offMsg
		except NameError:
			print('In ToggleMember: \n \
				  \t Asked for off message but none has been declared')

	def getOnText(self):
		try:
			return self.onText
		except NameError:
			print('In ToggleMember: \n \
				  \t Asked for on text but none has been declared')

	def getOffText(self):
		try:
			return self.offText
		except NameError:
			print('In ToggleMember: \n \
				  \t Asked for on text but none has been declared')

	def getOnState(self):
		try:
			return self.onState
		except NameError:
			print('In Alarm:\n'+\
				  '\t Asked for on state but none has been declared')


	def toggle(self):
		self.isOn = not self.isOn
		if self.isOn is True:
			return self.onText
		else:
			return self.offText

	def getValue(self):
		if self.isOn is True:
			return '1'
		else:
			return '0'


