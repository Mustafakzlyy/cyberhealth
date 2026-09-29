import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t

class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, app_ref, **kwargs):
        super().__init__(master, **kwargs)
        self.app_ref = app_ref
        self.lang = config_manager.get("language", "tr")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setup_ui()

    def update_i18n(self):
        self.lang = config_manager.get("language", "tr")
        self.clean_ui()
        self.setup_ui()

    def clean_ui(self):
        for w in self.winfo_children():
            w.destroy()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        ctk.CTkLabel(
            header,
            text=t("set_title", self.lang),
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=t("set_subtitle", self.lang),
            text_color=("gray40", "#A5B4FC"),
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(2, 0))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        vt_frame = ctk.CTkFrame(
            scroll,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        vt_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            vt_frame,
            text=t("set_vt_header", self.lang),
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=18, pady=(16, 6))

        ctk.CTkLabel(
            vt_frame,
            text=t("set_vt_desc", self.lang),
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "#94A3B8"),
            justify="left",
            wraplength=600
        ).pack(anchor="w", padx=18, pady=(0, 12))

        entry_frame = ctk.CTkFrame(vt_frame, fg_color="transparent")
        entry_frame.pack(fill="x", padx=18, pady=(0, 16))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_vt_key = ctk.CTkEntry(
            entry_frame,
            placeholder_text=t("set_vt_placeholder", self.lang),
            height=40,
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        self.entry_vt_key.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        current_vt_key = config_manager.get("virustotal_api_key", "")
        if current_vt_key:
            self.entry_vt_key.insert(0, current_vt_key)

        btn_save_vt = ctk.CTkButton(
            entry_frame,
            text=t("set_btn_save", self.lang),
            font=ctk.CTkFont(size=13, weight="bold"),
            width=135,
            height=40,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8,
            command=self.save_settings
        )
        btn_save_vt.grid(row=0, column=1)

        self.lbl_toast = ctk.CTkLabel(
            vt_frame,
            text="",
            text_color="#10B981",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_toast.pack(anchor="w", padx=18, pady=(0, 12))

        opts_frame = ctk.CTkFrame(
            scroll,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        opts_frame.pack(fill="x", pady=10)
        opts_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            opts_frame,
            text=t("set_lang_header", self.lang),
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=18, pady=(16, 6), sticky="w")

        if self.lang == "ku":
            lang_val = "Kurdî (KU)"
        elif self.lang == "tr":
            lang_val = "Türkçe (TR)"
        else:
            lang_val = "English (EN)"

        self.opt_lang = ctk.CTkOptionMenu(
            opts_frame,
            values=["Kurdî (KU)", "Türkçe (TR)", "English (EN)"],
            button_color="#6366F1",
            command=self.on_lang_change
        )
        self.opt_lang.set(lang_val)
        self.opt_lang.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="w")

        ctk.CTkLabel(
            opts_frame,
            text=t("set_theme_header", self.lang),
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, padx=18, pady=(16, 6), sticky="w")

        current_theme = config_manager.get("theme", "Dark")
        self.opt_theme = ctk.CTkOptionMenu(
            opts_frame,
            values=["Dark", "Light", "System"],
            button_color="#6366F1",
            command=self.on_theme_change
        )
        self.opt_theme.set(current_theme)
        self.opt_theme.grid(row=1, column=1, padx=18, pady=(0, 16), sticky="w")

        clean_frame = ctk.CTkFrame(
            scroll,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        clean_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            clean_frame,
            text=t("set_history_header", self.lang),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=18, pady=(16, 6))

        btn_clear = ctk.CTkButton(
            clean_frame,
            text=t("set_btn_clear_history", self.lang),
            fg_color="#F43F5E",
            hover_color="#E11D48",
            corner_radius=8,
            command=self.clear_history
        )
        btn_clear.pack(anchor="w", padx=18, pady=(0, 10))

        self.lbl_history_toast = ctk.CTkLabel(
            clean_frame,
            text="",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.lbl_history_toast.pack(anchor="w", padx=18, pady=(0, 16))

        about_frame = ctk.CTkFrame(
            scroll,
            fg_color=("#F8FAFC", "#1E293B"),
            corner_radius=14
        )
        about_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            about_frame,
            text=t("set_about_title", self.lang),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 6))

        ctk.CTkLabel(
            about_frame,
            text=t("set_about_desc", self.lang),
            font=ctk.CTkFont(size=12),
            justify="left",
            wraplength=600
        ).pack(anchor="w", padx=18, pady=(0, 16))

    def save_settings(self):
        vt_key = self.entry_vt_key.get().strip()
        config_manager.set("virustotal_api_key", vt_key)
        self.lbl_toast.configure(text=t("set_saved_toast", self.lang))

    def on_lang_change(self, val):
        if "Kurdî" in val or "KU" in val:
            new_lang = "ku"
        elif "Türkçe" in val or "TR" in val:
            new_lang = "tr"
        else:
            new_lang = "en"
        config_manager.set("language", new_lang)
        self.lang = new_lang
        self.app_ref.refresh_all_i18n()

    def on_theme_change(self, val):
        config_manager.set("theme", val)
        ctk.set_appearance_mode(val)

    def clear_history(self):
        config_manager.clear_history()
        self.lbl_history_toast.configure(text=t("set_history_cleared", self.lang))
