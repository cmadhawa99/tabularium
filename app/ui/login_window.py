from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QFrame, QMessageBox, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
import qtawesome as qta
from app.ui.themes import get_stylesheet
from app.settings_manager import settings


class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Secure Login - WPDC Archive")
        self.setFixedSize(450, 550)

        theme = settings.get("general", "theme") if settings.get("general", "theme") else "dark"
        self.setStyleSheet(get_stylesheet(theme))

        self.setup_ui()

    def create_glass_panel(self):
        frame = QFrame()
        frame.setObjectName("Card")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 40))
        frame.setGraphicsEffect(shadow)
        return frame

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        theme = settings.get("general", "theme")
        accent_color = "#0f5132" if theme == "light" else "#d4af37"

        lbl_icon = QLabel()
        lbl_icon.setPixmap(qta.icon('fa5s.user-lock', color=accent_color).pixmap(80, 80))
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_icon)

        lbl_title = QLabel("Authorized Access Only")
        lbl_title.setStyleSheet(
            f"font-size: 18px; font-family: 'Times New Roman', serif; font-weight: bold; color: {accent_color}; margin-bottom: 10px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        form_frame = self.create_glass_panel()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(25, 30, 25, 30)

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Username")
        self.txt_user.setFixedHeight(45)

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Password")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass.setFixedHeight(45)

        self.txt_2fa = QLineEdit()
        self.txt_2fa.setPlaceholderText("2FA Code (6 Digits)")
        self.txt_2fa.setMaxLength(6)
        self.txt_2fa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_2fa.setFixedHeight(45)
        self.txt_2fa.setStyleSheet("letter-spacing: 5px; font-weight: bold; font-size: 16px;")

        self.txt_2fa.returnPressed.connect(self.submit_login)

        form_layout.addWidget(self.txt_user)
        form_layout.addWidget(self.txt_pass)
        form_layout.addWidget(self.txt_2fa)
        layout.addWidget(form_frame)

        self.btn_login = QPushButton(" Login")
        self.btn_login.setIcon(qta.icon('fa5s.sign-in-alt', color='white'))
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setFixedHeight(50)
        self.btn_login.setObjectName("PrimaryActionBtn")
        self.btn_login.clicked.connect(self.submit_login)
        layout.addWidget(self.btn_login)

        layout.addStretch()

    def submit_login(self):
        user = self.txt_user.text().strip()
        pwd = self.txt_pass.text().strip()
        code = self.txt_2fa.text().strip()

        if not user or not pwd or not code:
            QMessageBox.warning(self, "Missing Info", "Please enter Username, Password, and 2FA Code.")
            return

        success, msg, role = self.controller.attempt_login(user, pwd, code)

        if success:
            self.login_successful.emit(role)
        else:
            QMessageBox.critical(self, "Login Failed", msg)
            self.txt_pass.clear()
            self.txt_2fa.clear()
            self.txt_pass.setFocus()