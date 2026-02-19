import qtawesome as qta
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QFrame, QStackedWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize
from app.ui.themes import get_stylesheet
from app.controllers import ArchiveController
from app.ui.pages.add_file_page import AddFilePage
from app.ui.pages.search_page import SearchPage
from app.ui.pages.circulation_page import CirculationPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.reports_page import ReportsPage
from app.ui.pages.disposal_page import DisposalPage


class InteractiveNavBtn(QPushButton):
    def __init__(self, text, icon_name, parent=None):
        super().__init__(f"  {text}", parent)
        self.icon_name = icon_name
        self.setObjectName("NavButton")
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(20, 20))
        self.accent_color = "#d4af37"
        self.setIcon(qta.icon(self.icon_name, color="#8f9bb3"))
        self.toggled.connect(self.on_toggled)

    def on_toggled(self, checked):
        if checked:
            self.setIcon(qta.icon(self.icon_name, color=self.accent_color))
        else:
            self.setIcon(qta.icon(self.icon_name, color="#8f9bb3"))

    def update_accent(self, color):
        self.accent_color = color
        if self.isChecked():
            self.setIcon(qta.icon(self.icon_name, color=self.accent_color))

    def enterEvent(self, event):
        spin = qta.Spin(self)
        self.setIcon(qta.icon(self.icon_name, color=self.accent_color, animation=spin))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.isChecked():
            self.setIcon(qta.icon(self.icon_name, color="#8f9bb3"))
        else:
            self.setIcon(qta.icon(self.icon_name, color=self.accent_color))
        super().leaveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ArchiveController()
        self.setWindowTitle("Weligepola DC Vault")
        self.resize(1280, 850)
        self.current_theme = "dark"

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.nav_buttons = []
        self.dashboard_icons = []
        self.dashboard_shadows = []

        self.setup_sidebar()

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(50, 40, 50, 40)

        self.page_header = QLabel("Dashboard")
        self.page_header.setObjectName("pageTitle")
        self.content_layout.addWidget(self.page_header)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_dashboard_page())
        self.stack.addWidget(SearchPage(self.controller))
        self.stack.addWidget(CirculationPage(self.controller))
        self.stack.addWidget(AddFilePage(self.controller))
        self.stack.addWidget(ReportsPage(self.controller))
        self.stack.addWidget(SettingsPage(self.controller))
        self.stack.addWidget(DisposalPage(self.controller))

        self.stack.currentChanged.connect(self.on_page_changed)
        self.content_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.content_area)

        self.apply_theme()
        self.refresh_stats()

    def refresh_stats(self):
        stats = self.controller.get_dashboard_stats()
        self.lbl_total_files.setText(f"{stats.get('total', 0):,}")
        self.lbl_borrowed.setText(str(stats.get('borrowed', 0)))
        self.lbl_removed.setText(str(stats.get('removed', 0)))

    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(280)

        self.sidebar_shadow = QGraphicsDropShadowEffect()
        self.sidebar_shadow.setBlurRadius(20)
        self.sidebar_shadow.setXOffset(5)
        self.sidebar_shadow.setColor(Qt.GlobalColor.black)
        self.sidebar.setGraphicsEffect(self.sidebar_shadow)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(25, 50, 25, 30)
        self.sidebar_layout.setSpacing(15)

        logo_layout = QHBoxLayout()
        self.logo_icon_label = QLabel()
        self.logo_icon_label.setPixmap(qta.icon('fa5s.landmark', color='#d4af37').pixmap(40, 40))
        title = QLabel("ARCHIVUM")
        title.setObjectName("Logo")
        logo_layout.addWidget(self.logo_icon_label)
        logo_layout.addWidget(title)
        logo_layout.addStretch()

        self.sidebar_layout.addLayout(logo_layout)
        self.sidebar_layout.addSpacing(50)

        self.add_nav_btn("Dashboard", 'fa5s.chart-pie', 0)
        self.add_nav_btn("Search Vault", 'fa5s.search', 1)
        self.add_nav_btn("Circulation", 'fa5s.exchange-alt', 2)
        self.add_nav_btn("New Entry", 'fa5s.plus-circle', 3)
        self.add_nav_btn("Reports", 'fa5s.file-alt', 4)
        self.add_nav_btn("Disposal", 'fa5s.skull', 6)
        self.add_nav_btn("Settings", 'fa5s.cogs', 5)

        self.sidebar_layout.addStretch()

        self.btn_theme = QPushButton(" Toggle Light/Dark")
        self.btn_theme.setIcon(qta.icon('fa5s.adjust', color="#8f9bb3"))
        self.btn_theme.setObjectName("NavButton")
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.sidebar_layout.addWidget(self.btn_theme)
        self.main_layout.addWidget(self.sidebar)

    def add_nav_btn(self, text, icon, index):
        btn = InteractiveNavBtn(text, icon)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(index))
        if index == 0: btn.setChecked(True)
        self.sidebar_layout.addWidget(btn)
        self.nav_buttons.append(btn)

    def create_dashboard_page(self):
        page = QWidget()
        layout = QGridLayout(page)
        layout.setSpacing(30)
        layout.setContentsMargins(10, 10, 10, 10)

        def create_glass_card(title, icon_name, value_label):
            card = QFrame()
            card.setObjectName("Card")
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 4)
            shadow.setColor(Qt.GlobalColor.black)
            card.setGraphicsEffect(shadow)
            self.dashboard_shadows.append(shadow)

            cl = QVBoxLayout(card)
            cl.setContentsMargins(25, 25, 25, 25)

            icn = QLabel()
            icn.setPixmap(qta.icon(icon_name, color='#d4af37').pixmap(32, 32))
            cl.addWidget(icn, alignment=Qt.AlignmentFlag.AlignRight)
            self.dashboard_icons.append((icn, icon_name))

            cl.addWidget(QLabel(title, objectName="CardTitle"))
            cl.addWidget(value_label)
            return card

        self.lbl_total_files = QLabel("...", objectName="CardValue")
        self.lbl_borrowed = QLabel("...", objectName="CardValue")
        self.lbl_removed = QLabel("...", objectName="CardValue")

        layout.addWidget(create_glass_card("Total Holdings", "fa5s.university", self.lbl_total_files), 0, 0)
        layout.addWidget(create_glass_card("Active Loans", "fa5s.hand-holding-usd", self.lbl_borrowed), 0, 1)
        layout.addWidget(create_glass_card("Archived/Purged", "fa5s.archive", self.lbl_removed), 0, 2)

        big_card = QFrame()
        big_card.setObjectName("Card")
        bcl = QVBoxLayout(big_card)
        bcl.addWidget(QLabel("RECENT VAULT ACTIVITY", objectName="CardTitle"))
        bcl.addSpacing(10)

        logs = [
            "• RR-2024-001 retrieved by Admin (Audit)",
            "• RR-2023-889 returned to Shelf 5",
            "• New Batch (Land Division) added to Vault"
        ]
        for log in logs:
            lbl = QLabel(log)
            lbl.setStyleSheet(
                "color: #8f9bb3; font-family: 'Consolas', monospace; font-size: 13px; margin-bottom: 5px;")
            bcl.addWidget(lbl)

        bcl.addStretch()
        layout.addWidget(big_card, 1, 0, 1, 3)
        layout.setRowStretch(1, 1)
        return page

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(get_stylesheet(self.current_theme))

        if self.current_theme == "light":
            accent = "#0f5132"
            shadows_enabled = False
        else:
            accent = "#d4af37"
            shadows_enabled = True

        self.sidebar_shadow.setEnabled(shadows_enabled)
        for shadow in self.dashboard_shadows:
            shadow.setEnabled(shadows_enabled)

        self.logo_icon_label.setPixmap(qta.icon('fa5s.landmark', color=accent).pixmap(40, 40))

        for icn_label, icon_name in self.dashboard_icons:
            icn_label.setPixmap(qta.icon(icon_name, color=accent).pixmap(32, 32))

        for btn in self.nav_buttons:
            btn.update_accent(accent)

        self.style().polish(self)

    def on_page_changed(self, index):
        titles = ["Dashboard", "Search Vault", "Circulation Desk", "New Entry", "Reports & Export", "Settings",
                  "Disposal"]
        if 0 <= index < len(titles):
            self.page_header.setText(titles[index])
        if index == 0:
            self.refresh_stats()