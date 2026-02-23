from PyQt6.QtGui import QColor

#_________________________________________________________________________________________________________________

PALETTES = {
    "dark": {
        "clk_bezel_a":   "#2a2410",
        "clk_bezel_b":   "#1a1608",
        "clk_bezel_c":   "#0a0800",
        "clk_face_a":    "#1e1c10",
        "clk_face_b":    "#14120a",
        "clk_face_c":    "#0a0900",
        "clk_ring":      "#c8992a",
        "clk_accent":    QColor("#d4af37"),
        "clk_secondary": QColor("#f5e6c0"),
        "clk_minor":     QColor("#7a6820"),
        "clk_second":    QColor("#c0392b"),
        "clk_center":    QColor("#d4af37"),
        "clk_deco":      QColor(212, 175, 55, 60),
        "log_retrieve":  "#e67e22",
        "log_return":    "#2ecc71",
        "log_add":       "#4d7cfe",
        "log_system":    "#8f9bb3",
        "log_text":      "#8f9bb3",
        "card_hdr":      "#d4af37",
        "quick_icon":    "#d4af37",
        "chip_bg":       "rgba(212,175,55,0.10)",
        "chip_border":   "rgba(212,175,55,0.28)",
        "chip_icon":     "#d4af37",
        "chip_text":     "#e0e0e0",
        "accent":        "#d4af37",
        "topbar_bg":     "rgba(14,14,14,0.97)",
        "topbar_title":  "#e0e0e0",
        "divider":       "rgba(212,175,55,0.18)",
        "section_lbl":   "#4a4020",
        "logo_sub":      "#4a4020",
        "clock_lbl":     "#4a4020",
    },
    "light": {
        "clk_bezel_a":   "#ccc9a0",
        "clk_bezel_b":   "#b8b480",
        "clk_bezel_c":   "#a0a060",
        "clk_face_a":    "#f7f3e4",
        "clk_face_b":    "#ede6cc",
        "clk_face_c":    "#e0d8b8",
        "clk_ring":      "#0f5132",
        "clk_accent":    QColor("#0f5132"),
        "clk_secondary": QColor("#1e3d2a"),
        "clk_minor":     QColor("#9db8a8"),
        "clk_second":    QColor("#8b1a0a"),
        "clk_center":    QColor("#0f5132"),
        "clk_deco":      QColor(15, 81, 50, 55),
        "log_retrieve":  "#a04a08",
        "log_return":    "#1a6b3a",
        "log_add":       "#1a4080",
        "log_system":    "#6b7b6e",
        "log_text":      "#2a4232",
        "card_hdr":      "#0f5132",
        "quick_icon":    "#0f5132",
        "chip_bg":       "rgba(15,81,50,0.08)",
        "chip_border":   "rgba(15,81,50,0.24)",
        "chip_icon":     "#0f5132",
        "chip_text":     "#0f3320",
        "accent":        "#0f5132",
        "topbar_bg":     "rgba(255,255,255,0.97)",
        "topbar_title":  "#1a2e22",
        "divider":       "rgba(15,81,50,0.16)",
        "section_lbl":   "#9db8ab",
        "logo_sub":      "#9db8ab",
        "clock_lbl":     "#7a9e8a",
    },
}


#_________________________________________________________________________________________________________________

