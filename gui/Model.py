#!/usr/bin/env python3

import AlarmMember
import InputMember
import OutputMember
import ToggleMember

import Group

import Module

from numpy import array
from numpy import append

import sys

class Model():

    def __init__(self):
        #self.END_FLAG = 1
        self.moduleNumber = 0
        self.initiateDictionaries()
        configFile = 'can_prog_config.txt'
        self.mainComponents = array([])
        self.configureAccordingToConfigFile(configFile)
        
        

    def initiateDictionaries(self):
        self.components={'MODULE': self.createModule,
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

    def createToggleMember(self, memberType, memberName):
        try:
            return ToggleMember.ToggleMember(memberType, memberName)
        except Exception:
            print('In Model:\n'+\
                  '\t Tried to create toggle member but failed')

    def createInputMember(self, memberType, memberName):
        try:
            return InputMember.InputMember(memberType, memberName)
        except Exception:
            print('In Model:\n'+\
                  '\t Tried to create input member but failed')

    def createOutputMember(self, memberType, memberName):
        try:
            return OutputMember.OutputMember(memberType, memberName)
        except Exception:
            print('In Model:\n'+\
                  '\t Tried to create output member but failed')

    def createAlarmMember(self, memberType, memberName):
        try:
            return AlarmMember.AlarmMember(memberType, memberName)
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
        try:
            member.setOnState(line[1])
        except AttributeError:
            print('In Model: \n'+\
                  '\t Tried to set on state but no function exist for '+\
                  member.getType()+' type of member.')

    def setResetMsgAddress(self, line, member):
        try:
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
            

    def createGroup(self, groupName, cf):
        #try:
        group = Group.Group(groupName)
        line = self.getAndPrepareLine(cf)
        while line[0] != 'END_GROUP':
            group.addMember(self.branch(line, cf))
            line = self.getAndPrepareLine(cf)
        return group
        #except Exception:
            #print('In Model:\n'+\
                  #'\t Creation of a new group failed')


    def createModule(self, moduleName, cf):
        #try:
        module = Module.Module(moduleName)
        self.moduleNumber += 1
        line = self.getAndPrepareLine(cf)
        while line[0] != 'END_MODULE':
            module.addMember(self.branch(line, cf))
            line = self.getAndPrepareLine(cf)
        return module
        #except Exception:
            #print('In Model:\n'+\
                  #'\t Creation of a new module failed')

    def createMember(self, memberName, cf):
        #try:
        line = self.getAndPrepareLine(cf)
        member = self.members[line[1]](line[1],memberName)
        line = self.getAndPrepareLine(cf)
        while line[0] != 'END_MEMBER':
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


    def branch(self, line, cf):
        return self.components[line[0]](line[1].replace('_',' '),cf)
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
                           self.mainComponents, self.branch(line,cf))
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
            

    def getModuleDueName(self, mame):
        for i in range(len(self.mainComponents)):
            if isinstance(self.mainComponents[i], Module.Module):
                if self.mainComponents[i].getName() == name:
                    return self.mainComponents[i]


        
