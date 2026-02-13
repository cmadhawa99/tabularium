from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QDateEdit, QPushButton, QLabel,
                             QTabWidget, QMessageBox, QFrame, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor, QBrush
import qtawesome as qta
import math


class CirculationPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Pagination State
        self.current_page = 1
        self.page_size = 50
        self.total_records = 0

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        title = QLabel("Circulation Management")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #3f3f5f; top: -1px; }
            QTabBar::tab { padding: 10px 20px; font-weight: bold; }
            QTabBar::tab:selected { background: #4d7cfe; color: white; }
        """)

        self.tabs.addTab(self.create_borrow_tab(), "Issue File (Borrow)")
        self.tabs.addTab(self.create_return_tab(), "Receive File (Return)")
        self.tabs.addTab(self.create_history_tab(), "History & Logs")  # <--- NEW TAB

        layout.addWidget(self.tabs)

    # --- TAB 1: BORROW ---
    def create_borrow_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #27293d; border-radius: 10px; padding: 20px;")
        form = QFormLayout(form_frame)
        form.setSpacing(20)

        # RR Number Search
        self.borrow_rr_input = QLineEdit()
        self.borrow_rr_input.setPlaceholderText("Enter RR Number (e.g. RR-2024-001)...")
        self.borrow_rr_input.returnPressed.connect(self.lookup_file_for_borrow)

        btn_check = QPushButton("Check File")
        btn_check.setFixedSize(100, 30)
        btn_check.setStyleSheet("background-color: #3498db; color: white;")
        btn_check.clicked.connect(self.lookup_file_for_borrow)

        rr_layout = QHBoxLayout()
        rr_layout.addWidget(self.borrow_rr_input)
        rr_layout.addWidget(btn_check)

        # Read-Only Info
        self.lbl_file_name = QLabel("-")
        self.lbl_status = QLabel("-")

        # Borrower Details
        self.inp_borrower = QLineEdit()
        self.inp_borrow_date = QDateEdit()
        self.inp_borrow_date.setDate(QDate.currentDate())
        self.inp_borrow_date.setCalendarPopup(True)

        form.addRow("RR Number:", rr_layout)
        form.addRow("File Name:", self.lbl_file_name)
        form.addRow("Current Status:", self.lbl_status)
        form.addRow(QLabel("-----------------"))
        form.addRow("Borrower Name:", self.inp_borrower)
        form.addRow("Date:", self.inp_borrow_date)

        layout.addWidget(form_frame)

        self.btn_issue = QPushButton(" Confirm Issue")
        self.btn_issue.setIcon(qta.icon('fa5s.paper-plane', color='white'))
        self.btn_issue.setFixedSize(200, 50)
        self.btn_issue.setStyleSheet("background-color: #e14eca; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_issue.clicked.connect(self.submit_borrow)
        self.btn_issue.setEnabled(False)

        layout.addWidget(self.btn_issue, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return tab

    # --- TAB 2: RETURN ---
    def create_return_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #27293d; border-radius: 10px; padding: 20px;")
        form = QFormLayout(form_frame)
        form.setSpacing(20)

        self.return_rr_input = QLineEdit()
        self.return_rr_input.setPlaceholderText("Enter RR Number to Return...")
        self.return_rr_input.returnPressed.connect(self.lookup_file_for_return)

        btn_check_ret = QPushButton("Find Loan")
        btn_check_ret.setStyleSheet("background-color: #3498db; color: white;")
        btn_check_ret.clicked.connect(self.lookup_file_for_return)

        ret_layout = QHBoxLayout()
        ret_layout.addWidget(self.return_rr_input)
        ret_layout.addWidget(btn_check_ret)

        self.lbl_ret_name = QLabel("-")
        self.lbl_ret_borrower = QLabel("-")
        self.lbl_ret_date = QLabel("-")

        form.addRow("RR Number:", ret_layout)
        form.addRow("File Name:", self.lbl_ret_name)
        form.addRow("Borrowed By:", self.lbl_ret_borrower)
        form.addRow("Borrowed Date:", self.lbl_ret_date)

        layout.addWidget(form_frame)

        self.btn_return = QPushButton(" Accept Return")
        self.btn_return.setIcon(qta.icon('fa5s.check-circle', color='white'))
        self.btn_return.setFixedSize(200, 50)
        self.btn_return.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_return.clicked.connect(self.submit_return)
        self.btn_return.setEnabled(False)

        layout.addWidget(self.btn_return, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return tab

    # --- TAB 3: HISTORY (NEW) ---
    def create_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # --- TOP BAR: SEARCH & REFRESH ---
        top_bar = QHBoxLayout()

        # Search Input
        self.hist_search_input = QLineEdit()
        self.hist_search_input.setPlaceholderText("Search History by RR Number or Borrower...")
        self.hist_search_input.setFixedWidth(300)
        self.hist_search_input.returnPressed.connect(self.reset_and_load_history)  # Search on Enter

        # Search Button
        btn_search = QPushButton(" Search")
        btn_search.setIcon(qta.icon('fa5s.search', color='white'))
        btn_search.setStyleSheet("background-color: #4d7cfe; color: white; border-radius: 5px;")
        btn_search.clicked.connect(self.reset_and_load_history)

        # Refresh Button
        btn_refresh = QPushButton(" Refresh")
        btn_refresh.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        btn_refresh.setStyleSheet("background-color: #3498db; color: white; border-radius: 5px;")
        btn_refresh.clicked.connect(self.reset_and_load_history)

        top_bar.addWidget(self.hist_search_input)
        top_bar.addWidget(btn_search)
        top_bar.addWidget(btn_refresh)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # --- TABLE ---
        self.hist_table = QTableWidget()
        cols = ["RR Number", "File Name", "Borrower", "Borrowed Date", "Returned Date", "Status"]
        self.hist_table.setColumnCount(len(cols))
        self.hist_table.setHorizontalHeaderLabels(cols)
        self.hist_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.hist_table.setAlternatingRowColors(True)
        self.hist_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.hist_table)

        # --- PAGINATION ---
        pagination_layout = QHBoxLayout()

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(qta.icon('fa5s.chevron-left', color='white'))
        self.btn_prev.setFixedSize(40, 30)
        self.btn_prev.setStyleSheet("background-color: #2b3553; border-radius: 5px;")
        self.btn_prev.clicked.connect(self.prev_page)

        self.lbl_page_info = QLabel("Page 1 of ?")
        self.lbl_page_info.setStyleSheet("font-weight: bold; margin: 0 15px;")

        self.lbl_total_records = QLabel("Total: 0")
        self.lbl_total_records.setStyleSheet("color: #8f9bb3; margin-right: 20px;")

        self.btn_next = QPushButton()
        self.btn_next.setIcon(qta.icon('fa5s.chevron-right', color='white'))
        self.btn_next.setFixedSize(40, 30)
        self.btn_next.setStyleSheet("background-color: #2b3553; border-radius: 5px;")
        self.btn_next.clicked.connect(self.next_page)

        pagination_layout.addStretch()
        pagination_layout.addWidget(self.lbl_total_records)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.lbl_page_info)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addStretch()

        layout.addLayout(pagination_layout)

        # Load initial data
        self.load_history_data()

        return tab

    # --- LOGIC ---

    def load_history_data(self):
        """Fetches data for the current page and updates table"""
        # Get Search Text
        search_text = self.hist_search_input.text().strip()

        # Pass search_text to controller
        records, total = self.controller.get_circulation_history(self.current_page, self.page_size, search_text)
        self.total_records = total

        # Update Table (Same as before)
        self.hist_table.setRowCount(0)
        for row_idx, record in enumerate(records):
            self.hist_table.insertRow(row_idx)

            file_name = record.file.file_name if record.file else "Unknown File"

            def add_item(col, text, color=None):
                item = QTableWidgetItem(str(text) if text else "-")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if color:
                    item.setForeground(QBrush(QColor(color)))
                self.hist_table.setItem(row_idx, col, item)

            add_item(0, record.file_rr_number)
            add_item(1, file_name)
            add_item(2, record.borrower_name)
            add_item(3, record.borrowed_date)
            add_item(4, record.returned_date)

            if record.is_returned:
                add_item(5, "Returned", "#2ecc71")
            else:
                add_item(5, "Borrowed", "#fdcb6e")

        # Update Pagination Labels
        total_pages = math.ceil(self.total_records / self.page_size) or 1
        self.lbl_page_info.setText(f"Page {self.current_page} of {total_pages}")
        self.lbl_total_records.setText(f"Total Records: {self.total_records}")

        # Enable/Disable Buttons
        self.btn_prev.setEnabled(self.current_page > 1)
        self.btn_next.setEnabled(self.current_page < total_pages)


    def next_page(self):
        total_pages = math.ceil(self.total_records / self.page_size) or 1
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_history_data()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_history_data()

    def lookup_file_for_borrow(self):
        rr = self.borrow_rr_input.text().strip()
        if not rr: return

        results = self.controller.search_files(rr)
        found = next((f for f in results if f.rr_number.lower() == rr.lower()), None)

        if found:
            self.lbl_file_name.setText(found.file_name)
            self.lbl_status.setText(found.current_status)
            if found.current_status == "Available":
                self.lbl_status.setStyleSheet("color: #2ecc71; font-weight: bold;")
                self.btn_issue.setEnabled(True)
            else:
                self.lbl_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
                self.btn_issue.setEnabled(False)
        else:
            self.lbl_file_name.setText("Not Found")
            self.btn_issue.setEnabled(False)

    def lookup_file_for_return(self):
        rr = self.return_rr_input.text().strip()
        if not rr: return

        results = self.controller.search_files(rr)
        found = next((f for f in results if f.rr_number.lower() == rr.lower()), None)

        if found and found.current_status == "Borrowed":
            self.lbl_ret_name.setText(found.file_name)
            self.lbl_ret_borrower.setText("(Hidden)")
            self.btn_return.setEnabled(True)
        else:
            QMessageBox.information(self, "Info", "File not found or not currently borrowed.")
            self.btn_return.setEnabled(False)

    def submit_borrow(self):
        rr = self.borrow_rr_input.text().strip()
        name = self.inp_borrower.text().strip()
        date = self.inp_borrow_date.date().toPyDate()

        if not name:
            QMessageBox.warning(self, "Missing Info", "Please enter Borrower Name.")
            return

        success, msg = self.controller.borrow_file(rr, name, date)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.load_history_data()  # Refresh history tab
            self.reset_forms()
        else:
            QMessageBox.critical(self, "Error", msg)

    def submit_return(self):
        rr = self.return_rr_input.text().strip()
        success, msg = self.controller.return_file(rr)
        if success:
            QMessageBox.information(self, "Success", msg)
            self.load_history_data()  # Refresh history tab
            self.reset_forms()
        else:
            QMessageBox.critical(self, "Error", msg)

    def reset_forms(self):
        self.borrow_rr_input.clear()
        self.lbl_file_name.setText("-")
        self.lbl_status.setText("-")
        self.inp_borrower.clear()
        self.btn_issue.setEnabled(False)
        self.return_rr_input.clear()
        self.lbl_ret_name.setText("-")
        self.btn_return.setEnabled(False)

    def reset_and_load_history(self):
        """
        Resets to page 1 and loads data (used for Search button)
        """
        self.current_page = 1
        self.load_history_data()