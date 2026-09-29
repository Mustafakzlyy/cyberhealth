import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t
from cyberhealth.modules.breach_checker import BreachChecker

class BreachTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lang = config_manager.get("language", "tr")
        self.checker = BreachChecker()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

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
            text=t("breach_title", self.lang),
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=t("breach_subtitle", self.lang),
            text_color=("gray40", "#A5B4FC"),
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(2, 0))

        input_frame = ctk.CTkFrame(
            self,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        lbl_input = ctk.CTkLabel(
            input_frame,
            text=t("breach_input_label", self.lang),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        lbl_input.grid(row=0, column=0, columnspan=2, padx=16, pady=(12, 6), sticky="w")

        self.entry_email = ctk.CTkEntry(
            input_frame,
            placeholder_text=t("breach_placeholder", self.lang),
            height=42,
            font=ctk.CTkFont(size=13),
            corner_radius=8
        )
        self.entry_email.grid(row=1, column=0, padx=(16, 6), pady=(0, 10), sticky="ew")

        btn_check = ctk.CTkButton(
            input_frame,
            text=t("breach_btn_check", self.lang),
            font=ctk.CTkFont(size=13, weight="bold"),
            width=155,
            height=42,
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=8,
            command=self.run_check
        )
        btn_check.grid(row=1, column=1, padx=(6, 16), pady=(0, 10))

        lbl_privacy = ctk.CTkLabel(
            input_frame,
            text=t("breach_privacy_note", self.lang),
            text_color="#10B981",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        lbl_privacy.grid(row=2, column=0, columnspan=2, padx=16, pady=(0, 14), sticky="w")

        self.lbl_status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=("gray40", "#94A3B8")
        )
        self.lbl_status.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")

        self.results_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_scroll.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.results_scroll.grid_columnconfigure(0, weight=1)

    def run_check(self):
        email = self.entry_email.get().strip()
        if not email:
            return

        self.lbl_status.configure(text=t("breach_checking", self.lang))
        self.update_idletasks()

        res = self.checker.check_email(email)
        if res.get("valid"):
            config_manager.add_email_history(email, res["is_breached"], res["breach_count"])

        self.lbl_status.configure(text="")
        self.render_results(res)

    def render_results(self, res: dict):
        for w in self.results_scroll.winfo_children():
            w.destroy()

        if not res.get("valid"):
            err_frame = ctk.CTkFrame(self.results_scroll, fg_color="#F43F5E", corner_radius=14)
            err_frame.pack(fill="x", pady=10)
            ctk.CTkLabel(
                err_frame,
                text="⚠️ Lütfen geçerli bir e-posta adresi girin!",
                text_color="white",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(padx=20, pady=16)
            return

        is_breached = res["is_breached"]
        count = res["breach_count"]

        if not is_breached:
            banner = ctk.CTkFrame(self.results_scroll, fg_color="#10B981", corner_radius=14)
            banner.pack(fill="x", pady=(0, 16))

            ctk.CTkLabel(
                banner,
                text=t("breach_safe_title", self.lang),
                text_color="white",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(padx=20, pady=(16, 6))

            ctk.CTkLabel(
                banner,
                text=t("breach_safe_desc", self.lang),
                text_color="white",
                font=ctk.CTkFont(size=13),
                wraplength=600
            ).pack(padx=20, pady=(0, 16))

        else:
            banner = ctk.CTkFrame(self.results_scroll, fg_color="#F43F5E", corner_radius=14)
            banner.pack(fill="x", pady=(0, 16))

            ctk.CTkLabel(
                banner,
                text=t("breach_found_title", self.lang),
                text_color="white",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(padx=20, pady=(16, 6))

            desc = t("breach_found_desc", self.lang).format(count=count)
            ctk.CTkLabel(
                banner,
                text=desc,
                text_color="white",
                font=ctk.CTkFont(size=13),
                wraplength=600
            ).pack(padx=20, pady=(0, 16))

            breaches_frame = ctk.CTkFrame(
                self.results_scroll,
                fg_color=("white", "#151C2C"),
                border_color=("#E2E8F0", "#334155"),
                border_width=1,
                corner_radius=14
            )
            breaches_frame.pack(fill="x", pady=10)

            ctk.CTkLabel(
                breaches_frame,
                text=t("breach_list_title", self.lang),
                font=ctk.CTkFont(size=15, weight="bold")
            ).pack(anchor="w", padx=18, pady=(16, 10))

            for b in res.get("breaches", []):
                card = ctk.CTkFrame(
                    breaches_frame,
                    fg_color=("#FFF1F2", "#1E293B"),
                    border_color=("#FECDD3", "#F43F5E"),
                    border_width=1,
                    corner_radius=10
                )
                card.pack(fill="x", padx=16, pady=6)

                title_str = f"🔴 {b['name']} ({b.get('date', 'N/A')})"
                ctk.CTkLabel(
                    card,
                    text=title_str,
                    font=ctk.CTkFont(size=13, weight="bold")
                ).pack(anchor="w", padx=14, pady=(10, 2))

                data_str = "• Sızan Veriler: " + ", ".join(b.get("data_classes", []))
                ctk.CTkLabel(
                    card,
                    text=data_str,
                    text_color=("gray30", "#94A3B8"),
                    font=ctk.CTkFont(size=12)
                ).pack(anchor="w", padx=14, pady=(0, 10))

            ctk.CTkFrame(breaches_frame, height=10, fg_color="transparent").pack()

        action_frame = ctk.CTkFrame(
            self.results_scroll,
            fg_color=("#F8FAFC", "#1E293B"),
            corner_radius=14
        )
        action_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            action_frame,
            text=t("breach_action_plan", self.lang),
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=18, pady=(16, 10))

        for step_idx in range(1, 5):
            step_text = t(f"breach_step_{step_idx}", self.lang)
            ctk.CTkLabel(
                action_frame,
                text=step_text,
                font=ctk.CTkFont(size=13),
                justify="left",
                wraplength=600
            ).pack(anchor="w", padx=20, pady=4)

        ctk.CTkFrame(action_frame, height=12, fg_color="transparent").pack()
