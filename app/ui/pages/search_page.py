from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
import qtawesome as qta
from app.ui.dialogs import FileDetailDialog  # <--- Import the new dialog


class SearchPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Store the raw data objects so we can pass them to the detail view
        self.current_results = []
        self.setup_ui()

        # Load all data by default on startup
        self.perform_search()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 1. Header & Search Bar
        top_bar = QHBoxLayout()

        lbl_title = QLabel("File Registry")
        lbl_title.setObjectName("PageTitle")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name, RR Number, Subject, or Sector...")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("QLineEdit { padding: 10px; border-radius: 5px; font-size: 14px; }")
        self.search_input.returnPressed.connect(self.perform_search)

        btn_search = QPushButton(" Search")
        btn_search.setIcon(qta.icon('fa5s.search', color='white'))
        btn_search.setFixedSize(100, 40)
        btn_search.setStyleSheet("background-color: #4d7cfe; color: white; border-radius: 5px; font-weight: bold;")
        btn_search.clicked.connect(self.perform_search)

        # Reload Button (to refresh the list)
        btn_refresh = QPushButton()
        btn_refresh.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        btn_refresh.setFixedSize(40, 40)
        btn_refresh.setStyleSheet("background-color: #2ecc71; border-radius: 5px;")
        btn_refresh.clicked.connect(lambda: self.perform_search())

        top_bar.addWidget(lbl_title)
        top_bar.addStretch()
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_search)
        top_bar.addWidget(btn_refresh)

        layout.addLayout(top_bar)

        # 2. Results Table
        self.table = QTableWidget()

        # Added more columns to match your screenshot requirement
        columns = ["RR Number", "Serial", "Sector", "Subject No", "File Name", "Shelf", "Deck", "File No", "Status"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        # Table Styling
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # Allow resizing
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Stretch Name column
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        # Connect Double Click Signal
        self.table.itemDoubleClicked.connect(self.open_detail_view)

        layout.addWidget(self.table)

    def perform_search(self):
        query = self.search_input.text().strip()

        # Call Backend
        self.current_results = self.controller.search_files(query)

        # Update UI
        self.table.setRowCount(0)

        for row_idx, file_data in enumerate(self.current_results):
            self.table.insertRow(row_idx)

            # Helper
            def add_item(col, text):
                item = QTableWidgetItem(str(text) if text else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Store the row index in the item to lookup data later
                item.setData(Qt.ItemDataRole.UserRole, row_idx)
                self.table.setItem(row_idx, col, item)

            add_item(0, file_data.rr_number)
            add_item(1, file_data.serial_number)
            add_item(2, file_data.sector)
            add_item(3, file_data.subject_number)
            add_item(4, file_data.file_name)
            add_item(5, file_data.shelf_number)
            add_item(6, file_data.deck_number)
            add_item(7, file_data.file_number)

            # Status Column
            status_item = QTableWidgetItem(file_data.current_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if file_data.current_status == "Available":
                status_item.setForeground(QBrush(QColor("#00b894")))
            elif file_data.current_status == "Borrowed":
                status_item.setForeground(QBrush(QColor("#fdcb6e")))
            elif file_data.current_status == "Removed":
                status_item.setForeground(QBrush(QColor("#ff7675")))

            self.table.setItem(row_idx, 8, status_item)

    def open_detail_view(self, item):
        """
        Triggered when a user double-clicks a row.
        """
        row_idx = item.row()
        # Retrieve the correct file object from our saved list
        file_data = self.current_results[row_idx]

        # Open the dialog
        dialog = FileDetailDialog(file_data, self)
        dialog.exec()