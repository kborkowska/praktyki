from numpy import array,append

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
