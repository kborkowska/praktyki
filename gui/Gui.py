#!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
#from PyQt4.QtCore import Qt as pcq

from numpy import array
from numpy import ndarray
from numpy import append

from weakref import ref

import sys

class View(pq.QWidget):

	def __init__(self, controler = None):
		super(View,self).__init__()
		
		self.controler = ref(controler)
		
		self.setSize()

		self.initiateColours()

		self.createMainView()

		self.show()

	def initiateColours(self):
		
		self.selectedComponentColor = 'rgb(204,253,139)'
		self.workingComponentColor = 'rgb(233,255,202)'
		self.shutoffComponentColor = 'rgb(233,255,202)'
		self.alarmComponentColor = 'rgb(252,77,42)'

		self.onBtnColor = 'rgb(136,255,67)'
		self.offBtnColor = 'rgb(192,196,198)'
		

	def createMainView(self):
		self.setLayout(pq.QHBoxLayout())

		self.selectedComponent = 1

		self.secondaryLayouts = self.createInsideLayouts(self, grid = True,\
															   gridIdx = 1)

		self.createBasicStatisticPanel(self.secondaryLayouts[0])
		self.createModulePanel(self.secondaryLayouts[1])
		self.createModuleTabs(self.secondaryLayouts[2])

	def createModuleTabs(self,pane):
		numberOfModules = self.controler().getNumberOfModules()
		for i in range(numberOfModules):
			moduleTabBtn = pq.QPushButton('Modul '+str(i+1))
			if i == self.selectedModule-1:
				moduleTabBtn.setStyleSheet('background-color:'+\
												self.selectedModuleColor)
			else:
				moduleTabBtn.setStyleSheet('background-color:'+\
												self.workingModuleColor)
			moduleTabBtn.setFlat(True)
			moduleTabBtn.setObjectName('Modul_'+str(i+1)+'_Btn')
			moduleTabBtn.clicked.connect(self.changeModuleTab)
			pane().addWidget(moduleTabBtn)

	def changeModuleTab(self):
		sender = self.sender()
		senderName = sender.objectName()
		senderNumber = senderName.split('_')[1]

		if self.selectedModule != senderNumber:
			self.findChild(pq.QPushButton,\
						   'Modul_'+str(self.selectedModule)+'_Btn').\
						setStyleSheet('background-color:'+\
									  self.selectedModuleColor)
			self.findChild(pq.QPushButton,\
						   'Modul_'+str(senderNumber)+'_Btn').\
						setStyleSheet('background-color:'+\
									  self.selectedModuleColor)
			self.changeModulePanelInfo(senderNumber)
			self.selectedModule = senderNumber
	

	def changeModulePanelInfo(self,senderNumber):
		self.findChild(pq.QLabel,'chosenModelLabel').setText('Modol nr. '+\
												   str(senderNumber))

				
		

	def createModulePanel(self, pane): 
		label = pq.QLabel('Modul nr. '+str(self.selectedModule))
		label.setObjectName('chosenModelLabel')
		pane().addWidget(label,1,1)

		moduleOnOffBtn = pq.QPushButton('On')
		moduleOnOffBtn.setStyleSheet('background-color:rgb(136,255,67)')
		moduleOnOffBtn.setObjectName('moduleOnOffBtn')
		moduleOnOffBtn.clicked.connect(self.toggleOnOffBtn)
		pane().addWidget(moduleOnOffBtn,1,2)

		labels = self.labelsIn, self.labelsOut
		pane().addLayout(self.createInfoGrid(labels,True),2,1)

		labels = 'Awarie:'
		pane().addLayout(self.createInfoGrid(labels),2,2)

		labels = 'Temperatura:','Temp1', 'Temp2', 'Temp3'
		pane().addLayout(self.createInfoGrid(labels),3,1)

		labels = 'Zadane:','U', 'I'
		pane().addLayout(self.createInfoGrid(labels),3,2)

		pane().addWidget(pq.QLabel('Tryb pracy:'),4,1)
		value = pq.QLabel('napieciowy')
		#value.setStyleSheet('background-color:rgb(255,255,255)')
		value.setMargin(4)
		value.setObjectName = 'Tryb pracy'
		pane().addWidget(value,4,2)


	def createBasicStatisticPanel(self, pane):
		mainOnOffBtn = pq.QPushButton('On')
		mainOnOffBtn.setStyleSheet('background-color:rgb(136,255,67)')
		mainOnOffBtn.setObjectName('mainOnOffBtn')
		mainOnOffBtn.clicked.connect(self.toggleOnOffBtn)

		pane().addWidget(mainOnOffBtn)

		self.labelsIn = 'Wejście','U<sub>in</sub>','I<sub>in</sub>','P<sub>in</sub>'
		self.labelsOut = 'Wyjście','U<sub>out</sub>','I<sub>out</sub>',\
					'P<sub>out</sub>'
		labels = self.labelsIn, self.labelsOut
		pane().addLayout(self.createInfoGrid(labels))

		labels = []
		labels = 'Info z baterii'
		pane().addLayout(self.createInfoGrid(labels))

	def createInfoGrid(self, labels, module = False):
		labelsArray = array(labels)
		layout = pq.QGridLayout()

		#print(labelsArray.shape)
		
		try:
			numberOfCollumns = labelsArray.shape[0]
			if numberOfCollumns < 1:
				print('no labels to add')
				return -1
		except IndexError:
			labelsArray = array([labels])
			numberOfCollumns = 1

		try:
			numberOfRows = labelsArray.shape[1]
		except IndexError:
			numberOfRows = 1

		moduleStr = ''
		if module:
			moduleStr = '_module'

		if numberOfRows == 1 and numberOfCollumns == 1:
			layout.addWidget(pq.QLabel(labelsArray[0]),1,1)
		elif numberOfRows == 1:
			layout.addWidget(pq.QLabel(labelsArray[0]),1,1)
			for i in range(2,numberOfCollumns+1):
				#print(i,j)
				layout.addWidget(pq.QLabel(labelsArray[i-1]),i,1)
				value = pq.QLabel('  ')
				value.setStyleSheet('background-color:rgb(255,255,255)')
				value.setMargin(4)
				value.setObjectName = labelsArray[i-1]+moduleStr
				layout.addWidget(value,i,2)
		else:
			for i in range(1,numberOfCollumns*2,2):
				layout.addWidget(pq.QLabel(labelsArray[int((i-1)/2)][0]),1,i)

			for i in range(2,numberOfRows+1):
				for j in range(1,numberOfCollumns*2,2):
					#print(i,j)
					layout.addWidget(pq.QLabel(labelsArray[int((j-1)/2)][i-1]),\
									 i,j)
					value = pq.QLabel('  ')
					value.setStyleSheet('background-color:rgb(255,255,255)')
					value.setMargin(4)
					value.setObjectName = labelsArray[int((j-1)/2)][i-1]\
										  +moduleStr
					layout.addWidget(value,i,j+1)

		return layout

	def createInsideLayouts(self, parent, numberOfPanes = 3, grid = False,\
							gridIdx = -1):
		newLayouts = []

		if not isinstance(gridIdx,(list,int)):
			print('wrong type of gridIdx')
			return -1

		if type(gridIdx) is int:
			gridIdx = [gridIdx]

		if not grid:
			for i in range(numberOfPanes):
				newLayout = pq.QVBoxLayout()
				newLayouts.append(ref(newLayout))
				parent.layout().insertLayout(i,newLayout)
		else:
			for i in range(numberOfPanes):
				if not i in gridIdx:
					newLayout = pq.QVBoxLayout()
					parent.layout().insertLayout(i,newLayout)
				else:
					newLayout = pq.QGridLayout()
					colorWidget = pq.QWidget()
					parent.layout().insertWidget(i,colorWidget)
					colorWidget.setStyleSheet(\
						'background-color:'+self.selectedComponentColor)
					colorWidget.setLayout(newLayout)
				newLayouts.append(ref(newLayout))

		return newLayouts


	def setSize(self):
		desktopGeometry = pq.QDesktopWidget().screenGeometry()
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
			 desktopGeometry.width()*3/5,\
						 desktopGeometry.height()*3/5)


	def toggleOnOffBtn(self):
		sender = self.sender()

		if sender.text() == 'On':
			sender.setText('Off')
			sender.setStyleSheet('background-color:rgb(192,196,198)')
			if sender.objectName() == 'mainOnOffBtn':
				try:
					self.controler().toggleMainPower('Off')
				except NoneType:
					print('controler object not defined')
			elif sender.objectName() == 'moduleOnOffBtn':
				try:
					self.controler().toggleModulePower('Off',self.selectedModule)
				except NoneType:
					print('controler object not defined')

		elif sender.text() == 'Off':
			sender.setText('On')
			sender.setStyleSheet('background-color:rgb(136,255,67)')
			if sender.objectName() == 'mainOnOffBtn':
				try:
					self.controler().toggleMainPower('On')
				except NoneType:
					print('controler object not defined')
			elif sender.objectName() == 'moduleOnOffBtn':
				try:
					self.controler().toggleModulePower('On',self.selectedModule)
				except NoneType:
					print('controler object not defined')

		else:
			print('error in view.toggleOnOffBtn wrong sender text')


