PALETTES = {
    "dark": {

        "bg_main": "#0d0c08",
        "bg_sidebar": "#0f0e0a",
        "bg_topbar": "#0f0e0a",
        "bg_card": "#17150e",
        "bg_input": "#111009",
        "bg_table_odd": "#111009",
        "bg_table_even": "#0f0e0a",
        "bg_table_sel": "#2a2515",
        "bg_table_head": "#0a0900",

        "accent": "#d4af37",
        "accent_hover": "#e8c94a",
        "accent_dim": "#8a7840",
        "accent_faint": "#3a3018",
        "accent_v_faint": "#1a1608",

        "border": "#2a2515",
        "border_focus": "#d4af37",
        "border_subtle": "#1e1c10",

        "text_primary": "#e8dcc8",
        "text_secondary": "#8a7840",
        "text_muted": "#4a4020",
        "text_accent": "#d4af37",

        "success": "#2ecc71",
        "warning": "#e67e22",
        "danger": "#e74c3c",
        "info": "#4d7cfe",

        "tree_bg": "#0f0e0a",
        "tree_field": "#0d0c08",
        "tree_sel_bg": "#2a2515",
        "tree_sel_fg": "#d4af37",
        "tree_head_bg": "#0a0900",
        "tree_head_fg": "#8a7840",
        "tree_row_fg": "#e8dcc8",
    },
    "light": {

        "bg_main": "#f0ece0",
        "bg_sidebar": "#e8e2d4",
        "bg_topbar": "#f8f5ed",
        "bg_card": "#faf7f0",
        "bg_input": "#ffffff",
        "bg_table_odd": "#faf7f0",
        "bg_table_even": "#f3efe4",
        "bg_table_sel": "#d8ede4",
        "bg_table_head": "#e8e2d4",

        "accent": "#0f5132",
        "accent_hover": "#1a7a4a",
        "accent_dim": "#9db8ab",
        "accent_faint": "#d8ede4",
        "accent_v_faint": "#eaf5ef",

        "border": "#c8c0a8",
        "border_focus": "#0f5132",
        "border_subtle": "#d8d0b8",

        "text_primary": "#1a180a",
        "text_secondary": "#5a6b5e",
        "text_muted": "#9aab9e",
        "text_accent": "#0f5132",

        "success": "#1a6b3a",
        "warning": "#a04a08",
        "danger": "#8b1a0a",
        "info": "#1a4080",

        "tree_bg": "#faf7f0",
        "tree_field": "#f3efe4",
        "tree_sel_bg": "#d8ede4",
        "tree_sel_fg": "#0f5132",
        "tree_head_bg": "#e8e2d4",
        "tree_head_fg": "#5a6b5e",
        "tree_row_fg": "#1a180a",
    },
}

def get_ctk_theme_colors(mode: str) -> dict:
    d = PALETTES["dark"]
    l = PALETTES["light"]
    if mode == "dark":
        return {
            "card_fg":   (d["bg_card"],    l["bg_card"]),
            "input_fg":  (d["bg_input"],   l["bg_input"]),
            "border":    (d["border"],      l["border"]),
            "accent":    (d["accent"],      l["accent"]),
        }
    return {}


def build_treeview_style(pal: dict, style_name: str = "Archive.Treeview"):

    return {
        "style_name": style_name,
        "bg": pal["tree_bg"],
        "field_bg": pal["tree_field"],
        "sel_bg": pal["tree_sel_bg"],
        "sel_fg": pal["tree_sel_fg"],
        "head_bg": pal["tree_head_bg"],
        "head_fg": pal["tree_head_fg"],
        "row_fg": pal["tree_row_fg"],
        "border": pal["border"],
        "rowheight": 48,
    }