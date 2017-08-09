from Member import Member

class OutputMember(Member):
    def __init__(self, memberType, memberName):
        Member.__init__(self, memberType, memberName)

    def setMsgAddress(self, msgAddress):
        self.msgAddress = msgAddress

    def setMsgBytes(self, msgBytes):
        try:
            self.firstMsgByte = msgBytes[0]
            self.lastMsgByte = msgBytes[1]
        except IndexError:
            self.firstMsgByte = msgBytes
            self.lastMsgByte = msgBytes
            
    def setMsgBits(self, msgBits = [1,8]):
        try:
            self.firstMsgBit = msgBits[0]
            self.lastMsgBit = msgBits[1]
        except IndexError:
            self.firstMsgBit = msgBits
            self.lastMsgBit = msgBits

    def getMsgAddress(self):
        try:
            return self.msgAddress
        except NameError:
            print('In InputMember:\n'+\
                  '\t Asked for message address but none has been declared')

    def getMsgBytes(self):
        try:
            return self.firstMsgByte, self.lastMsgByte
        except NameError:
            print('In InputMember:\n'+\
                  '\t Asked for message bytes but none have been declared')

    def getMsgBits(self):
        try:
            return self.firstMsgBit, self.lastMsgBit
        except NameError:
            print('In InputMember:\n'+\
                  '\t Asked for message bits but none have been declared')
