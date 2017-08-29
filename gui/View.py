 #!/usr/bin/env python3

from PyQt4 import QtGui as pq
from PyQt4 import QtCore as pc
#from PyQt4.QtCore import Qt as pcq

from numpy import array, ndarray, append

from weakref import ref

from collections import defaultdict


class View(pq.QWidget):

	def __init__(self, controler):
		super(View,self).__init__()


		self.controler = ref(controler)

		self.setSize()

		self.initiateColours()

		self.createAndShowGUI()


	def update(self, mem):
		memType = mem().getType()
		if memType == 'output':
			mem().getViewObject()().setText(mem().getValue())
		elif memType == 'alarm':
			viewObject = mem().getViewObject()
			if mem().isOn() == True:
				viewObject().setText(mem().getName())
				viewObject().setStyleSheet('background-color:'+self.alarmComponentColor)
			else:
				viewObject().setText('   ')
				viewObject().setStyleSheet('background-color:'+self.shutoffComponentColor)
			self.show()

	'''def reset(self):
		#layout = self.findChild(pq.QStackedLayout)
		self.sender().getViewObject()().reset()
		self.sender().getViewObject()().getViewObject()().setText('   ')
		self.sender().getViewObject()().setStyleSheet('background-color:'+self.shutoffComponentColor)
		self.sender().deleateLater()'''
		
		
	def createAndShowGUI(self):
		self.setLayout(pq.QHBoxLayout())
		#self.layout().setMargin(0)
		self.layout().setSpacing(0)
		#self.layout().setContentsMargins(0,0,0,0)

		self.secondaryLayouts = self.createInsideLayouts(self, grid = True,\
															   gridIdx = 1)

		#print(self.secondaryLayouts[1]().objectName())
		self.createBasicStatisticPanel(self.secondaryLayouts[0])
		self.createModulePanelAndTabs(self.secondaryLayouts[1],\
									  self.secondaryLayouts[2])

		self.show()

	def createModulePanelAndTabs(self,moduleLayout,moduleTabLayout):
		model = self.controler().getModel()
		moduleNumber = model.getModuleNumber()
		self.selectedComponentIdx = 0
		
		for i in range(1,moduleNumber):
			module = model.getModuleDueIndex(i)
			label = ModelLabel(module.getName())
			if i != self.selectedComponentIdx:
				label.setStyleSheet('background-color:'+\
									self.shutoffComponentColor)
			else:
				label.setStyleSheet('background-color:'+\
									self.selectedComponentColor)
			moduleTabLayout().setSpacing(0)
			moduleTabLayout().setMargin(0)
			moduleTabLayout().addWidget(label)

			newWidget = pq.QWidget()
			newWidget.setStyleSheet('background-color:'+\
									self.selectedComponentColor)
			newWidget.setLayout(self.createMemberInfoGrid(module, True))
			moduleLayout().addWidget(newWidget)
 
		moduleLayout().setCurrentIndex(0)

	def createMemberInfoGrid(self,parent, first = False):
		layout = pq.QGridLayout()
		name = pq.QLabel(parent.getName())
		layout.addWidget(name,1,1)
		if first is True:
			name.setFont(pq.QFont('Any',23))
			name.setMaximumSize((self.width()*2/7), self.height()/10)
		i = 4
		for mem in parent.getMemberArray():
			if mem.canHaveChildren():
				layout.addLayout(self.createMemberInfoGrid(mem),int(i/2),i%2+1)
				i += 1
			else:
				memberType = mem.getType()
				#inLayout = pq.QHBoxLayout()
				if memberType == 'input':
					layout.addWidget(pq.QLabel(mem.getName()),int(i/2),i%2+1)
					i += 1
					value = ValueInputLabel(mem, mem.getValue())
					value.setFrameStyle(pq.QFrame.Box)
					value.setFrameShadow(pq.QFrame.Plain)
					value.setStyleSheet('background-color:'+self.valueLabel)
					layout.addWidget(value,int(i/2),i%2+1)
					i += 1
				elif memberType == 'output':
					layout.addWidget(pq.QLabel(mem.getName()),int(i/2),i%2+1)
					i += 1
					value = pq.QLabel(mem.getValue())
					value.setFrameStyle(pq.QFrame.Box)
					value.setFrameShadow(pq.QFrame.Plain)
					value.setStyleSheet('background-color:'+self.valueLabel)
					mem.setViewObject(value)
					layout.addWidget(value,int(i/2),i%2+1)
					i += 1
				elif memberType == 'toggle':
					layout.addWidget(pq.QLabel(mem.getName()),int(i/2),i%2+1)
					i += 1
					button = pq.QPushButton(mem.getOffText())
					button.setObjectName(mem.getName())
					button.setStyleSheet('background-color:'+self.offBtnColor)
					button.clicked.connect(self.Toggle)
					mem.setViewObject(button)
					layout.addWidget(button,int(i/2),i%2+1)
					i += 1
				elif memberType == 'alarm':
					label = AlarmLabel('  ')
					layout.addWidget(label,int(i/2),i%2+1)
					label.setViewObject(mem)
					mem.setViewObject(label)
					i += 1
				#layout.addLayout(inLayout)

		return layout

	def Toggle(self):
		layout = self.findChild(pq.QStackedLayout)
		text = self.controler().getModel().toggle(self.sender().objectName(),\
						  layout.currentIndex())
		self.sender().setText(text)
		self.sender().setStyleSheet('background-color:'+self.toggleColors[text])

	def ToggleMain(self):
		text = self.controler().getModel().toggle(self.sender().objectName(),\
						  'main')
		self.sender().setText(text)
		self.sender().setStyleSheet('background-color:'+self.toggleColors[text])

	def createBasicStatisticPanel(self, pane):
		model = self.controler().getModel()
		layout = pq.QVBoxLayout()
		if model.hasMain == True:
			ma = model.getMain()
			for i,child in enumerate(ma.members):
				if child.canHaveChildren() == True:
					layout.addLayout(self.createMemberInfoGrid(child, False))
				elif child.memberType == 'toggle':
					button = pq.QPushButton(child.getOffText())
					button.setObjectName(child.getName())
					button.setStyleSheet('background-color:'+self.offBtnColor)
					button.setMinimumSize( self.width()/3.5, self.height()/10)
					button.clicked.connect(self.ToggleMain)
					child.setViewObject(button)
					layout.addWidget(button)
				else:
					layout.addLayout(self.createMemberInfoGrid(child, True))

			labels = []
			labels = 'Info z baterii'
			layout.addLayout(self.createInfoGrid(labels))

			pane().addLayout(layout)
			frame = pq.QFrame()
			frame.setFrameStyle(pq.QFrame.VLine)
			frame.setFrameShadow(pq.QFrame.Plain)
			pane().addWidget(frame)
		else:
			mainOnOffBtn = pq.QPushButton('On')
			mainOnOffBtn.setMinimumSize( self.width()/3.5, self.height()/10)
			mainOnOffBtn.setStyleSheet('background-color:'+self.onBtnColor)
			mainOnOffBtn.setObjectName('mainOnOffBtn')
			#mainOnOffBtn.clicked.connect(self.toggleOnOffBtn)

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
				value.super.setFrameStale(pc.Qt.QFrame.Box)
				value.super.setFrameShadow(pc.Qt.QFrame.Plain)
				#value.setStyleSheet('border: 20px solid grey')
				value.setStyleSheet('background-color:'+self.valueLabel)
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
					value.setFrameStyle(pq.QFrame.Box)
					value.setFrameShadow(pq.QFrame.Plain)
					value.setStyleSheet('background-color:'+self.valueLabel)
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
				newLayout.setMargin(0)
				newLayouts.append(ref(newLayout))
				parent.layout().insertLayout(i,newLayout)
		else:
			for i in range(numberOfPanes):
				
				if not i in gridIdx:
					colorWidget = pq.QWidget()
					#colorWidget.setMargin(0)
					parent.layout().insertWidget(i,colorWidget)
					if i == 0:
						newLayout = pq.QHBoxLayout()
					else:
						newLayout = pq.QVBoxLayout()
					colorWidget.setStyleSheet(\
						'background-color:'+self.normalBackgroundColor)
					colorWidget.setLayout(newLayout)
				else:
					newLayout = pq.QStackedLayout()
					newLayout.setMargin(0)
					newLayout.setObjectName('lol')
					parent.layout().insertLayout(i,newLayout)
				#newLayout.setMargin(0)
				
				newLayouts.append(ref(newLayout))

		return newLayouts

	def initiateColours(self):

		self.normalBackgroundColor = 'rgb(235,235,235)'
		
		self.selectedComponentColor = 'rgb(246,246,235)'
		self.workingComponentColor = 'rgb(233,255,202)'
		self.shutoffComponentColor = 'rgb(235,235,235)'
		self.alarmComponentColor = 'rgb(252,77,42)'

		self.onBtnColor = 'rgb(136,255,67)'
		self.offBtnColor = 'rgb(192,196,198)'
		self.defBtnColor = 'rgb(222,214,192)'

		self.valueLabel = 'rgb(255,255,255)'
		
		self.toggleColors = defaultdict(lambda: self.defBtnColor)
		on = {'on','ON','On','oN'}
		off = {'off','OFF','Off','ofF','oFf','oFF','OfF','OFf'}
		for i in on:
			self.toggleColors[i] = self.onBtnColor
		for i in off:
			self.toggleColors[i] = self.offBtnColor
		
	def setSize(self):
		desktopGeometry = pq.QDesktopWidget().screenGeometry()
		self.setGeometry(desktopGeometry.x(), desktopGeometry.y(),\
			 desktopGeometry.width()*3/5,\
						 desktopGeometry.height()*3/5)

	def changeSelectedModel(self, index):
		self.secondaryLayouts[1]().setCurrentIndex(index)
		for i in range(self.secondaryLayouts[2]().count()):
			ch = self.secondaryLayouts[2]().itemAt(i).widget()
			if i != index:
				ch.setSelected(False)
				ch.setStyleSheet('background-color:'+self.shutoffComponentColor)
			else:
				ch.setSelected(True)
				ch.setStyleSheet('background-color:'+self.selectedComponentColor)
		
		

