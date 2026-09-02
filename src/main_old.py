import customtkinter as ctk
import tkinter.filedialog as fd
import threading
import subprocess
import os
import sys
import logging
import requests

# ====== CONFIGURACIÓN DE LOGS ======
log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "autosubs.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.info("=========================================")
logging.info("SubsForge (legacy V3) - Interfaz Iniciada")
logging.info("=========================================")

if os.name == 'nt':
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ====== DICCIONARIO i18n ======
T = {
    "es": {
        "btn_translate": "  Traductor IA",
        "btn_sync": "  Sincronización VAD",
        "btn_whisper": "  Transcripción Whisper",
        "btn_mux": "  Fusión Lossless (MKV)",
        "btn_cleaner": "  Limpiador Anime (ASS)",
        "lang_toggle": "🇪🇸 ES",
        "title_trans": "Traductor IA",
        "desc_trans": "Traduce subtítulos al español. Compatible con Ollama Local.",
        "browse_file": "Examinar Archivo",
        "browse_dir": "Examinar Carpeta",
        "btn_run_trans": "Traducir",
        "engine": "Motor IA:",
        "detecting": "Buscando Ollama...",
        "title_sync": "Sincronización Automática",
        "desc_sync": "Alinea subtítulos desfasados utilizando detección de voz (VAD).",
        "vid_orig": "Vídeo original:",
        "sub_desf": "Subtítulo desfasado:",
        "btn_run_sync": "Sincronizar",
        "title_whisp": "Generación con Whisper (Maratón)",
        "desc_whisp": "Extrae el audio y transcribe. Soporta archivos o carpetas enteras.",
        "btn_run_whisp": "Procesar",
        "title_mux": "Fusión Lossless (MKV Muxer)",
        "desc_mux": "Integra el subtítulo dentro del archivo de vídeo sin perder calidad.",
        "vid_mkv": "Vídeo (.mkv):",
        "sub_final": "Subtítulo (.srt):",
        "btn_run_mux": "Integrar Archivos",
        "title_clean": "Limpiador Anime (ASS -> SRT)",
        "desc_clean": "Convierte subtítulos complejos .ass en texto plano compatible con TV.",
        "file_ass": "Archivo (.ass):",
        "btn_run_clean": "Limpiar Subtítulo",
        "btn_ollama_help": "Instalar IA Local ℹ️"
    },
    "en": {
        "btn_translate": "  AI Translator",
        "btn_sync": "  VAD Synchronization",
        "btn_whisper": "  Whisper Transcription",
        "btn_mux": "  Lossless Muxer (MKV)",
        "btn_cleaner": "  Anime Cleaner (ASS)",
        "lang_toggle": "🇬🇧 EN",
        "title_trans": "AI Translator",
        "desc_trans": "Translate subtitles to Spanish. Supports Local Ollama.",
        "browse_file": "Browse File",
        "browse_dir": "Browse Folder",
        "btn_run_trans": "Translate",
        "engine": "AI Engine:",
        "detecting": "Detecting Ollama...",
        "title_sync": "Auto Synchronization",
        "desc_sync": "Align desynced subtitles using Voice Activity Detection (VAD).",
        "vid_orig": "Original Video:",
        "sub_desf": "Desynced Subtitle:",
        "btn_run_sync": "Synchronize",
        "title_whisp": "Whisper Generation (Batch)",
        "desc_whisp": "Extract audio and transcribe. Supports single files or entire folders.",
        "btn_run_whisp": "Process",
        "title_mux": "Lossless Muxer (MKV)",
        "desc_mux": "Embed subtitles directly into the video file without quality loss.",
        "vid_mkv": "Video (.mkv):",
        "sub_final": "Subtitle (.srt):",
        "btn_run_mux": "Mux Files",
        "title_clean": "Anime Cleaner (ASS -> SRT)",
        "desc_clean": "Convert complex .ass subtitles into plain text TV-compatible SRT.",
        "file_ass": "File (.ass):",
        "btn_run_clean": "Clean Subtitle",
        "btn_ollama_help": "Install Local AI ℹ️"
    }
}

class AutoSubsGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "es"
        self.title("SubsForge")
        self.geometry("950x650")
        self.minsize(800, 500)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.active_tab = "translate"

        self.build_sidebar()
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#242424")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.refresh_ui()

    def t(self, key):
        return T[self.lang].get(key, key)

    def toggle_language(self):
        self.lang = "en" if self.lang == "es" else "es"
        self.build_sidebar()
        self.refresh_ui()

    def build_sidebar(self):
        if hasattr(self, 'sidebar_frame'):
            self.sidebar_frame.destroy()
            
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="SubsForge", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=20, pady=(30, 40))

        btn_kwargs = {"fg_color": "transparent", "text_color": ("gray10", "gray90"), "hover_color": ("gray70", "gray30"), "anchor": "w", "font": ctk.CTkFont(size=14)}

        ctk.CTkButton(self.sidebar_frame, text=self.t("btn_translate"), command=lambda: self.set_tab("translate"), **btn_kwargs).grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar_frame, text=self.t("btn_sync"), command=lambda: self.set_tab("sync"), **btn_kwargs).grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar_frame, text=self.t("btn_whisper"), command=lambda: self.set_tab("whisper"), **btn_kwargs).grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar_frame, text=self.t("btn_mux"), command=lambda: self.set_tab("mux"), **btn_kwargs).grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self.sidebar_frame, text=self.t("btn_cleaner"), command=lambda: self.set_tab("cleaner"), **btn_kwargs).grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkButton(self.sidebar_frame, text=self.t("lang_toggle"), command=self.toggle_language, fg_color="#333333", width=80).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def set_tab(self, tab_name):
        self.active_tab = tab_name
        self.refresh_ui()

    def refresh_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        if self.active_tab == "translate": self.show_translate_frame()
        elif self.active_tab == "sync": self.show_sync_frame()
        elif self.active_tab == "whisper": self.show_whisper_frame()
        elif self.active_tab == "mux": self.show_mux_frame()
        elif self.active_tab == "cleaner": self.show_cleaner_frame()

    def run_command_in_thread(self, command, console_box):
        cmd_str = ' '.join(command)
        logging.info(f"Lanzando proceso: {cmd_str}")
        
        console_box.configure(state="normal")
        console_box.insert(ctk.END, f"\n> Executing...\n")
        console_box.see(ctk.END)
        console_box.configure(state="disabled")
        self.update()
        
        def task():
            try:
                env = os.environ.copy()
                if os.name == 'nt':
                    user_script_path = os.path.join(os.getenv('APPDATA'), 'Python', f'Python{sys.version_info.major}{sys.version_info.minor}', 'Scripts')
                    env["PATH"] = env.get("PATH", "") + os.pathsep + user_script_path
                
                env["PYTHONUNBUFFERED"] = "1"
                env["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
                env["PYTHONIOENCODING"] = "utf-8"
                
                kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "text": True, "encoding": "utf-8", "env": env}
                if os.name == 'nt': kwargs["creationflags"] = CREATE_NO_WINDOW
                
                process = subprocess.Popen(command, **kwargs)
                
                for line in iter(process.stdout.readline, ''):
                    clean_line = line.strip()
                    if clean_line: logging.info(f"[PROCESO] {clean_line}")
                    console_box.configure(state="normal")
                    console_box.insert(ctk.END, line)
                    console_box.see(ctk.END)
                    console_box.configure(state="disabled")
                    
                process.stdout.close()
                process.wait()
                
                logging.info("Process complete.")
                console_box.configure(state="normal")
                console_box.insert(ctk.END, "\n[✔] Task Completed.\n")
                
            except Exception as e:
                logging.error(f"Fatal error: {str(e)}")
                console_box.configure(state="normal")
                console_box.insert(ctk.END, f"\n[ERROR] {str(e)}\n")
                
            console_box.see(ctk.END)
            console_box.configure(state="disabled")
            self.update()

        threading.Thread(target=task, daemon=True).start()

    def create_title(self, title_key, subtitle_key):
        ctk.CTkLabel(self.main_frame, text=self.t(title_key), font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self.main_frame, text=self.t(subtitle_key), font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 20))

    def create_console(self):
        console = ctk.CTkTextbox(self.main_frame, width=600, height=200, corner_radius=8, fg_color="#1a1a1a", text_color="#a3a3a3")
        console.pack(pady=20, fill="both", expand=True, padx=30)
        console.configure(state="disabled")
        return console

    def fetch_ollama_models(self):
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1)
            return [m["name"] for m in r.json().get("models", [])]
        except:
            return []

    # --- PESTAÑAS ---
    def show_translate_frame(self):
        self.create_title("title_trans", "desc_trans")
        
        path_var = ctk.StringVar()
        engine_var = ctk.StringVar(value="google")
        
        def execute():
            if not path_var.get(): return
            script_path = os.path.join(os.path.dirname(__file__), "core", "translator.py")
            self.run_command_in_thread(["python", script_path, path_var.get(), engine_var.get()], console)

        # File selection
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(pady=5, fill="x", padx=30)
        ctk.CTkEntry(row, textvariable=path_var, state="disabled", corner_radius=6).pack(side="left", padx=(0,10), expand=True, fill="x")
        ctk.CTkButton(row, text=self.t("browse_file"), command=lambda: path_var.set(fd.askopenfilename()), width=100).pack(side="left")

        # Engine selection
        row_eng = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row_eng.pack(pady=10, fill="x", padx=30)
        ctk.CTkLabel(row_eng, text=self.t("engine"), width=80, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        models = ["google"]
        ollama_models = self.fetch_ollama_models()
        if ollama_models:
            models.extend([f"ollama:{m}" for m in ollama_models])
            
        dropdown = ctk.CTkOptionMenu(row_eng, variable=engine_var, values=models, width=250)
        dropdown.pack(side="left", padx=10)

        if not ollama_models:
            ctk.CTkButton(row_eng, text=self.t("btn_ollama_help"), command=self.show_ollama_guide, fg_color="#b38600", hover_color="#806000", width=140).pack(side="left", padx=10)

        ctk.CTkButton(self.main_frame, text=self.t("btn_run_trans"), command=execute, width=200).pack(pady=10)
        console = self.create_console()

    def show_sync_frame(self):
        self.create_title("title_sync", "desc_sync")

        vid_path, sub_path = ctk.StringVar(), ctk.StringVar()
        
        def execute():
            if not vid_path.get() or not sub_path.get(): return
            out_file = os.path.splitext(vid_path.get())[0] + "_sincronizado.srt"
            cmd = ["ffsubsync", vid_path.get(), "-i", sub_path.get(), "-o", out_file]
            self.run_command_in_thread(cmd, console)

        for text_key, var, is_dir in [("vid_orig", vid_path, False), ("sub_desf", sub_path, False)]:
            row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            row.pack(pady=5, fill="x", padx=30)
            ctk.CTkLabel(row, text=self.t(text_key), width=140, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, state="disabled", corner_radius=6).pack(side="left", padx=(10,10), expand=True, fill="x")
            ctk.CTkButton(row, text=self.t("browse_file"), command=lambda v=var: v.set(fd.askopenfilename()), width=100).pack(side="left")

        ctk.CTkButton(self.main_frame, text=self.t("btn_run_sync"), command=execute, width=200).pack(pady=15)
        console = self.create_console()
        
    def show_whisper_frame(self):
        self.create_title("title_whisp", "desc_whisp")

        path_var = ctk.StringVar()
        
        def execute():
            if not path_var.get(): return
            script_path = os.path.join(os.path.dirname(__file__), "core", "whisper_gen.py")
            self.run_command_in_thread(["python", script_path, path_var.get()], console)

        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(pady=10, fill="x", padx=30)
        ctk.CTkEntry(row, textvariable=path_var, state="disabled", corner_radius=6).pack(side="left", padx=(0,10), expand=True, fill="x")
        ctk.CTkButton(row, text=self.t("browse_file"), command=lambda: path_var.set(fd.askopenfilename()), width=100).pack(side="left", padx=5)
        ctk.CTkButton(row, text=self.t("browse_dir"), command=lambda: path_var.set(fd.askdirectory()), width=100, fg_color="#555555").pack(side="left")

        ctk.CTkButton(self.main_frame, text=self.t("btn_run_whisp"), command=execute, width=200).pack(pady=10)
        console = self.create_console()
        
    def show_mux_frame(self):
        self.create_title("title_mux", "desc_mux")

        vid_path, sub_path = ctk.StringVar(), ctk.StringVar()
        
        def execute():
            if not vid_path.get() or not sub_path.get(): return
            out_file = os.path.splitext(vid_path.get())[0] + "_FINAL.mkv"
            cmd = ["ffmpeg", "-i", vid_path.get(), "-i", sub_path.get(), "-c", "copy", "-c:s", "srt", out_file]
            self.run_command_in_thread(cmd, console)

        for text_key, var in [("vid_mkv", vid_path), ("sub_final", sub_path)]:
            row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            row.pack(pady=5, fill="x", padx=30)
            ctk.CTkLabel(row, text=self.t(text_key), width=140, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
            ctk.CTkEntry(row, textvariable=var, state="disabled", corner_radius=6).pack(side="left", padx=(10,10), expand=True, fill="x")
            ctk.CTkButton(row, text=self.t("browse_file"), command=lambda v=var: v.set(fd.askopenfilename()), width=100).pack(side="left")

        ctk.CTkButton(self.main_frame, text=self.t("btn_run_mux"), command=execute, width=200).pack(pady=15)
        console = self.create_console()
        
    def show_cleaner_frame(self):
        self.create_title("title_clean", "desc_clean")

        path_var = ctk.StringVar()
        
        def execute():
            if not path_var.get(): return
            script_path = os.path.join(os.path.dirname(__file__), "core", "ass_cleaner.py")
            self.run_command_in_thread(["python", script_path, path_var.get()], console)

        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(pady=10, fill="x", padx=30)
        ctk.CTkLabel(row, text=self.t("file_ass"), width=140, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkEntry(row, textvariable=path_var, state="disabled", corner_radius=6).pack(side="left", padx=(10,10), expand=True, fill="x")
        ctk.CTkButton(row, text=self.t("browse_file"), command=lambda: path_var.set(fd.askopenfilename(filetypes=[("ASS Subtitles", "*.ass")])), width=100).pack(side="left")

        ctk.CTkButton(self.main_frame, text=self.t("btn_run_clean"), command=execute, width=200, fg_color="#b32400", hover_color="#801a00").pack(pady=15)
        console = self.create_console()

    def show_ollama_guide(self):
        guide = ctk.CTkToplevel(self)
        guide.title("Guía: IA Local")
        guide.geometry("550x380")
        guide.attributes("-topmost", True)
        
        ctk.CTkLabel(guide, text="🧠 Cómo usar IA Local (Ollama)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        instrucciones = (
            "1. Descarga Ollama desde su web oficial: https://ollama.com\n"
            "2. Instálalo en tu ordenador.\n"
            "3. Abre una terminal (CMD) y escribe el siguiente comando:\n\n"
            "   ollama run llama3\n\n"
            "4. Espera a que se descargue el modelo de Inteligencia Artificial.\n"
            "5. Reinicia SubsForge y el modelo aparecerá automáticamente\n"
            "   en el menú desplegable para traducir sin necesidad de internet."
        ) if self.lang == "es" else (
            "1. Download Ollama from the official website: https://ollama.com\n"
            "2. Install it on your computer.\n"
            "3. Open a terminal (CMD) and type the following command:\n\n"
            "   ollama run llama3\n\n"
            "4. Wait for the Artificial Intelligence model to download.\n"
            "5. Restart SubsForge and the model will appear automatically\n"
            "   in the dropdown menu for offline translation."
        )
        
        ctk.CTkLabel(guide, text=instrucciones, justify="left", font=ctk.CTkFont(size=14)).pack(padx=30, pady=10, fill="x")
        ctk.CTkButton(guide, text="Cerrar / Close", command=guide.destroy).pack(pady=20)

if __name__ == "__main__":
    try:
        app = AutoSubsGUI()
        app.mainloop()
        logging.info("App closed by user.")
    except Exception as e:
        logging.critical(f"Fatal GUI crash: {str(e)}")