def get_stylesheet(theme="dark"):
    if theme == "dark":
        bg_main = "#121212"
        bg_sidebar = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e24, stop:1 #121212)"
        glass_panel = "rgba(30, 30, 35, 0.7)"
        glass_border = "rgba(255, 255, 255, 0.08)"
        text_primary = "#e0e0e0"
        text_secondary = "#8f9bb3"
        text_accent = "#d4af37"
        btn_hover = "rgba(212, 175, 55, 0.15)"
        table_header_bg = "rgba(255, 255, 255, 0.03)"
        table_row_border = "rgba(255, 255, 255, 0.05)"
    else:
        bg_main = "#f4f4f8"
        bg_sidebar = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f0f0f0)"
        glass_panel = "rgba(255, 255, 255, 0.9)"
        glass_border = "rgba(0, 0, 0, 0.08)"
        text_primary = "#2d2d2d"
        text_secondary = "#6b7280"
        text_accent = "#0f5132"
        btn_hover = "rgba(15, 81, 50, 0.1)"
        table_header_bg = "rgba(0, 0, 0, 0.02)"
        table_row_border = "rgba(0, 0, 0, 0.06)"

    return f"""
    QMainWindow {{ background-color: {bg_main}; }}

    #Sidebar {{
        background: {bg_sidebar};
        border-right: 2px solid {text_accent};
    }}

    #Logo {{
        color: {text_accent};
        font-family: "Times New Roman", serif;
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}

    #NavButton {{
        background-color: transparent;
        color: {text_primary};
        text-align: left;
        padding: 12px 20px;
        border-radius: 8px;
        font-family: "Segoe UI", sans-serif;
        font-size: 14px;
        border: none;
    }}
    #NavButton:hover {{
        background-color: {btn_hover};
        color: {text_accent};
        border-left: 3px solid {text_accent};
    }}
    #NavButton:checked {{
        background-color: {btn_hover};
        color: {text_accent};
        font-weight: bold;
        border-left: 4px solid {text_accent};
    }}

    #Card, #GradientCard {{
        background-color: {glass_panel};
        border: 1px solid {glass_border};
        border-radius: 12px;
    }}

    #CardTitle {{
        color: {text_secondary};
        font-size: 13px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    #CardValue {{
        color: {text_accent};
        font-size: 32px;
        font-family: "Times New Roman", serif;
        font-weight: bold;
    }}

    #pageTitle {{
        color: {text_primary};
        font-family: "Times New Roman", serif;
        font-size: 28px;
        border-bottom: 1px solid {text_accent};
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}

    QLabel {{ color: {text_primary}; }}

    QLineEdit, QComboBox, QDateEdit {{
        background-color: {glass_panel};
        border: 1px solid {glass_border};
        color: {text_primary};
        padding: 10px 15px;
        border-radius: 8px;
        font-family: "Nirmala UI", "Iskoola Pota", sans-serif;
    }}
    QLineEdit:focus {{ border: 1px solid {text_accent}; }}

    #GlassButton {{
        background-color: {glass_panel};
        border: 1px solid {glass_border};
        color: {text_primary};
        border-radius: 8px;
        padding: 8px 15px;
        font-weight: bold;
    }}
    #GlassButton:hover {{
        background-color: {btn_hover};
        border: 1px solid {text_accent};
        color: {text_accent};
    }}
    #GlassButton:disabled {{
        color: gray;
        border: 1px solid transparent;
    }}

    #PrimaryActionBtn {{
        background-color: {text_accent};
        color: white;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
    }}

    QTabWidget::pane {{ border: none; background: transparent; }}
    QTabBar::tab {{
        background: transparent;
        color: {text_secondary};
        padding: 10px 25px;
        font-weight: bold;
        font-size: 14px;
        border-bottom: 3px solid transparent;
        margin-right: 5px;
    }}
    QTabBar::tab:selected {{
        color: {text_accent};
        border-bottom: 3px solid {text_accent};
    }}
    QTabBar::tab:hover {{ background: {btn_hover}; color: {text_primary}; }}

    QTableWidget {{
        background-color: transparent;
        border: none;
        color: {text_primary};
        gridline-color: transparent;
        outline: none;
    }}

    QHeaderView::section {{
        background-color: {table_header_bg};
        color: {text_secondary};
        font-weight: bold;
        font-size: 13px;
        border: none;
        border-bottom: 1px solid {glass_border};
        padding: 15px 10px;
    }}

    QTableWidget::item {{
        border-bottom: 1px solid {table_row_border};
        padding: 5px 10px;
    }}

    QTableWidget::item:selected {{
        background-color: {btn_hover};
        color: {text_accent};
    }}

    QScrollBar:vertical {{ border: none; background: transparent; width: 6px; }}
    QScrollBar::handle:vertical {{ background: {glass_border}; border-radius: 3px; }}
    QScrollBar::handle:vertical:hover {{ background: {text_accent}; }}
    """


#_________________________________________________________________________________________________________________

