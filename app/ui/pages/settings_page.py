from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QComboBox, QCheckBox, QPushButton, QLabel,
                             QTabWidget, QLineEdit, QFileDialog,
                             QListWidget, QMessageBox, QInputDialog, QFrame, QGraphicsDropShadowEffect)
import qtawesome as qta
import os
from PyQt6.QtGui import QColor
from app.settings_manager import settings


class SettingsPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

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

        title = QLabel("System Settings")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_general_tab(), "General & Display")
        self.tabs.addTab(self.create_master_data_tab(), "Master Data")
        self.tabs.addTab(self.create_backup_tab(), "Data & Backup")

        layout.addWidget(self.tabs)

    def create_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)

        grp_gen = self.create_glass_panel()
        gen_layout = QVBoxLayout(grp_gen)
        gen_layout.setContentsMargins(20, 20, 20, 20)
        gen_layout.addWidget(QLabel("General Preferences", objectName="CardTitle"))

        form = QFormLayout()
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItems(["English", "Sinhala", "Tamil"])
        self.cmb_lang.setCurrentText(settings.get("general", "language"))
        self.cmb_lang.currentTextChanged.connect(lambda t: settings.set("general", "language", t))

        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems(["dark", "light"])
        self.cmb_theme.setCurrentText(settings.get("general", "theme"))
        self.cmb_theme.currentTextChanged.connect(self.change_theme)

        form.addRow("Language:", self.cmb_lang)
        form.addRow("App Theme:", self.cmb_theme)
        gen_layout.addLayout(form)
        layout.addWidget(grp_gen)

        grp_disp = self.create_glass_panel()
        disp_layout = QVBoxLayout(grp_disp)
        disp_layout.setContentsMargins(20, 20, 20, 20)
        disp_layout.addWidget(QLabel("Display Options", objectName="CardTitle"))

        form_disp = QFormLayout()
        self.cmb_page_size = QComboBox()
        self.cmb_page_size.addItems(["25", "50", "100", "200"])
        self.cmb_page_size.setCurrentText(str(settings.get("general", "page_size")))
        self.cmb_page_size.currentTextChanged.connect(lambda t: settings.set("general", "page_size", int(t)))

        form_disp.addRow("Records Per Page:", self.cmb_page_size)
        disp_layout.addLayout(form_disp)
        layout.addWidget(grp_disp)

        layout.addStretch()
        return tab

    def create_master_data_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)

        def create_list_editor(title, setting_key):
            grp = self.create_glass_panel()
            vbox = QVBoxLayout(grp)
            vbox.setContentsMargins(20, 20, 20, 20)
            vbox.addWidget(QLabel(title, objectName="CardTitle"))

            list_widget = QListWidget()
            list_widget.addItems(settings.get("master_data", setting_key))
            list_widget.setStyleSheet(
                "background: transparent; border: 1px solid rgba(150,150,150,0.2); border-radius: 5px;")
            vbox.addWidget(list_widget)

            hbox = QHBoxLayout()
            btn_add = QPushButton("Add")
            btn_add.setObjectName("GlassButton")
            btn_add.clicked.connect(lambda: self.add_master_item(list_widget, setting_key))

            btn_del = QPushButton("Remove")
            btn_del.setStyleSheet(
                "background-color: #e74c3c; color: white; border-radius: 5px; font-weight: bold; padding: 8px;")
            btn_del.clicked.connect(lambda: self.remove_master_item(list_widget, setting_key))

            hbox.addWidget(btn_add)
            hbox.addWidget(btn_del)
            vbox.addLayout(hbox)
            return grp

        layout.addWidget(create_list_editor("Manage Sectors", "sectors"))
        layout.addWidget(create_list_editor("Manage Subjects", "subjects"))
        return tab

    def create_backup_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)

        grp_set = self.create_glass_panel()
        set_layout = QVBoxLayout(grp_set)
        set_layout.setContentsMargins(20, 20, 20, 20)
        set_layout.addWidget(QLabel("Backup Configuration", objectName="CardTitle"))

        form = QFormLayout()
        self.chk_auto = QCheckBox("Enable Auto Daily Backup (SQL)")
        self.chk_auto.setChecked(settings.get("backup", "auto_backup"))
        self.chk_auto.toggled.connect(lambda c: settings.set("backup", "auto_backup", c))

        path_layout = QHBoxLayout()
        self.txt_path = QLineEdit(settings.get("backup", "backup_path"))
        btn_browse = QPushButton("Browse...")
        btn_browse.setObjectName("GlassButton")
        btn_browse.clicked.connect(self.browse_folder)
        path_layout.addWidget(self.txt_path)
        path_layout.addWidget(btn_browse)

        form.addRow("Auto Backup:", self.chk_auto)
        form.addRow("Backup Location:", path_layout)
        set_layout.addLayout(form)

        lbl_note = QLabel("Note: Manual exports (CSV/Excel) are located in the Reports section.")
        lbl_note.setStyleSheet("color: #8f9bb3; font-style: italic; margin-top: 10px;")

        layout.addWidget(grp_set)
        layout.addWidget(lbl_note)
        layout.addStretch()
        return tab

    def change_theme(self, theme_name):
        settings.set("general", "theme", theme_name)
        QMessageBox.information(self, "Theme Changed", "Theme saved! Please restart the app to apply changes fully.")

    def add_master_item(self, list_widget, key):
        text, ok = QInputDialog.getText(self, "Add New Item", f"Enter new {key[:-1]}:")
        if ok and text:
            list_widget.addItem(text)
            current_list = settings.get("master_data", key)
            current_list.append(text)
            settings.set("master_data", key, current_list)

    def remove_master_item(self, list_widget, key):
        row = list_widget.currentRow()
        if row >= 0:
            item = list_widget.takeItem(row)
            current_list = settings.get("master_data", key)
            if item.text() in current_list:
                current_list.remove(item.text())
            settings.set("master_data", key, current_list)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
        if folder:
            self.txt_path.setText(folder)
            settings.set("backup", "backup_path", folder)