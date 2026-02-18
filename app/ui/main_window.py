import qtawesome as qta
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QFrame, QStackedWidget, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from app.ui.themes import get_stylesheet
from app.controllers import ArchiveController
from app.ui.pages.add_file_page import AddFilePage
from app.ui.pages.search_page import SearchPage
from app.ui.pages.circulation_page import CirculationPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.reports_page import ReportsPage
from app.ui.pages.disposal_page import DisposalPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Initialize Backend
        self.controller = ArchiveController()

        self.setWindowTitle("Weligepola DC Archive System")
        self.resize(1280, 800)
        self.current_theme = "dark"

        # --- MAIN CONTAINER ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- SIDEBAR ---
        self.setup_sidebar()

        # --- MAIN CONTENT ---
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(40, 40, 40, 40)

        # Header
        self.page_header = QLabel("Dashboard")
        self.page_header.setObjectName("pageTitle")
        self.content_layout.addWidget(self.page_header)

        # Stack (Pages)
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_dashboard_page())

        # Index 1: Search Page
        self.search_page = SearchPage(self.controller)
        self.stack.addWidget(self.search_page)

        # Index 2: Circulation Page
        self.circulation_page = CirculationPage(self.controller)
        self.stack.addWidget(self.circulation_page)

        # Index 3: Add Page
        self.add_file_page = AddFilePage(self.controller)
        self.stack.addWidget(self.add_file_page)

        # Index 4: Report Page
        self.report_page = ReportsPage(self.controller)
        self.stack.addWidget(self.report_page)

        # Index 5: Settings Page
        self.settings_page = SettingsPage(self.controller)
        self.stack.addWidget(self.settings_page)

        # Index 6: Disposal Page
        self.disposal_page = DisposalPage(self.controller)
        self.stack.addWidget(self.disposal_page)


        self.stack.currentChanged.connect(self.on_page_changed)

        self.content_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.content_area)

        # Apply theme at the end of init
        self.apply_theme()

        # 2. Trigger Initial Data Load
        self.refresh_stats()

    def refresh_stats(self):
        """
        Fetches real numbers from the Controller and updates the UI labels.
        """
        # Get dictionary like: {'total': 10, 'borrowed': 2, 'removed': 0}
        stats = self.controller.get_dashboard_stats()

        # Update the specific labels we created in create_dashboard_page
        self.lbl_total_files.setText(str(stats.get('total', 0)))
        self.lbl_borrowed.setText(str(stats.get('borrowed', 0)))
        self.lbl_removed.setText(str(stats.get('removed', 0)))

    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 40, 20, 20)
        self.sidebar_layout.setSpacing(15)

        # Logo
        logo_layout = QHBoxLayout()
        logo_icon = QLabel()
        logo_icon.setPixmap(qta.icon('fa5s.layer-group', color='#e14eca').pixmap(32, 32))
        title = QLabel("WPDC Archive")
        title.setObjectName("Logo")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(title)
        logo_layout.addStretch()
        self.sidebar_layout.addLayout(logo_layout)
        self.sidebar_layout.addSpacing(40)

        # Buttons with Icons
        self.btn_dashboard = self.add_nav_btn("Dashboard", 'fa5s.chart-pie')
        self.btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        self.btn_search = self.add_nav_btn("Search Files", 'fa5s.search')
        self.btn_search.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        self.btn_borrow = self.add_nav_btn("Circulation", 'fa5s.exchange-alt')
        self.btn_borrow.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        self.btn_add = self.add_nav_btn("Add New File", 'fa5s.plus-circle')
        self.btn_add.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        self.btn_reports = self.add_nav_btn("Reports", 'fa5s.file-alt')
        self.btn_reports.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        self.btn_disposal =  self.add_nav_btn("Disposal", 'fa5s.trash-alt')
        self.btn_disposal.clicked.connect(lambda: self.stack.setCurrentIndex(6))

        self.btn_settings = self.add_nav_btn("Settings", 'fa5s.cog')
        self.btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(5))

        self.sidebar_layout.addStretch()

        # Theme Toggle
        self.btn_theme = QPushButton(" Switch Theme")
        self.btn_theme.setIcon(qta.icon('fa5s.moon', color="#8f9bb3"))
        self.btn_theme.setObjectName("NavButton")
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.sidebar_layout.addWidget(self.btn_theme)

        self.main_layout.addWidget(self.sidebar)

    def add_nav_btn(self, text, icon_name):
        btn = QPushButton(f" {text}")
        btn.setIcon(qta.icon(icon_name, color="#8f9bb3"))
        btn.setIconSize(QSize(18, 18))
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        if text == "Dashboard": btn.setChecked(True)
        self.sidebar_layout.addWidget(btn)
        return btn

    def create_dashboard_page(self):
        page = QWidget()
        layout = QGridLayout(page)
        layout.setSpacing(25)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- CREATE DYNAMIC LABELS ---
        # We assign these to 'self' so we can access them in refresh_stats()
        self.lbl_total_files = QLabel("Loading...", objectName="CardValue")
        self.lbl_borrowed = QLabel("Loading...", objectName="CardValue")
        self.lbl_removed = QLabel("Loading...", objectName="CardValue")

        # --- TOP ROW: STATS CARDS ---

        # 1) Total files card (Gradient Style)
        card1 = QFrame()
        card1.setObjectName("GradientCard")
        c1_layout = QVBoxLayout(card1)
        c1_icon = QLabel()
        c1_icon.setPixmap(qta.icon('fa5s.folder', color='white').pixmap(40, 40))
        c1_layout.addWidget(c1_icon, alignment=Qt.AlignmentFlag.AlignRight)
        c1_layout.addWidget(QLabel("Total Files", objectName="WhiteText"))
        c1_layout.addWidget(self.lbl_total_files)  # <--- Variable Label
        layout.addWidget(card1, 0, 0)

        # 2) Borrowed (Manual build to insert variable label)
        card2 = QFrame()
        card2.setObjectName("Card")
        c2_layout = QVBoxLayout(card2)
        c2_layout.setContentsMargins(20, 20, 20, 20)
        c2_icon = QLabel()
        c2_icon.setPixmap(qta.icon('fa5s.hand-holding', color='#e14eca').pixmap(30, 30))
        c2_layout.addWidget(c2_icon, alignment=Qt.AlignmentFlag.AlignRight)
        c2_layout.addWidget(QLabel("Currently Borrowed", objectName="CardTitle"))
        c2_layout.addWidget(self.lbl_borrowed)  # <--- Variable Label
        layout.addWidget(card2, 0, 1)

        # 3) Removed/Overdue (Manual build to insert variable label)
        card3 = QFrame()
        card3.setObjectName("Card")
        c3_layout = QVBoxLayout(card3)
        c3_layout.setContentsMargins(20, 20, 20, 20)
        c3_icon = QLabel()
        c3_icon.setPixmap(qta.icon('fa5s.trash', color='#fd5d93').pixmap(30, 30))
        c3_layout.addWidget(c3_icon, alignment=Qt.AlignmentFlag.AlignRight)
        c3_layout.addWidget(QLabel("Removed Files", objectName="CardTitle"))
        c3_layout.addWidget(self.lbl_removed)  # <--- Variable Label
        layout.addWidget(card3, 0, 2)

        # --- MIDDLE ROW: BIG SECTIONS ---

        # "Quick action Panel"
        action_card = QFrame()
        action_card.setObjectName("Card")
        ac_layout = QVBoxLayout(action_card)
        ac_layout.addWidget(QLabel("Quick Actions", objectName="CardTitle"))

        # Add a couple of dummy action buttons
        btn_quick_add = QPushButton("Scan New Document")
        btn_quick_add.setStyleSheet("background: #2b3553; color: white; padding: 10px; border-radius: 5px;")
        ac_layout.addWidget(btn_quick_add)
        ac_layout.addStretch()
        layout.addWidget(action_card, 1, 0, 1, 1)  # Row 1, Col 0, Span 1 row, 1 col

        # "Recent Activity" Panel (Spans 2 columns)
        recent_card = QFrame()
        recent_card.setObjectName("Card")
        rc_layout = QVBoxLayout(recent_card)
        rc_layout.addWidget(QLabel("Recent Activity", objectName="CardTitle"))

        # Dummy List of activity
        for i in range(3):
            lbl = QLabel(f"• File #102{i} returned by K. Perera")
            lbl.setStyleSheet("color: #8f9bb3; padding: 5px;")
            rc_layout.addWidget(lbl)

        rc_layout.addStretch()
        layout.addWidget(recent_card, 1, 1, 1, 2)  # Row 1, Col 1, Span 1 row, 2 cols

        # Push everything up
        layout.setRowStretch(2, 1)

        return page

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(get_stylesheet(self.current_theme))


    def on_page_changed(self, index):
        """
        Triggered every time the user switches pages.
        If they switch TO the Dashboard (Index 0), we refresh the stats.
        """

        if index == 0:
            print("Switched to Dashboard -> Refreshing Stats...")
            self.refresh_stats()