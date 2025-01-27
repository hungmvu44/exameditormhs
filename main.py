import os
import sys
import sqlite3
import win32api
import tempfile
import subprocess
from os import path
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from docx2pdf import convert
from PyQt6.QtWidgets import *
from datetime import timedelta
from PIL.ImageQt import ImageQt
from docxtpl import DocxTemplate
from PyQt6.QtGui import QPainter
from PyQt6.uic import loadUiType
from AboutDialog import AboutDialog
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtGui import QPainter
from pdf2image import convert_from_path
from InsertExamDialog import InsertExamDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
FORM_CLASS,_ = loadUiType(path.join(path.dirname('__file__'),"exameditor - Copy.ui"))
data = []
EXAM_TABLE_COLUMN = 13


class Main(QMainWindow, FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()
        self.selected_row_data = {}
        self.setWindowIcon(QIcon('logon.png'))
        self.context_menu = QMenu(self)
        print_menu = self.menuBar().addMenu("&Print")
        print_action1 = QAction("Print Selected", self)
        print_action1.triggered.connect(self.print_selected_exam)
        print_menu.addAction(print_action1)
        print_action2 = QAction("Print All", self)
        print_action2.triggered.connect(self.print_exams)
        print_menu.addAction(print_action2)

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
        exam_table = self.findChild(QTableWidget,"exam_table")
        exam_table.setStyleSheet('background-color:#ADD8E6')
        exam_table.setColumnWidth(2,60)
        exam_table.setColumnWidth(3,60)
        exam_table.setColumnWidth(4,50)
        exam_table.setColumnWidth(5,60)
        exam_table.setColumnWidth(6,60)
        exam_table.setColumnWidth(7,60)
        exam_table.setColumnWidth(8,60)
        exam_table.setColumnWidth(9,60)
        exam_table.setColumnWidth(10,80)
        exam_table.setColumnWidth(11,205)
        exam_table.setColumnWidth(12,230)
        exam_table.cellClicked.connect(self.on_cell_click)
        
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
        remove = self.context_menu.addAction("Remove TimeID")
        remove.triggered.connect(self.remove_examsession)
        self.connect_exam()

    def print_pdf(self):
        file_path = os.path.join(os.getcwd(),"temp.pdf")
        # pdf_document = QPdfDocument(self)
        # pdf_document.load(file_path)

        # Setup printer
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(file_path, dpi=300, output_folder=path, poppler_path = r"C:\Users\PMYLS\Desktop\Softwares\Installed\poppler-24.08.0\Library\bin")
                print(len(images))
                painter = QPainter()
                painter.begin(printer)
                for i, image in enumerate(images):
                    if i > 0:
                        break
                        print("Adding new_page")
                        printer.newPage()
                    rect = painter.viewport()
                    qtImage = ImageQt(image)
                    qtImageScaled = qtImage.scaled(rect.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    painter.drawImage(rect, qtImageScaled)
                painter.end()

    def on_cell_click(self, row, column):
        print(f"Clicked on cell at row {row}, column {column}")
        exam_table = self.findChild(QTableWidget,"exam_table")
        # Retrieve and print all the items in the selected row
        row_data = []
        for col in range(exam_table.columnCount()):
            item = exam_table.item(row, col)
            if item:
                row_data.append(item.text())
        self.selected_row_data = row_data


    def get_teacher_name_by_id(self, teacher_id):
        query = f''' Select first_name, last_name from Teachers WHERE teacher_id="{teacher_id}" '''
        result = cursor.execute(query)
        for row in result:
            return f"{row[0]} {row[1]}"

    def create_context(self):
        context_list = []
        for i, exam in enumerate(self.exam_table_data):
            context = {
                        "date": exam[0], "day": exam[1], "room_value": exam[2], 
                        "Subject": exam[3], "teacher_name": self.get_teacher_name_by_id(exam[9]),
                        "year": exam[0][-4:], "class": exam[7],
                        "session": exam[6], "number": exam[10], 
                    }
            exam_session = self.get_examsession(context["session"], exam[5])
            for session in exam_session:                
                context |= {"duration": session[6], "start_time": session[2], "Read_time": session[3], "Write_time": session[4],
                        "Stop_time": session[5]}
                break
            # return context
            context_list.append(context)
        return context_list

    def create_context2(self, exam):
        context = {
                    "date": exam[0], "day": exam[1], "room_value": exam[2], 
                    "Subject": exam[3], "teacher_name": self.get_teacher_name_by_id(exam[9]),
                    "year": exam[0][-4:], "class": exam[7],
                    "session": exam[6], "number": exam[10], 
                }
        exam_session = self.get_examsession(context["session"], exam[5])
        for session in exam_session:                
            context |= {"duration": session[6], "start_time": session[2], "Read_time": session[3], "Write_time": session[4],
                    "Stop_time": session[5]}
            break
        return context

    def command_print(self, event=None):
        try:
            win32api.ShellExecute(0, "print", "temp.pdf", None, ".", 0)
        except Exception as e:
            print(f"Error during printing: {e}")


    def print_exams(self):
        print("Printing Exams..")
        contexts = self.create_context()
        for context in contexts:
            try:
                doc = DocxTemplate("MELBOURNE HIGH SCHOOL.docx")
                doc.render(context)
                name = f"temp.docx"
                doc.save(name)
                convert(name)
                # self.command_print()
                self.print_pdf()
            finally:
                for file in [name, "temp.pdf"]:
                    if os.path.exists(file):
                        os.remove(file)


    def print_selected_exam(self):
        print("Printing Exams..")
        if self.selected_row_data == {}:
            print("No Row or Cell Selected..")
            return
        context = self.create_context2(self.selected_row_data)
        try:
            doc = DocxTemplate("MELBOURNE HIGH SCHOOL.docx")
            doc.render(context)
            name = f"temp.docx"
            doc.save(name)
            convert(name)
            # self.command_print()
            self.print_pdf()
        finally:
            for file in [name, "temp.pdf"]:
                if os.path.exists(file):
                    os.remove(file)


    def add_exam_table(self):
        self.connect_exam()
        exam_dialog  = InsertExamDialog()
        exam_dialog.exec()
    
    def show_about(self):
        dlg = AboutDialog()
        dlg.exec()
    
    def contextMenuEvent(self, event):
        # Show the context menu
        self.context_menu.exec(event.globalPos())

    def get_examsession(self, session, time_id=None):
        if time_id is None:
            query = f''' Select * from Exam_Session WHERE session= {session} '''
        else:
            query = f''' Select * from Exam_Session WHERE session= {session} and time_id={time_id} '''
        return cursor.execute(query)

    def load_examsession(self):
        try: 
            session = self.session_menu.currentText()
            result = self.get_examsession(session)
            self.schedule_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.schedule_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.schedule_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            print("Error occurred", e)
             
    def remove_examsession(self):
        selected_row = self.schedule_table.currentRow()
        item = str(self.schedule_table.item(selected_row,0))
        
        if selected_row <= 0:
                QMessageBox.warning(self, 'Warning', 'Choose timeID to delete')
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
    
    def connect_exam(self):
      query = ''' 
            
            SELECT  e.Exam_Date, e.Day as ExamDay, e.Room, e.Subject, e.Groupe, es.time_id, es.session, s.class, s.subject_code as subject_code, ts.teacher_id, COUNT(st.student_id), MIN(ss.Firstname || " " || ss.Surname) as FirstStudent, MAX(ss.Firstname || " " || ss.Surname) as LastStudent
            FROM Exam e 
            LEFT JOIN Exam_Session es ON es.time_id = e.TimeID
            LEFT JOIN Subjects s ON  s.subject_id = e.Subject 
            LEFT JOIN Teachers_Subjects ts ON ts.subject_id = s.subject_id
            LEFT JOIN Students_Subjects ss ON ss.subject_id = s.subject_id
            LEFT JOIN Students st ON st.student_id = ss.Student_id 
            GROUP BY e.Exam_Date, e.Day, e.Room, e.Subject, e.Groupe, es.time_id, es.session, s.subject_code, s.class, ts.teacher_id
            '''
      result = cursor.execute(query)
      self.exam_table_data = [row for row in result]
      self.exam_table.setRowCount(0)
      for row_number, row_data in enumerate(self.exam_table_data):
            self.exam_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
               self.exam_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))  
      
## Connect to database
db = sqlite3.connect("mhsexam.db", timeout=1)
cursor = db.cursor()


if __name__ == '__main__':
    # template_loader = jinja2.FileSystemLoader('./')
    # template_env = jinja2.Environment(loader=template_loader)
    # context = {}
    # html_template = 'index.html'
    # template = template_env.get_template(html_template)
    # output_text = template.render(context)

    # config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # output_pdf = 'pdf_generated.pdf'
    # pdfkit.from_string(output_text, output_pdf, configuration=config)
    
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()
    