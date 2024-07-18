from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from os import path
from PyQt6.uic import loadUiType
import sqlite3
from datetime import timedelta
from AboutDialog import AboutDialog
from InsertExamDialog import InsertExamDialog
FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"exameditor.ui"))



class Main(QMainWindow, FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('logo.png'))
        self.context_menu = QMenu(self)
        
        
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
        
        self.subject_table = self.findChild(QTableWidget, "subject_table")
        item = QTableWidgetItem('Subject')
        item.setForeground(QBrush(QColor(0,255,0)))
        self.subject_table.setStyleSheet('background-color:#FDCBC8')
        self.subject_table.setFont(font)
        self.subject_table.setColumnWidth(0,80)
        self.subject_table.setColumnWidth(1,60)
        self.subject_table.setColumnWidth(2,60)
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
        # Initialise Qdialog Item from InsertExamDialog ###
        self.date = self.findChild(QDateEdit, "date")
        self.day = self.findChild(QComboBox, "comboBox_day")
        self.room = self.findChild(QComboBox, "comboBox_room")
        self.subject = self.findChild(QComboBox, "comboBox_subject")
        self.timeid = self.findChild(QLineEdit, "lineEdit_timeID")
        # End Qdialog Item from InsertExamDialog ###
        
        self.session_menu = self.findChild(QComboBox, "session_menu")
        self.schedule_table = self.findChild(QTableWidget, "schedule_table")
        self.schedule_table.setStyleSheet('background-color: #CCEBCB')
        self.schedule_table.setFont(font)
        self.schedule_table.setColumnWidth(0,50)
        self.schedule_table.setColumnWidth(1,50)
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
        self.session_menu.currentTextChanged.connect(self.load_examsession)
        
        ####### User insert exam date dialog #########
        self.addExam_btn.clicked.connect(self.add_exam_table)
        ####### END User insert exam date dialog #########
        self.context_menu = QMenu(self)
        remove = self.context_menu.addAction("Remove record")
        remove.triggered.connect(self.delete_examsession)
        
        
        
        
    def add_exam_table(self):
        exam_dialog  = InsertExamDialog()
        exam_dialog.exec()
    
    def show_about(self):
        dlg = AboutDialog()
        dlg.exec()
    
    def contextMenuEvent(self, event):
        # Show the context menu
        self.context_menu.exec(event.globalPos())
    def load_examsession(self):
        try: 
            session = self.session_menu.currentText()
            query1 = f''' Select * from Exam_Session WHERE session= {session} '''
            result = cursor.execute(query1)
            self.schedule_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.schedule_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.schedule_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            print("Error occurred", e)
            
    def delete_examsession(self):
            
            selected_row = self.schedule_table.currentRow()
            if selected_row > 0: 
                item = str(self.schedule_table.item(selected_row,0).text())
                msg = QMessageBox.question(self, 'Confirmation', 'Are you sure want to delete this record', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    
                if msg ==  QMessageBox.StandardButton.Yes:
                    
                    qry = 'DELETE FROM Exam_Session WHERE time_id=?'
                    cursor.execute(qry,(item,))
                    db.commit()
                    self.load_examsession()     
    def remove_examsession(self):
        selected_row = self.schedule_table.currentRow()
        item = str(self.schedule_table.item(selected_row,0))
        if item == None:
            if selected_row < 0:
                
                QMessageBox.warning(self, 'Warning', 'TChoose record to delete')
        else:
            item = str(self.schedule_table.item(selected_row,0).text())
            msg = QMessageBox.question(self, 'Confirmation', 'Are you sure want to delete this record', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
            if msg ==  QMessageBox.StandardButton.Yes: 
                
                qry = 'DELETE FROM Exam_Session WHERE time_id=?'
                cursor.execute(qry,(item,))
                db.commit()
                self.load_examsession()      
            
    def insert_examsession(self):
        session = self.session_menu.currentText()
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
                    VALUES (?,?,?,?,?,?) """
        
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
    def connect_database(self):
            
            query = ''' Select * from classroom '''
            result = cursor.execute(query)
            self.examroom_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.examroom_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.examroom_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            
            query1 = '''SELECT 
                            s.subject_code,
                            s.class,
                            t.teacher_id
                        FROM
                            Subjects s
                            INNER JOIN Teachers_Subjects t ON s.subject_id = t.subject_id 
                            ORDER BY s.subject_id DESC
                            '''
            result1 = cursor.execute(query1)
            self.subject_table.setRowCount(0)
            for row_number, row_data in enumerate(result1):
                self.subject_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.subject_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
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
  
## Connect to database
db = sqlite3.connect("mhsexam.db", timeout=1)
cursor = db.cursor()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()
    