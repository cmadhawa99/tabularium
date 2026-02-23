import math
import datetime
import qtawesome as qta
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QStackedWidget,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize, QTimer, QTime, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QRadialGradient, QBrush

from app.ui.themes import get_stylesheet, get_structural_stylesheet, PALETTES
from app.controllers import ArchiveController
from app.ui.pages.add_file_page import AddFilePage
from app.ui.pages.search_page import SearchPage
from app.ui.pages.circulation_page import CirculationPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.reports_page import ReportsPage
from app.ui.pages.disposal_page import DisposalPage

#_________________________________________________________________________________________________________________

class AnalogClock(QWidget):
    ROMAN = ["XII", "I", "II", "III", "IV", "V",
             "VI", "VII", "VIII", "IX", "X", "XI"]

    def __init__(self, theme: str = "dark", parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 180)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pal = PALETTES[theme]
        t = QTimer(self)
        t.timeout.connect(self.update)
        t.start(1000)

    def set_theme(self, theme: str):
        self._pal = PALETTES[theme]
        self.update()

    def paintEvent(self, event):
        pal  = self._pal
        side = min(self.width(), self.height())
        r    = side / 2 - 4

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.translate(self.width() / 2, self.height() / 2)

        bezel = QRadialGradient(0, -r * 0.2, r * 1.1)
        bezel.setColorAt(0.0,  QColor(pal["clk_bezel_a"]))
        bezel.setColorAt(0.75, QColor(pal["clk_bezel_b"]))
        bezel.setColorAt(1.0,  QColor(pal["clk_bezel_c"]))
        p.setBrush(QBrush(bezel))
        p.setPen(QPen(pal["clk_accent"], 2.5))
        p.drawEllipse(QRect(int(-r-3), int(-r-3), int(r*2+6), int(r*2+6)))

        face = QRadialGradient(0, -r * 0.15, r)
        face.setColorAt(0.0, QColor(pal["clk_face_a"]))
        face.setColorAt(0.6, QColor(pal["clk_face_b"]))
        face.setColorAt(1.0, QColor(pal["clk_face_c"]))
        p.setBrush(QBrush(face))
        p.setPen(QPen(QColor(pal["clk_ring"]), 1.5))
        p.drawEllipse(QRect(int(-r), int(-r), int(r*2), int(r*2)))

        for i in range(12):
            a  = math.radians(i * 30 - 90)
            iq = i % 3 == 0
            p.setPen(QPen(pal["clk_accent"], 2.0 if iq else 1.0))
            p.drawLine(int(math.cos(a)*(r-6)),          int(math.sin(a)*(r-6)),
                       int(math.cos(a)*(r-(14 if iq else 10))),
                       int(math.sin(a)*(r-(14 if iq else 10))))

        p.setPen(QPen(pal["clk_minor"], 0.8))
        for i in range(60):
            if i % 5 == 0:
                continue
            a = math.radians(i * 6 - 90)
            p.drawLine(int(math.cos(a)*(r-6)), int(math.sin(a)*(r-6)),
                       int(math.cos(a)*(r-9)), int(math.sin(a)*(r-9)))

        font = QFont("Times New Roman", 6)
        font.setBold(True)
        p.setFont(font)
        p.setPen(QPen(pal["clk_secondary"]))
        lr = r - 24
        fm = p.fontMetrics()
        for i, num in enumerate(self.ROMAN):
            a = math.radians(i * 30 - 90)
            x = math.cos(a) * lr
            y = math.sin(a) * lr
            p.drawText(int(x - fm.horizontalAdvance(num)/2),
                       int(y + fm.height()/3), num)

        now = QTime.currentTime()
        hr, mn, sc = now.hour() % 12, now.minute(), now.second()
        ha = math.radians((hr + mn/60.0) * 30 - 90)
        ma = math.radians(mn * 6 + sc * 0.1 - 90)
        sa = math.radians(sc * 6 - 90)

        self._draw_hand(p, ha, r * 0.48, 3.5, pal["clk_accent"])
        self._draw_hand(p, ma, r * 0.68, 2.5, pal["clk_secondary"])

        p.setPen(QPen(pal["clk_second"], 1.2))
        p.drawLine(int(math.cos(sa+math.pi)*(r*0.18)), int(math.sin(sa+math.pi)*(r*0.18)),
                   int(math.cos(sa)*(r*0.72)),          int(math.sin(sa)*(r*0.72)))

        p.setBrush(QBrush(pal["clk_center"]))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPoint(0, 0), 4, 4)

        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(pal["clk_deco"], 1))
        p.drawEllipse(QRect(int(-r-8), int(-r-8), int(r*2+16), int(r*2+16)))

    @staticmethod
    def _draw_hand(p: QPainter, angle: float, length: float, width: float, color):
        xt, yt = math.cos(angle)*length, math.sin(angle)*length
        shadow = QPen(QColor(0, 0, 0, 55), width + 2)
        shadow.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(shadow)
        p.drawLine(2, 2, int(xt)+2, int(yt)+2)
        main = QPen(color, width)
        main.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(main)
        p.drawLine(0, 0, int(xt), int(yt))

