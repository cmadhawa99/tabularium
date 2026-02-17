from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QLabel, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta


class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Secure Login - WPDC Archive")
        self.setFixedSize(450, 550)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo / Icon
        # --------------------------------------------------------------------------------------------------------------
        lbl_icon = QLabel()
        lbl_icon.setPixmap(qta.icon('fa5s.user-lock', color='#4d7cfe').pixmap(80, 80))
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_icon)

        lbl_title = QLabel("Authorized Access Only")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #8f9bb3; margin-bottom: 20px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Input Fields Container
        # --------------------------------------------------------------------------------------------------------------
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #27293d; border-radius: 10px; padding: 20px;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Username")
        self.txt_user.setStyleSheet(
            "padding: 12px; border: 1px solid #4d7cfe; border-radius: 5px; background: #1e1e2f; color: white;")

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Password")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass.setStyleSheet(
            "padding: 12px; border: 1px solid #4d7cfe; border-radius: 5px; background: #1e1e2f; color: white;")

        self.txt_2fa = QLineEdit()
        self.txt_2fa.setPlaceholderText("2FA Code (6 Digits)")
        self.txt_2fa.setMaxLength(6)
        self.txt_2fa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_2fa.setStyleSheet(
            "padding: 12px; border: 1px solid #e14eca; border-radius: 5px; background: #1e1e2f; color: white; font-weight: bold; letter-spacing: 5px;")


        self.txt_2fa.returnPressed.connect(self.submit_login)

        form_layout.addWidget(self.txt_user)
        form_layout.addWidget(self.txt_pass)
        form_layout.addWidget(self.txt_2fa)
        layout.addWidget(form_frame)

        # Login Button
        # --------------------------------------------------------------------------------------------------------------
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setFixedHeight(50)
        self.btn_login.setStyleSheet("""
            QPushButton { background-color: #4d7cfe; border-radius: 5px; font-weight: bold; font-size: 16px; }
            QPushButton:hover { background-color: #3d63cb; }
        """)
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