class ModelLabel(pq.QLabel):

	def __init__(self, *args, **kwargs):
		super(pq.QLabel,self).__init__(*args, **kwargs)
		self.seleced = False

	def setSelected(self, isSelected):
		self.seleced = isSelected

	def mousePressEvent(self, event):
		p = self.parent()
		while p.parent() != None:
			p = p.parent()
		text = self.text()
		p.changeSelectedModel(int(text.split('.')[1])-1)

class AlarmLabel(pq.QLabel):
	def __init__(self, *args, **kwargs):
		super(pq.QLabel,self).__init__(*args, **kwargs)

	def mousePressEvent(self, event):
		self.createResetWin()

	def createResetWin(self):
		self.resWin = pq.QWidget()
		self.resWin.setWindowModality(pc.Qt.ApplicationModal)

		dG = pq.QDesktopWidget().screenGeometry()
		self.resWin.setGeometry(dG.width()*0.25, dG.height()*0.10,\
						 dG.width()*0.2,dG.height()*0.2)

		layout = pq.QVBoxLayout()
		layout.addWidget(pq.QLabel(self.text()))
		button = pq.QPushButton('reset')
		button.clicked.connect(self.closeResWin)
		layout.addWidget(button)

		self.resWin.setLayout(layout)
		self.resWin.show()

	def setViewObject(self, viewObject):
		self.viewObject = ref(viewObject)

	def closeResWin(self):
		self.resWin.close()
		self.viewObject().reset()

