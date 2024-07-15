from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from os import path
from PyQt6.uic import loadUiType
import sqlite3
FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"InsertExamDialog.ui"))

db = sqlite3.connect("mhsexam.db", timeout=1)
cursor = db.cursor()
qury = 'select subject_id from Subjects'
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
      
      
      
      
