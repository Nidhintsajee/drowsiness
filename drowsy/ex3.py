import sys
import webbrowser

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication, QTableWidget, QTableWidgetItem
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtGui import QGridLayout, QLineEdit, QWidget, QHeaderView
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from q import index_value
import numpy as np
import pygame
import cv2
from moviepy.editor import *
# from smsmod import smsmod_send

# loads classifiers ie dataset
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

	  
	
class UrlInput(QLineEdit):
	def __init__(self, browser):
		super(UrlInput, self).__init__()
		self.browser = browser
		self.returnPressed.connect(self._return_pressed)

	def _return_pressed(self):
		url = QUrl(self.text())
		browser.load(url)

class JavaScriptEvaluator(QLineEdit):
    def __init__(self, page):
        super(JavaScriptEvaluator, self).__init__()
        self.page = page
        self.returnPressed.connect(self._return_pressed)

    def _return_pressed(self):
        frame = self.page.currentFrame()
        result = frame.evaluateJavaScript(self.text())

# class ActionInputBox(QLineEdit):
#     def __init__(self, page):
#         super(ActionInputBox, self).__init__()
#         self.page = page
#         self.returnPressed.connect(self._return_pressed)

#     def _return_pressed(self):
#         frame = self.page.currentFrame()
#         action_string = str(self.text()).lower()
#         if action_string == "b":
#             self.page.triggerAction(QWebPage.Back)
#         elif action_string == "f":
#             self.page.triggerAction(QWebPage.Forward)
#         elif action_string == "s":
#             self.page.triggerAction(QWebPage.Stop)
#         elif action_string == "r":
#             self.page.triggerAction(QWebPage.Reload)


class RequestsTable(QTableWidget):
    header = ["url", "status", "content-type"]

    def __init__(self):
        super(RequestsTable, self).__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(self.header)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.ResizeToContents)

    def update(self, data):
        last_row = self.rowCount()
        next_row = last_row + 1
        self.setRowCount(next_row)
        for col, dat in enumerate(data, 0):
            if not dat:
                continue
            self.setItem(last_row, col, QTableWidgetItem(dat))

class Manager(QNetworkAccessManager):
    def __init__(self, table):
        QNetworkAccessManager.__init__(self)
        self.finished.connect(self._finished)
        self.table = table

    def _finished(self, reply):
        headers = reply.rawHeaderPairs()
        headers = {str(k):str(v) for k,v in headers}
        content_type = headers.get("Content-Type")
        url = reply.url().toString()
        status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        status, ok = status.toInt()
        self.table.update([url, str(status), content_type])

