import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.font as tkfont
import threading
import subprocess
import webbrowser
import os
import sys
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='urllib3')
import glob
import logging
import requests

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageTk
    _PIL = True
except Exception:
    _PIL = False

# ======================================================================
#  SubsForge  ·  GUI v4
#  Design language shared with ivanjonasfc.dev / DozeForge: near-black
#  OLED surface, orange "forge" accent, a faint reactive grid and a
#  radial glow that trails the cursor. Space Grotesk (display) / Inter
#  (UI) / JetBrains Mono (data). Fonts + icons under src/assets.
# ======================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
FONT_DIR = os.path.join(ASSETS, "fonts")
ICON_DIR = os.path.join(ASSETS, "icons")

PORTFOLIO_URL = "https://ivanjonasfc.dev"
GITHUB_URL = "https://github.com/IvanjonasFC"

log_path = os.path.join(os.path.dirname(BASE_DIR), "autosubs.log")
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logging.info("=========================================")
logging.info("SubsForge V4 - Interfaz Iniciada")
logging.info("=========================================")

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

# ======================================================================
#  DESIGN TOKENS  (mirrors portfolio tailwind.config.ts + global.css)
# ======================================================================
C = {
    "bg0": "#050505",          # page / root  (--background)
    "bg1": "#0B0B0E",          # sidebar
    "bg2": "#121216",          # solid card fallback
    "bg3": "#1A1A1F",          # hover / raised
    "bg4": "#232329",          # pressed
    "input": "#0A0A0D",        # input fill
    "term": "#0A0A0C",         # terminal body
    "term_head": "#141418",    # terminal title bar (bg-white/5)
    "grid": "#0E0E11",         # faint grid line  (#ffffff09 over bg0)
    "border": "#212127",
    "border_strong": "#33333B",
    "fg0": "#FFFFFF",
    "fg1": "#D4D4D8",
    "fg2": "#A0A0A0",          # text.secondary
    "fg3": "#71717A",
    "accent": "#FF6B00",       # primary.DEFAULT
    "accent_hover": "#FF3C00",  # primary.hover
    "accent_soft": "#231206",
    "good": "#3FB27F",
    "warn": "#F59E0B",
    "bad": "#EF4444",
    "bad_hover": "#B91C1C",
    "dot_red": "#C24E4E",
    "dot_yellow": "#C2A03C",
    "dot_green": "#3FB27F",
}

ctk.set_appearance_mode("Dark")
ctk.set_widget_scaling(1.0)


def register_fonts():
    if os.name != "nt" or not os.path.isdir(FONT_DIR):
        return
    try:
        import ctypes
        FR_PRIVATE = 0x10
        gdi = ctypes.windll.gdi32
        for ttf in glob.glob(os.path.join(FONT_DIR, "*.ttf")):
            gdi.AddFontResourceExW(ctypes.c_wchar_p(ttf), FR_PRIVATE, 0)
        logging.info("Fuentes registradas correctamente.")
    except Exception as e:
        logging.warning(f"No se pudieron registrar las fuentes: {e}")


def pick(candidates):
    try:
        fams = set(tkfont.families())
    except Exception:
        return candidates[-1]
    for c in candidates:
        if c in fams:
            return c
    return candidates[-1]


# ======================================================================
#  i18n
# ======================================================================
T = {
    "es": {
        "tagline": "Kit de subtítulos",
        "section_tools": "HERRAMIENTAS",
        "btn_translate": "Traductor IA", "btn_sync": "Sincronización VAD",
        "btn_whisper": "Transcripción Whisper", "btn_mux": "Fusión Lossless",
        "btn_cleaner": "Limpiador Anime", "lang_toggle": "Español",
        "title_trans": "Traductor IA", "desc_trans": "Traduce subtítulos al español. Compatible con Ollama local.",
        "browse_file": "Archivo", "browse_dir": "Carpeta", "btn_run_trans": "Traducir", "engine": "Motor IA",
        "title_sync": "Sincronización automática", "desc_sync": "Alinea subtítulos desfasados con detección de voz (VAD).",
        "vid_orig": "Vídeo original", "sub_desf": "Subtítulo desfasado", "btn_run_sync": "Sincronizar",
        "title_whisp": "Generación con Whisper", "desc_whisp": "Extrae el audio y transcribe. Soporta archivos o carpetas enteras.",
        "input_source": "Origen", "btn_run_whisp": "Procesar",
        "title_mux": "Fusión Lossless (MKV)", "desc_mux": "Integra el subtítulo en el vídeo sin perder calidad.",
        "vid_mkv": "Vídeo (.mkv)", "sub_final": "Subtítulo (.srt)", "btn_run_mux": "Integrar",
        "title_clean": "Limpiador Anime (ASS → SRT)", "desc_clean": "Convierte subtítulos .ass complejos en texto plano compatible con TV.",
        "file_ass": "Archivo (.ass)", "btn_run_clean": "Limpiar subtítulo", "btn_ollama_help": "Instalar IA local",
        "ready": "listo. Selecciona un archivo para empezar.",
    },
    "en": {
        "tagline": "Subtitle toolkit",
        "section_tools": "TOOLS",
        "btn_translate": "AI Translator", "btn_sync": "VAD Sync",
        "btn_whisper": "Whisper Transcription", "btn_mux": "Lossless Muxer",
        "btn_cleaner": "Anime Cleaner", "lang_toggle": "English",
        "title_trans": "AI Translator", "desc_trans": "Translate subtitles to Spanish. Supports local Ollama.",
        "browse_file": "File", "browse_dir": "Folder", "btn_run_trans": "Translate", "engine": "AI Engine",
        "title_sync": "Auto synchronization", "desc_sync": "Align desynced subtitles using Voice Activity Detection (VAD).",
        "vid_orig": "Original video", "sub_desf": "Desynced subtitle", "btn_run_sync": "Synchronize",
        "title_whisp": "Whisper generation", "desc_whisp": "Extract audio and transcribe. Supports single files or whole folders.",
        "input_source": "Source", "btn_run_whisp": "Process",
        "title_mux": "Lossless Muxer (MKV)", "desc_mux": "Embed subtitles into the video without quality loss.",
        "vid_mkv": "Video (.mkv)", "sub_final": "Subtitle (.srt)", "btn_run_mux": "Mux",
        "title_clean": "Anime Cleaner (ASS → SRT)", "desc_clean": "Convert complex .ass subtitles into TV-compatible plain text.",
        "file_ass": "File (.ass)", "btn_run_clean": "Clean subtitle", "btn_ollama_help": "Install local AI",
        "ready": "ready. Pick a file to start.",
    },
}