def get_structural_stylesheet(pal: dict) -> str:
    return f"""
        #TopBar {{
            background: {pal['topbar_bg']};
            border-bottom: 1px solid {pal['divider']};
        }}
        #TopBarTitle {{
            font-family: "Times New Roman", serif;
            font-size: 22px;
            font-weight: bold;
            color: {pal['topbar_title']};
        }}
        #LogoBlock {{ background: transparent; }}
        #LogoSub {{
            font-size: 10px;
            font-family: "Segoe UI", sans-serif;
            letter-spacing: 1.5px;
            color: {pal['logo_sub']};
        }}
        #SectionLabel {{
            font-size: 10px;
            font-family: "Segoe UI", sans-serif;
            letter-spacing: 2px;
            color: {pal['section_lbl']};
            margin-top: 6px;
            margin-bottom: 2px;
        }}
        #Divider {{
            color: {pal['divider']};
            background: {pal['divider']};
            border: none;
            max-height: 1px;
        }}
        #UserChip {{
            background: {pal['chip_bg']};
            border: 1px solid {pal['chip_border']};
            border-radius: 16px;
        }}
        #ChipLabel {{
            font-size: 13px;
            font-weight: bold;
            color: {pal['chip_text']};
        }}
        #ClockLabel {{
            font-family: "Consolas", monospace;
            font-size: 10px;
            color: {pal['clock_lbl']};
        }}
        #PageTitle {{
            font-family: "Times New Roman", serif;
            font-size: 28px;
        }}
        #ThemeToggleBtn {{
            background: {pal['chip_bg']};
            border: 1px solid {pal['chip_border']};
            border-radius: 8px;
        }}
        #ThemeToggleBtn:hover {{
            background: {pal['chip_border']};
        }}
    """


#_________________________________________________________________________________________________________________

def login_container_stylesheet() -> str:
    return """
        #LoginContainer {
            background: #0d0c08;
            border: 1px solid rgba(212, 175, 55, 0.32);
            border-radius: 16px;
        }
    """


def login_close_btn_stylesheet() -> str:
    return """
        QPushButton {
            background: rgba(212, 175, 55, 0.06);
            border: 1px solid rgba(212, 175, 55, 0.14);
            border-radius: 6px;
        }
        QPushButton:hover {
            background: rgba(200, 50, 50, 0.28);
            border: 1px solid rgba(220, 80, 80, 0.45);
        }
    """


def login_title_stylesheet() -> str:
    return """
        color: #d4af37;
        font-family: "Times New Roman", serif;
        font-size: 30px;
        font-weight: bold;
        letter-spacing: 8px;
    """


def login_org_stylesheet() -> str:
    return """
        color: #4a4020;
        font-family: "Segoe UI", sans-serif;
        font-size: 9px;
        letter-spacing: 3.5px;
    """


def login_badge_stylesheet() -> str:
    return """
        color: #3a3018;
        font-family: "Segoe UI", sans-serif;
        font-size: 9px;
        letter-spacing: 2px;
    """


def login_footer_stylesheet() -> str:
    return """
        color: rgba(212, 175, 55, 0.16);
        font-family: "Times New Roman", serif;
        font-size: 9px;
        letter-spacing: 2px;
        padding-bottom: 20px;
    """


def login_status_stylesheet(success: bool = False) -> str:
    color = "#2ecc71" if success else "#c0392b"
    return f"color: {color}; font-size: 12px; font-family: 'Segoe UI', sans-serif;"


def vault_input_field_stylesheet() -> str:
    return """
        QLineEdit {
            background: transparent;
            border: none;
            color: #faedc0;
            font-family: "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 500;
            padding: 0px;
        }
    """


def vault_input_normal_stylesheet() -> str:
    return """
        VaultInput {
            background: rgba(28, 24, 10, 0.92);
            border: 1px solid rgba(212, 175, 55, 0.55);
            border-radius: 7px;
        }
    """


def vault_input_active_stylesheet() -> str:
    return """
        VaultInput {
            background: rgba(38, 32, 12, 0.98);
            border: 2px solid rgba(212, 175, 55, 1.0);
            border-radius: 7px;
        }
    """


def gold_button_stylesheet() -> str:
    return """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #b8940e, stop:0.5 #d4af37, stop:1 #b8940e
            );
            color: #0d0c08;
            border: none;
            border-radius: 8px;
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
        }
        QPushButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #c8a420, stop:0.5 #e8c94a, stop:1 #c8a420
            );
        }
        QPushButton:pressed {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #9a7a08, stop:0.5 #b8940e, stop:1 #9a7a08
            );
        }
        QPushButton:disabled {
            background: rgba(212, 175, 55, 0.22);
            color: rgba(13, 12, 8, 0.45);
        }
    """