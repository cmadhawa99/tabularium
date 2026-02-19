from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel,
                             QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor
import qtawesome as qta


class DisposalPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_rr = None
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

        title = QLabel("File Disposal & Archiving")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        search_frame = self.create_glass_panel()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(20, 20, 20, 20)

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Enter RR Number to Manage (e.g., RR-2024-001)...")
        self.inp_search.setFixedHeight(40)
        self.inp_search.returnPressed.connect(self.lookup_file)

        btn_search = QPushButton(" Find File")
        btn_search.setIcon(qta.icon('fa5s.search', color='white'))
        btn_search.setObjectName("PrimaryActionBtn")
        btn_search.setFixedHeight(40)
        btn_search.clicked.connect(self.lookup_file)

        search_layout.addWidget(self.inp_search)
        search_layout.addWidget(btn_search)
        layout.addWidget(search_frame)

        details_frame = self.create_glass_panel()
        details_layout = QFormLayout(details_frame)
        details_layout.setContentsMargins(20, 20, 20, 20)

        lbl_details_title = QLabel("File Details", objectName="CardTitle")
        details_layout.addRow(lbl_details_title)

        self.lbl_name = QLabel("-")
        self.lbl_status = QLabel("-")
        self.lbl_removed_status = QLabel("-")
        self.lbl_removed_status.setStyleSheet("font-weight: bold;")

        details_layout.addRow("File Name:", self.lbl_name)
        details_layout.addRow("Current Status:", self.lbl_status)
        details_layout.addRow("Removal Status:", self.lbl_removed_status)
        layout.addWidget(details_frame)

        self.grp_schedule = self.create_glass_panel()
        sch_layout = QHBoxLayout(self.grp_schedule)
        sch_layout.setContentsMargins(20, 20, 20, 20)

        lbl_sch_title = QLabel("Schedule Removal", objectName="CardTitle")
        self.inp_date = QDateEdit()
        self.inp_date.setCalendarPopup(True)
        self.inp_date.setDate(QDate.currentDate())

        btn_update_schedule = QPushButton(" Update Schedule")
        btn_update_schedule.setIcon(qta.icon('fa5s.calendar-alt', color='white'))
        btn_update_schedule.setObjectName("PrimaryActionBtn")
        btn_update_schedule.clicked.connect(self.update_schedule)

        sch_layout.addWidget(lbl_sch_title)
        sch_layout.addWidget(self.inp_date)
        sch_layout.addWidget(btn_update_schedule)
        layout.addWidget(self.grp_schedule)

        self.grp_remove = self.create_glass_panel()
        rem_layout = QVBoxLayout(self.grp_remove)
        rem_layout.setContentsMargins(20, 20, 20, 20)

        lbl_rem_title = QLabel("Permanent Removal", objectName="CardTitle")
        lbl_warning = QLabel("WARNING: This action cannot be undone. The file record will be locked.")
        lbl_warning.setStyleSheet("color: #e74c3c; font-style: italic;")

        self.btn_remove = QPushButton(" MARK AS REMOVED (PERMANENT)")
        self.btn_remove.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        self.btn_remove.setFixedHeight(45)
        self.btn_remove.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 8px; font-weight: bold;")
        self.btn_remove.clicked.connect(self.confirm_removal)

        rem_layout.addWidget(lbl_rem_title)
        rem_layout.addWidget(lbl_warning)
        rem_layout.addWidget(self.btn_remove)
        layout.addWidget(self.grp_remove)

        layout.addStretch()
        self.set_actions_enabled(False)

    def lookup_file(self):
        rr = self.inp_search.text().strip()
        if not rr: return

        results = self.controller.search_files(rr)
        found = next((f for f in results if f.rr_number.lower() == rr.lower()), None)

        if found:
            self.current_rr = found.rr_number
            self.lbl_name.setText(found.file_name)
            self.lbl_status.setText(found.current_status)

            if found.is_removed:
                self.lbl_removed_status.setText("REMOVED (LOCKED)")
                self.lbl_removed_status.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")
                self.set_actions_enabled(False)
                self.inp_date.setDate(QDate.currentDate())
                if found.removed_date:
                    self.lbl_removed_status.setText(f"REMOVED ON {found.removed_date}")
            else:
                self.lbl_removed_status.setText("Active Record")
                self.lbl_removed_status.setStyleSheet("color: #2ecc71; font-weight: bold;")
                self.set_actions_enabled(True)

                if found.to_be_removed_date:
                    py_date = found.to_be_removed_date
                    q_date = QDate(py_date.year, py_date.month, py_date.day)
                    self.inp_date.setDate(q_date)
                else:
                    self.inp_date.setDate(QDate.currentDate())
        else:
            QMessageBox.warning(self, "Not Found", "File Not Found")
            self.current_rr = None
            self.lbl_name.setText("-")
            self.lbl_status.setText("-")
            self.set_actions_enabled(False)

    def set_actions_enabled(self, enabled):
        self.grp_schedule.setEnabled(enabled)
        self.grp_remove.setEnabled(enabled)

    def update_schedule(self):
        if not self.current_rr: return
        date_val = self.inp_date.date().toPyDate()
        success, msg = self.controller.schedule_removal(self.current_rr, date_val)
        if success:
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.critical(self, "Error", msg)

    def confirm_removal(self):
        if not self.current_rr: return
        reply = QMessageBox.question(self, "Confirm Removal",
                                     "Are you sure you want to mark this file as REMOVED?\n\nThis cannot be undone and will lock the record.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.controller.confirm_removal(self.current_rr)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.lookup_file()
            else:
                QMessageBox.critical(self, "Error", msg)