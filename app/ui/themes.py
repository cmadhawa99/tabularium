def get_stylesheet(theme="dark"):
    if theme == "dark":
        bg_main = "#121212"
        bg_sidebar = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1e1e24, stop:1 #121212)"

        glass_panel = "rgba(30, 30, 35, 0.7)"
        glass_border = "rgba(255, 255, 255, 0.08)"  # Very faint border

        text_primary = "#e0e0e0"
        text_secondary = "#8f9bb3"
        text_accent = "#d4af37"  # Roman Gold
        btn_hover = "rgba(212, 175, 55, 0.15)"

        table_header_bg = "rgba(255, 255, 255, 0.03)"
        table_row_border = "rgba(255, 255, 255, 0.05)"

    else:  # Light Mode
        bg_main = "#f4f4f8"
        bg_sidebar = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f0f0f0)"

        glass_panel = "rgba(255, 255, 255, 0.9)"
        glass_border = "rgba(0, 0, 0, 0.08)"  # Very faint border

        text_primary = "#2d2d2d"
        text_secondary = "#6b7280"
        text_accent = "#0f5132"  # Dark Emerald
        btn_hover = "rgba(15, 81, 50, 0.1)"

        table_header_bg = "rgba(0, 0, 0, 0.02)"
        table_row_border = "rgba(0, 0, 0, 0.06)"

    return f"""
    /* --- MAIN WINDOW --- */
    QMainWindow {{ background-color: {bg_main}; }}

    /* --- SIDEBAR --- */
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

    /* --- NAVIGATION --- */
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

    /* --- PANELS & CARDS (Glassmorphism) --- */
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

    /* --- INPUTS & BUTTONS --- */
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

    /* --- MODERN TABS --- */
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

    /* --- SLEEK SAAS TABLES --- */
    QTableWidget {{
        background-color: transparent;
        border: none;
        color: {text_primary};
        gridline-color: transparent; /* Removes heavy grid */
        outline: none; /* Removes focus dotted line */
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
        border-bottom: 1px solid {table_row_border}; /* Faint horizontal line only */
        padding: 5px 10px;
    }}

    QTableWidget::item:selected {{ 
        background-color: {btn_hover}; 
        color: {text_accent};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{ border: none; background: transparent; width: 6px; }}
    QScrollBar::handle:vertical {{ background: {glass_border}; border-radius: 3px; }}
    QScrollBar::handle:vertical:hover {{ background: {text_accent}; }}
    """