class Model():

	def __init__(self):
		self.initiateDictionaries()
		configFile = 'can_prog_config.txt'
		self.mainComponents = array([])
		self.configureAccordingToConfigFile(configFile)
		

	def initiateDictionaries(self):
		self.components={'MODULE': self.createModule,
						'MEMBER': self.createMember,
						'GROUP': self.createGroup}
		self.members={'toggle': ToggleMember,
					 'input': InputMember,
					 'output': OutputMember,
					 'alarm': AlarmMemeber}
		self.properties={'ON_MSG': self.setOnMsg,
						'OFF_MSG': self.setOffMsg,
						'ON_PRINT': self.setOnPrint,
						'OFF_PRINT': self.setOffPrint,
						'MSG_ADDRESS': self.setMsgAddress,
						'MSG_BYTE': self.setMsgByte,
						'MSG_BIT': self.setMsgBit,
						'ON_STATE': self.setOnState,
						'RESET_MSG_ADDRESS': self.setResetMsgAddress,
						'RESET_MSG_BYTE': self.setResetMsgByte,
						'RESET_MSG_BIT': self.setReserMsgBit,
						'RESET_ON_STATE': self.setResetOnState}

	def setOnMsg(self, line, member):
		try:
			memember.setOnMsg(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set on msg but no function exist for '+\
				  member.getType()+' type of member.')
			
			
	def setOffMsg(self, line, member):
		try:
			memember.setOffMsg(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set off msg but no function exist for '+\
				  member.getType()+' type of member.')

	def setOnPrint(self, line, member):
		try:
			memember.setOnPrint(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set on print but no function exist for '+\
				  member.getType()+' type of member.')

	def setOffPrint(self, line, member):
		try:
			memember.setOffPrint(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set off print but no function exist for '+\
				  member.getType()+' type of member.')

	def setMsgAddress(self, line, member):
		try:
			memember.setMsgAddress(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set msg address but no function exist for '+\
				  member.getType()+' type of member.')

	def setMsgByte(self, line, member):
		try:
			memember.setMsgByte([line[1],line[2]])
		except IndexError:
			memember.setMsgByte(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set msg byte but no function exist for '+\
				  member.getType()+' type of member.')

	def setMsgBit(self, line, member):
		try:
			memember.setMsgBit([line[1],line[2]])
		except IndexError:
			memember.setMsgBit(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set msg bit but no function exist for '+\
				  member.getType()+' type of member.')

	def setOnState(self, line, member):
		try:
			memember.setOnState(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set on state but no function exist for '+\
				  member.getType()+' type of member.')

	def setResetMsgAddress(self, line, member):
		try:
			memember.setResetMsgAddress(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset msg address but no function '+\
				  'exist for '+member.getType()+' type of member.')

	def setResetMsgByte(self, line, member):
		try:
			memember.setResetMsgByte([line[1],line[2]])
		except IndexError:
			memember.setResetMsgByte(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset msg byte but no function exist '+\
				  'for '+member.getType()+' type of member.')

	def setResetMsgBit(self, line, member):
		try:
			memember.setResetMsgBit([line[1],line[2]])
		except IndexError:
			memember.setResetMsgBit(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset msg bit but no function exist '+\
				  'for '+member.getType()+' type of member.')

	def setResetOnState(self, line, member):
		try:
			memember.setResetOnState(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset on state but no function exist for '+\
				  member.getType()+' type of member.')
			

	def createGroup(self, groupName, cf):
		try:
			group = Group(self, groupName)
			line = self.getAndPrepareLine(cf)
			while line != 'END_GROUP':
				group.addMember(self.branch(cf))
				line = self.getAndPrepareLine(cf)
			return group
		except Exception:
			print('In Model:\n'+\
				  '\t Creation of a new group failed')


	def createModule(self, moduleName, cf):
		try:
			module = Module(self, moduleName)
			line = self.getAndPrepareLine(cf)
			while line != 'END_MODULE':
				module.addMember(self.branch(cf))
				line = self.getAndPrepareLine(cf)
			return module
		except Exception:
			print('In Model:\n'+\
				  '\t Creation of a new module failed')

	def createMember(self, memberName, memberType, cf):
		try:
			member = self.members[memberType](memberName,memberType)
			line = self.getAndPrepareLine(cf)
			while line[0] != 'END_MEMBER'
				self.properties[line[0]](line, member)
				line = self.getAndPrepareLine(cf)
			return member
		except Exception:
			print('In Model:\n'+\
				  '\t Creation of a new member failed')

	def getAndPrepareLine(self, cf):
		line = cf.readline()
		line = line.strip()
		if line == '':
			return getAndPrepareLine(cf)
		elif line[0] == '#':
			return getAndPrepareLine(cf)
		else:
			line = line.replace(' ','')
			line = line.split(':')
			return line

	def branch(self, line, cf):
		try:
			return self.components[line[0]](line[1].replace('_',' '),cf)
		except KeyError:
			print('In Model:\n'+\
				  '\t Error in config file: main component '+\
				  'type given does not exist')
		except IndexError:
			print('In Model:\n'+\
				  '\t no name was given for a main component')


	def configureAccordingToConfigFile(self, configFile):
		try:
			with open(configFile) as cf:
				line = self.getAndPrepareLine(cf)
				while line[0] != 'END_CONFIG':
					self.mainComponents = append(\
							self.mainComponents, self.branch(line,cf))
					line = self.getAndPrepareLine(cf)
		except NameError:
			print('NameError: Config file ('+configFile+') not found')
			sys.exit()


	def getMainComponents(self):
		try:
			return self.mainComponents
		except NameError:
			print('In Model:\n'+\
				  '\t Tried to get main components but none were declared')

	def getModuleComponents(self):
		try:
			return 


class Group():
	def __init__(self, groupName):
		self.groupName = groupName

	def getGroupName(self):
		try:
			return self.groupName
		except NameError:
			print('In Group:\n'+\
				  '\t Asked for group name but none has been declared')

	def addMember(self, member):
		try:
			self.members = append(self.members, member)
		except NameError:
			self.members = array(member)

	def getMemberArray(self):
		try:
			return self.members
		except NameError:
			print('In Module:\n'+\
				  '\t Asked for member array but none has been declared')


class Module():
	def __init__(self, moduleName):
		self.moduleName = moduleName

	def addMember(self, member):
		try:
			self.members = append(self.members, member)
		except NameError:
			self.members = array(member)

	def getMemberArray(self):
		try:
			return self.members
		except NameError:
			print('In Module:\n'+\
				  '\t Asked for member array but none has been declared')

  
class Member():
	def __init__(self, memberType, memberName):
		self.memberType = memberType
		self.memberName = memberName


class ToggleMember(Member):
	def __init__(self, memeberType, memberName)):
		Member.__init__(memberType, memberName))
  
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

	def getOnText(self);
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

class InputMember(Member):
	def __init__(self, memberType, memberName)):
		Member.__init__(memberType, memberName))
		self.setMsgBits()

	def setMsgAddress(self, msgAddress):
		self.msgAddress = msgAddress

	def setMsgBytes(self, msgBytes):
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
			self.lastMsgBit = msgBits

	def getMsgAddress(self, msgAddress):
		try:
			return self.msgAddress
		except NameError:
			print('In InputMember:\n'+\
				  '\t Asked for message address but none has been declared')

	def setMsgBytes(self, msgBytes):
		try:
			return self.firstMsgByte, self.lastMsgByte
		except NameError:
			print('In InputMember:\n'+\
				  '\t Asked for message bytes but none have been declared')

	def setMsgBits(self, msgBits = [1,8]):
		try:
			return self.firstMsgBit, self.lastMsgBit
		except NameError:
			print('In InputMember:\n'+\
				  '\t Asked for message bits but none have been declared')
	

class OutputMemeber(Member):
	def __init__(self, memberType, memberName)):
		Member.__init__(memberType, memberName))

	def setMsgAddress(self, msgAddress):
		self.msgAddress = msgAddress

	def setMsgBytes(self, msgBytes):
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
			self.lastMsgBit = msgBits

	def getMsgAddress(self, msgAddress):
		try:
			return self.msgAddress
		except NameError:
			print('In InputMember:\n'+\
				  '\t Asked for message address but none has been declared')

	def getMsgBytes(self, msgBytes):
		try:
			return self.firstMsgByte, self.lastMsgByte
		except NameError:
			print('In InputMember:\n'+\
				  '\t Asked for message bytes but none have been declared')

	def getMsgBits(self, msgBits = [1,8]):
		try:
			return self.firstMsgBit, self.lastMsgBit
		except NameError:
			print('In InputMember:\n'+\
				  '\t Asked for message bits but none have been declared')

class AlarmMemeber(Member):
	def __init__(self, memberType, memberName)):
		Member.__init__(memberType, memberName))
			
	def setMsgAddress(self, msgAddress):
		self.msgAddress = msgAddress
				
	def serMsgBytes(self, msgBytes):
		try:
			self.firstMsgByte = msgBytes[0]
			self.lastMsgByte = msgBytes[1]
		except TypeError:
			self.firstMsgByte = msgBytes
			self.lastMsgByte = msgBytes

	def setMsgBits(self, msgBits = [1:8]):
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

	def setResetMsgBits(self, resetMsgBits = [1:8]):
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
			

class Controler():

	def __init__(self):
		#style = pq.QStyleFactory.create('motif')
		#pq.QApplication.setStyle(style)
		app = pq.QApplication(sys.argv)
		self.model = Model()
		self.view = View(self)
		app.exec_()
		self.execteShutdown()

	def getNumberOfModules(self):
		return self.model.getNumberOfModules()

	def execteShutdown(self):
		sys.exit()

	def getComponentMemebers(self, component):
		

	def toggleModulePower(self, toggleString, selectedModule):
		if toggleString is 'On':
			self.model.turnOnModulePwr(selectedModule)
		elif toggleString is 'Off':
			self.model.turnOffModulePwr(selectedModule)
		else:
			print('error in controler.toggleMainPower wrong toggleString')

	def toggleMainPower(self, toggleString):
		if toggleString is 'On':
			self.model.turnOnMainPwr()
		elif toggleString is 'Off':
			self.model.turnOffMainPwr()
		else:
			print('error in controler.toggleMainPower wrong toggleString')

if __name__ == "__main__":
		#sys.settrace
		con = Controler()
