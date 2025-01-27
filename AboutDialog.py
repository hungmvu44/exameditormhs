from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(500)
        self.setFixedHeight(250)
        self.setWindowTitle("About")
        QBtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        font = QFont("Roboto", 13)
        font.setBold(True)
        copyright_label = QLabel("Copyright© by Andy VU Melbourne High School")
        copyright_label.setFont(font)
        layout = QVBoxLayout()
        labelpic = QLabel()
        pixmap = QPixmap('logo.png')
        pixmap = pixmap.scaledToHeight(120)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedWidth(120)

        layout.addWidget(copyright_label)
        layout.addWidget(labelpic)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)