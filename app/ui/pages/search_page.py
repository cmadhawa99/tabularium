from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QAbstractItemView,
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
import qtawesome as qta
from app.ui.dialogs import FileDetailDialog


class SearchPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_results = []
        self.setup_ui()
        self.perform_search()

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

        lbl_title = QLabel("File Registry")
        lbl_title.setObjectName("PageTitle")
        layout.addWidget(lbl_title)

        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name, RR Number, Subject, or Sector...")
        self.search_input.setFixedHeight(40)
        self.search_input.returnPressed.connect(self.perform_search)

        btn_search = QPushButton(" Search")
        btn_search.setIcon(qta.icon('fa5s.search', color='white'))
        btn_search.setFixedSize(120, 40)
        btn_search.setObjectName("PrimaryActionBtn")
        btn_search.clicked.connect(self.perform_search)

        btn_refresh = QPushButton()
        btn_refresh.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        btn_refresh.setFixedSize(40, 40)
        btn_refresh.setObjectName("PrimaryActionBtn")
        btn_refresh.clicked.connect(self.perform_search)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_search)
        top_bar.addWidget(btn_refresh)
        layout.addLayout(top_bar)

        table_frame = self.create_glass_panel()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(5, 5, 5, 5)

        self.table = QTableWidget()
        columns = ["RR Number", "Serial", "Sector", "Subject No", "File Name", "Shelf", "Deck", "File No", "Status"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setAlternatingRowColors(False)

        self.table.itemDoubleClicked.connect(self.open_detail_view)

        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)

    def perform_search(self):
        query = self.search_input.text().strip()
        self.current_results = self.controller.search_files(query)
        self.table.setRowCount(0)

        for row_idx, file_data in enumerate(self.current_results):
            self.table.insertRow(row_idx)

            def add_item(col, text):
                item = QTableWidgetItem(str(text) if text else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
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

            status_item = QTableWidgetItem(file_data.current_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if file_data.current_status == "Available":
                status_item.setForeground(QBrush(QColor("#2ecc71")))
            elif file_data.current_status == "Borrowed":
                status_item.setForeground(QBrush(QColor("#e67e22")))
            elif file_data.current_status == "Removed":
                status_item.setForeground(QBrush(QColor("#e74c3c")))

            self.table.setItem(row_idx, 8, status_item)

    def open_detail_view(self, item):
        row_idx = item.row()
        file_data = self.current_results[row_idx]
        dialog = FileDetailDialog(file_data, self)
        dialog.exec()