NAV = [
    ("translate", "btn_translate", "translate"),
    ("sync", "btn_sync", "waveform"),
    ("whisper", "btn_whisper", "microphone"),
    ("mux", "btn_mux", "stack"),
    ("cleaner", "btn_cleaner", "broom"),
]

SIDEBAR_W = 248
SIDEBAR_W_MIN = 68
TOPBAR_H = 46
GRIP = 5
PAD_TOP = 30
PAD_LEFT = 34
PAD_RIGHT = 40
PAD_BOTTOM = 26
GRID_STEP = 32
CARD_PAD = 22
ROW_H = 40
ROW_GAP = 14


class AutoSubsGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        register_fonts()

        self.lang = "es"
        self.active_tab = "translate"
        self._icon_cache = {}
        self._img_cache = {}
        self._nav = {}
        self._resize_job = None
        self._last_size = (0, 0)
        self._glow_pos = [-2000.0, -2000.0]
        self._glow_target = [-2000.0, -2000.0]

        self.f_title = pick(["Space Grotesk SemiBold", "Space Grotesk", "Segoe UI Semibold", "Segoe UI"])
        self.f_bold = pick(["Space Grotesk Bold", "Space Grotesk", "Segoe UI Semibold", "Segoe UI"])
        self.f_ui = pick(["Inter Display", "Inter", "Segoe UI"])
        self.f_ui_med = pick(["Inter Medium", "Inter", "Segoe UI Semibold", "Segoe UI"])
        self.f_ui_semi = pick(["Inter SemiBold", "Inter", "Segoe UI Semibold", "Segoe UI"])
        self.f_mono = pick(["JetBrains Mono NL", "JetBrains Mono", "Consolas"])

        self.title("SubsForge")
        self._win_w, self._win_h = 1060, 710
        self._minsize = (920, 610)
        self.configure(fg_color=C["bg0"])
        self._maximized = False
        self._normal_geo = None
        self._drag_off = (0, 0)
        self._rz = None
        self._ollama_models = []
        self._dropdown = None
        self.collapsed = False
        self.sidebar_w = SIDEBAR_W

        # Frameless window (custom title bar, like DozeForge).
        self.overrideredirect(True)
        self._set_app_icon()
        self._center_window(self._win_w, self._win_h)

        # Body region below the custom title bar (plain tk.Frame supports the
        # height offset that CTk's place() rejects).
        self.body = tk.Frame(self, bg=C["bg0"], highlightthickness=0, bd=0)
        self.body.place(x=0, y=TOPBAR_H, relwidth=1, relheight=1, height=-TOPBAR_H)
        self.canvas = tk.Canvas(self.body, bg=C["bg0"], highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Glow is built just after the first paint so the window appears instantly.
        self.glow_img = None
        self.glow_item = None
        self.after(20, self._init_glow)

        self.bar_img = self._make_header_bar()
        self.build_topbar()
        self._add_grips()

        self.canvas.bind("<Configure>", self._on_configure)
        self.bind_all("<Motion>", self._on_motion)
        self.bind("<Button-1>", self._maybe_close_dropdown, add="+")

        self._ease_glow()          # start the inertial follow loop
        self.after(10, self._win_taskbar_fix)
        self.after(60, self.refresh_ui)
        threading.Thread(target=self._load_ollama, daemon=True).start()

    def _load_ollama(self):
        # Detect local Ollama models off the UI thread so startup never blocks.
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=0.8)
            self._ollama_models = [m["name"] for m in r.json().get("models", [])]
        except Exception:
            self._ollama_models = []
        try:
            self.after(0, self._maybe_refresh_engine)
        except Exception:
            pass

    def _maybe_refresh_engine(self):
        if getattr(self, "active_tab", None) == "translate" and self._ollama_models:
            self.refresh_ui()

    # ------------------------------------------------------------------
    #  Frameless window chrome (custom title bar, drag, resize, controls)
    # ------------------------------------------------------------------
    def _set_app_icon(self):
        ico = os.path.join(ICON_DIR, "app.ico")
        png = os.path.join(ICON_DIR, "app.png")
        try:
            if os.name == "nt" and os.path.exists(ico):
                self.iconbitmap(default=ico)
        except Exception:
            pass
        try:
            if _PIL and os.path.exists(png):
                self._appicon = ImageTk.PhotoImage(Image.open(png))
                self.iconphoto(True, self._appicon)
        except Exception:
            pass

    def _center_window(self, w, h):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (sw - w) // 2, max(0, (sh - h) // 2 - 20)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def build_topbar(self):
        if hasattr(self, "topbar"):
            self.topbar.destroy()
        tb = ctk.CTkFrame(self, height=TOPBAR_H, corner_radius=0, fg_color=C["bg1"])
        tb.place(x=0, y=0, relwidth=1)
        tb.pack_propagate(False)
        self.topbar = tb
        ctk.CTkFrame(tb, height=1, fg_color=C["border"]).place(x=0, rely=1.0, y=-1, relwidth=1)

        # Sidebar collapse toggle (far left)
        ctk.CTkButton(tb, text="", image=self.icon("sidebar", "gray", 18), width=44, height=TOPBAR_H,
                      corner_radius=0, fg_color="transparent", hover_color=C["bg3"],
                      command=self._toggle_sidebar).pack(side="left")

        # Left: window identity (app icon + wordmark) — drag region
        left = ctk.CTkFrame(tb, fg_color="transparent")
        left.pack(side="left", padx=(6, 0))
        drag_widgets = [tb, left]
        ic = self.icon("cc", "accent", 18)
        if ic:
            lbl_ic = ctk.CTkLabel(left, text="", image=ic)
            lbl_ic.pack(side="left", padx=(0, 9))
            drag_widgets.append(lbl_ic)
        l1 = ctk.CTkLabel(left, text="SubsForge", font=self.font(self.f_ui_semi, 13), text_color=C["fg1"])
        l1.pack(side="left")
        l2 = ctk.CTkLabel(left, text="Pro", font=self.font(self.f_ui_semi, 13), text_color=C["accent"])
        l2.pack(side="left", padx=(4, 0))
        sep = ctk.CTkLabel(left, text="·", font=self.font(self.f_ui, 13), text_color=C["fg3"])
        sep.pack(side="left", padx=(10, 0))
        tag = ctk.CTkLabel(left, text=self.t("tagline"), font=self.font(self.f_mono, 11), text_color=C["fg3"])
        tag.pack(side="left", padx=(10, 0))
        drag_widgets += [l1, l2, sep, tag]
        for wdg in drag_widgets:
            wdg.bind("<Button-1>", self._start_move)
            wdg.bind("<B1-Motion>", self._do_move)
            wdg.bind("<Double-Button-1>", lambda e: self.win_toggle_max())

        # Right: window controls (min / max / close)
        controls = ctk.CTkFrame(tb, fg_color="transparent")
        controls.pack(side="right")
        for name, cmd, hover in [("min", self.win_minimize, C["bg3"]),
                                 ("max", self.win_toggle_max, C["bg3"]),
                                 ("close", self.win_close, "#B23A3A")]:
            ctk.CTkButton(controls, text="", image=self.icon(f"win_{name}", "gray", 15),
                          width=46, height=TOPBAR_H, corner_radius=0, fg_color="transparent",
                          hover_color=hover, command=cmd).pack(side="left")

        # Right: quick links (GitHub + Portfolio), left of the window controls
        links = ctk.CTkFrame(tb, fg_color="transparent")
        links.pack(side="right", padx=(0, 8))
        ctk.CTkButton(links, text=" Portfolio", image=self.icon("extlink", "gray", 15), compound="left",
                      font=self.font(self.f_ui_med, 12), fg_color="transparent", hover_color=C["bg3"],
                      text_color=C["fg2"], corner_radius=8, height=30, width=94,
                      command=lambda: self.open_url(PORTFOLIO_URL)).pack(side="left", padx=2)
        ctk.CTkButton(links, text=" GitHub", image=self.icon("github", "gray", 15), compound="left",
                      font=self.font(self.f_ui_med, 12), fg_color="transparent", hover_color=C["bg3"],
                      text_color=C["fg2"], corner_radius=8, height=30, width=82,
                      command=lambda: self.open_url(GITHUB_URL)).pack(side="left", padx=2)
        ctk.CTkFrame(links, width=1, height=20, fg_color=C["border"]).pack(side="left", padx=(8, 4))

        tb.lift()

    # ---- window drag ----
    def _start_move(self, e):
        self._drag_off = (e.x_root - self.winfo_x(), e.y_root - self.winfo_y())

    def _do_move(self, e):
        if self._maximized:
            return
        self.geometry(f"+{e.x_root - self._drag_off[0]}+{e.y_root - self._drag_off[1]}")

    # ---- window controls ----
    def _hwnd(self):
        import ctypes
        return ctypes.windll.user32.GetParent(self.winfo_id())

    def win_minimize(self):
        if os.name == "nt":
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(self._hwnd(), 6)  # SW_MINIMIZE
                return
            except Exception:
                pass
        try:
            self.overrideredirect(False)
            self.iconify()
        except Exception:
            pass

    def _work_area(self):
        if os.name == "nt":
            try:
                import ctypes
                from ctypes import wintypes
                r = wintypes.RECT()
                ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(r), 0)
                return r.left, r.top, r.right - r.left, r.bottom - r.top
            except Exception:
                pass
        return 0, 0, self.winfo_screenwidth(), self.winfo_screenheight()

    def win_toggle_max(self):
        if self._maximized:
            if self._normal_geo:
                self.geometry(self._normal_geo)
            self._maximized = False
        else:
            self._normal_geo = self.geometry()
            x, y, w, h = self._work_area()
            self.geometry(f"{w}x{h}+{x}+{y}")
            self._maximized = True

    def win_close(self):
        try:
            self.destroy()
        except Exception:
            os._exit(0)

    def _win_taskbar_fix(self):
        # overrideredirect drops the taskbar button on Windows; re-add it.
        if os.name != "nt":
            return
        try:
            import ctypes
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            hwnd = self._hwnd()
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            self.withdraw()
            self.after(12, self.deiconify)
        except Exception:
            pass

    # ---- edge / corner resize grips ----
    def _cursor_for(self, side):
        if side in ("e", "w"):
            return "sb_h_double_arrow"
        if side in ("n", "s"):
            return "sb_v_double_arrow"
        return "sizing"

    def _add_grips(self):
        self._grips = []
        for side in ["n", "s", "e", "w", "ne", "nw", "se", "sw"]:
            g = tk.Frame(self, bg=C["bg0"], cursor=self._cursor_for(side))
            self._place_grip(g, side)
            g.bind("<Button-1>", lambda e, s=side: self._rz_start(e, s))
            g.bind("<B1-Motion>", lambda e, s=side: self._rz_move(e, s))
            self._grips.append(g)

    def _place_grip(self, g, side):
        G = GRIP
        if side == "n":
            g.place(x=G, y=0, relwidth=1, width=-2 * G, height=G)
        elif side == "s":
            g.place(x=G, rely=1, y=-G, relwidth=1, width=-2 * G, height=G)
        elif side == "w":
            g.place(x=0, y=G, width=G, relheight=1, height=-2 * G)
        elif side == "e":
            g.place(relx=1, x=-G, y=G, width=G, relheight=1, height=-2 * G)
        elif side == "nw":
            g.place(x=0, y=0, width=G, height=G)
        elif side == "ne":
            g.place(relx=1, x=-G, y=0, width=G, height=G)
        elif side == "sw":
            g.place(x=0, rely=1, y=-G, width=G, height=G)
        elif side == "se":
            g.place(relx=1, x=-G, rely=1, y=-G, width=G, height=G)

    def _rz_start(self, e, side):
        self._rz = {"x": e.x_root, "y": e.y_root, "gx": self.winfo_x(), "gy": self.winfo_y(),
                    "w": self.winfo_width(), "h": self.winfo_height(), "side": side}

    def _rz_move(self, e, side):
        if self._maximized or not self._rz:
            return
        r = self._rz
        dx, dy = e.x_root - r["x"], e.y_root - r["y"]
        x, y, w, h = r["gx"], r["gy"], r["w"], r["h"]
        minw, minh = self._minsize
        if "e" in side:
            w = max(minw, r["w"] + dx)
        if "s" in side:
            h = max(minh, r["h"] + dy)
        if "w" in side:
            nw = max(minw, r["w"] - dx)
            x = r["gx"] + (r["w"] - nw)
            w = nw
        if "n" in side:
            nh = max(minh, r["h"] - dy)
            y = r["gy"] + (r["h"] - nh)
            h = nh
        self.geometry(f"{int(w)}x{int(h)}+{int(x)}+{int(y)}")

    # ------------------------------------------------------------------
    #  Reactive background (grid + trailing glow)
    # ------------------------------------------------------------------
    def _init_glow(self):
        self._build_glow()
        if self.glow_img is not None and self.glow_item is None:
            self.glow_item = self.canvas.create_image(-2000, -2000, image=self.glow_img, tags="glow")
            self.canvas.tag_raise(self.glow_item)

    def _build_glow(self):
        self.glow_img = None
        if not _PIL:
            return
        size = 660
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx = cy = size / 2
        steps = 72
        peak = 42
        for i in range(steps):
            t = i / steps
            r = int((1 - t) * (size / 2))
            a = int(peak * (t ** 1.7))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 107, 0, a))
        img = img.filter(ImageFilter.GaussianBlur(30))
        self.glow_img = ImageTk.PhotoImage(img)

    def redraw_grid(self):
        self.canvas.delete("grid")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        for x in range(0, w, GRID_STEP):
            self.canvas.create_line(x, 0, x, h, fill=C["grid"], tags="grid")
        for y in range(0, h, GRID_STEP):
            self.canvas.create_line(0, y, w, y, fill=C["grid"], tags="grid")
        self.canvas.tag_lower("grid")
        if self.glow_item is not None:
            self.canvas.tag_raise(self.glow_item)

    def _on_motion(self, e):
        try:
            self._glow_target[0] = e.x_root - self.canvas.winfo_rootx()
            self._glow_target[1] = e.y_root - self.canvas.winfo_rooty()
        except Exception:
            pass

    def _ease_glow(self):
        # Inertial trail: ease the glow toward the cursor a fraction each frame,
        # like the portfolio blob's 3s follow. Cheap: just moves one image.
        if self.glow_item is not None:
            p, t = self._glow_pos, self._glow_target
            p[0] += (t[0] - p[0]) * 0.12
            p[1] += (t[1] - p[1]) * 0.12
            self.canvas.coords(self.glow_item, p[0], p[1])
        self.after(16, self._ease_glow)

    def _on_configure(self, e):
        size = (self.canvas.winfo_width(), self.canvas.winfo_height())
        if size == self._last_size:
            return
        self._last_size = size
        self.redraw_grid()
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(90, self.refresh_ui)

    # ------------------------------------------------------------------
    #  Image factories (rounded panels, header bar)
    # ------------------------------------------------------------------
    def _round_img(self, w, h, radius, fill, border=None):
        key = ("rr", w, h, radius, fill, border)
        if key in self._img_cache:
            return self._img_cache[key]
        if not _PIL:
            return None
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=fill,
                            outline=border, width=1 if border else 0)
        ph = ImageTk.PhotoImage(img)
        self._img_cache[key] = ph
        return ph

    def _make_header_bar(self):
        if not _PIL:
            return None
        w, h = 26, 48
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle([9, 8, 15, h - 8], radius=3, fill=(255, 90, 0, 200))
        glow = glow.filter(ImageFilter.GaussianBlur(4))
        bar = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        db = ImageDraw.Draw(bar)
        for yy in range(8, h - 8):
            t = (yy - 8) / (h - 16)
            g = int(107 - (107 - 60) * t)   # #ff6b00 -> #ff3c00
            db.line([(9, yy), (14, yy)], fill=(255, g, 0, 255))
        img = Image.alpha_composite(glow, bar)
        return ImageTk.PhotoImage(img)

    # ------------------------------------------------------------------
    #  Small helpers
    # ------------------------------------------------------------------
    def t(self, key):
        return T[self.lang].get(key, key)

    def font(self, family, size, weight="normal"):
        return ctk.CTkFont(family=family, size=int(round(size)), weight=weight)

    def icon(self, name, variant="gray", size=20):
        key = f"{name}_{variant}_{size}"
        if key in self._icon_cache:
            return self._icon_cache[key]
        if not _PIL:
            return None
        path = os.path.join(ICON_DIR, f"{name}_{variant}.png")
        if not os.path.exists(path):
            return None
        img = ctk.CTkImage(Image.open(path), size=(size, size))
        self._icon_cache[key] = img
        return img

    def open_url(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            logging.warning(f"No se pudo abrir {url}: {e}")

    def toggle_language(self):
        self.lang = "en" if self.lang == "es" else "es"
        self.build_topbar()
        self.refresh_ui()

    def _toggle_sidebar(self):
        self.collapsed = not self.collapsed
        self.sidebar_w = SIDEBAR_W_MIN if self.collapsed else SIDEBAR_W
        self._close_dropdown()
        self.refresh_ui()

    # ------------------------------------------------------------------
    #  Translucent sidebar (drawn on the canvas; grid + glow show through)
    # ------------------------------------------------------------------
    def _draw_sidebar(self):
        self.canvas.delete("sidebar")
        w = self.sidebar_w
        H = self.canvas.winfo_height()
        if H < 60:
            return
        # Glass panel: translucent so the grid bleeds through, like DozeForge.
        panel = self._round_img(w, H, 0, (12, 12, 16, 128), None)
        self.canvas.create_image(0, 0, anchor="nw", image=panel, tags="sidebar")
        self.canvas.create_line(w, 0, w, H, fill=C["border"], tags="sidebar")

        exp = not self.collapsed
        if exp:
            self.canvas.create_text(26, 24, anchor="w", text=self.t("section_tools"),
                                    font=(self.f_ui_semi, 11), fill=C["fg3"], tags="sidebar")
        y = 46
        for tab, key, ic in NAV:
            self._nav_item(tab, key, ic, y, w, 44, tab == self.active_tab, exp)
            y += 50
        self._sidebar_footer(w, H, exp)

    def _nav_item(self, tab, key, ic, y, w, ih, active, exp):
        tag = f"nav_{tab}"
        x0, bw = 12, w - 24
        hid = None
        if active:
            self.canvas.create_image(x0, y, anchor="nw",
                                     image=self._round_img(bw, ih, 9, (255, 107, 0, 26), (255, 107, 0, 55)),
                                     tags=("sidebar", tag))
            self.canvas.create_image(4, y + (ih - 22) // 2, anchor="nw",
                                     image=self._round_img(3, 22, 2, (255, 107, 0, 255), None),
                                     tags=("sidebar", tag))
        else:
            hid = self.canvas.create_image(x0, y, anchor="nw",
                                           image=self._round_img(bw, ih, 9, (255, 255, 255, 12), (0, 0, 0, 0)),
                                           tags=("sidebar", tag), state="hidden")
        icon_img = self._pimg(ic, "accent" if active else "gray", 20)
        tcol = C["accent"] if active else C["fg2"]
        if exp:
            self.canvas.create_image(30, y + ih / 2, anchor="w", image=icon_img, tags=("sidebar", tag))
            self.canvas.create_text(62, y + ih / 2, anchor="w", text=self.t(key),
                                    font=(self.f_ui_med, 14), fill=tcol, tags=("sidebar", tag))
        else:
            self.canvas.create_image(w / 2, y + ih / 2, image=icon_img, tags=("sidebar", tag))

        def enter(_e, h=hid):
            self.canvas.config(cursor="hand2")
            if h is not None:
                self.canvas.itemconfigure(h, state="normal")

        def leave(_e, h=hid):
            self.canvas.config(cursor="")
            if h is not None:
                self.canvas.itemconfigure(h, state="hidden")

        self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tab: self.set_tab(t))
        self.canvas.tag_bind(tag, "<Enter>", enter)
        self.canvas.tag_bind(tag, "<Leave>", leave)

    def _sidebar_footer(self, w, H, exp):
        fy = H - 62
        self.canvas.create_line(18, fy, w - 18, fy, fill=C["border"], tags="sidebar")
        by = H - 48
        globe = self._pimg("globe", "gray", 16)
        if exp:
            self.canvas.create_image(18, by, anchor="nw",
                                     image=self._round_img(w - 36, 34, 8, (255, 255, 255, 14), (255, 255, 255, 24)),
                                     tags=("sidebar", "langbtn"))
            self.canvas.create_image(32, by + 17, anchor="w", image=globe, tags=("sidebar", "langbtn"))
            self.canvas.create_text(52, by + 17, anchor="w", text=self.t("lang_toggle"),
                                    font=(self.f_ui_med, 12), fill=C["fg1"], tags=("sidebar", "langbtn"))
            self.canvas.create_text(w - 16, by + 17, anchor="e", text="v4.0",
                                    font=(self.f_mono, 11), fill=C["fg3"], tags="sidebar")
        else:
            self.canvas.create_image((w - 40) / 2, by, anchor="nw",
                                     image=self._round_img(40, 34, 8, (255, 255, 255, 14), (255, 255, 255, 24)),
                                     tags=("sidebar", "langbtn"))
            self.canvas.create_image(w / 2, by + 17, image=globe, tags=("sidebar", "langbtn"))
        self.canvas.tag_bind("langbtn", "<Button-1>", lambda e: self.toggle_language())
        self.canvas.tag_bind("langbtn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("langbtn", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def set_tab(self, tab_name):
        self.active_tab = tab_name
        self.refresh_ui()

    # ------------------------------------------------------------------
    #  Content (widgets float on the canvas so grid + glow show through)
    # ------------------------------------------------------------------
    @property
    def content_x(self):
        return self.sidebar_w + PAD_LEFT

    @property
    def content_w(self):
        return max(360, self.canvas.winfo_width() - self.content_x - PAD_RIGHT)

    def refresh_ui(self):
        self._resize_job = None
        self._close_dropdown()
        self.canvas.delete("content")
        self._draw_sidebar()
        self._y = PAD_TOP
        {
            "translate": self.show_translate_frame,
            "sync": self.show_sync_frame,
            "whisper": self.show_whisper_frame,
            "mux": self.show_mux_frame,
            "cleaner": self.show_cleaner_frame,
        }[self.active_tab]()

    def begin_page(self, title_key, sub_key):
        x, y = self.content_x, PAD_TOP
        if self.bar_img is not None:
            self.canvas.create_image(x - 8, y - 4, anchor="nw", image=self.bar_img, tags="content")
        else:
            self.canvas.create_rectangle(x, y + 5, x + 4, y + 33, fill=C["accent"], outline="", tags="content")
        self.canvas.create_text(x + 18, y, anchor="nw", text=self.t(title_key),
                                font=(self.f_title, 26), fill=C["fg0"], tags="content")
        self.canvas.create_text(x + 18, y + 46, anchor="nw", text=self.t(sub_key),
                                font=(self.f_ui, 13), fill=C["fg2"], tags="content")
        self._y = y + 84

    # ----- translucent card -----
    def card_open(self, n_rows):
        h = CARD_PAD * 2 + n_rows * ROW_H + (n_rows - 1) * ROW_GAP
        w = self.content_w
        img = self._round_img(w, h, 16, (18, 18, 22, 102), (255, 255, 255, 22))
        if img is not None:
            self.canvas.create_image(self.content_x, self._y, anchor="nw", image=img, tags="content")
        self._card_top = self._y
        self._card_h = h
        self._cy = self._y + CARD_PAD

    def card_close(self, gap=20):
        self._y = self._card_top + self._card_h + gap

    # ----- translucent canvas primitives (grid shows through, no widget corners) -----
    def _measure(self, family, size, text):
        try:
            return tkfont.Font(family=family, size=int(round(size))).measure(text)
        except Exception:
            return len(text) * 7

    def _pimg(self, name, variant, size):
        # Tk PhotoImage for canvas.create_image (CTkImage can't be drawn on a canvas).
        key = f"p_{name}_{variant}_{size}"
        if key in self._icon_cache:
            return self._icon_cache[key]
        if not _PIL:
            return None
        path = os.path.join(ICON_DIR, f"{name}_{variant}.png")
        if not os.path.exists(path):
            return None
        im = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
        ph = ImageTk.PhotoImage(im)
        self._icon_cache[key] = ph
        return ph

    def _box(self, x, y, w, h, fill, border, radius=9):
        img = self._round_img(int(w), int(h), radius, fill, border)
        return self.canvas.create_image(x, y, anchor="nw", image=img, tags="content")

    def _short(self, path, maxlen=70):
        if not path:
            return ""
        return path if len(path) <= maxlen else "…" + path[-(maxlen - 1):]

    def field_box(self, x, y, w, var, command=None):
        h = ROW_H
        bid = self._box(x, y, w, h, (14, 14, 20, 70), (255, 255, 255, 24))
        ph = "Ninguno seleccionado" if self.lang == "es" else "None selected"
        tid = self.canvas.create_text(x + 14, y + h / 2, anchor="w", text="",
                                      font=(self.f_mono, 11), fill=C["fg3"], tags="content")

        def upd(*_a):
            v = var.get()
            self.canvas.itemconfigure(tid, text=(self._short(v) if v else ph),
                                      fill=C["fg1"] if v else C["fg3"])
        var.trace_add("write", upd)
        upd()
        if command:
            for i in (bid, tid):
                self.canvas.tag_bind(i, "<Button-1>", lambda e: command())
            self.canvas.tag_bind(bid, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(bid, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def button_box(self, x, y, w, text, icon_name, command, surface=True,
                   icon_variant="gray", text_color=None):
        h = ROW_H
        if surface:
            n_fill, n_bd, h_fill = (255, 255, 255, 15), (255, 255, 255, 26), (255, 255, 255, 30)
        else:
            n_fill, n_bd, h_fill = (0, 0, 0, 0), (255, 255, 255, 40), (255, 255, 255, 16)
        n_img = self._round_img(int(w), h, 9, n_fill, n_bd)
        hv_img = self._round_img(int(w), h, 9, h_fill, n_bd)
        box = self.canvas.create_image(x, y, anchor="nw", image=n_img, tags="content")
        ic = self._pimg(icon_name, icon_variant, 16) if icon_name else None
        tw = self._measure(self.f_ui_med, 12, text)
        total = (22 if ic else 0) + tw
        sx = x + (w - total) / 2
        ids = [box]
        if ic:
            ids.append(self.canvas.create_image(sx, y + h / 2, anchor="w", image=ic, tags="content"))
            sx += 22
        ids.append(self.canvas.create_text(sx, y + h / 2, anchor="w", text=text,
                                           font=(self.f_ui_med, 12), fill=text_color or C["fg1"], tags="content"))
        for i in ids:
            self.canvas.tag_bind(i, "<Button-1>", lambda e: command())
            self.canvas.tag_bind(i, "<Enter>", lambda e: (self.canvas.itemconfigure(box, image=hv_img),
                                                          self.canvas.config(cursor="hand2")))
            self.canvas.tag_bind(i, "<Leave>", lambda e: (self.canvas.itemconfigure(box, image=n_img),
                                                          self.canvas.config(cursor="")))

    def primary_box(self, text, command, color=(255, 107, 0, 255), hover=(255, 122, 26, 255), w=190):
        x, y, h = self.content_x, self._y, 44
        n_img = self._round_img(w, h, 10, color, None)
        hv_img = self._round_img(w, h, 10, hover, None)
        box = self.canvas.create_image(x, y, anchor="nw", image=n_img, tags="content")
        tid = self.canvas.create_text(x + w / 2, y + h / 2, text=text,
                                      font=(self.f_ui_semi, 14), fill="#FFFFFF", tags="content")
        for i in (box, tid):
            self.canvas.tag_bind(i, "<Button-1>", lambda e: command())
            self.canvas.tag_bind(i, "<Enter>", lambda e: (self.canvas.itemconfigure(box, image=hv_img),
                                                          self.canvas.config(cursor="hand2")))
            self.canvas.tag_bind(i, "<Leave>", lambda e: (self.canvas.itemconfigure(box, image=n_img),
                                                          self.canvas.config(cursor="")))
        self._y += h + 20

    # ----- rows -----
    def row(self, label_key, var, buttons):
        x = self.content_x + CARD_PAD
        w = self.content_w - CARD_PAD * 2
        y = self._cy
        lblw = 158 if label_key else 0
        if label_key:
            self.canvas.create_text(x, y + ROW_H / 2, anchor="w", text=self.t(label_key),
                                    font=(self.f_ui_semi, 12), fill=C["fg1"], tags="content")
        ctrl_w = sum(b["w"] + 8 for b in buttons)
        fw = max(140, w - lblw - ctrl_w)
        self.field_box(x + lblw, y, fw - 8, var, buttons[0]["cmd"] if buttons else None)
        bx = x + lblw + fw
        for b in buttons:
            self.button_box(bx, y, b["w"], self.t(b["text"]), b["icon"], b["cmd"])
            bx += b["w"] + 8
        self._cy += ROW_H + ROW_GAP

    def row_engine(self, var, values, help_cmd=None):
        x = self.content_x + CARD_PAD
        y = self._cy
        lblw = 158
        self.canvas.create_text(x, y + ROW_H / 2, anchor="w", text=self.t("engine"),
                                font=(self.f_ui_semi, 12), fill=C["fg1"], tags="content")
        dw = 230
        self.dropdown_box(x + lblw, y, dw, var, values)
        if help_cmd:
            self.button_box(x + lblw + dw + 10, y, 160, self.t("btn_ollama_help"), "info", help_cmd,
                            surface=False, icon_variant="accent", text_color=C["warn"])
        self._cy += ROW_H + ROW_GAP

    # ----- translucent dropdown (canvas items; grid shows through) -----
    def dropdown_box(self, x, y, w, var, values):
        h = ROW_H
        bid = self._box(x, y, w, h, (14, 14, 20, 70), (255, 255, 255, 24))
        tid = self.canvas.create_text(x + 14, y + h / 2, anchor="w", text=var.get(),
                                      font=(self.f_ui_med, 12), fill=C["fg0"], tags="content")
        ids = [bid, tid]
        car = self._pimg("caret", "gray", 14)
        if car:
            ids.append(self.canvas.create_image(x + w - 14, y + h / 2, anchor="e", image=car, tags="content"))
        for i in ids:
            self.canvas.tag_bind(i, "<Button-1>", lambda e: self._open_dd(x, y + h + 6, w, var, values, tid))
            self.canvas.tag_bind(i, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(i, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def _open_dd(self, x, y, w, var, values, value_tid):
        self._close_dropdown()
        rows = len(values)
        ph = 10 + rows * 34
        self._round_img(int(w), ph, 10, (20, 20, 26, 240), (255, 255, 255, 34))  # cache
        self.canvas.create_image(x, y, anchor="nw",
                                 image=self._round_img(int(w), ph, 10, (20, 20, 26, 240), (255, 255, 255, 34)),
                                 tags="dropdown")
        oy = y + 6
        hi_img = self._round_img(int(w) - 10, 30, 6, (255, 255, 255, 20), (0, 0, 0, 0))
        for opt in values:
            sel = (opt == var.get())
            hid = self.canvas.create_image(x + 5, oy, anchor="nw", image=hi_img, tags="dropdown", state="hidden")
            tt = self.canvas.create_text(x + 16, oy + 15, anchor="w", text=opt, font=(self.f_ui_med, 12),
                                         fill=C["accent"] if sel else C["fg1"], tags="dropdown")
            rids = [hid, tt]
            if sel:
                ci = self._pimg("check", "accent", 14)
                if ci:
                    rids.append(self.canvas.create_image(x + w - 16, oy + 15, anchor="e", image=ci, tags="dropdown"))
            for i in rids:
                self.canvas.tag_bind(i, "<Button-1>", lambda e, o=opt: self._pick_dd(var, value_tid, o))
                self.canvas.tag_bind(i, "<Enter>", lambda e, hh=hid: (self.canvas.itemconfigure(hh, state="normal"),
                                                                      self.canvas.config(cursor="hand2")))
                self.canvas.tag_bind(i, "<Leave>", lambda e, hh=hid: (self.canvas.itemconfigure(hh, state="hidden"),
                                                                      self.canvas.config(cursor="")))
            oy += 34
        self._dropdown = True

    def _pick_dd(self, var, value_tid, opt):
        var.set(opt)
        self.canvas.itemconfigure(value_tid, text=opt)
        self._close_dropdown()

    def _close_dropdown(self):
        if self._dropdown is not None:
            self.canvas.delete("dropdown")
            self._dropdown = None

    def _maybe_close_dropdown(self, e):
        if self._dropdown is None:
            return
        cx = e.x_root - self.canvas.winfo_rootx()
        cy = e.y_root - self.canvas.winfo_rooty()
        over = set(self.canvas.find_overlapping(cx, cy, cx, cy))
        dd = set(self.canvas.find_withtag("dropdown"))
        if over & dd:
            return
        self._close_dropdown()

    # ----- terminal-style console -----
    def add_terminal(self):
        x = self.content_x
        h = max(150, self.canvas.winfo_height() - self._y - PAD_BOTTOM)
        term = ctk.CTkFrame(self.canvas, fg_color=C["term"], corner_radius=12,
                            border_width=1, border_color=C["border"], bg_color=C["bg0"])
        head = ctk.CTkFrame(term, fg_color=C["term_head"], height=34, corner_radius=0)
        head.pack(fill="x", padx=1, pady=(1, 0))
        head.pack_propagate(False)
        dots = ctk.CTkFrame(head, fg_color="transparent")
        dots.pack(side="left", padx=(14, 0))
        for col in (C["dot_red"], C["dot_yellow"], C["dot_green"]):
            ctk.CTkFrame(dots, width=11, height=11, corner_radius=99, fg_color=col).pack(side="left", padx=3)
        ctk.CTkLabel(head, text="subsforge@local: ~", font=self.font(self.f_mono, 11),
                     text_color=C["fg3"]).pack(side="left", padx=12)

        console = ctk.CTkTextbox(term, fg_color=C["term"], corner_radius=0, border_width=0,
                                 text_color=C["fg2"], font=self.font(self.f_mono, 12), wrap="word")
        console.pack(fill="both", expand=True, padx=14, pady=(8, 12))
        try:
            inner = console._textbox
            inner.tag_configure("prompt", foreground=C["good"])
            console.insert("0.0", "$ ")
            inner.tag_add("prompt", "1.0", "1.2")
            console.insert("end", self.t("ready") + "\n")
        except Exception:
            console.insert("0.0", "$ " + self.t("ready") + "\n")
        console.configure(state="disabled")

        self.canvas.create_window(x, self._y, anchor="nw", width=self.content_w, height=h,
                                  window=term, tags="content")
        return console

    # ------------------------------------------------------------------
    #  Process runner
    # ------------------------------------------------------------------
    def run_command_in_thread(self, command, console_box):
        logging.info("Lanzando proceso: " + " ".join(command))
        console_box.configure(state="normal")
        console_box.insert(ctk.END, "\n> Ejecutando...\n")
        console_box.see(ctk.END)
        console_box.configure(state="disabled")
        self.update()

        def task():
            try:
                env = os.environ.copy()
                if os.name == "nt":
                    user_scripts = os.path.join(os.getenv("APPDATA", ""), "Python",
                                                f"Python{sys.version_info.major}{sys.version_info.minor}", "Scripts")
                    env["PATH"] = env.get("PATH", "") + os.pathsep + user_scripts
                env["PYTHONUNBUFFERED"] = "1"
                env["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
                kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "text": True, "env": env}
                if os.name == "nt":
                    kwargs["creationflags"] = CREATE_NO_WINDOW
                process = subprocess.Popen(command, **kwargs)
                for line in iter(process.stdout.readline, ""):
                    clean = line.strip()
                    if clean:
                        logging.info(f"[PROCESO] {clean}")
                    console_box.configure(state="normal")
                    console_box.insert(ctk.END, line)
                    console_box.see(ctk.END)
                    console_box.configure(state="disabled")
                process.stdout.close()
                process.wait()
                logging.info("Proceso completado.")
                console_box.configure(state="normal")
                console_box.insert(ctk.END, "\n[✔] Tarea completada.\n")
            except Exception as e:
                logging.error(f"Error fatal: {e}")
                console_box.configure(state="normal")
                console_box.insert(ctk.END, f"\n[ERROR] {e}\n")
            console_box.see(ctk.END)
            console_box.configure(state="disabled")
            self.update()

        threading.Thread(target=task, daemon=True).start()

    def fetch_ollama_models(self):
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1)
            return [m["name"] for m in r.json().get("models", [])]
        except Exception:
            return []

    # ==================================================================
    #  TABS
    # ==================================================================
    def show_translate_frame(self):
        self.begin_page("title_trans", "desc_trans")
        path_var = ctk.StringVar()
        engine_var = ctk.StringVar(value="google")

        def execute():
            if not path_var.get():
                return
            script = os.path.join(BASE_DIR, "core", "translator.py")
            self.run_command_in_thread(["python", script, path_var.get(), engine_var.get()], console)

        models = ["google"]
        ollama = self._ollama_models
        if ollama:
            models += [f"ollama:{m}" for m in ollama]

        self.card_open(2)
        self.row(None, path_var, [{"text": "browse_file", "icon": "file",
                                   "cmd": lambda: path_var.set(fd.askopenfilename()), "w": 112}])
        self.row_engine(engine_var, models, help_cmd=(None if ollama else self.show_ollama_guide))
        self.card_close()

        self.primary_box(self.t("btn_run_trans"), execute)
        console = self.add_terminal()

    def show_sync_frame(self):
        self.begin_page("title_sync", "desc_sync")
        vid_path, sub_path = ctk.StringVar(), ctk.StringVar()

        def execute():
            if not vid_path.get() or not sub_path.get():
                return
            out_file = os.path.splitext(vid_path.get())[0] + "_sincronizado.srt"
            self.run_command_in_thread(["ffsubsync", vid_path.get(), "-i", sub_path.get(), "-o", out_file], console)

        self.card_open(2)
        for key, var in [("vid_orig", vid_path), ("sub_desf", sub_path)]:
            self.row(key, var, [{"text": "browse_file", "icon": "file",
                                 "cmd": lambda v=var: v.set(fd.askopenfilename()), "w": 112}])
        self.card_close()
        self.primary_box(self.t("btn_run_sync"), execute)
        console = self.add_terminal()

    def show_whisper_frame(self):
        self.begin_page("title_whisp", "desc_whisp")
        path_var = ctk.StringVar()

        def execute():
            if not path_var.get():
                return
            script = os.path.join(BASE_DIR, "core", "whisper_gen.py")
            self.run_command_in_thread(["python", script, path_var.get()], console)

        self.card_open(1)
        self.row("input_source", path_var, [
            {"text": "browse_file", "icon": "file", "cmd": lambda: path_var.set(fd.askopenfilename()), "w": 108},
            {"text": "browse_dir", "icon": "folder", "cmd": lambda: path_var.set(fd.askdirectory()), "w": 108},
        ])
        self.card_close()
        self.primary_box(self.t("btn_run_whisp"), execute)
        console = self.add_terminal()

    def show_mux_frame(self):
        self.begin_page("title_mux", "desc_mux")
        vid_path, sub_path = ctk.StringVar(), ctk.StringVar()

        def execute():
            if not vid_path.get() or not sub_path.get():
                return
            out_file = os.path.splitext(vid_path.get())[0] + "_FINAL.mkv"
            lang_code = "spa" if self.lang == "es" else "eng"
            lang_title = "Español" if self.lang == "es" else "English"
            cmd = [
                "ffmpeg", "-i", vid_path.get(), "-i", sub_path.get(),
                "-map", "0:v", "-map", "0:a", "-map", "1:0",
                "-c:v", "copy", "-c:a", "copy", "-c:s", "srt",
                "-metadata:s:s:0", f"language={lang_code}",
                "-metadata:s:s:0", f"title={lang_title}",
                "-disposition:s:s:0", "default+forced",
                "-y", out_file
            ]
            self.run_command_in_thread(cmd, console)

        self.card_open(2)
        for key, var in [("vid_mkv", vid_path), ("sub_final", sub_path)]:
            self.row(key, var, [{"text": "browse_file", "icon": "file",
                                 "cmd": lambda v=var: v.set(fd.askopenfilename()), "w": 112}])
        self.card_close()
        self.primary_box(self.t("btn_run_mux"), execute)
        console = self.add_terminal()

    def show_cleaner_frame(self):
        self.begin_page("title_clean", "desc_clean")
        path_var = ctk.StringVar()

        def execute():
            if not path_var.get():
                return
            script = os.path.join(BASE_DIR, "core", "ass_cleaner.py")
            self.run_command_in_thread(["python", script, path_var.get()], console)

        self.card_open(1)
        self.row("file_ass", path_var, [{"text": "browse_file", "icon": "file",
                 "cmd": lambda: path_var.set(fd.askopenfilename(filetypes=[("ASS Subtitles", "*.ass")])), "w": 112}])
        self.card_close()
        self.primary_box(self.t("btn_run_clean"), execute, color=(239, 68, 68, 255), hover=(220, 60, 60, 255))
        console = self.add_terminal()

    # ------------------------------------------------------------------
    #  Ollama guide modal
    # ------------------------------------------------------------------
    def show_ollama_guide(self):
        g = ctk.CTkToplevel(self)
        g.title("IA Local · Ollama")
        g.geometry("560x400")
        g.configure(fg_color=C["bg0"])
        g.attributes("-topmost", True)
        wrap = ctk.CTkFrame(g, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=28, pady=26)
        titlerow = ctk.CTkFrame(wrap, fg_color="transparent")
        titlerow.pack(anchor="w")
        ctk.CTkFrame(titlerow, width=4, height=26, corner_radius=99, fg_color=C["accent"]).pack(side="left", padx=(0, 12))
        ctk.CTkLabel(titlerow, text="Cómo usar IA local (Ollama)" if self.lang == "es" else "Using local AI (Ollama)",
                     font=self.font(self.f_title, 19), text_color=C["fg0"]).pack(side="left")
        steps = (
            "1.  Descarga Ollama desde ollama.com\n"
            "2.  Instálalo en tu ordenador.\n"
            "3.  Abre una terminal (CMD) y escribe:\n\n"
            "        ollama run llama3\n\n"
            "4.  Espera a que se descargue el modelo.\n"
            "5.  Reinicia SubsForge y el modelo aparecerá\n"
            "     automáticamente en el menú de motores."
        ) if self.lang == "es" else (
            "1.  Download Ollama from ollama.com\n"
            "2.  Install it on your computer.\n"
            "3.  Open a terminal (CMD) and type:\n\n"
            "        ollama run llama3\n\n"
            "4.  Wait for the model to download.\n"
            "5.  Restart SubsForge and the model will appear\n"
            "     automatically in the engine menu."
        )
        box = ctk.CTkFrame(wrap, fg_color=C["bg2"], corner_radius=12, border_width=1, border_color=C["border"])
        box.pack(fill="both", expand=True, pady=(18, 18))
        ctk.CTkLabel(box, text=steps, justify="left", font=self.font(self.f_mono, 12),
                     text_color=C["fg1"]).pack(padx=22, pady=18, anchor="w")
        ctk.CTkButton(wrap, text="Cerrar" if self.lang == "es" else "Close", command=g.destroy, height=40, width=120,
                      corner_radius=10, font=self.font(self.f_ui_semi, 13), fg_color=C["accent"],
                      hover_color=C["accent_hover"], text_color="#FFFFFF").pack(anchor="e")


if __name__ == "__main__":
    try:
        app = AutoSubsGUI()
        app.mainloop()
        logging.info("App cerrada por el usuario.")
    except Exception as e:
        logging.critical(f"Fallo fatal de la GUI: {e}")

