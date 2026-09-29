import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t

class DashboardTab(ctk.CTkFrame):
    def __init__(self, master, nav_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.nav_callback = nav_callback
        self.lang = config_manager.get("language", "tr")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.setup_ui()

    def update_i18n(self):
        self.lang = config_manager.get("language", "tr")
        self.clean_ui()
        self.setup_ui()

    def clean_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_ui(self):
        header_frame = ctk.CTkFrame(
            self,
            fg_color=("white", "#1E1B4B"),
            border_color=("#E0E7FF", "#4338CA"),
            border_width=2,
            corner_radius=14
        )
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkLabel(
            header_frame,
            text=t("dash_welcome", self.lang),
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_lbl.grid(row=0, column=0, padx=20, pady=(16, 6), sticky="w")

        status_frame = ctk.CTkFrame(header_frame, fg_color="#10B981", corner_radius=8)
        status_frame.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="w")

        status_lbl = ctk.CTkLabel(
            status_frame,
            text=t("dash_status_ok", self.lang),
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        status_lbl.pack(padx=14, pady=6)

        sub_lbl = ctk.CTkLabel(
            header_frame,
            text=t("dash_status_ok_sub", self.lang),
            text_color=("gray30", "#A5B4FC"),
            font=ctk.CTkFont(size=12)
        )
        sub_lbl.grid(row=2, column=0, padx=20, pady=(0, 16), sticky="w")

        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1)

        lbl_actions = ctk.CTkLabel(
            actions_frame,
            text=t("dash_quick_actions", self.lang),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lbl_actions.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")

        btn_url = ctk.CTkButton(
            actions_frame,
            text=t("dash_btn_url", self.lang),
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6366F1",
            hover_color="#4F46E5",
            height=48,
            corner_radius=10,
            command=lambda: self.nav_callback("url")
        )
        btn_url.grid(row=1, column=0, padx=6, pady=5, sticky="ew")

        btn_email = ctk.CTkButton(
            actions_frame,
            text=t("dash_btn_email", self.lang),
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10B981",
            hover_color="#059669",
            height=48,
            corner_radius=10,
            command=lambda: self.nav_callback("email")
        )
        btn_email.grid(row=1, column=1, padx=6, pady=5, sticky="ew")

        btn_pass = ctk.CTkButton(
            actions_frame,
            text=t("dash_btn_pass", self.lang),
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#F59E0B",
            hover_color="#D97706",
            height=48,
            corner_radius=10,
            command=lambda: self.nav_callback("pass")
        )
        btn_pass.grid(row=1, column=2, padx=6, pady=5, sticky="ew")

        stats_frame = ctk.CTkFrame(
            self,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#1E293B"),
            border_width=1,
            corner_radius=14
        )
        stats_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        stats_title = ctk.CTkLabel(
            stats_frame,
            text=t("dash_stats_title", self.lang),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_title.grid(row=0, column=0, columnspan=3, padx=18, pady=(16, 12), sticky="w")

        url_history = config_manager.get("url_history", [])
        email_history = config_manager.get("email_history", [])
        vt_key = config_manager.get("virustotal_api_key", "")

        c1 = ctk.CTkFrame(
            stats_frame,
            fg_color=("#F0F9FF", "#1E293B"),
            border_color=("#BAE6FD", "#0EA5E9"),
            border_width=1,
            corner_radius=12
        )
        c1.grid(row=1, column=0, padx=12, pady=12, sticky="nsew")
        ctk.CTkLabel(c1, text="🔗", font=ctk.CTkFont(size=28)).pack(pady=(16, 4))
        ctk.CTkLabel(c1, text=str(len(url_history)), font=ctk.CTkFont(size=26, weight="bold"), text_color="#38BDF8").pack()
        ctk.CTkLabel(c1, text=t("dash_stat_url", self.lang), font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(0, 16))

        c2 = ctk.CTkFrame(
            stats_frame,
            fg_color=("#FFF1F2", "#1E293B"),
            border_color=("#FECDD3", "#F43F5E"),
            border_width=1,
            corner_radius=12
        )
        c2.grid(row=1, column=1, padx=12, pady=12, sticky="nsew")
        ctk.CTkLabel(c2, text="✉️", font=ctk.CTkFont(size=28)).pack(pady=(16, 4))
        ctk.CTkLabel(c2, text=str(len(email_history)), font=ctk.CTkFont(size=26, weight="bold"), text_color="#FB7185").pack()
        ctk.CTkLabel(c2, text=t("dash_stat_breach", self.lang), font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(0, 16))

        c3 = ctk.CTkFrame(
            stats_frame,
            fg_color=("#ECFDF5", "#1E293B"),
            border_color=("#A7F3D0", "#10B981"),
            border_width=1,
            corner_radius=12
        )
        c3.grid(row=1, column=2, padx=12, pady=12, sticky="nsew")
        ctk.CTkLabel(c3, text="☁️", font=ctk.CTkFont(size=28)).pack(pady=(16, 4))
        vt_status_str = t("dash_vt_connected", self.lang) if vt_key else t("dash_vt_local", self.lang)
        vt_color = "#34D399" if vt_key else "#38BDF8"
        ctk.CTkLabel(c3, text=vt_status_str, text_color=vt_color, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(4, 0))
        ctk.CTkLabel(c3, text=t("dash_stat_vt", self.lang), font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(0, 16))
