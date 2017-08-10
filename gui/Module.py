from numpy import array, append

class Module():
    def __init__(self, moduleName):
        self.moduleName = moduleName

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
