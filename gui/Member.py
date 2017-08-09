#!/usr/bin/env python3

class Member():
    def __init__(self, memberType, memberName):
        self.memberType = memberType
        self.memberName = memberName

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
