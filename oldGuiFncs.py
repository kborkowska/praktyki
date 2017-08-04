#from model::

class Model():

    def __init__(self):

        self.numberOfModules = 4
        
        self.initMessages()
        
        self.configureModules()

    def initMessages(self):
        

    def createListOfModuleProperties(self):
        # creates list of string containig names of properties of any
        # given module to be displayed and/or changed via gui

        # position of a property name in this list determines where
        # it will be stored in arrays dedicated specyfic modules

        # if the row has more than one string entry, the first one 
        # is group name, while others represent individual values

        self.modulePropertyList = array([['pwrState'],\

                                       ['Wejście','U<sub>in</sub>',\
                                        'I<sub>in</sub>','P<sub>in</sub>'],\

                                       ['Wyjście','U<sub>out</sub>',\
                                        'I<sub>out</sub>','P<sub>out</sub>'],\

                                       ['Temperatura','Temp1','Temp2','Temp3'],\

                                       ['Zadane','U','I'],\

                                       ['Tryb pracy'],\

                                       ['Awarie']])

    def getListOfModuleProperties(self):
        try:
            return self.moduleProprtyList
        except NameError:
            self.createListOfModuleProperties()
            return self.moduleProprtyList

    def getIndexOfAProperty(self,propertyName):
        #returns position of a proprty in a property value table

        try:
            self.modulePropertyList
        except NameError:
            self.createListOfModuleProperties()

        numberOfRows = self.modulePropertyList.shape[0]

        index = -1

        for i in range(numberOfRows):
            l = len(self.modulePropertyList[i])
            if l > 1:
                for j in range(1,l):
                    index += 1
                    if self.modulePropertyList[i][j] == propertyName:
                        return index
            else:
                index += 1
                if self.modulePropertyList[i] == propertyName:
                        return index

    def configureModules(self):
        self.

    def getNumberOfModules(self):
        return self.numberOfModules

    def getPwrStateOfModule(self, moduleNumber):
        try:
            return self.moduleState[moduleNumber-1][self.pwrStateIndex]
        except IndexError:
            print('In Model.getStateOfModule: wrong module number')
    
    def turnOffModulePwr(self,chosenModule):
        self.sendOffModulePwrMsg(chosenModule)

    def turnOnModulePwr(self,chosenModule):
        self.sendOnModulePwrMsg(chosenModule)

    def turnOffMainPwr(self):
        self.sendOffMainPwrMsg()

    def turnOnMainPwr(self):
        self.sendOnMainPwrMsg()

    def sendOffModulePwrMsg(self,chosenModule):
        print('turned module no.'+str(chosenModule)+' off')

    def sendOnModulePwrMsg(self,chosenModule):
        print('turned module no.'+str(chosenModule)+' on')

    def sendOffMainPwrMsg(self):
        print('turned charger off')

    def sendOnMainPwrMsg(self):
        print('turned charger on')
