#!/usr/bin/env python3

import AlarmMember
import InputMember
import OutputMember
import ToggleMember

import Group

import Module

import Main

from numpy import array
from numpy import append

from weakref import ref

import sys

class Model():

	def __init__(self, controler):
		#self.END_FLAG = 1
		self.hasMain = False
		self.controler = ref(controler)
		self.moduleNumber = 0
		self.initiateDictionaries()
		configFile = 'can_prog_config.txt'
		self.mainComponents = array([])
		self.configureAccordingToConfigFile(configFile)
		self.msgIterator = 0


	def initiateDictionaries(self):
		self.msgInAddresses = {}
		self.msgOutAddresses = {}
		self.components={'MAIN':self.createMain,
						 'MODULE': self.createModule,
						 'MEMBER': self.createMember,
						 'GROUP': self.createGroup}
		self.members={'toggle': self.createToggleMember,
					  'input': self.createInputMember,
					  'output': self.createOutputMember,
					  'alarm': self.createAlarmMember}
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
						 'RESET_MSG_BIT': self.setResetMsgBit,
						 'RESET_ON_STATE': self.setResetOnState}

	def createMain(self, mainName, cf, parent):
		#try:
		self.hasMain = True
		print('lol')
		main = Main.Main(parent, mainName)
		self.moduleNumber += 1
		line = self.getAndPrepareLine(cf)
		while line[0] != 'END_MAIN':
			main.addMember(self.branch(line, cf, main))
			line = self.getAndPrepareLine(cf)
		return main
		#except Exception:
			#print('In Model:\n'+\
				  #'\t Creation of a new module failed')

	def createToggleMember(self, parent, memberType, memberName):
		try:
			return ToggleMember.ToggleMember(parent, memberType, memberName)
		except Exception:
			print('In Model:\n'+\
				  '\t Tried to create toggle member but failed')

	def createInputMember(self, parent, memberType, memberName):
		try:
			return InputMember.InputMember(parent, memberType, memberName)
		except Exception:
			print('In Model:\n'+\
				  '\t Tried to create input member but failed')

	def createOutputMember(self, parent, memberType, memberName):
		try:
			return OutputMember.OutputMember(parent, memberType, memberName)
		except Exception:
			print('In Model:\n'+\
				  '\t Tried to create output member but failed')

	def createAlarmMember(self, parent, memberType, memberName):
		try:
			return AlarmMember.AlarmMember(parent, memberType, memberName)
		except Exception:
			print('In Model:\n'+\
				  '\t Tried to create alarm member but failed')

	def setOnMsg(self, line, member):
		try:
			member.setOnMsg(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set on msg but no function exist for '+\
				  member.getType()+' type of member.')
			
			
	def setOffMsg(self, line, member):
		try:
			member.setOffMsg(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set off msg but no function exist for '+\
				  member.getType()+' type of member.')

	def setOnPrint(self, line, member):
		try:
			member.setOnText(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set on print but no function exist for '+\
				  member.getType()+' type of member.')

	def setOffPrint(self, line, member):
		try:
			member.setOffText(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set off print but no function exist for '+\
				  member.getType()+' type of member.')

	def setMsgAddress(self, line, member):
		try:
			if member.isInput():
				try:
					self.msgInAddresses[line[1]].append(ref(member))
				except KeyError:
					self.msgInAddresses[line[1]] = [ref(member)]
			else:
				try:
					self.msgOutAddresses[line[1]].append(ref(member))
				except KeyError:
					self.msgOutAddresses[line[1]] = [ref(member)]
			member.setMsgAddress(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set msg address but no function exist for '+\
				  member.getType()+' type of member.')

	def setMsgByte(self, line, member):
		try:
			member.setMsgBytes([line[1],line[2]])
		except IndexError:
			member.setMsgBytes(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set msg byte but no function exist for '+\
				  member.getType()+' type of member.')

	def setMsgBit(self, line, member):
		try:
			member.setMsgBits([line[1],line[2]])
		except IndexError:
			member.setMsgBits(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set msg bit but no function exist for '+\
				  member.getType()+' type of member.')

	def setOnState(self, line, member):
		member.setOnState(line[1])
		try:
			member.setOnState(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set on state but no function exist for '+\
				  member.getType()+' type of member.')

	def setResetMsgAddress(self, line, member):
		try:
			try:
				self.msgOutAddresses[line[1]].append(ref(member))
			except KeyError:
				self.msgOutAddresses[line[1]] = [ref(member)]
			member.setResetMsgAddress(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset msg address but no function '+\
				  'exist for '+member.getType()+' type of member.')

	def setResetMsgByte(self, line, member):
		try:
			member.setResetMsgBytes([line[1],line[2]])
		except IndexError:
			member.setResetMsgBytes(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset msg byte but no function exist '+\
				  'for '+member.getType()+' type of member.')

	def setResetMsgBit(self, line, member):
		try:
			member.setResetMsgBits([line[1],line[2]])
		except IndexError:
			member.setResetMsgBits(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset msg bit but no function exist '+\
				  'for '+member.getType()+' type of member.')

	def setResetOnState(self, line, member):
		try:
			member.setResetOnState(line[1])
		except AttributeError:
			print('In Model: \n'+\
				  '\t Tried to set reset on state but no function exist for '+\
				  member.getType()+' type of member.')
			

	def createGroup(self, groupName, cf, parent):
		#try:
		group = Group.Group(parent, groupName)
		line = self.getAndPrepareLine(cf)
		while line[0] != 'END_GROUP':
			group.addMember(self.branch(line, cf, group))
			line = self.getAndPrepareLine(cf)
		return group
		#except Exception:
			#print('In Model:\n'+\
				  #'\t Creation of a new group failed')


	def createModule(self, moduleName, cf, parent):
		#try:
		module = Module.Module(parent, moduleName)
		self.moduleNumber += 1
		line = self.getAndPrepareLine(cf)
		while line[0] != 'END_MODULE':
			module.addMember(self.branch(line, cf, module))
			line = self.getAndPrepareLine(cf)
		return module
		#except Exception:
			#print('In Model:\n'+\
				  #'\t Creation of a new module failed')

	def createMember(self, memberName, cf, parent):
		#try:
		line = self.getAndPrepareLine(cf)
		member = self.members[line[1]](parent,line[1],memberName)
		line = self.getAndPrepareLine(cf)
		while line[0] != 'END_MEMBER':
			#print(line)
			self.properties[line[0]](line, member)
			line = self.getAndPrepareLine(cf)
		return member
		#except Exception:
			#print('In Model:\n'+\
				  #'\t Creation of a new member failed')

	def getAndPrepareLine(self, cf):
		line = cf.readline()
		#print(line)
		'''if line == 'END_CONFIG':
			self.END_FLAG = 0''
		if self.END_FLAG:'''
		line = line.strip()
		if line == '':
			return self.getAndPrepareLine(cf)
		elif line[0] == '#':
			return self.getAndPrepareLine(cf)
		else:
			line = line.replace(' ','')
			line = line.split(':')
			return line
		#return -1


	def branch(self, line, cf, parent):
		return self.components[line[0]](line[1].replace('_',' '),cf,parent)
		'''try:
			
		except KeyError:
			print('In Model:\n'+\
				  '\t Error in config file: main component '+\
				  'type given does not exist')
		except IndexError:
			print('In Model:\n'+\
				  '\t no name was given for a main component')'''


	def configureAccordingToConfigFile(self, configFile):
		with open(configFile) as cf:
			line = self.getAndPrepareLine(cf)
			while line[0] != 'END_CONFIG':
				self.mainComponents = append(\
						   self.mainComponents, self.branch(line,cf,None))
				line = self.getAndPrepareLine(cf)
		


	def getMainComponents(self):
		try:
			return self.mainComponents
		except NameError:
			print('In Model:\n'+\
				  '\t Tried to get main components but none were declared')


	def getModuleNumber(self):
		try:
			return self.moduleNumber
		except NameError:
			print('In Module:\n'+\
				  '\t no module number has been declared')

	def getComponentNumber(self):
		try:
			return len(self.mainComponents)
		except NameError:
			print('In Module:\n'+\
				  '\t no components number has been declared')


	def getModuleDueIndex(self, index):
		for i in range(index, len(self.mainComponents)):
			if isinstance(self.mainComponents[i], Module.Module):
				return self.mainComponents[i]
			

	def getMain(self):
		for i in range(len(self.mainComponents)):
			if isinstance(self.mainComponents[i], Main.Main):
				return self.mainComponents[i]

	def getModuleDueName(self, name):
		for i in range(len(self.mainComponents)):
			if isinstance(self.mainComponents[i], Module.Module):
				if self.mainComponents[i].getName() == name:
					return self.mainComponents[i]

	def toggle(self, toggleName, moduleIndex):
		#print(toggleName)
		if moduleIndex == 'main':
			return self.toggleChild(toggleName, self.getMain().getMemberArray())
		else:
			return self.toggleChild(toggleName, self.mainComponents[moduleIndex].getMemberArray())


	def toggleChild(self, toggleName, components):
		for i in components:
			if toggleName == i.getName():
				try:
					return i.toggle()
				except AttributeError:
					return 'Error'
			elif i.canHaveChildren() is True:
				text = self.toggleChild(toggleName, i.getMemberArray())
				if text is not None:
					return text
		return None

	def getMsgToSend(self):
		bits = 8
		bytes = 8
		msg = ''
		address = list(self.msgOutAddresses)[self.msgIterator]

		self.msgIterator += 1
		if self.msgIterator == len(self.msgOutAddresses):
			self.msgIterator = 0

		for i in range(bits*bytes):
			msg = msg + '0'

		for i, mem in enumerate(self.msgOutAddresses[address]):
			info = mem().getOutMsgInfo()
			binMsg = bin(int(info[2])).split('b')[1]
			startPtn = (info[0][0]-1)*8 + info[1][0]-1 + info[1][1] - info[1][0] + 1 - len(binMsg)
			msg = msg[0:startPtn]+binMsg+msg[(startPtn+len(binMsg)):len(msg)]

		msg = hex(int(msg,2)).split('x')[1]
		for k in range(bytes*2 - len(msg)):
			msg = '0' + msg
				
		return address+'#'+msg	



	def setRecievedValues(self, msg):
		msg = msg.split()
		tmp = ''
		for i in range(int(msg[4][1])):
			tmp += msg[5+i]

		tmp = bin(int(tmp,16)).split('b')[1]

		try:
			for i,mem in enumerate(self.msgInAddresses[msg[3]]):
				info = mem().getInMsgInfo()

				l = (info[1][1]-info[1][0]+1)
				startPtn = (info[0][0]-1)*8 + info[1][0]-1
				val = ''
				for j in range(l):
					val += tmp[startPtn+j]

				val = str(int(val,2))
				#print(val)
				lol = mem().setValue(val) 
				if lol is True:
					self.controler().updateView(mem)
		except KeyError:
			print('recieved msg with unknown address '+ msg[3])




