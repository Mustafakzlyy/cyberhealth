import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t
from cyberhealth.ui.dashboard_tab import DashboardTab
from cyberhealth.ui.url_tab import URLTab
from cyberhealth.ui.breach_tab import BreachTab
from cyberhealth.ui.password_tab import PasswordTab
from cyberhealth.ui.guide_tab import GuideTab
from cyberhealth.ui.settings_tab import SettingsTab

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        saved_theme = config_manager.get("theme", "Dark")
        ctk.set_appearance_mode(saved_theme)
        ctk.set_default_color_theme("blue")

        self.title("CyberHealth Desktop - Son Kullanıcı Güvenlik Asistanı")
        self.geometry("1060 x 690")
        self.minsize(940, 620)

        self.lang = config_manager.get("language", "tr")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_tab_name = "dashboard"

        self.setup_sidebar()
        self.setup_container()
        self.select_tab("dashboard")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=("#F1F5F9", "#0B0F19")
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        logo_lbl = ctk.CTkLabel(
            self.sidebar,
            text="🛡️ CyberHealth",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#4F46E5", "#818CF8")
        )
        logo_lbl.grid(row=0, column=0, padx=20, pady=(22, 2))

        sub_lbl = ctk.CTkLabel(
            self.sidebar,
            text="Security & Health Assistant",
            text_color=("gray40", "#A5B4FC"),
            font=ctk.CTkFont(size=11)
        )
        sub_lbl.grid(row=1, column=0, padx=20, pady=(0, 22))

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "dash_btn", "nav_dashboard", "🏠"),
            ("url", "url_btn", "nav_url_analyzer", "🔗"),
            ("email", "email_btn", "nav_breach_checker", "✉️"),
            ("pass", "pass_btn", "nav_pass_generator", "🔑"),
            ("guide", "guide_btn", "nav_guide", "🛡️"),
            ("settings", "set_btn", "nav_settings", "⚙️")
        ]

        for idx, (tab_key, btn_key, title_key, icon) in enumerate(nav_items, start=2):
            btn_text = f"{icon}  {t(title_key, self.lang)}"
            btn = ctk.CTkButton(
                self.sidebar,
                text=btn_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                height=42,
                corner_radius=10,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("#E2E8F0", "#1E293B"),
                command=lambda k=tab_key: self.select_tab(k)
            )
            btn.grid(row=idx, column=0, padx=14, pady=4, sticky="ew")
            self.nav_buttons[tab_key] = btn

        badge = ctk.CTkLabel(
            self.sidebar,
            text=t("zero_friction_badge", self.lang),
            text_color=("gray40", "#64748B"),
            font=ctk.CTkFont(size=10, weight="bold")
        )
        badge.grid(row=8, column=0, padx=10, pady=16, sticky="s")

    def setup_container(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.tabs = {
            "dashboard": DashboardTab(self.container, nav_callback=self.select_tab),
            "url": URLTab(self.container),
            "email": BreachTab(self.container),
            "pass": PasswordTab(self.container),
            "guide": GuideTab(self.container),
            "settings": SettingsTab(self.container, app_ref=self)
        }

        for tab_widget in self.tabs.values():
            tab_widget.grid(row=0, column=0, sticky="nsew")

    def select_tab(self, tab_key: str):
        self.current_tab_name = tab_key

        for key, tab_widget in self.tabs.items():
            if key == tab_key:
                tab_widget.tkraise()
            
        for key, btn in self.nav_buttons.items():
            if key == tab_key:
                btn.configure(fg_color="#6366F1", text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def refresh_all_i18n(self):
        self.lang = config_manager.get("language", "tr")

        nav_items = [
            ("dashboard", "nav_dashboard", "🏠"),
            ("url", "nav_url_analyzer", "🔗"),
            ("email", "nav_breach_checker", "✉️"),
            ("pass", "nav_pass_generator", "🔑"),
            ("guide", "nav_guide", "🛡️"),
            ("settings", "nav_settings", "⚙️")
        ]

        for tab_key, title_key, icon in nav_items:
            if tab_key in self.nav_buttons:
                self.nav_buttons[tab_key].configure(text=f"{icon}  {t(title_key, self.lang)}")

        for tab_widget in self.tabs.values():
            if hasattr(tab_widget, "update_i18n"):
                tab_widget.update_i18n()
