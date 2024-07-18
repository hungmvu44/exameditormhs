from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from os import path
from PyQt6.uic import loadUiType
import sqlite3

FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"InsertExamDialog.ui"))

db = sqlite3.connect("mhsexam.db", timeout=1)
cursor = db.cursor()
qury = 'SELECT DISTINCT subject_code from Subjects DESC'
result = cursor.execute(qury).fetchall()
qury2 = 'select classroomid from classroom'
r = cursor.execute(qury2).fetchall()
qury3 = 'select time_id from Exam_Session '
r3 = cursor.execute(qury3).fetchall()

# Convert tuple to string
def converttoString(tuple_, list_):
   for i in tuple_:
      st = ' '.join(i)
      list_.append(st)
   return list_

classrooms = []
list_subject = []
session = []
classroom = converttoString(r, classrooms)
subject = converttoString(result,list_subject)


class InsertExamDialog(QDialog, FORM_CLASS):
   def __init__(self):
      super().__init__()
      self.setupUi(self)
      self.setWindowIcon(QIcon('logo.png'))
      self.setWindowTitle("Insert Exam Schedule")
      self.subject_list = self.findChild(QComboBox,"comboBox_subject")
      self.subject_list.addItems([subject for subject in list_subject])
      self.comboBox_room.addItems([classroom for classroom in classrooms])
      # Initialise Qdialog Item from InsertExamDialog ###
      self.date = self.findChild(QDateEdit, "date")
      self.day = self.findChild(QComboBox, "comboBox_day")
      self.room = self.findChild(QComboBox, "comboBox_room")
      self.subject = self.findChild(QComboBox, "comboBox_subject")
      self.timeid = self.findChild(QLineEdit, "lineEdit_timeID")
      # End Qdialog Item from InsertExamDialog ###
        
      self.insert_exam = self.findChild(QPushButton, "insert_exam")
      self.insert_exam.clicked.connect(self.add_exam)
      
      
   def add_exam(self):
        date = self.date.date().toString("DD-MM-YYYY")
        day = self.day.currentText()
        room = self.room.currentText()
        timeid = self.timeid.text()
        subject = self.subject.currentText()
        examgroup = self.exam_menu.currentText()
        
        
        query = ''' INSERT INTO Exam (Exam_Date, Day, Room, TimeID, Subject, Groupe)
                    VALUES (?, ?, ?, ?, ?, ?)'''
        row = (date, day, room, timeid, subject, examgroup)
        cursor.execute(query,row)
        db.commit()
        
        self.date.setDate(QDate.currentDate())
        self.day.setCurrentIndex(0)
        self.room.setCurrentIndex(0)
        self.timeid.clear()
        self.subject.setCurrentIndex(0)
        self.exam_menu.setCurrentIndex(0)
        self.connect_exam()

        
   def connect_exam(self):
            query = ''' 
                    SELECT e.Exam_Date,es.session,e.Groupe,e.Day,e.Room,e.TimeID, s.subject_code as subject,ts.teacher_id
                    FROM Exam e
                    JOIN Exam_Session es
                    ON e.TimeID = es.time_id
                    JOIN Subjects s
                    ON s.subject_id = e.Subject
                    JOIN Teachers_Subjects ts
                    ON s.subject_id = ts.subject_id
                '''
            result = cursor.execute(query)
            self.exam_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.exam_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.exam_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))  
      
   
      
       
      



      
      
      
