import math
import qtawesome as qta
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QLabel, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPoint
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, QFont,
                          QLinearGradient, QRadialGradient, QPainterPath, QPalette)

from app.ui.themes import (
    login_container_stylesheet, login_close_btn_stylesheet,
    login_title_stylesheet, login_org_stylesheet,
    login_badge_stylesheet, login_footer_stylesheet,
    login_status_stylesheet, vault_input_field_stylesheet,
    vault_input_normal_stylesheet, vault_input_active_stylesheet,
    gold_button_stylesheet,
)


class VaultCanvas(QWidget):

    GOLD       = QColor("#d4af37")
    GOLD_DIM   = QColor(212, 175, 55, 50)
    GOLD_FAINT = QColor(212, 175, 55, 18)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        bg = QLinearGradient(0, 0, 0, H)
        bg.setColorAt(0.0, QColor("#111009"))
        bg.setColorAt(0.5, QColor("#0d0c08"))
        bg.setColorAt(1.0, QColor("#080700"))
        p.fillRect(self.rect(), QBrush(bg))

        glow = QRadialGradient(W / 2, H * 0.38, H * 0.55)
        glow.setColorAt(0.0, QColor(212, 175, 55, 20))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.fillRect(self.rect(), QBrush(glow))

        m = 18
        p.setPen(QPen(self.GOLD_DIM, 1.2))
        p.drawRect(m, m, W - m*2, H - m*2)
        p.setPen(QPen(self.GOLD_FAINT, 0.7))
        p.drawRect(m+5, m+5, W-(m+5)*2, H-(m+5)*2)

        cs = 22
        p.setPen(QPen(self.GOLD_DIM, 1.5))
        for cx, cy, sx, sy in [(m,m,1,1),(W-m,m,-1,1),(m,H-m,1,-1),(W-m,H-m,-1,-1)]:
            p.drawLine(cx, cy, cx+sx*cs, cy)
            p.drawLine(cx, cy, cx, cy+sy*cs)
            p.drawLine(cx+sx*5, cy+sy*5, cx+sx*(cs-4), cy+sy*5)
            p.drawLine(cx+sx*5, cy+sy*5, cx+sx*5, cy+sy*(cs-4))

        arch_cx = W / 2
        arch_cy = int(H * 0.10) + 52
        arch_r  = 52
        p.setPen(QPen(self.GOLD_DIM, 1.0))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QPoint(int(arch_cx), arch_cy), arch_r, arch_r)
        p.setPen(QPen(self.GOLD_FAINT, 0.7))
        p.drawEllipse(QPoint(int(arch_cx), arch_cy), arch_r+8, arch_r+8)
        p.setPen(QPen(self.GOLD_DIM, 1.2))
        for i in range(12):
            a  = math.radians(i * 30)
            dx = math.cos(a) * (arch_r - 7)
            dy = math.sin(a) * (arch_r - 7)
            p.drawPoint(int(arch_cx + dx), int(arch_cy + dy))

        ry  = int(H * 0.37)
        rm  = 44
        rg  = 88
        p.setPen(QPen(QColor(212,175,55,55), 1.0))
        p.drawLine(rm, ry, W//2-rg, ry)
        p.drawLine(W//2+rg, ry, W-rm, ry)
        p.setPen(QPen(QColor(212,175,55,20), 0.6))
        p.drawLine(rm, ry+3, W//2-rg, ry+3)
        p.drawLine(W//2+rg, ry+3, W-rm, ry+3)

        p.setPen(QPen(self.GOLD_DIM, 1.0))
        p.setBrush(QBrush(self.GOLD_DIM))
        d = QPainterPath()
        d.moveTo(W/2, ry-4); d.lineTo(W/2+5, ry)
        d.lineTo(W/2, ry+4); d.lineTo(W/2-5, ry)
        d.closeSubpath()
        p.drawPath(d)

        p.setPen(QPen(self.GOLD_FAINT, 0.7))
        p.drawLine(rm, int(H*0.92), W-rm, int(H*0.92))

        p.setPen(QPen(QColor(212,175,55,10), 1))
        for x in [int(W*0.12), int(W*0.88)]:
            p.drawLine(x, int(H*0.33), x, int(H*0.90))


class GoldDivider(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(14)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W   = self.width()
        mid = W // 2
        y   = self.height() // 2
        gap = 10

        p.setPen(QPen(QColor(212,175,55,55), 1.0))
        p.drawLine(40, y, mid-gap, y)
        p.drawLine(mid+gap, y, W-40, y)

        p.setPen(QPen(QColor(212,175,55,90), 1.2))
        p.setBrush(QBrush(QColor(212,175,55,80)))
        path = QPainterPath()
        path.moveTo(mid, y-5); path.lineTo(mid+5, y)
        path.lineTo(mid, y+5); path.lineTo(mid-5, y)
        path.closeSubpath()
        p.drawPath(path)


class VaultInput(QWidget):

    def __init__(self, placeholder: str, icon_name: str,
                 echo_mode=QLineEdit.EchoMode.Normal, parent=None):
        super().__init__(parent)
        self._icon_name = icon_name
        self.setFixedHeight(52)

        h = QHBoxLayout(self)
        h.setContentsMargins(16, 0, 16, 0)
        h.setSpacing(12)

        self._icon_lbl = QLabel()
        self._icon_lbl.setFixedSize(18, 18)
        self._icon_lbl.setPixmap(qta.icon(icon_name, color="#8a7840").pixmap(16, 16))
        h.addWidget(self._icon_lbl)

        self.field = QLineEdit()
        self.field.setPlaceholderText(placeholder)
        self.field.setEchoMode(echo_mode)
        self.field.setFrame(False)
        self.field.setStyleSheet(vault_input_field_stylesheet())
        palette = self.field.palette()
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#6a5e38"))
        self.field.setPalette(palette)
        h.addWidget(self.field)

        self._style_normal()
        self.field.focusInEvent  = self._on_focus_in
        self.field.focusOutEvent = self._on_focus_out

    def _style_normal(self):
        self.setStyleSheet(vault_input_normal_stylesheet())

    def _style_active(self):
        self.setStyleSheet(vault_input_active_stylesheet())

    def _on_focus_in(self, e):
        self._style_active()
        self._icon_lbl.setPixmap(qta.icon(self._icon_name, color="#d4af37").pixmap(16, 16))
        QLineEdit.focusInEvent(self.field, e)

    def _on_focus_out(self, e):
        self._style_normal()
        self._icon_lbl.setPixmap(qta.icon(self._icon_name, color="#8a7840").pixmap(16, 16))
        QLineEdit.focusOutEvent(self.field, e)

    def text(self) -> str:
        return self.field.text()

    def clear(self):
        self.field.clear()

    def setFocus(self):
        self.field.setFocus()

    def connect_return(self, slot):
        self.field.returnPressed.connect(slot)


class GoldButton(QPushButton):

    def __init__(self, text: str, icon_name: str, parent=None):
        super().__init__(f"  {text}", parent)
        self.setFixedHeight(50)
        self.setIcon(qta.icon(icon_name, color="#0d0c08"))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(gold_button_stylesheet())


class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller  = controller
        self._drag_pos   = None

        self.setWindowTitle("Archivum — Secure Access")
        self.setFixedSize(480, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build_ui()

    # __________ DRAG SUPPORT __________

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, _e):
        self._drag_pos = None

    # __________ BUILD UI __________

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setObjectName("LoginContainer")
        container.setStyleSheet(login_container_stylesheet())
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(70)
        shadow.setOffset(0, 14)
        shadow.setColor(QColor(0, 0, 0, 210))
        container.setGraphicsEffect(shadow)
        root.addWidget(container)

        self._canvas = VaultCanvas(container)
        self._canvas.setGeometry(0, 0, 480, 650)
        self._canvas.lower()

        v = QVBoxLayout(container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        # __________ Top bar with close button __________

        top = QHBoxLayout()
        top.setContentsMargins(16, 14, 16, 0)
        top.addStretch()
        btn_close = QPushButton()
        btn_close.setFixedSize(28, 28)
        btn_close.setIcon(qta.icon("fa5s.times", color="#4a4020"))
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet(login_close_btn_stylesheet())
        btn_close.clicked.connect(self.close)
        top.addWidget(btn_close)
        v.addLayout(top)

        # __________ Seal icon __________

        v.addSpacing(12)
        seal = QLabel()
        seal.setPixmap(qta.icon("fa5s.landmark", color="#d4af37").pixmap(46, 46))
        seal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(seal)

        # __________ Title __________

        v.addSpacing(12)
        lbl_title = QLabel("ARCHIVUM")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(login_title_stylesheet())
        v.addWidget(lbl_title)

        lbl_org = QLabel("WELIGEPOLA DISTRICT COUNCIL")
        lbl_org.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_org.setStyleSheet(login_org_stylesheet())
        v.addWidget(lbl_org)

        # __________ Divider __________

        v.addSpacing(18)
        v.addWidget(GoldDivider())
        v.addSpacing(16)

        # __________ Access badge __________

        badge = QHBoxLayout()
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ic = QLabel()
        ic.setPixmap(qta.icon("fa5s.shield-alt", color="#3a3018").pixmap(11, 11))
        bl = QLabel("AUTHORIZED ACCESS ONLY")
        bl.setStyleSheet(login_badge_stylesheet())
        badge.addWidget(ic)
        badge.addSpacing(6)
        badge.addWidget(bl)
        v.addLayout(badge)

        # __________ Input fields __________

        v.addSpacing(26)
        form = QVBoxLayout()
        form.setContentsMargins(46, 0, 46, 0)
        form.setSpacing(14)

        self._inp_user = VaultInput("Username", "fa5s.user")
        self._inp_pass = VaultInput("Password", "fa5s.lock",
                                    echo_mode=QLineEdit.EchoMode.Password)
        self._inp_2fa  = VaultInput("2FA Code  (6 digits)", "fa5s.key")
        self._inp_2fa.field.setMaxLength(6)
        self._inp_2fa.field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._inp_2fa.connect_return(self._submit)

        for inp in (self._inp_user, self._inp_pass, self._inp_2fa):
            form.addWidget(inp)

        v.addLayout(form)

        # __________ Login button __________

        v.addSpacing(26)
        btn_wrap = QHBoxLayout()
        btn_wrap.setContentsMargins(46, 0, 46, 0)
        self._btn_login = GoldButton("ENTER THE VAULT", "fa5s.sign-in-alt")
        self._btn_login.clicked.connect(self._submit)
        btn_wrap.addWidget(self._btn_login)
        v.addLayout(btn_wrap)

        # __________ Status label __________

        v.addSpacing(14)
        self._lbl_status = QLabel("")
        self._lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lbl_status.setFixedHeight(18)
        self._lbl_status.setStyleSheet(login_status_stylesheet())
        v.addWidget(self._lbl_status)

        # __________ Footer __________

        v.addStretch()
        footer = QLabel("ARCHIVUM  ·  AUCTORITAS ET CUSTODIA")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(login_footer_stylesheet())
        v.addWidget(footer)

    # __________ SUBMIT __________

    def _submit(self):
        user = self._inp_user.text().strip()
        pwd  = self._inp_pass.text().strip()
        code = self._inp_2fa.text().strip()

        if not user or not pwd or not code:
            self._show_error("All fields are required.")
            return

        self._btn_login.setEnabled(False)
        self._btn_login.setText("  AUTHENTICATING...")

        success, msg, role = self.controller.attempt_login(user, pwd, code)

        if success:
            self._lbl_status.setStyleSheet(login_status_stylesheet(success=True))
            self._lbl_status.setText("Access granted — opening vault…")
            QTimer.singleShot(700, lambda: self.login_successful.emit(role))
        else:
            self._btn_login.setEnabled(True)
            self._btn_login.setText("  ENTER THE VAULT")
            self._show_error(msg)
            self._inp_pass.clear()
            self._inp_2fa.clear()
            self._inp_pass.setFocus()

    def _show_error(self, msg: str):
        self._lbl_status.setStyleSheet(login_status_stylesheet(success=False))
        self._lbl_status.setText(msg)
        QTimer.singleShot(3500, lambda: self._lbl_status.setText(""))