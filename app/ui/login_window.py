import code
import math
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from sqlalchemy.sql.functions import user

BG_COLOR = "#0d0c08"
GOLD = "#d4af37"
GOLD_DIM = "#8a7840"
GOLD_FAINT = "#3a3018"
GOLD_VERY_FAINT = "#1a1608"

class VaultInput(ctk.CTkFrame):
    def __init_(self, master, placeholder, icon_text, is_password=False, max_len=None, width=388):
        super().__init__(master, width=width, height=52, fg_color="#111009", border_color="#2a2515", border_width=1, corner_radius=4)

        self.max_len = max_len
        self.is_password = is_password

        self.icon_lbl = ctk.CTkLabel(self, text=icon_text, text_color=GOLD_DIM, font=("Arial",16))
        self.icon_lbl.place(x=16, rely=0.5, anchor="w")

        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, fg_color="transparent", border_width=0,
                                  text_color="#ffffff", placeholder_text_color="#6a5e38", font=("Arial", 14))

        self.entry.place(x=48, rely=0.5, anchor="n", relwidth=0.5)

        self.entry.bind("<FocusIn>", self._on_focus)


    def _limit_length(self, *args):
        val = self.entry.get()
        if len(val) > self.max_len:
            self.entry.delete(self.max_len, tk.END)

    def _on_focus(self, event):
        self.configure(border_color=GOLD)
        self.icon_lbl.configure(text_color=GOLD)

        if self.is_password:
            self.entry.configure(show="*")

    def _on_focus_out(self, event):
        self.configure(border_color="#2a515")
        self.icon_lbl.configure(text_color=GOLD_DIM)

        if self.is_password and len(self.entry.get()) == 0:
            self.entry.configure(show="")

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, tk.END)
        if self.is_password:
            self.entry.configure(show="")

    def focus_set(self):
        self.entry.focus_set()


class LoginWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.on_login_successful = None

        self.title ("Archive - Secure Access")
        self.geometry("480x650")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)

        self.bg_photo = None

        self._build_canvas_background()
        self._build_ui()

    def _generate_gradient_image(self, width, height):
        img = Image.new("RGBA", (width, height))
        pixels = img.load()

        c_top = (17, 16, 9)
        c_mid = (13, 12, 8)
        c_bottom = (8, 7, 0)

        glow_color = (212, 175, 55)
        glow_center = (width // 2, int(height * 0.38))
        glow_radius = height * 0.55

        linear_colors = []
        for y in range(height):
            if y < height / 2:
                ratio = y / (height/2)
                r = c_top[0] * (1 - ratio) + c_mid[0] * ratio
                g = c_top[1] * (1 - ratio) + c_mid[1] * ratio
                b = c_top[2] * (1 - ratio) + c_mid[2] * ratio
            else:
                ratio = (y - height / 2) / (height / 2)
                r = c_mid[0] * (1 - ratio) + c_bottom[0] * ratio
                g = c_mid[1] * (1 - ratio) + c_bottom[1] * ratio
                b = c_mid[2] * (1 - ratio) + c_bottom[2] * ratio

            linear_colors.append((r, g, b))

        for y in range(height):
            base_r, base_g, base_b = linear_colors[y]
            dy = y - glow_center[1]
            dy2 = dy * dy
            for x in range(width):
                dx = x - glow_center[0]
                dist = math.sqrt(dx * dx + dy2)

                if dist < glow_radius:
                    glow_ratio = 1.0 - (dist / glow_radius)
                    alpha = glow_ratio * 0.12
                    r_out = int(base_r * (1 - alpha) + glow_color[0] * alpha)
                    g_out = int(base_g * (1 - alpha) + glow_color[1] * alpha)
                    b_out = int(base_b * (1 - alpha) + glow_color[2] * alpha)
                    pixels[x, y] = (r_out, g_out, b_out, 255)

                else:
                    pixels[x, y] = (int(base_r), int(base_g), int(base_b), 255)

            return ImageTk.PhotoImage(img)


    def _build_canvas_background(self):
        self.canvas = tk.Canvas(self, width=480, height=650, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        Width, Height = 480, 650

        self.bg_photo = self._generate_gradient_image(Width, Height)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        m = 18

        self.canvas.create_rectangle(m, m, Width-m, Height-m, outline=GOLD_FAINT, width=1)
        self.canvas.create_rectangle(m+5, m+5, Width-(m+5), Height-(m+5), outline=GOLD_VERY_FAINT, width=1)

        cs = 22
        corners = [(m, m, 1, 1), (Width-m, m, -1, 1), (m, Height-m, 1, -1), (Width-m, Height-m, -1, -1)]
        for cx, cy, sx, sy in corners:
            self.canvas.create_line(cx, cy, cx+sx*cs, cy, fill=GOLD_FAINT, width=2)
            self.canvas.create_line(cx, cy, cx, cy+sy*cs, fill=GOLD_FAINT, width=2)
            self.canvas.create_line(cx+sx*5, cy+sy*5, cx+sx*(cs-4), cy+sy*5, fill=GOLD_FAINT, width=2)
            self.canvas.create_line(cx+sx*5, cy+sy*5, cx+sx*5, cy+sy*(cs-4), fill=GOLD_FAINT, width=2)

        arch_cx = Width / 2
        arch_cy = int(Height * 0.10) + 52
        arch_r = 52

        self.canvas.create_oval(arch_cx-arch_r, arch_cy-arch_r, arch_cx+arch_r, arch_cy+arch_r, outline=GOLD_FAINT)
        self.canvas.create_oval(arch_cx-(arch_r+8), arch_cy-(arch_r+8), arch_cx+(arch_r+8), arch_cy+(arch_r+8), outline=GOLD_VERY_FAINT)

        for i in range(12):
            a = math.radians(i * 30)
            dx = math.cos(a) * (arch_r - 7)
            dy = math.sin(a) * (arch_r - 7)
            self.canvas.create_oval(arch_cx+dx-1, arch_cy+dy-1, arch_cx+dx+1, arch_cy+dy+1, fill=GOLD_FAINT, outline=GOLD_FAINT)

        ry = int(Height * 0.37)
        rm = 44
        rg = 88
        self.canvas.create_line(rm, ry, Width//2-rg, ry, fill=GOLD_FAINT)
        self.canvas.create_line(Width//2+rg, ry, Width-rm, ry, fill=GOLD_FAINT)
        self.canvas.create_line(rm, ry+3, Width//2-rg, ry+3, fill=GOLD_VERY_FAINT)
        self.canvas.create_line(Width//2+rg, ry+3, Width-m,ry+3, fill=GOLD_VERY_FAINT)
        self.canvas.create_polygon(Width/2, ry-4, Width/2+5, ry, Width/2, ry+4, Width/2-5, ry, fill=GOLD_FAINT)

        self.canvas.create_line(rm, int(Height*0.92), Width-rm, int(Height*0.92), fill=GOLD_VERY_FAINT)
        for x in [int(Width*0.12), int(Width*0.88)]:
            self.canvas.create_line(x, int(Height * 0.33), x, int(Height * 0.90), fill=GOLD_VERY_FAINT)


        self.canvas.create_text(240,117, text="🏛", fill=GOLD, font=("Arial", 38))
        self.canvas.create_text(240, 185, text="A R C H I V E", fill=GOLD, font=("Georgia", 22, "bold"))
        self.canvas.create_text(240, 210, text= "W E L I G E P O L A   D I V I S I O N A L   C O U N C I L", fill=GOLD_DIM, font=("Arial", 10))
        self.canvas.create_text(240, 285, text="🛡   AUTHORIZED ACCESS ONLY", fill=GOLD_DIM, font=("Arial", 10))
        self.canvas.create_text(240, 628, text="ARCHIVUM  ·  AUCTORITAS ET CUSTODIA", fill=GOLD_VERY_FAINT, font=("Arial", 9))

        self.status_text = self.canvas.create_text(240, 605, text="", fill="#ff5252", font=("Arial", 12))


    def _build_ui(self):
        return