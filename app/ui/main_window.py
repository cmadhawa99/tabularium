import qtawesome as qta
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame, QStackedWidget, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from app.ui.themes import get_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.stack =QStackedWidget()
        #self.stack.addWidget(self.create_dashboard_page())
        self.stack.addWidget(QLabel("Search Page Placeholder"))

        self.content_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.content_area)

    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 40, 20, 20)
        self.sidebar_layout.setSpacing(15)

        #Logo
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
        self.btn_search = self.add_nav_btn("Search Files", 'fa5s.search')
        self.btn_add = self.add_nav_btn("Add New File", 'fa5s.plus-circle')
        self.btn_borrow = self.add_nav_btn("Circulation", 'fa5s.exchange-alt')
        self.btn_reports = self.add_nav_btn("Reports", 'fa5s.file-alt')
        self.btn_settings = self.add_nav_btn("Settings", 'fa5s.cog')

        self.sidebar_layout.addStretch()

        #Theme Toggle
        self.btn_theme = QPushButton(" Switch Theme")
        self.btn_theme.setIcon(qta.icon('fa5s.moon', color="8f9bb3"))
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

        # --- TOP ROW: STATS CARDS ---

        # 1) Total files card
        card1 = QFrame()
        card1.setObjectName("GradientCard")
        c1_layout = QVBoxLayout(card1)
        c1_icon = QLabel()
        c1_icon.setPixmap(qta.icon('fa5s.folder', color='white').pixmap(40, 40))
        c1_layout.addWidget(c1_icon, alignment=Qt.AlignmentFlag.AlignRight)
        c1_layout.addWidget(QLabel("Total Files", objectName="WhiteText"))
        c1_layout.addWidget(QLabel("12,450", objectName="CarcValue"))
        layout.addWidget(card1, 0, 0)

        # 2) Borrowed
        card2 = self.create_stat_card ("Currently Borrowed", "45", 'fa5s.hand-holding', "#e14eca")
        layout.addWidget(card2, 0, 1)

        # 3) Overdue
        card3 = self.create_stat_card("Overdue Returns", "3", 'fa5s.exclamation-circle', "fd5d93")
        layout.addWidget(card3, 0, 2)

        # --- MIDDLE ROW: BIG SECTIONS ---

        # "Quick action Panel
        action_card = QFrame()
        action_card.setObjectName("Card")
        ac_layout = QVBoxLayout(action_card)
        ac_layout.addWidget(QLabel("Quick Actions", objectName="CardTItle"))

        #Add a couple of dummy action buttons
        btn_quick_add = QPushButton("Scan New Document")
        btn_quick_add.setStyleSheet("background: #2b3553; color: white; padding: 10px; border-radius: 5px;")
        ac_layout.addWidget(btn_quick_add)
        ac_layout.addStretch()
        layout.addWidget(action_card, 1, 0, 1, 1) # Row 1, Col 0, Span 1 row, 1 col

        # "Recent Activity" Panel (Spans 2 columns)
        recent_card = QFrame()
        recent_card.setObjectName("Card")
        rc_layout = QVBoxLayout(recent_card)
        rc_layout.addWidget(QLabel("Recent Activity", objectName="CardTitle"))

        #Dummy List of activity

        for i in range (3):
            lbl = QLabel(f"• File #102{i} returned by K. Perera")
            lbl.setStyleSheet("color: #8f9bb3; padding: 5px;")
            rc_layout.addWidget(lbl)

        rc_layout.addStretch()
        layout.addWidget(recent_card, 1, 1, 1, 2) # Row 1, Col 1, Span 1 row, 2 cols

        # Push everything up

        layout.setRowStretch(2, 1)

        return page


    def create_stat_card(self, title, value, icon_name, icon_color):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        # Icon Top Right
        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color=icon_color).pixmap(30, 30))
        layout.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(QLabel(title, objectName="CardTitle"))
        layout.addWidget(QLabel(value, objectName="CardValue"))
        return card



    def toggle_theme(self):
        self.current_theme ="light" if self.current_theme == "dark" else "dark"
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(get_stylesheet(self.current_theme))