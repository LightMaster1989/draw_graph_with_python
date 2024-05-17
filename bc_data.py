# importing Qt widgets
from PyQt5.QtWidgets import *

# importing system
import sys

# importing numpy as np
import numpy as np

from PIL import Image
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import math
import pyautogui
import csv
def myFunc(e):
  return e[0]
  
class Window(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("PyQtGraph")
		self.setGeometry(100, 100, 600, 500)
		icon = QIcon("skin.png")
		self.setWindowIcon(icon)
		self.x = [0]
		self.y = [0]
		self.c = [0]
		self.peak = [0]
		self.pm1 = [0]
		self.pm2 = [0]
		self.subpeak = [0]
		self.data = [0]
		self.UiComponents()
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.scaleLine = []
		self.show()
		#self.line3 =None
		self.pause = False
	# method for components
	def recog(self):
		
		positionList = []
		digitStr =""
		pyautogui.screenshot("temp.png",region=(380,375, 250, 51))
		pos = pyautogui.locate("./images/dot_red.png","temp.png", confidence=0.87)
		#print(pos)

		if self.pause == True and pos != None:
			return
		if self.pause == True and pos == None:
			self.pause = False
			return
		if pos == None:
			return
		pos0 = list(pyautogui.locateAll("./images/0_red.png","temp.png", confidence=0.87))
		pos1 = list(pyautogui.locateAll("./images/1_red.png","temp.png", confidence=0.87))
		pos2 = list(pyautogui.locateAll("./images/2_red.png","temp.png", confidence=0.87))
		pos3 = list(pyautogui.locateAll("./images/3_red.png","temp.png", confidence=0.87))
		pos4 = list(pyautogui.locateAll("./images/4_red.png","temp.png", confidence=0.87))
		pos5 = list(pyautogui.locateAll("./images/5_red.png","temp.png", confidence=0.87))
		pos6 = list(pyautogui.locateAll("./images/6_red.png","temp.png", confidence=0.87))
		pos7 = list(pyautogui.locateAll("./images/7_red.png","temp.png", confidence=0.87))
		pos8 = list(pyautogui.locateAll("./images/8_red.png","temp.png", confidence=0.87))
		pos9 = list(pyautogui.locateAll("./images/9_red.png","temp.png", confidence=0.80))

		if(pos != None):
			positionList.append([pos[0] , "."])
			for p in pos0:
				positionList.append([p[0] , "0"])
			for p in pos1:
				positionList.append([p[0] , "1"])
			for p in pos2:
				positionList.append([p[0] , "2"])
			for p in pos3:
				positionList.append([p[0] , "3"])
			for p in pos4:
				positionList.append([p[0] , "4"])  
			for p in pos5:
				positionList.append([p[0] , "5"]) 
			for p in pos6:
				positionList.append([p[0] , "6"]) 
			for p in pos7:
				positionList.append([p[0] , "7"]) 
			for p in pos8:
				positionList.append([p[0] , "8"])  
			for p in pos9:
				positionList.append([p[0] , "9"])
			positionList.sort(key=myFunc) 
			digitStr +=positionList[0][1]
			for i in range(len(positionList)):
				if(i != (len(positionList)-1)):
					if positionList[i][0]  < (positionList[i+1][0]-5):
						digitStr +=positionList[i+1][1]
		#print(digitStr)		
		if len(digitStr)<4:
			return
		bcdata = float(digitStr)
		self.pause =  True
		if bcdata >= 1.0:
			self.y.append(math.log2(bcdata))
			self.data.append(bcdata)
			self.bcvalue.setText(digitStr)
		if self.line != None:
			self.line.clear()
		self.writeTocsv(str(bcdata))
		self.draw()
		self.drawScaleLine()
		self.analysis()
		#self.fft()
	def draw (self):
		if len(self.y) > 200:
			self.y = self.y[-200:]
			self.data = self.data[-200:]
			
		self.x = range(len(self.y))
		
		if len(self.x) > 0 :
			self.line = self.plt.plot(self.x, self.y, symbol='o',symbolBrush=0.2,symbolSize = 2,symbolPen='w', pen={'color': 'b', 'width': 1})
	def startTimer(self):
		self.timer.start(330)
		self.startBtn.setEnabled(False)
		# self.loadBcData()
		# self.draw()
		# self.drawScaleLine()
		# self.analysis()
	def addData(self):
		val = float(self.bcvalue.text())
		self.y.append(math.log2(val))
		self.data.append(self.bcvalue.text())
		if self.line != None:
			self.line.clear()

		self.draw()
		
	def drawScaleLine(self):
		for j in self.scaleLine:	
			j.clear()
		self.scaleLine.append(self.plt2.plot([0,250], [0,0], pen={'color': 'r', 'width': 1}))
		self.scaleLine.append(self.plt.plot([0,250], [1,1], symbolPen='w',symbolSize = 1, pen={'color': 'r', 'width': 1}))
		self.scaleLine.append(self.plt.plot([0,250], [2.32,2.32], symbolPen='w',symbolSize = 1, pen={'color': 'r', 'width': 1}))
		self.scaleLine.append(self.plt.plot([0,250], [3.32,3.32], symbolPen='w',symbolSize = 1, pen={'color': 'r', 'width': 1}))
		self.scaleLine.append(self.plt.plot([0,250], [4.9,4.9], symbolPen='w',symbolSize = 1, pen={'color': 'r', 'width': 1}))        
		self.scaleLine.append(self.plt.plot([0,250], [5.64,5.64], symbolPen='w',symbolSize = 1, pen={'color': 'r', 'width': 1}))
		self.scaleLine.append(self.plt.plot([0,250], [6.64,6.64], symbolPen='w',symbolSize = 1, pen={'color': 'r', 'width': 1}))
		
	def modifyData(self):
		val = float(self.bcvalue.text())
		self.y[-1]= (math.log2(val))
		self.data[-1] = self.bcvalue.text()
		if self.line != None:
			self.line.clear()
		self.draw()
		
	def UiComponents(self):
		widget = QWidget()
		self.startBtn = QPushButton("Start")
		self.startBtn.clicked.connect(self.startTimer)
		
		self.bcvalue = QLineEdit("")

		self.addBtn = QPushButton("Add")
		self.addBtn.clicked.connect(self.addData)
		
		self.modifyBtn = QPushButton("Modify")
		self.modifyBtn.clicked.connect(self.modifyData)
		self.indicator = QLineEdit("")
		
		pg.setConfigOptions(antialias=True)

		self.plt = pg.plot()
		self.plt2 = pg.plot()
		#self.plt3 = pg.plot()
		vb = self.plt.getViewBox()                                                           
		vb.setAspectLocked(lock=False)                                                  
		vb.setAutoVisible(y=1.0)                                                        
		vb.enableAutoRange(axis='y', enable=True) 
		vb.enableAutoRange(axis='x', enable=True)  
		self.timer=QTimer()
		self.timer.timeout.connect(self.recog)
		# plotting the data on plot window
		self.line = None
		self.line2 = None
		# Creating a grid layout
		layout = QGridLayout()

		# setting this layout to the widget
		widget.setLayout(layout)

		# adding label in the layout
		layout.addWidget(self.indicator, 0, 0) 
		layout.addWidget(self.startBtn, 1, 0) 
		layout.addWidget(self.bcvalue,1, 1) 
		layout.addWidget(self.addBtn, 1, 2) 
		layout.addWidget(self.modifyBtn, 1, 3) 
		# plot window goes on right side, spanning 3 rows
		layout.addWidget(self.plt, 2, 0, 1, 4)
		layout.addWidget(self.plt2, 5, 0, 2, 4)
		#layout.addWidget(self.plt3, 6, 0, 2, 4)
		# setting this widget as central widget of the main window
		self.setCentralWidget(widget)
	
	def analysis(self):
		self.indicator.setText("")
		self.c = [*range(len(self.y))]
		self.peak = [*range(len(self.y))]
		self.peak[len(self.y)-1] = 0		
		self.pm1 = [*range(len(self.y))]
		self.pm1[len(self.y)-1] = 0
		self.pm1[len(self.y)-2] = 0
		self.pm2 = [*range(len(self.y))]
		self.pm2[len(self.y)-1] = 0
		self.pm2[len(self.y)-2] = 0
		count = 0
		i = 0
		temp = self.y[0]
		for i in range(len(self.y)-1):
			if self.y[i] < self.y[i+1]:
				self.c[i+1] = 1
			elif self.y[i] > self.y[i+1]:
				self.c[i+1] = -1
			else:
				self.c[i+1] = 0
				
		for i in range(len(self.y)-1):
			if self.c[i] * self.c[i+1] < 0 and self.c[i] > 0:
				self.peak[i] = 1
			elif self.c[i] * self.c[i+1] < 0 and self.c[i] < 0:
				self.peak[i] = -1
			else:
				self.peak[i] = 0
				
		for i in range(len(self.y)-1):
			if self.c[i] * self.c[i+1] > 0:
				self.c[i+1] = self.c[i+1] + self.c[i]
				self.c[i] = 0
		if self.line2 != None:
			self.line2.clear()
		hp = [0,0,0]
		hpx = [0,0,0]
		lp = [0,0,0]
		lpx = [0,0,0]
		pc1 = 0
		pc2 = 0
		#for i in range(len(self.y)-2):
		i = len(self.y)-1
		pc1 = 0
		pc2 = 0
		my_list = range(i-1)
		print (self.peak[i])
		for n in reversed(my_list):
			if pc1 <3 and self.peak[n] == 1:
				hp[pc1] = self.y[n]
				hpx[pc1] = n 
				pc1 +=1
			elif pc2 <3 and self.peak[n] == -1:
				lp[pc2] = self.y[n]
				lpx[pc2] = n 
				pc2 +=1
			if pc2 >= 3 and pc1>=3:
				print(hp,hpx,lp,lpx)
				if hpx[0] < lpx[0] and hp[0] > 1.0 and lp[0] < 0.9 and self.y[i] > 1.0 and  hp[0] >= self.y[i]:
					#if self.y[i] > 1.0 and self.y[i+1] > 1.0 and  self.y[i+2]>1.0:
					self.indicator.setText("RED BULL")
				break
			
			# if hp[0] > hp[2]:
			# 	self.pm1[i] = 1
			# elif hp[0] < hp[2]:
			# 	self.pm1[i] = -1
			# else:
			# 	self.pm1[i] = 0
			# if lp[0] > lp[2]:
			# 	self.pm2[i] = 1
			# elif lp[0] < lp[2]:
			# 	self.pm2[i] = -1
			# else:
			# 	self.pm2[i] = 0
		
		if len(self.x) > 0 :
		 	self.line2 = self.plt2.plot(self.x, self.c, pen={'color': 'r', 'width': 1})
		 	#self.line3 = self.plt2.plot(self.x, self.pm1, pen={'color': 'r', 'width': 1})
		 	#self.line3 = self.plt2.plot(self.x, self.pm2, pen={'color': 'b', 'width': 1})
	def writeTocsv(self , val):
	    filename = "./data/bc_log.csv"
	    log_file = open(filename, 'a')
	    log_file.write(val +"\n")
	    log_file.close()	
	    
	def loadBcData(self):
	    bc_data_file = open("./data/bc_log.csv", 'r')
	    bc_data = csv.reader(bc_data_file)
	    self.data = list(bc_data)
	    self.y = list(map(lambda x: math.log2(float(x[0])), self.data))
	    
	def fft(self):
		
		# bigindex = 0
		# val = 0
		# for i in range(len(self.y)):
		# 	if val < self.y[i]:
		# 		val = self.y[i]
		# 		bigindex = i
		temp = []
		if  len(self.y) > 100:
			temp = self.y[(len(self.y)-100):(len(self.y)-1)]
		else:
			temp = self.y
		n_samples = len(temp)
		if n_samples < 10:
			return
		np_fft = np.fft.fft(temp)
		amplitudes = 2 / n_samples * np.abs(np_fft) 
		frequencies = np.fft.fftfreq(n_samples) * n_samples
		amplitudes[0] = 0
		xxx = list(zip(amplitudes[:len(np_fft) // 2],frequencies[:len(frequencies) // 2]))
		xxx.sort(key=lambda a: a[0], reverse=True)
		# for k in range(5):
		# 	print(xxx[k])
		if self.line3 != None:
			self.line3.clear()
		if len(self.x) > 0 :
		 	self.line3 = self.plt3.plot(frequencies[:len(frequencies) // 2], amplitudes[:len(np_fft) // 2], pen={'color': 'r', 'width': 1})
		
# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
