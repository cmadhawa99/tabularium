from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLineEdit, QDateEdit, QComboBox, QPushButton,
                             QLabel, QFrame, QMessageBox, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from app.settings_manager import settings

class AddFilePage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def create_glass_panel(self):
        frame = QFrame()
        frame.setObjectName("Card")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 30))
        frame.setGraphicsEffect(shadow)
        return frame

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        header = QLabel("Add New File Record")
        header.setObjectName("PageTitle")
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        form_frame = self.create_glass_panel()
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(30)

        def add_field(label_text, widget, row, col, width=1):
            lbl = QLabel(label_text)
            form_layout.addWidget(lbl, row, col)
            form_layout.addWidget(widget, row + 1, col, 1, width)

        self.inp_rr = QLineEdit()
        self.inp_rr.setPlaceholderText("Ex: RR-2024-001")
        add_field("RR Number *", self.inp_rr, 0, 0)

        self.inp_serial = QLineEdit()
        self.inp_serial.setPlaceholderText("Auto-generated or Manual")
        add_field("Serial Number", self.inp_serial, 0, 1)

        self.inp_sector = QComboBox()
        self.inp_sector.addItems(settings.get("master_data", "sectors"))
        add_field("Sector", self.inp_sector, 2, 0)

        self.inp_subject = QLineEdit()
        add_field("Subject Number", self.inp_subject, 2, 1)

        self.inp_name = QLineEdit()
        add_field("File Name *", self.inp_name, 4, 0, 2)

        self.inp_type = QComboBox()
        self.inp_type.addItems(settings.get("master_data", "file_types"))
        add_field("File Type", self.inp_type, 6, 0)

        self.inp_pages = QLineEdit()
        add_field("Total Pages", self.inp_pages, 6, 1)

        self.inp_start = QDateEdit()
        self.inp_start.setDisplayFormat("yyyy-MM-dd")
        self.inp_start.setCalendarPopup(True)
        self.inp_start.setDate(QDate.currentDate())
        add_field("Start Date", self.inp_start, 8, 0)

        self.inp_end = QDateEdit()
        self.inp_end.setDisplayFormat("yyyy-MM-dd")
        self.inp_end.setCalendarPopup(True)
        self.inp_end.setDate(QDate.currentDate())
        add_field("End Date", self.inp_end, 8, 1)

        self.inp_shelf = QLineEdit()
        add_field("Shelf No", self.inp_shelf, 10, 0)

        self.inp_deck = QLineEdit()
        add_field("Deck No", self.inp_deck, 10, 1)

        self.inp_file_no = QLineEdit()
        add_field("File No", self.inp_file_no, 10, 2)

        content_layout.addWidget(form_frame)
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        btn_layout = QHBoxLayout()

        self.btn_clear = QPushButton("Clear Form")
        self.btn_clear.setFixedSize(120, 40)
        self.btn_clear.setObjectName("GlassButton")
        self.btn_clear.clicked.connect(self.clear_form)

        self.btn_save = QPushButton("Save Record")
        self.btn_save.setFixedSize(150, 40)
        self.btn_save.setObjectName("PrimaryActionBtn")
        self.btn_save.clicked.connect(self.save_data)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def save_data(self):
        if not self.inp_rr.text().strip() or not self.inp_name.text().strip():
            QMessageBox.warning(self, "Validation Error", "RR Number and File Name are required!")
            return

        data = {
            "rr_number": self.inp_rr.text().strip(),
            "serial_number": int(self.inp_serial.text()) if self.inp_serial.text().isdigit() else None,
            "sector": self.inp_sector.currentText(),
            "subject_number": self.inp_subject.text(),
            "file_name": self.inp_name.text(),
            "file_type": self.inp_type.currentText(),
            "start_date": self.inp_start.date().toPyDate(),
            "end_date": self.inp_end.date().toPyDate(),
            "total_pages": int(self.inp_pages.text()) if self.inp_pages.text().isdigit() else 0,
            "shelf_number": int(self.inp_shelf.text()) if self.inp_shelf.text().isdigit() else None,
            "deck_number": int(self.inp_deck.text()) if self.inp_deck.text().isdigit() else None,
            "file_number": int(self.inp_file_no.text()) if self.inp_file_no.text().isdigit() else None,
        }

        success, message = self.controller.add_new_file(data)

        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_form()
        else:
            QMessageBox.critical(self, "Error", message)

    def clear_form(self):
        self.inp_rr.clear()
        self.inp_serial.clear()
        self.inp_subject.clear()
        self.inp_name.clear()
        self.inp_pages.clear()
        self.inp_shelf.clear()
        self.inp_deck.clear()
        self.inp_file_no.clear()
        self.inp_sector.setCurrentIndex(0)
        self.inp_type.setCurrentIndex(0)
        self.inp_rr.setFocus()