#_________________________________________________________________________________________________________________

class LiveDateLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._refresh()
        t = QTimer(self)
        t.timeout.connect(self._refresh)
        t.start(1000)

    def _refresh(self):
        self.setText(QTime.currentTime().toString("hh:mm:ss  ·  ") +
                     datetime.date.today().strftime("%d %b %Y"))

#_________________________________________________________________________________________________________________

class InteractiveNavBtn(QPushButton):
    def __init__(self, text, icon_name, parent=None):
        super().__init__(f"  {text}", parent)
        self.icon_name    = icon_name
        self.accent_color = "#d4af37"
        self.setObjectName("NavButton")
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(18, 18))
        self.setIcon(qta.icon(icon_name, color="#8f9bb3"))
        self.toggled.connect(lambda c: self.setIcon(
            qta.icon(self.icon_name, color=self.accent_color if c else "#8f9bb3")))

    def update_accent(self, color: str):
        self.accent_color = color
        if self.isChecked():
            self.setIcon(qta.icon(self.icon_name, color=color))

    def enterEvent(self, e):
        self.setIcon(qta.icon(self.icon_name, color=self.accent_color,
                              animation=qta.Spin(self)))
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setIcon(qta.icon(self.icon_name,
                              color=self.accent_color if self.isChecked() else "#8f9bb3"))
        super().leaveEvent(e)

#_________________________________________________________________________________________________________________

