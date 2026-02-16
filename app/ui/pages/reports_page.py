from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QGroupBox, QRadioButton, QPushButton, QLabel,
                             QLineEdit, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import qtawesome as qta
import os
import csv
import subprocess
from datetime import datetime
from app.settings_manager import settings

class ReportsPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.last_generated_excel = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Header
        title = QLabel ("Reports & Data Exports")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        # Data source selection
        # -------------------------------------------------------------------------------------
        grp_source = QGroupBox("1. Select Data Source")
        source_layout = QVBoxLayout(grp_source)

        self.rad_files = QRadioButton("File Records (Main Archive Inventory")
        self.rad_files.setChecked(True)
        self.rad_borrow = QRadioButton("Circulation History (Borrow/Return Logs)")

        source_layout.addWidget(self.rad_files)
        source_layout.addWidget(self.rad_borrow)
        layout.addWidget(grp_source)

        # Export Format
        # -------------------------------------------------------------------------------------
        grp_format = QGroupBox("2. Select Format")
        format_layout = QHBoxLayout(grp_format)

        self.rad_xlsx = QRadioButton("Excel (.xlsx)")
        self.rad_xlsx.setChecked(True)
        self.rad_csv = QRadioButton("CSV (.csv)")
        self.rad_sql = QRadioButton("SQL Database Dump (.sql)")

        format_layout.addWidget(self.rad_xlsx)
        format_layout.addWidget(self.rad_csv)
        format_layout.addWidget(self.rad_sql)
        layout.addWidget(grp_format)

        # Save Location
        # -------------------------------------------------------------------------------------
        grp_loc = QGroupBox("3. Select Save Location")
        loc_layout = QHBoxLayout(grp_loc)

        self.txt_path = QLineEdit(settings.get("backup", "backup_path"))
        btn_browse = QPushButton("Browse...")
        btn_browse.setIcon(qta.icon('fa5s.folder-open'))
        btn_browse.clicked.connect(self.browse_folder)

        loc_layout.addWidget(self.txt_path)
        loc_layout.addWidget(btn_browse)
        layout.addWidget(grp_loc)

        # Action Buttons
        # -------------------------------------------------------------------------------------
        action_layout = QHBoxLayout()

        self.btn_export = QPushButton(" Generate Export")
        self.btn_export.setIcon(qta.icon('fa5s.download', color='white'))
        self.btn_export.setFixedSize(200, 50)
        self.btn_export.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_export.clicked.connect(self.generate_export)

        self.btn_print = QPushButton(" Print Latest Excel")
        self.btn_print.setIcon(qta.icon('fa5s.print', color='white'))
        self.btn_print.setFixedSize(200, 50)
        self.btn_print.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_print.clicked.connect(self.print_excel)
        self.btn_print.setEnabled(False)

        action_layout.addStretch()
        action_layout.addWidget(self.btn_export)
        action_layout.addWidget(self.btn_print)
        action_layout.addStretch()

        layout.addLayout(action_layout)
        layout.addStretch()


    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
        if folder:
            self.txt_path.setText(folder)
            settings.set("backup", "backup_path", folder)

    def generate_export(self):
        path = self.txt_path.text()
        if not os.path.exists(path):
            QMessageBox.warning(self, "Invalid Path", "The selected save location does not exist.")
            return

        # Determine Data Source
        # -------------------------------------------------------------------------------------
        is_files = self.rad_files.isChecked()
        prefix = "FileRecords" if is_files else "BorrowHistory"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # I) SQL Dump
        # -------------------------------------------------------------------------------------
        if self.rad_sql.isChecked():
            filename = os.path.join(path, f"{prefix}_{timestamp}.sql")
            self.export_sql(filename, is_files)
            return

        # Get Data for CSV/XLSX
        # -------------------------------------------------------------------------------------
        if is_files:
            records = self.controller.search_files("")  # Gets all files
            headers = ["RR Number", "Serial", "Sector", "Subject", "File Name", "File Type", "Start Date", "End Date",
                       "Shelf", "Deck", "Status"]
            data_rows = [[r.rr_number, r.serial_number, r.sector, r.subject_number, r.file_name, r.file_type, r.start_date, r.end_date, r.shelf_number, r.deck_number, r.current_status] for r in records]
        else:
            records = self.controller.get_all_borrow_records()
            headers = ["RR Number", "Borrower Name", "Borrowed Date", "Returned Date", "Status"]
            data_rows = [[r.file_rr_number, r.borrower_name, r.borrowed_date, r.returned_date, "Returned" if r.is_returned else "Borrowed"] for r in records]

        # II) CSV Export
        # -------------------------------------------------------------------------------------
        if self.rad_csv.isChecked():
            filename = os.path.join(path, f"{prefix}_{timestamp}.csv")
            self.export_csv(filename, headers, data_rows)

        #) III) XLSX Export
        # -------------------------------------------------------------------------------------
        if self.rad_xlsx.isChecked():
            filename = os.path.join(path, f"{prefix}_{timestamp}.xlsx")
            self.export_csv(filename, headers, data_rows)


    def export_csv(self, filename, headers, data_rows):
        try:
            with open(filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data_rows)
            QMessageBox.information(self, "Success", f"CSV Exported successfully to:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def export_xlsx(self, filename, headers, data_rows):
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Report Data"

            ws.append(headers)
            for row in data_rows:
                ws.append(row)

            wb.save(filename)

            self.last_generated_excel = filename
            self.btn_print.setEnabled(True)

            QMessageBox.information(self, "Success",f"Excel Exported successfully to:\n{filename}\n\nYou can now use the Print button.")

        except ImportError:
            QMessageBox.warning(self, "Missing Library","Please run 'pip install openpyxl' in your terminal to export Excel files.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def export_sql(self, filename, is_files):
        """
        Runs pg_dump
        Requires PostgreSQL 'pg_dump' to be in system PATH
        """

        table_name = "file_records" if is_files else "borrow_records"

        try:
            cmd = [
                "pg_dump"
                "-U", "postgres",
                "-h", "localhost",
                "-d", "archive_db",
                "-t", table_name,
                "-f", filename,
            ]

            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.run(cmd, check=True, startupinfo=si)
            QMessageBox.information(self, "Success", f"SQL Dump created at:\n{filename}")

        except FileNotFoundError:
            QMessageBox.critical(self, "PostgreSQL Error", "Could not find 'pg_dump'. Ensure PostgreSQL is installed and added to Windows PATH.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to dump SQL: {str(e)}")


    def print_excel(self):

        if not self.last_generated_excel or not os.path.exists(self.last_generated_excel):
            QMessageBox.warning(self, "Printing", "The file has been sent to your default LAN printer")
            return

        try:
            os.startfile(self.last_generated_excel, "print")
            QMessageBox.information(self, "Printing", "The file has been sent to your default LAN printer.")
        except Exception as e:
            QMessageBox.critical(self, "Print Error",f"Failed to print. Make sure Microsoft Excel is installed.\nError: {e}")
