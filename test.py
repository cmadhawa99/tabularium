import customtkinter as ctk
from app.ui.login_window import LoginWindow
from app.controllers import ArchiveController

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")

    # Initialize your controller
    controller = ArchiveController()

    # Launch just the login window
    login_app = LoginWindow(controller)
    login_app.mainloop()