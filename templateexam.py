from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow,QApplication
import sys
from os import path
from PyQt6.uic import loadUiType
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import sqlite3
from datetime import timedelta, datetime

FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"exameditor.ui"))

class Main(QMainWindow, FORM_CLASS):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.png'))
        self.connect_database()
        
        ####### Setup exam room table #########
        examroom = self.findChild(QTableWidget,"examroom_table")
        examroom.setStyleSheet('background-color:#ECE75F')
        font = QFont("Roboto", 10)
        examroom.setFont(font)
        examroom.setColumnWidth(0,50)
        examroom.setColumnWidth(1,70)
        ####### End Setup exam room table #########
        ####### Setup min for read write stop #########
        self.setup_hr = self.findChild(QComboBox, "setup_hr")
        
        self.read_hr = self.findChild(QComboBox, "read_hr")
        self.write_hr = self.findChild(QComboBox, "write_hr")
        self.stop_hr = self.findChild(QComboBox, "stop_hr")
        ####### Setup min for read write stop #########
        self.setup_min = self.findChild(QComboBox, "setup_min")
        self.read_min = self.findChild(QComboBox, "read_min")
        self.write_min = self.findChild(QComboBox, "write_min")
        self.stop_min = self.findChild(QComboBox, "stop_min")
        
        self.session_menu = self.findChild(QComboBox, "session_menu")
        self.schedule_table = self.findChild(QTableWidget, "schedule_table")
        ##set up minutes from 0 to 59
        mins = []
        for min in range(0,60):
            mins.append(min)
            
        self.setup_min.addItems([str(i) for i in mins])
        self.read_min.addItems([str(i) for i in mins])
        self.write_min.addItems([str(i) for i in mins])
        self.stop_min.addItems([str(i) for i in mins])
        
        ###Initialise time
        
        
        ####### Time for set up ,read write stop #########
       
        
        
        
        
        # ####### END Time for set up ,read write stop #########
    # def insert_schedule(self):
    #     pass
       
   
    def insert_examsession(self):
        setup_time = timedelta(hours=int(self.setup_hr.currentText()), minutes=int(self.setup_min.currentText()))
         
        read_time = timedelta(hours=int(self.read_hr.currentText()), minutes=int(self.read_min.currentText()))
         
        written_time = timedelta(hours=int(self.write_hr.currentText()), minutes=int(self.write_min.currentText()))
         
        stoppage_time = timedelta(hours=int(self.stop_hr.currentText()), minutes=int(self.stop_min.currentText()))
         
        total_read_to_written_time = written_time - read_time
        duration = stoppage_time - written_time + total_read_to_written_time
        
        session = int(self.session_menu.currentText())
         
        db = sqlite3.connect("mhsexam.db")
        cursor = db.cursor()
        cursor1 = db.cursor()
        
        query = f""" INSERT INTO Exam_Session (time_id, session, setup_time, read_time, write_time, stop_time, duration)
                    VALUES
        
                    ({120}, {session}, {setup_time}, {read_time}, {written_time}, {stoppage_time}, {duration})"""
        
        result = cursor.execute(query)
        show_schedule = cursor1.execute("Select * from Exam_Session")
         
         
       
             
    def connect_database(self):
            db = sqlite3.connect("mhsexam.db")
            cursor = db.cursor()
            
            query = ''' Select * from classroom '''
            result = cursor.execute(query)
            self.examroom_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.examroom_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.examroom_table.setItem(row_number,column_number,QTableWidgetItem(str(data))) 
                
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()