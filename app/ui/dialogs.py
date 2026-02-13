from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel,
                             QPushButton, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt


class FileDetailDialog(QDialog):
    def __init__(self, file_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Details: {file_data.rr_number}")
        self.setFixedSize(600, 700)
        self.setStyleSheet("background-color: #2c3e50; color: white; font-size: 14px;")

        layout = QVBoxLayout(self)

        # Header
        title = QLabel(file_data.file_name)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px; color: #4d7cfe;")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Content Container
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #34495e; border-radius: 10px; padding: 10px;")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)

        # Helper to add rows
        def add_row(label, value):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #95a5a6; font-weight: bold;")
            val = QLabel(str(value) if value else "-")
            val.setStyleSheet("color: white; font-weight: normal;")
            val.setWordWrap(True)
            form_layout.addRow(lbl, val)

        # --- DATA FIELDS ---
        add_row("RR Number:", file_data.rr_number)
        add_row("Serial Number:", file_data.serial_number)
        add_row("Current Status:", file_data.current_status)

        # Separator
        form_layout.addRow(QLabel("-------------------------------------------------"), QLabel(""))

        add_row("Sector:", file_data.sector)
        add_row("Subject No:", file_data.subject_number)
        add_row("File Type:", file_data.file_type)
        add_row("Total Pages:", file_data.total_pages)

        # Dates
        add_row("Start Date:", file_data.start_date)
        add_row("End Date:", file_data.end_date)

        # Location
        loc_str = f"Shelf: {file_data.shelf_number} | Deck: {file_data.deck_number} | File No: {file_data.file_number}"
        add_row("Location:", loc_str)

        layout.addWidget(form_frame)

        # Close Button
        btn_close = QPushButton("Close")
        btn_close.setFixedHeight(40)
        btn_close.setStyleSheet("background-color: #e74c3c; border: none; border-radius: 5px; font-weight: bold;")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)