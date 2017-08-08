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
