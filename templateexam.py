from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow,QApplication
import sys
from os import path
from PyQt6.uic import loadUiType
import sqlite3
from datetime import timedelta
from AboutDialog import AboutDialog
FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"exameditor.ui"))



class Main(QMainWindow, FORM_CLASS):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.png'))
        
        about_menu = self.menuBar().addMenu("&About")
        about_action = QAction("Developer", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)
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
        self.schedule_table.setStyleSheet('background-color: #CCEBCB')
        self.schedule_table.setFont(font)
        self.schedule_table.setColumnWidth(0,80)
        self.save_btn = self.findChild(QPushButton, "btn_save_schedule")
        ##set up minutes from 0 to 59
        mins = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]

        self.setup_min.addItems([i for i in mins])
        self.read_min.addItems([i for i in mins])
        self.write_min.addItems([i for i in mins])
        self.stop_min.addItems([i for i in mins])
        self.connect_database()
        ###Initialise time
        self.load_examsession()
        self.save_btn.clicked.connect(self.insert_examsession)
        self.ChangeSession.clicked.connect(self.load_examsession)
        
        ####### Time for set up ,read write stop #########
        
        # ####### END Time for set up ,read write stop #########
    
    
    def show_about(self):
        dlg = AboutDialog()
        dlg.exec()
        
    def load_examsession(self):
        try: 
            session = self.session_menu.currentText()
            cursor1 = db.cursor()
            query1 = f''' Select * from Exam_Session WHERE session= {session} '''
            result = cursor1.execute(query1)
            self.schedule_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.schedule_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.schedule_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            print("Error occurred", e)
        
            

    def insert_examsession(self):
        session = self.session_menu.currentText()
        cursor = db.cursor()
        
        ##### Calculate the duration of the exam
        
        setup_time = timedelta(hours=float(self.setup_hr.currentText()), minutes=float(self.setup_min.currentText()))
        read_time = timedelta(hours=float(self.read_hr.currentText()), minutes=float(self.read_min.currentText()))
        written_time = timedelta(hours=float(self.write_hr.currentText()), minutes=float(self.write_min.currentText()))
        stoppage_time = timedelta(hours=float(self.stop_hr.currentText()), minutes=float(self.stop_min.currentText()))
        total_read_to_written_time = written_time - read_time
        duration = str(stoppage_time - written_time + total_read_to_written_time)

        set_up_hr = self.setup_hr.currentText()
        set_up_min = self.setup_min.currentText()
        read_hr = self.read_hr.currentText()
        read_min = self.read_min.currentText()
        written_hr = self.write_hr.currentText()
        written_min = self.write_min.currentText()
        stop_hr = self.stop_hr.currentText()
        stop_min = self.stop_min.currentText()

        setup = f"{set_up_hr}:{set_up_min}"
        read = f"{read_hr}:{read_min}"
        write = f"{written_hr}:{written_min}"
        stop = f"{stop_hr}:{stop_min}"
        
        row = (session, setup, read, write, stop, duration)
        
        query = """ INSERT INTO Exam_Session (session, setup_time, read_time, write_time, stop_time, duration)
                    VALUES (?,?,?,?,?,?)"""
        
        cursor.execute(query,row)
        db.commit()
       
        
        self.setup_hr.setCurrentIndex(0)
        self.setup_min.setCurrentIndex(0)
        self.read_hr.setCurrentIndex(0)
        self.read_min.setCurrentIndex(0)
        self.write_hr.setCurrentIndex(0)
        self.write_min.setCurrentIndex(0)
        self.stop_hr.setCurrentIndex(0)
        self.stop_min.setCurrentIndex(0)
        self.load_examsession()
        cursor.close()
       
                    
    def connect_database(self):
           
            cursor = db.cursor()
            query = ''' Select * from classroom '''
            result = cursor.execute(query)
            self.examroom_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.examroom_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.examroom_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

## Connect to database
db = sqlite3.connect("mhsexam.db", timeout=1)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()