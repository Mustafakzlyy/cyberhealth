import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t
from cyberhealth.modules.url_analyzer import URLAnalyzer

class URLTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lang = config_manager.get("language", "tr")
        self.analyzer = URLAnalyzer(vt_api_key=config_manager.get("virustotal_api_key", ""))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.setup_ui()

    def update_i18n(self):
        self.lang = config_manager.get("language", "tr")
        self.analyzer.set_api_key(config_manager.get("virustotal_api_key", ""))
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
            text=t("url_title", self.lang),
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=t("url_subtitle", self.lang),
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
            text=t("url_input_label", self.lang),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        lbl_input.grid(row=0, column=0, columnspan=3, padx=16, pady=(12, 6), sticky="w")

        self.entry_url = ctk.CTkEntry(
            input_frame,
            placeholder_text=t("url_placeholder", self.lang),
            height=42,
            font=ctk.CTkFont(size=13),
            corner_radius=8
        )
        self.entry_url.grid(row=1, column=0, padx=(16, 6), pady=(0, 16), sticky="ew")

        btn_paste = ctk.CTkButton(
            input_frame,
            text=t("url_btn_paste", self.lang),
            width=105,
            height=42,
            fg_color=("gray70", "#334155"),
            hover_color=("gray60", "#475569"),
            corner_radius=8,
            command=self.paste_from_clipboard
        )
        btn_paste.grid(row=1, column=1, padx=6, pady=(0, 16))

        btn_scan = ctk.CTkButton(
            input_frame,
            text=t("url_btn_analyze", self.lang),
            font=ctk.CTkFont(size=13, weight="bold"),
            width=145,
            height=42,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8,
            command=self.run_analysis
        )
        btn_scan.grid(row=1, column=2, padx=(6, 16), pady=(0, 16))

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

    def paste_from_clipboard(self):
        try:
            clipboard_content = self.clipboard_get()
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, clipboard_content)
        except Exception:
            pass

    def run_analysis(self):
        url = self.entry_url.get().strip()
        if not url:
            return

        self.lbl_status.configure(text=t("url_scanning", self.lang))
        self.update_idletasks()

        self.analyzer.set_api_key(config_manager.get("virustotal_api_key", ""))
        result = self.analyzer.analyze(url)
        config_manager.add_url_history(url, result["status"], result["score"])

        self.lbl_status.configure(text="")
        self.render_results(result)

    def render_results(self, res: dict):
        for w in self.results_scroll.winfo_children():
            w.destroy()

        status = res["status"]
        score = res["score"]

        color_map = {
            "safe": ("#10B981", t("url_risk_safe", self.lang)),
            "caution": ("#F59E0B", t("url_risk_caution", self.lang)),
            "danger": ("#F43F5E", t("url_risk_danger", self.lang))
        }
        badge_color, badge_text = color_map.get(status, ("#10B981", "UNKNOWN"))

        banner = ctk.CTkFrame(self.results_scroll, fg_color=badge_color, corner_radius=14)
        banner.pack(fill="x", pady=(0, 12))

        lbl_badge = ctk.CTkLabel(
            banner,
            text=badge_text,
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_badge.pack(padx=20, pady=(16, 4))

        lbl_score = ctk.CTkLabel(
            banner,
            text=f"{t('url_score_label', self.lang)}: {score} / 100",
            text_color="white",
            font=ctk.CTkFont(size=14)
        )
        lbl_score.pack(padx=20, pady=(0, 16))

        details_frame = ctk.CTkFrame(
            self.results_scroll,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        details_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            details_frame,
            text=t("url_details_title", self.lang),
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=18, pady=(16, 10))

        findings = res.get("findings", [])
        if not findings:
            ctk.CTkLabel(
                details_frame,
                text="✔️ " + t("url_advice_safe", self.lang),
                font=ctk.CTkFont(size=13),
                text_color="#10B981"
            ).pack(anchor="w", padx=20, pady=(0, 16))
        else:
            for item in findings:
                f_type = item[0]
                f_val = item[1] if len(item) > 1 else ""

                msg_key = f"find_{f_type}"
                msg_template = t(msg_key, self.lang)
                if "{brand}" in msg_template:
                    msg = msg_template.format(brand=f_val)
                elif "{tld}" in msg_template:
                    msg = msg_template.format(tld=f_val)
                elif "{keyword}" in msg_template:
                    msg = msg_template.format(keyword=f_val)
                else:
                    msg = msg_template

                item_lbl = ctk.CTkLabel(
                    details_frame,
                    text=f"• {msg}",
                    font=ctk.CTkFont(size=13),
                    justify="left",
                    wraplength=600
                )
                item_lbl.pack(anchor="w", padx=20, pady=4)

            ctk.CTkFrame(details_frame, height=10, fg_color="transparent").pack()

        vt_info = res.get("vt", {})
        vt_frame = ctk.CTkFrame(
            self.results_scroll,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        vt_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            vt_frame,
            text=f"☁️ {t('url_vt_cloud_status', self.lang)}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 6))

        if vt_info.get("active"):
            malicious = vt_info.get("malicious", 0)
            total = vt_info.get("total", 0)
            vt_msg = t("find_vt_engines", self.lang).format(malicious=malicious, total=total)
            color = "#F43F5E" if malicious > 0 else "#10B981"
            ctk.CTkLabel(
                vt_frame,
                text=f"• {vt_msg}",
                text_color=color,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", padx=20, pady=(0, 14))
        else:
            ctk.CTkLabel(
                vt_frame,
                text=f"• {t('url_vt_inactive', self.lang)}",
                text_color=("gray50", "#94A3B8"),
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=20, pady=(0, 14))

        advice_frame = ctk.CTkFrame(
            self.results_scroll,
            fg_color=("#F8FAFC", "#1E293B"),
            corner_radius=14
        )
        advice_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            advice_frame,
            text=f"💡 {t('url_advice_title', self.lang)}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 6))

        advice_text = t(f"url_advice_{status}", self.lang)
        ctk.CTkLabel(
            advice_frame,
            text=advice_text,
            font=ctk.CTkFont(size=13),
            justify="left",
            wraplength=600
        ).pack(anchor="w", padx=20, pady=(0, 16))
