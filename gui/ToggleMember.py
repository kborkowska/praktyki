from Member import Member

class ToggleMember(Member):
    def __init__(self, memeberType, memberName):
        Member.__init__(memberType, memberName)
  
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
