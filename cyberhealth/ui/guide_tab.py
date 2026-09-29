import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t

class GuideTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
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
            text=t("guide_title", self.lang),
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=t("guide_subtitle", self.lang),
            text_color=("gray40", "#A5B4FC"),
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(2, 0))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        cards_data = [
            ("gcard_1_title", "gcard_1_desc", "#6366F1", "#EEF2FF"),
            ("gcard_2_title", "gcard_2_desc", "#F59E0B", "#FEF3C7"),
            ("gcard_3_title", "gcard_3_desc", "#10B981", "#D1FAE5"),
            ("gcard_4_title", "gcard_4_desc", "#06B6D4", "#CFFAFE")
        ]

        for title_key, desc_key, accent_color, light_bg in cards_data:
            card = ctk.CTkFrame(
                scroll,
                fg_color=("white", "#151C2C"),
                border_color=("#E2E8F0", "#334155"),
                border_width=1,
                corner_radius=14
            )
            card.pack(fill="x", pady=10)

            bar = ctk.CTkFrame(card, width=7, fg_color=accent_color, corner_radius=0)
            bar.pack(side="left", fill="y", padx=(0, 12))

            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(side="left", fill="both", expand=True, padx=12, pady=14)

            ctk.CTkLabel(
                content_frame,
                text=t(title_key, self.lang),
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                content_frame,
                text=t(desc_key, self.lang),
                font=ctk.CTkFont(size=13),
                justify="left",
                wraplength=600
            ).pack(anchor="w", pady=(6, 0))