class ValueInputLabel(pq.QLabel):

	def __init__(self, viewObject, *args, **kwargs):
		super(pq.QLabel,self).__init__(*args, **kwargs)
		self.setFrameStyle(pq.QFrame.Box)
		self.setFrameShadow(pq.QFrame.Plain)
		self.viewObject = ref(viewObject)

	def mousePressEvent(self, event):
		self.createInputPanel()
		#self.parent.changeSelectedModel()

	def createInputPanel(self):
		self.calcWin = pq.QWidget()
		self.calcWin.setWindowModality(pc.Qt.ApplicationModal)
		
		dG = pq.QDesktopWidget().screenGeometry()
		btnWidth = 0.3
		btnHight = 0.15
		btnXStartPtn = 0.05
		btnYStartPtn = 0.05
		self.calcWin.setGeometry(dG.width()*0.5, dG.height()*0.10,\
						 dG.width()*0.46,dG.height()*0.46)

		self.calcInput=self.createLabel(self.calcWin,\
											[btnXStartPtn,btnYStartPtn,\
											btnWidth*3,btnHight],'calcInput',\
										backColor = 'white')
		
		self.createInputBtn(self.calcWin,[btnXStartPtn,btnYStartPtn+btnHight,\
										  btnWidth,btnHight],'7',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
										  btnYStartPtn+btnHight,\
										  btnWidth,btnHight],'8',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
										  btnYStartPtn+btnHight,\
										  btnWidth,btnHight],'9',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn,\
										  btnYStartPtn+btnHight*2,\
										  btnWidth,btnHight],'4',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
										  btnYStartPtn+btnHight*2,\
										  btnWidth,btnHight],'5',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
										  btnYStartPtn+btnHight*2,\
										  btnWidth,btnHight],'6',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn,\
										  btnYStartPtn+btnHight*3,
										  btnWidth,btnHight],'1',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
										  btnYStartPtn+btnHight*3,\
										  btnWidth,btnHight],'2',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
										  btnYStartPtn+btnHight*3,\
										  btnWidth,btnHight],'3',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn,\
										  btnYStartPtn+btnHight*4,\
										  btnWidth,btnHight],'0',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth,\
										  btnYStartPtn+btnHight*4,\
										  btnWidth,btnHight],'.',\
										  self.addANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn+btnWidth*2,\
										  btnYStartPtn+btnHight*4,\
										  btnWidth,btnHight],'del',\
										  self.deleteANumber)
		self.createInputBtn(self.calcWin,[btnXStartPtn,\
										  btnYStartPtn+btnHight*5,\
										  btnWidth*3,btnHight],'Zatwierdz',\
										  self.closeCalcWin)
		self.calcWin.show()


	def createLabel(self,parent,normlizedSize,name,function = None,\
					text='Podaj wartosc zadana',backColor = 'none'):
		inputLabel = pq.QLabel(parent)
		inputLabel.setObjectName(name)
		inputLabel.setGeometry(parent.width()*normlizedSize[0],\
							 parent.height()*normlizedSize[1],\
							 parent.width()*normlizedSize[2],\
							 parent.height()*normlizedSize[3])
		inputLabel.setText(text)
		inputLabel.setStyleSheet('background-color: '+backColor)
		if function is not None:
			inputLabel.linkActivated.connect(function)
		return ref(inputLabel)
	
	def createInputBtn(self,parent,normlizedSize,txt,function):
		inputBtn = pq.QPushButton(parent)
		inputBtn.setGeometry(parent.width()*normlizedSize[0],\
							 parent.height()*normlizedSize[1],\
							 parent.width()*normlizedSize[2],\
							 parent.height()*normlizedSize[3])
		inputBtn.setText(txt)
		inputBtn.released.connect(function)

	def deleteANumber(self):
		if self.calcInput().text() != 'Podaj wartosc zadana':
			self.calcInput().setText(self.calcInput().text()\
									 [0:len(self.calcInput().text())-1])

	def addANumber(self):
		if self.calcInput().text() != 'Podaj wartosc zadana':
			self.calcInput().setText(self.calcInput().text()+self.sender().text())
		else:
			self.calcInput().setText(self.sender().text())

	def closeCalcWin(self):
		dataToSend = str(int(self.calcInput().text()))
		self.calcWin.close()
		self.setText(dataToSend)
		self.viewObject().setValue(dataToSend)



