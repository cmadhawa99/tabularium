"""
All CTk colors use (dark, light) tuples via C() so ctk.set_appearance_mode()
handles switching automatically. Only TTK Treeview pages need retheme().
Idk what this mean btw
"""

import customtkinter as ctk
import datetime

from app.ui.ctk_utils import C
from app.controllers import ArchiveController
from app.ui.pages.search_page import SearchPage
from app.ui.pages.add_file_page import AddFilePage
from app.ui.pages.circulation_page import CirculationPage
from app.ui.pages.reports_page import ReportsPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.disposal_page import DisposalPage

class DigitalClock(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('fg_color', 'transparent')
        super().__init__(master, **kwargs)
        self.lbl_time = ctk.CTkLabel(self, text="00:00:00", font=ctk.CTkFont("Courier New", 28, "bold"), tex_color=C("accent"))
        self.lbl_time.pack(pady=(0,2))

        self.lbl_date = ctk.CTkLabel