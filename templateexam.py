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
        self.connect_classroom()
        
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
        self.setup_hr.removeItem(1)
        self.read_hr = self.findChild(QComboBox, "read_hr")
        self.write_hr = self.findChild(QComboBox, "write_hr")
        self.stop_hr = self.findChild(QComboBox, "stop_hr")
        ####### Setup min for read write stop #########
        self.setup_min = self.findChild(QComboBox, "setup_min")
        self.read_min = self.findChild(QComboBox, "read_min")
        self.write_min = self.findChild(QComboBox, "write_min")
        self.stop_min = self.findChild(QComboBox, "stop_min")
        ##set up minutes from 0 to 59
        mins = []
        for min in range(0,60):
            mins.append(min)
            
        self.setup_min.addItems([str(i) for i in mins])
        self.read_min.addItems([str(i) for i in mins])
        self.write_min.addItems([str(i) for i in mins])
        self.stop_min.addItems([str(i) for i in mins])
        
        self.setup_hr.currentTextChanged.connect(self.setuphr_changed)
        self.setup_min.currentTextChanged.connect(self.setupmin_changed)
        self.read_hr.currentTextChanged.connect(self.readhr_changed)
        self.read_min.currentTextChanged.connect(self.readmin_changed)
        self.write_hr.currentTextChanged.connect(self.writehr_changed)
        self.write_min.currentTextChanged.connect(self.writemin_changed)
        self.stop_hr.currentTextChanged.connect(self.stophr_changed)
        self.stop_min.currentTextChanged.connect(self.stopmin_changed)
        
        ###Initialise time
        
        
        ####### Time for set up ,read write stop #########
        # setup_time = timedelta(hours=int(self.setup_hr.currentText()), minutes=int(self.setup_min.currentText()))
        # read_time = timedelta(hours=int(self.read_hr.currentText()), minutes=int(self.read_min.currentText()))
        
        # duration = setup_time - read_time
        # print(duration)
        # ####### END Time for set up ,read write stop #########
    
    def setuphr_changed(self):
       self.setup_hr.currentText()
        
        
    def readhr_changed(self):
       self.read_hr.currentText()
        
    def writehr_changed(self):
        self.write_hr.currentText()
        
    def stophr_changed(self):
        self.stop_hr.currentText()
        
    
        
    def setupmin_changed(self):
        self.setup_min.currentText()
        
    def readmin_changed(self):
        self.read_min.currentText()
    
    def writemin_changed(self):
        self.write_min.currentText()
        
    def stopmin_changed(self):
        self.stop_min.currentText()
    
        
       
       
        
    def connect_classroom(self):
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