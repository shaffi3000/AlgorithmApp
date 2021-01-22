import sys, os
from PyQt5 import QtCore, QtGui, uic  
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QComboBox, QTextEdit 
import smtplib
import imghdr
from email.message import EmailMessage
import random


winHome = uic.loadUiType("homeScreen.ui") [0]
winQs = uic.loadUiType("quiestionScreen.ui") [0]
winEmail = uic.loadUiType("emailResults.ui") [0]
winResults = uic.loadUiType("answersScreen.ui") [0]

import sqlite3

con = sqlite3.connect('algorithms.db')
cur = con.cursor()


class HomeScreen(QtWidgets.QMainWindow, winHome): #imports the PyQT 'main window' functionality, winMain links to UI screens above
	def __init__(self, parent = None):
	    QtWidgets.QMainWindow.__init__(self,parent) ##setting the screen up, defining where the buttons are linking to, and where text box information is being stored 
	    self.setupUi(self)

	    self.GCSEBtn.clicked.connect(self.GCSE)
	    self.aLevelBtn.clicked.connect(self.ALevel)
	    self.numOfQs = self.numOfQsBox.currentText() #workout drop down


	def GCSE(self):
	    user1.numOfQs = self.numOfQsBox.currentText() #drop down
	    user1.level = "GCSE"
	    quiestion.setupQ()

	    self.hide()
	    self.newWin = QuiestionScreen()
	    self.newWin.show()
	    pass
		
	def ALevel(self):
	    user1.numOfQs = self.numOfQsBox.currentText()
	    user1.level = "ALevel"
	    quiestion.setupQ()

	    self.hide()
	    self.newWin = QuiestionScreen
	    self.newWin.show()

	def back(self):
	    pass

class QuiestionScreen(QtWidgets.QMainWindow, winQs):
	def __init__(self, parent = None):
	    QtWidgets.QMainWindow.__init__(self,parent) ##setting the screen up, defining where the buttons are linking to, and where text box information is being stored 
	    self.setupUi(self)
	    self.answerTxt.setPlainText(" ") #textedit
	    self.scoreTxt.setText(" ")
	    self.quiestion = str(quiestion.currentQ)
	    self.quiestionLbl.setText(self.quiestion)
	    self.maxMarkLbl.setText("/" + str(quiestion.mark))
	    self.checkBtn.clicked.connect(self.check)
	    self.nextBtn.clicked.connect(self.next)
	    self.checked = False
		   


	def check(self):
		if self.answerTxt.toPlainText() != " ":
			user1.answer = self.answerTxt.toPlainText()
			self.answerTxt.setReadOnly(True)
			
			self.answerLbl.setPixmap(QtGui.QPixmap(quiestion.image))
			self.checked = True
		else:
			QtWidgets.QMessageBox.information(self,"Error", "Please enter an answer", QMessageBox.Ok)
		return self.checked
	    

	def next(self):
		if self.checked == True:
			if self.scoreTxt.text() != " ":
				user1.answer = self.answerTxt.toPlainText()
				if user1.qsDone != int(user1.numOfQs):
					quiestion.x += 1
					user1.qsDone += 1
					quiestion.maxScore += quiestion.mark
					user1.score.append([quiestion.QuiestionsL[quiestion.x], int(self.scoreTxt.text()), user1.answer])
					quiestion.setupQ()
					self.newWin = QuiestionScreen()
					self.close()
					self.newWin.show()
				else:
					user1.score.append([quiestion.QuiestionsL[quiestion.x], int(self.scoreTxt.text()), user1.answer])
					quiestion.maxScore += quiestion.mark
					QtWidgets.QMessageBox.information(self,"Finished", "Click Ok to email your results", QMessageBox.Ok)
					user1.displayResults()
					self.hide()
					self.newWin = Email()
					self.newWin.show()
			else:
				QtWidgets.QMessageBox.information(self,"Error", "Please enter a mark", QMessageBox.Ok)
		else:
		       QtWidgets.QMessageBox.information(self,"Error", "You have not checked your answer yet", QMessageBox.Ok)