class Window(QtGui.QMainWindow):

	def __init__(self):
		
		super(Window,self).__init__()

		# Main PyQt window geometry and set fixed size
		self.setGeometry(630, 180, 400, 500)
		self.setWindowTitle('Your Car Touch Pad')
		self.setFixedSize(1123,702)

		self.home()


	def home(self):
		
		# set buttons and editline
		# extractAction = QtGui.QAction(QtGui.QIcon('/media/pc45/DATA/StudentProjects/drowsinessdetect/drowsy/touch.png'),'Flee the scene',self)
		# extractAction.triggered.connect(self.close_application)
		self.setWindowIcon(QtGui.QIcon('touch.png'))        
		self.styleChoice = QtGui.QLabel('Select Audio',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		self.styleChoice.setFont(newfont)
 
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(125,150,100,550))
		self.styleChoice = QtGui.QLabel('Play Music',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		self.styleChoice.setFont(newfont)
 
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(290,150,100,550))
		self.styleChoice = QtGui.QLabel('Drowsiness Detection',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		# newfont.setColor('white')
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(415,150,180,780))
		self.styleChoice = QtGui.QLabel('Stop Detection',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		# newfont.setColor('white')
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(600,150,600,780))
		self.styleChoice = QtGui.QLabel('Select Video',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		# newfont.setColor('white')
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(765,150,600,550))
		self.styleChoice = QtGui.QLabel('Play Video',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		# newfont.setColor('white')
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(930,150,600,550))

		# self.edit = QtGui.QLineEdit(self)
		# self.edit.resize(200,30)
		# self.edit.move(150,10)

		self.styleChoice = QtGui.QLabel('Google',self)
		newfont=QtGui.QFont("sans-serif", 10,weight=QtGui.QFont.Bold) 
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(120,87,200,25))

		self.styleChoice = QtGui.QLabel('Google Chrome',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(120,530,200,25))

		self.styleChoice = QtGui.QLabel('Google Map',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(290,530,200,25))
		
		self.styleChoice = QtGui.QLabel('Youtube',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(780,530,200,25))
		
		self.styleChoice = QtGui.QLabel('Gmail',self)
		newfont=QtGui.QFont("sans-serif", 10) 
		self.styleChoice.setFont(newfont)
		self.styleChoice.setStyleSheet("color: rgb(255,255,255)")
		self.styleChoice.setGeometry(QtCore.QRect(950,530,200,25))
		# self.edit1 = QtGui.QLineEdit(self)
		# self.edit1.resize(200,30)
		# self.edit1.move(150,70)
		btn1 = QtGui.QPushButton('                                                                                                                                                                                                                           ',self)
		# btn1.clicked.connect(lambda: webbrowser.open('https://assistant.google.com/intl/en_in/'))
		
		btn1.clicked.connect(self.brow)
		btn1.setIcon(QtGui.QIcon('assist.png'))
		btn1.setIconSize(QtCore.QSize(20,20))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(180,85)

		btn1 = QtGui.QPushButton(self)
		btn1.clicked.connect(lambda: webbrowser.open('https://www.google.com/chrome/'))
		btn1.setIcon(QtGui.QIcon('chrome.png'))
		btn1.setIconSize(QtCore.QSize(52,52))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(130,465)
		
		btn1 = QtGui.QPushButton(self)
		btn1.clicked.connect(lambda: webbrowser.open('https://www.google.com/maps'))
		btn1.setIcon(QtGui.QIcon('maps.png'))
		btn1.setIconSize(QtCore.QSize(52,52))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(290,465)
		
		btn1 = QtGui.QPushButton(self)
		btn1.clicked.connect(lambda: webbrowser.open('https://www.youtube.com/'))
		btn1.setIcon(QtGui.QIcon('youtube.png'))
		btn1.setIconSize(QtCore.QSize(52,52))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(770,465)
		
		btn1 = QtGui.QPushButton(self)
		btn1.clicked.connect(lambda: webbrowser.open('https://mail.google.com/'))
		btn1.setIcon(QtGui.QIcon('gmail.png'))
		btn1.setIconSize(QtCore.QSize(52,52))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(930,465)

		btn1 = QtGui.QPushButton(self)
		btn1.clicked.connect(self.file_open)
		btn1.setIcon(QtGui.QIcon('folder.png'))
		btn1.setIconSize(QtCore.QSize(52,52))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(130,350)

		btn1 = QtGui.QPushButton(self)
		btn1.clicked.connect(self.file_open)
		btn1.setIcon(QtGui.QIcon('folder.png'))
		btn1.setIconSize(QtCore.QSize(52,52))
		btn1.resize(btn1.minimumSizeHint())
		btn1.move(770,350)
		
		btn = QtGui.QPushButton(self)
		btn.clicked.connect(self.beep)
		btn.setIcon(QtGui.QIcon('music.png'))
		btn.setIconSize(QtCore.QSize(52,52))
		btn.resize(btn.minimumSizeHint())
		btn.move(290,350)

		btn = QtGui.QPushButton(self)
		btn.clicked.connect(self.play_video)
		btn.setIcon(QtGui.QIcon('video.png'))
		btn.setIconSize(QtCore.QSize(52,52))
		btn.resize(btn.minimumSizeHint())
		btn.move(930,350)

		self.filepath = QtGui.QLineEdit(self).hide()
		# self.filepath.setGeometry(150, 150, 200, 30)

		
		btn = QtGui.QPushButton(self)
		btn.clicked.connect(self.startcapture)
		btn.setIcon(QtGui.QIcon('drowsy.png'))
		btn.setIconSize(QtCore.QSize(52,52))
		btn.resize(btn.minimumSizeHint())
		btn.move(450,465)


		btn2 = QtGui.QPushButton(self)
		self.connect(btn2,QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
		btn2.setIcon(QtGui.QIcon('stop.png'))
		btn2.setIconSize(QtCore.QSize(52,52))
		btn2.resize(btn2.minimumSizeHint())
		btn2.move(610,465)
	   
		self.show()


	
	def brow(self):
		app1 = QtGui.QApplication(sys.argv)
		grid = QGridLayout()
		browser = QWebView()
		global browser
		url_input = UrlInput(browser)
		requests_table = RequestsTable()

		manager = Manager(requests_table)
		page = QWebPage()
		page.setNetworkAccessManager(manager)
		browser.setPage(page)

		js_eval = JavaScriptEvaluator(page)
		# action_box = ActionInputBox(page)

		grid.addWidget(url_input, 1, 0)
		# grid.addWidget(action_box, 2, 0)
		grid.addWidget(browser, 3, 0)
		# grid.addWidget(requests_table, 4, 0)
		# grid.addWidget(js_eval, 5, 0)

		main_frame = QWidget()
		main_frame.setLayout(grid)
		main_frame.show()
		sys.exit(app.exec_())
	
	def beep(self):

		# for i in xrange(4):
		pygame.init()
		# print "beep",self.filename
		# fnamespl = self.filename.split('/')
		# file=fnamespl[-1]
		# pygame.mixer.music.load("1.wav")
		pygame.mixer.music.load("{}".format(self.filename))
		print "dfgdgg",file
		# winsound.Beep(1500, 250)
		pygame.mixer.music.play()
		self.close_application()
			 
	def startcapture(self):
		try:
			self.setWindowIcon(QtGui.QIcon('touch.png')) 
			# and self.edit.text() and self.edit1.text()
			if self.filename:

				# name = self.edit.text()
				# phone=self.edit1.text()
				# print "name:",name,"phone:",phone
				index=index_value()
				print "index",index
				count = 0
				iters = 0
				cam = cv2.VideoCapture(0)
				print"cam",cam
				# test = cam.get(cv2.CAP_PROP_POS_MSEC)
				# ratio = cam.get(cv2.CAP_PROP_POS_AVI_RATIO)
				# frame_rate = cam.get(cv2.CAP_PROP_FPS)
				# width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
				# height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
				# brightness = cam.get(cv2.CAP_PROP_BRIGHTNESS)
				# contrast = cam.get(cv2.CAP_PROP_CONTRAST)
				# saturation = cam.get(cv2.CAP_PROP_SATURATION)
				# hue = cam.get(cv2.CAP_PROP_HUE)
				# gain = cam.get(cv2.CAP_PROP_GAIN)
				# exposure = cam.get(cv2.CAP_PROP_EXPOSURE)
				# print "Test: ", test
				# print "Ratio: ", ratio
				# print "Frame Rate: ", frame_rate
				# print "Height: ", height
				# print "Width: ", width
				# print "Brightness: ", brightness
				# print "Contrast: ", contrast
				# print "Saturation: ", saturation
				# print "Hue: ", hue
				# print "Gain: ", gain
				# print "Exposure: ", exposure

				# print "cam",cam.isOpened()

				while(True):
					ret, cur = cam.read()
					# cam.open()
					print "start video",ret
					print "cur",cur
					gray = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
					print "gray",gray
					faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors=1, minSize=(10,10))
					for (x,y,w,h) in faces:
				 
					# cv2.rectangle(cur,(x,y),(x+w,y+h),(255,0,0),2)
						roi_gray = gray[y:y+h,x:x+w]
						roi_color = cur[y:y+h,x:x+w]
						eyes = eye_cascade.detectMultiScale(roi_gray)
						len_eyes = len(eyes)
						print "eye..>",eyes,"length of eye ..>",len_eyes
						if len_eyes == 0:
							print "Eyes closed"
							iters += 1
						else:
							print "Eyes open"
						print 'iters',iters
						count += len_eyes
						
						if iters >= 4:
							iters = 0
							if count == 0:
								print "Drowsiness Detected!!!"
								# self.styleChoice = QtGui.QLabel('Drowsiness Detected...!',self)
								# self.styleChoice.setGeometry(QtCore.QRect(60,0,100,50))
								############## sms code #################
								message = '''
									ALERT........................!
									Drowsiness Detected At  
								'''

								print "message to be sent is ",message

								# smsmod_send(message,phone)

								# thread.start_new_thread(self.beep,())
								self.beep()
							count = 0  
													   
						for (ex,ey,ew,eh) in eyes:
							cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh), (0,255,0),2)
					cv2.imshow('frame', cur)
					################
					key = cv2.waitKey(1) & 0xFF
					##################
			else:
				print "choose alarm and give your name and phone"
		except Exception as e:
			print "error",e
			# print "choose alarm and give your name and phone"

	
	def play_video(self):
		pygame.display.set_caption('Video Player')

		clip = VideoFileClip("{}".format(self.filename))
		clip.preview()

		pygame.quit()

	def file_open(self):

		# can open files with .wav extensions only
		self.filename = QtGui.QFileDialog.getOpenFileName(self,'Open .wav files',"","*.*")
		print 'Path file :', self.filename
		self.filepath.setText(self.filename)
		print(self.filename)
		return self.filename


	def styleChoice(self,text):

		self.styleChoice.setText(text)                                  
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text)) 


	def close_application(self):

		choice = QtGui.QMessageBox.question(self,'Extract','Do you want to exit?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			sys.exit()
		else:
			print "close the app;ocation"
			pass


	def closeEvent(self, event):

		self.reply = QtGui.QMessageBox.critical(self, 'Message',"Are you sure to quit?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
		if self.reply == QtGui.QMessageBox.Yes:
			event.accept() 
			print "Clicked YES to Quit"
		else:
			event.ignore()
			print "Clicked NO"   
# class Videoviewer(QWidget):


def run():
# if __name__ == "__main__":

	app = QtGui.QApplication(sys.argv)
	app.setStyleSheet("QMainWindow{background-image: url('Background.jpg');}");
	GUI = Window()
	# sys.exit(app.exec_())

	# app = QApplication(sys.argv)

	# grid = QGridLayout()
	# browser = QWebView()
	# global browser
	# url_input = UrlInput(browser)
	# requests_table = RequestsTable()

	# manager = Manager(requests_table)
	# page = QWebPage()
	# page.setNetworkAccessManager(manager)
	# browser.setPage(page)

	# js_eval = JavaScriptEvaluator(page)
	# # action_box = ActionInputBox(page)

	# grid.addWidget(url_input, 1, 0)
	# # grid.addWidget(action_box, 2, 0)
	# grid.addWidget(browser, 3, 0)
	# # grid.addWidget(requests_table, 4, 0)
	# # grid.addWidget(js_eval, 5, 0)

	# main_frame = QWidget()
	# main_frame.setLayout(grid)
	# main_frame.show()

	sys.exit(app.exec_())
run()

#  # +18284774747
#  curl 'https://api.twilio.com/2010-04-01/Accounts/AC35fba91173bb38a1f098b799c79f1183/Messages.json' -X POST \
# --data-urlencode 'To=+919567777553' \
# --data-urlencode 'From=+18284774747' \
# -u AC35fba91173bb38a1f098b799c79f1183:6ce09eb7a6f085bae10bfc750ac52e4f


# auth=6ce09eb7a6f085bae10bfc750ac52e4f