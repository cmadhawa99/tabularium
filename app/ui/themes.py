THEMES = {
    "dark": {
        "bg_main": "#1e1e2f",
        "bg_panel": "#27293d",
        "text_main": "#ffffff",
        "text_sec": "#8f9bb3",
        "accent": "#e14eca",
        "accent_2": "#4d7cfe",
        "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1d8cf8, stop:1 #3358f4)",
        "danger": "#fd5d93",
        "success": "#00f2c3",
        "border": "none",
        "hover": "#344675"

    },

    "light": {
        "bg_main": "#f5f6fa",
        "bg_panel": "#ffffff",
        "text_main": "#2c3e50",
        "text_sec": "#95a5a6",
        "accent": "#e14eca",
        "accent_2": "#4d7cfe",
        "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4d7cfe, stop:1 #9b59b6)",
        "danger": "#e74c3c",
        "success": "#2ecc71",
        "border": "1px solid #dcdde1",
        "hover": "#ecf0f1"
    }
}

def get_stylesheet(theme_name="dark"):
    t = THEMES[theme_name]

    return f"""
    QMainWindow {{ background-color: {t['bg_main']}; }}
    QWidget {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; color: {t['text_main']}; 
    }}
    
    /*  --------------- SIDEBAR --------------- */
    
    QFrame#Sidebar {{
        background-color: {t['bg_main']}
    }}
    
    QLabel#logo {{
        font-size: 22px;
        font-weight: 900;
        color: {t['text_sec']};
        padding-left: 10px;
    }}
    
    /* --------------- NAV BUTTONS --------------- */
    
    QPushButton#NavButton {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        color: {t['text_sec']};
        text-alight: left;
        padding: 15px 20px;
        font-weight: 600;
        font-size: 14px;
    }}
    
    QPushButton#NavButton:hover {{
        background-color: {t['hover']};
        color: {t['text_main']};
    }}
    
    QPushButton#NavButton:checked {{
        background-color: {t['accent_2']};
        color: white;
        font-weight: bold;
    }}
    
    /* --------------- CARDS --------------- */
    
    QFrame#Card {{
        background-color: {t['bg_panel']};
        border-radius: 12px;
    }}
    
    QFrame#GradientCard {{
        background-color: {t['accent_2']};  /* Fallback */
        background: {t['gradient']};
        border-radius: 12px;
        color: white;
    }}
    
    /* --------------- TEXT HIERARCHY --------------- */
    
    QLabel#PageTitle {{
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }}
    
    QLabel#CardTitle {{
        font-size: 13px;
        color: {t['text_sec']}; 
        font-weight: 500;
    }}
    
    QLabel#CardValue {{
        font-size: 32px;
        font-weight: bold;
        margin-top: 5px;
    }}
    
    QLabel#CardIcon {{
        font-size: 40px;
        color: {t['accent']}
    }}
    
    
    /* --------------- SPECIAL FOR GRADIENT CARD --------------- */
    
    QLabel#WhiteText {{ color: white; }}
       
"""