# class Results(QtWidgets.QMainWindow, winResults):
# 		def __init__(self,parent = None):
# 			QtWidgets.QMainWindow.__init__(self,parent)
# 			self.setupUi(self)
# 			self.sendEmailBtn.clicked.connect(self.sendEmail)
# 			self.userScoreLbl.setText(str(user1.totalScore))
# 			self.totalMarksLbl.setText(str(quiestion.maxScore))
# 			self.answersLbl.setText(user1.answerOut)





# 		def sendEmail(self):
			
# 			self.hide()
# 			self.newWin = Email()
# 			self.newWin.show()



class Email(QtWidgets.QMainWindow, winEmail):
	def __init__(self, parent = None):
	    QtWidgets.QMainWindow.__init__(self,parent) ##setting the screen up, defining where the buttons are linking to, and where text box information is being stored 
	    self.setupUi(self)
	    self.sendBtn.clicked.connect(self.sendEmail)
	    self.email_address = os.environ.get('EMAIL_USER')
	    self.email_pass = os.environ.get('EMAIL_PASS')
	    #self.teacherDrop.currentText() # drop downn

	def sendEmail(self):
		if self.emailTxt.text() != " " and self.studentIDTxt.text() != " ":
			email_to = self.emailTxt.text()
			subject = "Student Algorithm results"
			body = f'{user1.message}'
			msg = f'Subject: {subject} \n\n {body}'
			messageSent = 0
			while messageSent == 0:
				smtp = smtplib.SMTP('smtp.gmail.com', 587)
				smtp.ehlo()
				smtp.starttls()
				smtp.login(self.email_address, self.email_pass)
				smtp.sendmail(self.email_address, email_to, msg)
				smtp.close()
				messageSent =1
				break
		else:
			QtWidgets.QMessageBox.information(self,"Error", "You have not entered an email and/or student ID", QMessageBox.Ok)
 
	


	

class User():
	def __init__(self, name, numOfQs):
	    self.name = name
	    self.numOfQs = numOfQs
	    self.level = " "
	    self.answer = None
	    self.score = []
	    self.qsDone = 1
	    self.answer = " "
	    self.totalScore = 0
	    self.answers = []
	    self.answerOut = " "
	    self.results = []
	    self.message = " "


	def displayResults(self):
		self.totalScore = 0
		for x in range(len(self.score)):
			self.totalScore = self.totalScore + self.score[x][1]
			self.answers.append(self.score[x][2])
		print(self.answers)

		
		for item in self.answers:
			i = 0
			self.answerOut = ["Quiestion " + str(i+1) ,"\n %s" %item, " - %s" %str(self.score[i][1])]
			i += 1
			self.results.append(self.answerOut)
			print(self.results)
			#return self.answerOut

		for j in range(0, len(self.results)-1):
			self.message = self.message + (self.results[j][0] + self.results[j][1] + ". Mark: " + self.results[j][1] + '\n')




class Quiestion():
		def __init__(self):
			self.currentQ = " "
			self.mark = 0
			self.QuiestionsL = []
			self.quiestion = 0
			self.x = 0
			self.maxScore = 0


		def setupQ(self):
			if user1.level != None:
				numOfQs = int(user1.numOfQs)
				while len(quiestion.QuiestionsL) != numOfQs:
					self.q = random.randint(1, numOfQs)
					if self.q not in quiestion.QuiestionsL:
						self.QuiestionsL.append(self.q)
					else:
						pass

				if user1.level == "GCSE":
					Sql = ("""SELECT quiestion, image_name, marks FROM GCSE_Qs WHERE ID = '%d' """) %self.QuiestionsL[self.x]
					cur.execute(Sql)
					results = cur.fetchall()
					#print(results)
					self.currentQ = results[0][0]
					self.image = results[0][1]
					self.mark = results[0][2]
				else:
					Sql = ("""SELECT quiestion, image_name, marks FROM ALEVEL_Qs WHERE ID = '%d' """) %self.QuiestionsL[self.x]
					cur.execute(Sql)
					results = cur.fetchone()
					self.currentQ = results[0][0]
					self.image = results[0][1]
					self.mark = results[0][2]
	    

app = QtWidgets.QApplication(sys.argv) #think of this as the 'main ()' section in procedural programming. Allows you to call the program into action 

user1 = User(" ", " ") #creates a customer object with no name or age
quiestion = Quiestion()
win1 = HomeScreen()
win2 = QuiestionScreen()
win4 = Email()
#win3 = Results()


win1.show()
app.exec_()