class StatCard(QFrame):
    def __init__(self, title: str, icon_name: str, value_label: QLabel, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self._icon_name = icon_name
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        v = QVBoxLayout(self)
        v.setContentsMargins(22, 22, 22, 22)
        v.setSpacing(8)

        top = QHBoxLayout()
        self._icon_frame = QFrame()
        self._icon_frame.setFixedSize(42, 42)
        il = QHBoxLayout(self._icon_frame)
        il.setContentsMargins(0, 0, 0, 0)
        self._icon_lbl = QLabel()
        self._icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        il.addWidget(self._icon_lbl)
        top.addStretch()
        top.addWidget(self._icon_frame)
        v.addLayout(top)

        lbl_t = QLabel(title.upper())
        lbl_t.setObjectName("CardTitle")
        v.addWidget(lbl_t)
        v.addWidget(value_label)

    def update_accent(self, color: str):
        c = QColor(color)
        self._icon_frame.setStyleSheet(
            f"background:rgba({c.red()},{c.green()},{c.blue()},0.14);border-radius:10px;")
        self._icon_lbl.setPixmap(qta.icon(self._icon_name, color=color).pixmap(22, 22))

#_________________________________________________________________________________________________________________

class MainWindow(QMainWindow):
    def __init__(self, username: str = "Admin"):
        super().__init__()
        self._username     = username
        self.controller    = ArchiveController()
        self.current_theme = "dark"

        # __________ Theme-sensitive widget registries __________

        self._nav_buttons:    list[InteractiveNavBtn]       = []
        self._stat_cards:     list[StatCard]                = []
        self._log_icons:      list[tuple[QLabel, str, str]] = []
        self._log_texts:      list[QLabel]                  = []
        self._card_hdr_icons: list[tuple[QLabel, str]]      = []
        self._quick_btns:     list[tuple[QPushButton, str]] = []

        self.setWindowTitle("Archivum — Weligepola DC Vault")
        self.resize(1380, 900)
        self.setMinimumSize(1100, 700)

        root = QWidget()
        self.setCentralWidget(root)
        rh = QHBoxLayout(root)
        rh.setContentsMargins(0, 0, 0, 0)
        rh.setSpacing(0)
        rh.addWidget(self._build_sidebar())

        cv = QVBoxLayout()
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(0)
        cv.addWidget(self._build_topbar())

        pw = QWidget()
        pv = QVBoxLayout(pw)
        pv.setContentsMargins(44, 32, 44, 32)
        pv.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_dashboard())
        self.stack.addWidget(SearchPage(self.controller))
        self.stack.addWidget(CirculationPage(self.controller))
        self.stack.addWidget(AddFilePage(self.controller))
        self.stack.addWidget(ReportsPage(self.controller))
        self.stack.addWidget(SettingsPage(self.controller))
        self.stack.addWidget(DisposalPage(self.controller))
        self.stack.currentChanged.connect(self._on_page_changed)
        pv.addWidget(self.stack)
        cv.addWidget(pw, stretch=1)

        cw = QWidget()
        cw.setLayout(cv)
        rh.addWidget(cw, stretch=1)

        self._apply_theme()
        self._refresh_stats()

    # __________ Sidebar __________

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(270)
        self._sidebar_shadow = QGraphicsDropShadowEffect()
        self._sidebar_shadow.setBlurRadius(30)
        self._sidebar_shadow.setXOffset(8)
        self._sidebar_shadow.setColor(QColor(0, 0, 0, 160))
        sidebar.setGraphicsEffect(self._sidebar_shadow)

        v = QVBoxLayout(sidebar)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        lb = QFrame()
        lb.setObjectName("LogoBlock")
        lb.setFixedHeight(100)
        lv = QVBoxLayout(lb)
        lv.setContentsMargins(28, 18, 28, 18)
        lv.setSpacing(2)
        lr = QHBoxLayout()
        self._logo_icon = QLabel()
        lbl_name = QLabel("ARCHIVUM")
        lbl_name.setObjectName("Logo")
        lr.addWidget(self._logo_icon)
        lr.addWidget(lbl_name)
        lr.addStretch()
        lv.addLayout(lr)
        lbl_sub = QLabel("Weligepola District Council")
        lbl_sub.setObjectName("LogoSub")
        lv.addWidget(lbl_sub)
        v.addWidget(lb)
        v.addWidget(self._divider())

        nw = QWidget()
        nv = QVBoxLayout(nw)
        nv.setContentsMargins(28, 20, 28, 8)
        nv.setSpacing(4)
        nl = QLabel("NAVIGATION")
        nl.setObjectName("SectionLabel")
        nv.addWidget(nl)

        for label, icon, idx in [
            ("Dashboard",    "fa5s.chart-pie",    0),
            ("Search Vault", "fa5s.search",        1),
            ("Circulation",  "fa5s.exchange-alt",  2),
            ("New Entry",    "fa5s.plus-circle",   3),
            ("Reports",      "fa5s.file-alt",      4),
            ("Disposal",     "fa5s.skull",         6),
        ]:
            btn = self._make_nav_btn(label, icon, idx)
            nv.addWidget(btn)
            if idx == 0:
                btn.setChecked(True)

        nv.addSpacing(12)
        sl = QLabel("SYSTEM")
        sl.setObjectName("SectionLabel")
        nv.addWidget(sl)
        nv.addWidget(self._make_nav_btn("Settings", "fa5s.cogs", 5))
        v.addWidget(nw, stretch=1)
        v.addWidget(self._divider())

        bw = QWidget()
        bv = QVBoxLayout(bw)
        bv.setContentsMargins(0, 16, 0, 20)
        bv.setSpacing(8)
        self._clock = AnalogClock(theme="dark")
        bv.addWidget(self._clock, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._date_lbl = LiveDateLabel()
        self._date_lbl.setObjectName("ClockLabel")
        self._date_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bv.addWidget(self._date_lbl)
        v.addWidget(bw)
        return sidebar

    def _make_nav_btn(self, label: str, icon: str, index: int) -> InteractiveNavBtn:
        btn = InteractiveNavBtn(label, icon)
        btn.clicked.connect(lambda _=False, i=index: self.stack.setCurrentIndex(i))
        self._nav_buttons.append(btn)
        return btn

    # __________ Top bar __________

    def _build_topbar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(62)
        h = QHBoxLayout(bar)
        h.setContentsMargins(44, 0, 32, 0)

        self._page_title = QLabel("Dashboard")
        self._page_title.setObjectName("TopBarTitle")
        h.addWidget(self._page_title)
        h.addStretch()

        self._chip = QFrame()
        self._chip.setObjectName("UserChip")
        ch = QHBoxLayout(self._chip)
        ch.setContentsMargins(14, 0, 14, 0)
        self._chip.setFixedHeight(38)
        ch.setSpacing(8)
        self._chip_icon = QLabel()
        ch.addWidget(self._chip_icon)
        self._chip_lbl = QLabel(f"Welcome,  {self._username}!")
        self._chip_lbl.setObjectName("ChipLabel")
        ch.addWidget(self._chip_lbl)
        h.addWidget(self._chip)

        h.addSpacing(10)

        self._btn_refresh = QPushButton()
        self._btn_refresh.setToolTip('Refresh Application')
        self._btn_refresh.setFixedSize(38, 38)
        self._btn_refresh.setObjectName('ThemeToggleBtn')
        self._btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_refresh.clicked.connect(self._refresh_app)
        h.addWidget(self._btn_refresh)

        h.addSpacing(6)

        self._btn_theme = QPushButton()
        self._btn_theme.setToolTip('Toggle Light / Dark Theme')
        self._btn_theme.setFixedSize(38, 38)
        self._btn_theme.setObjectName('ThemeToggleBtn')
        self._btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_theme.clicked.connect(self._toggle_theme)
        h.addWidget(self._btn_theme)
        return bar

    # __________ Dashboard __________

    def _build_dashboard(self) -> QWidget:
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(28)

        sr = QHBoxLayout()
        sr.setSpacing(20)
        self.lbl_total    = QLabel("…", objectName="CardValue")
        self.lbl_borrowed = QLabel("…", objectName="CardValue")
        self.lbl_removed  = QLabel("…", objectName="CardValue")
        for title, icon, lbl in [
            ("Total Holdings",    "fa5s.university",       self.lbl_total),
            ("Active Loans",      "fa5s.hand-holding-usd", self.lbl_borrowed),
            ("Archived / Purged", "fa5s.archive",          self.lbl_removed),
        ]:
            card = StatCard(title, icon, lbl)
            self._stat_cards.append(card)
            sr.addWidget(card)
        v.addLayout(sr)

        br = QHBoxLayout()
        br.setSpacing(20)
        br.addWidget(self._build_activity_card(), stretch=3)
        br.addWidget(self._build_quick_card(),    stretch=2)
        v.addLayout(br, stretch=1)
        return page

    def _build_activity_card(self) -> QFrame:
        card = self._glass_card()
        av = QVBoxLayout(card)
        av.setContentsMargins(26, 24, 26, 24)
        av.setSpacing(14)

        hdr = QHBoxLayout()
        hi = QLabel()
        hi.setFixedSize(18, 18)
        self._card_hdr_icons.append((hi, "fa5s.scroll"))
        hdr.addWidget(hi)
        hdr.addWidget(QLabel("VAULT ACTIVITY LOG", objectName="CardTitle"))
        hdr.addStretch()
        av.addLayout(hdr)

        for ico_name, pal_key, txt in [
            ("fa5s.sign-out-alt", "log_retrieve", "RR-2024-001 retrieved by Admin (Audit)"),
            ("fa5s.sign-in-alt",  "log_return",   "RR-2023-889 returned — Shelf 5, Deck 2"),
            ("fa5s.plus",         "log_add",       "New Batch (Land Division) added to Vault"),
            ("fa5s.clock",        "log_system",    "Daily SQL backup completed — 03:00 AM"),
        ]:
            row = QHBoxLayout()
            dot = QLabel()
            dot.setFixedSize(20, 16)
            self._log_icons.append((dot, ico_name, pal_key))
            row.addWidget(dot)
            lbl = QLabel(txt)
            lbl.setStyleSheet("font-size:13px;font-family:'Consolas',monospace;")
            self._log_texts.append(lbl)
            row.addWidget(lbl)
            row.addStretch()
            av.addLayout(row)

        av.addStretch()
        return card

    def _build_quick_card(self) -> QFrame:
        card = self._glass_card()
        qv = QVBoxLayout(card)
        qv.setContentsMargins(26, 24, 26, 24)
        qv.setSpacing(12)

        hdr = QHBoxLayout()
        qi = QLabel()
        qi.setFixedSize(16, 16)
        self._card_hdr_icons.append((qi, "fa5s.bolt"))
        hdr.addWidget(qi)
        hdr.addWidget(QLabel("QUICK ACCESS", objectName="CardTitle"))
        hdr.addStretch()
        qv.addLayout(hdr)

        for label, ico_name, idx in [
            ("Search Vault", "fa5s.search",      1),
            ("Issue File",   "fa5s.paper-plane",  2),
            ("Add New File", "fa5s.plus-circle",  3),
            ("Run Report",   "fa5s.file-alt",     4),
        ]:
            btn = QPushButton(f"  {label}")
            btn.setObjectName("GlassButton")
            btn.setFixedHeight(38)
            btn.clicked.connect(lambda _=False, i=idx: self.stack.setCurrentIndex(i))
            self._quick_btns.append((btn, ico_name))
            qv.addWidget(btn)

        qv.addStretch()
        return card

    # __________ Helpers __________

    @staticmethod
    def _glass_card() -> QFrame:
        f = QFrame()
        f.setObjectName("Card")
        s = QGraphicsDropShadowEffect()
        s.setBlurRadius(22)
        s.setOffset(0, 5)
        s.setColor(QColor(0, 0, 0, 70))
        f.setGraphicsEffect(s)
        return f

    @staticmethod
    def _divider() -> QFrame:
        d = QFrame()
        d.setFrameShape(QFrame.Shape.HLine)
        d.setObjectName("Divider")
        return d

    # __________ Theme __________

    def _toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme()

    def _apply_theme(self):
        pal = PALETTES[self.current_theme]

        self.setStyleSheet(get_stylesheet(self.current_theme) + get_structural_stylesheet(pal))
        self._sidebar_shadow.setEnabled(self.current_theme == "dark")

        self._logo_icon.setPixmap(qta.icon("fa5s.landmark", color=pal["accent"]).pixmap(28, 28))

        for btn in self._nav_buttons:
            btn.update_accent(pal["accent"])

        for card in self._stat_cards:
            card.update_accent(pal["accent"])

        self._clock.set_theme(self.current_theme)

        for (dot, ico_name, pal_key) in self._log_icons:
            dot.setPixmap(qta.icon(ico_name, color=pal[pal_key]).pixmap(13, 13))

        for lbl in self._log_texts:
            lbl.setStyleSheet(
                f"color:{pal['log_text']};font-size:13px;font-family:'Consolas',monospace;")

        for (lbl_w, ico_name) in self._card_hdr_icons:
            size = 18 if ico_name == "fa5s.scroll" else 16
            lbl_w.setPixmap(qta.icon(ico_name, color=pal["card_hdr"]).pixmap(size, size))

        for (btn, ico_name) in self._quick_btns:
            btn.setIcon(qta.icon(ico_name, color=pal["quick_icon"]))

        self._chip_icon.setPixmap(
            qta.icon("fa5s.user-shield", color=pal["chip_icon"]).pixmap(16, 16))
        self._chip_lbl.setStyleSheet(
            f"color:{pal['chip_text']};font-size:13px;font-weight:bold;")

        self._btn_refresh.setIcon(qta.icon('fa5s.sync-alt', color=pal['chip_icon']))

        toggle_icon = 'fa5s.sun' if self.current_theme == 'light' else 'fa5s.moon'
        self._btn_theme.setIcon(qta.icon(toggle_icon, color=pal['chip_icon']))

        self.style().polish(self)

    # __________ Refresh btn __________
    def _refresh_app(self):
        """Refreshes stats and briefly spins the refresh icon."""
        self._refresh_stats()
        pal = PALETTES[self.current_theme]
        spin = qta.Spin(self._btn_refresh, interval=60)
        self._btn_refresh.setIcon(
            qta.icon('fa5s.sync-alt', color=pal['chip_icon'], animation=spin))
        QTimer.singleShot(900, lambda: self._btn_refresh.setIcon(
            qta.icon('fa5s.sync-alt', color=pal['chip_icon'])))

    # __________ Stats __________

    def _refresh_stats(self):
        stats = self.controller.get_dashboard_stats()
        self.lbl_total.setText(f"{stats.get('total', 0):,}")
        self.lbl_borrowed.setText(str(stats.get("borrowed", 0)))
        self.lbl_removed.setText(str(stats.get("removed", 0)))

    # __________ Page Change __________
    def _on_page_changed(self, index: int):
        titles = {
            0: "Dashboard",       1: "Search Vault",
            2: "Circulation Desk", 3: "New Entry",
            4: "Reports & Export", 5: "Settings",
            6: "Disposal",
        }
        self._page_title.setText(titles.get(index, ""))
        if index == 0:
            self._refresh_stats()