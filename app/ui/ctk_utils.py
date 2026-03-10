from tkinter import ttk
import customtkinter as ctk
from app.ui.themes import PALETTES

def C(key: str) -> tuple:
    return (PALETTES["dark"][key], PALETTES["light"][key])

def apply_treeview_style(style: ttk.Style, theme: str, style_name: str = "Arch.Treeview"):
    pal = PALETTES[theme]
    style.theme_use("default")\

    style.configure (style_name,
                     background=pal["tree_bg"],
                     fieldbackground=pal["tree_field"],
                     foreground=pal["tree_row_fg"],
                     rowheight=48,
                     borderwidth=0,
                     relief="flat",
                     font=("Georgia", 12))

    style.configure (f"{style_name}.Heading",
                     background=pal["tree_head_bg"],
                     foreground=pal["tree_head_fg"],
                     font=("Georgia", 11, "bold"),
                     relief="flat",
                     borderwidth=0,
                     padding=(10, 12))

    style.map (style_name,
              background=[("selected", pal["tree_sel_bg"])],
              foreground=[("selected", pal["tree_sel_fg"])],
              )

    style.map (f"{style_name}.Heading",
               background=[("active", pal["accent_faint"])],
               )

    sb = f"{style_name}.Vertical.TScrollbar"

    style.configure (sb,
                     troughcolor=pal["bg_main"],
                     background=pal["border"],
                     arrowcolor=pal["accent"],
                     borderwidth=0,
                     relief="flat",
                     width=8,)

    style.map(sb, background=[("active", pal["accent"])])

def make_treeview(parent, columns: list, theme: str, style: ttk.Style, style_name: str = "Arch.Treeview",
                  height: int = 20) -> ttk.Treeview:
    apply_treeview_style(style, theme, style_name)
    pal = PALETTES[theme]

    tree = ttk.Treeview (
        parent,
        columns=[c[0] for c in columns],
        show="headings",
        style=style_name,
        height=height,
    )

    for col_id, heading, width, anchor in columns:
        tree.heading(col_id, text=heading, anchor=anchor)
        tree.column(col_id, width=width, anchor=anchor, stretch=True)


    tree.tag_configure("odd", background=pal["bg_table_odd"], foreground=pal["tree_row_fg"])
    tree.tag_configure("even", background=pal["bg_table_even"], foreground=pal["tree_row_fg"])
    tree.tag_configure("borrowed", foreground=pal["warning"])
    tree.tag_configure("removed", foreground=pal["danger"])
    tree.tag_configure("available", foreground=pal["success"])
    return tree

def add_scrolled_tree(parent, tree: ttk.Treeview, style: ttk.Style,
                      style_name: str = "Arch.Treeview") -> ttk.Scrollbar:
    sb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview,
                       style=f"{style_name}.Vertical.TScrollbar")
    tree.configure(yscrollcommand=sb.set)
    return sb



def primary_btn (master, text: str, theme: str = "dark", **kwargs) -> ctk.CTkButton:

    kwargs.setdefault ("fg_color", C("accent"))
    kwargs.setdefault ("hover_color", C("accent_hover"))
    kwargs.setdefault("text_color",  ("#0d0c08", "#ffffff"))
    kwargs.setdefault ("font", ctk.CTkFont("Georgia", 13, "bold"))
    kwargs.setdefault("corner_radius", 7)
    kwargs.setdefault("height", 40)
    return ctk.CTkButton(master, text=text, **kwargs)


def glass_btn (master, text: str, theme: str = "dark", **kwargs) -> ctk.CTkButton:

    kwargs.setdefault("fg_color", C("bg_card"))
    kwargs.setdefault ("hover_color", C("accent_faint"))
    kwargs.setdefault ("text_color", C("text_primary"))
    kwargs.setdefault ("border_color", C("border"))
    kwargs.setdefault ("border_width", 1)
    kwargs.setdefault ("font", ctk.CTkFont("Georgia", 12))
    kwargs.setdefault ("corner_radius", 7)
    kwargs.setdefault ("height", 38)
    return ctk.CTkButton(master, text=text, **kwargs)

def styled_entry (master, theme: str = "dark", **kwargs) -> ctk.CTkEntry:
    kwargs.setdefault("fg_color", C("bg_input"))
    kwargs.setdefault("border_color", C("border"))
    kwargs.setdefault("border_width", 1)
    kwargs.setdefault("text_color", C("text_primary"))
    kwargs.setdefault("placeholder_text_color", C("text_muted"))
    kwargs.setdefault("font", ctk.CTkFont("Georgia", 13))
    kwargs.setdefault("corner_radius", 7)
    kwargs.setdefault("height", 42)
    return ctk.CTkEntry(master, **kwargs)

def styled_combo(master, values: list, theme: str = "dark", **kwargs) -> ctk.CTkComboBox:
    kwargs.setdefault("fg_color", C("bg_input"))
    kwargs.setdefault("border_color", C("border"))
    kwargs.setdefault("border_width", 1)
    kwargs.setdefault("button_color", C("accent"))
    kwargs.setdefault("button_hover_color", C("accent_hover"))
    kwargs.setdefault("text_color", C("text_primary"))
    kwargs.setdefault("dropdown_fg_color", C("bg_card"))
    kwargs.setdefault("dropdown_text_color", C("text_primary"))
    kwargs.setdefault("dropdown_hover_color", C("accent_faint"))
    kwargs.setdefault("font", ctk.CTkFont("Georgia", 13))
    kwargs.setdefault("corner_radius", 7)
    kwargs.setdefault("height", 42)
    return ctk.CTkComboBox(master, values=values, **kwargs)