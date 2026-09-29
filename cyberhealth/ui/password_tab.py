import customtkinter as ctk
from cyberhealth.config import config_manager
from cyberhealth.i18n import t
from cyberhealth.modules.pass_generator import PasswordGenerator

class PasswordTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lang = config_manager.get("language", "tr")
        self.generator = PasswordGenerator()
        self.mode = "passphrase"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.setup_ui()
        self.generate()

    def update_i18n(self):
        self.lang = config_manager.get("language", "tr")
        self.clean_ui()
        self.setup_ui()
        self.generate()

    def clean_ui(self):
        for w in self.winfo_children():
            w.destroy()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        ctk.CTkLabel(
            header,
            text=t("pass_title", self.lang),
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=t("pass_subtitle", self.lang),
            text_color=("gray40", "#A5B4FC"),
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(2, 0))

        selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        selector_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.mode_segmented = ctk.CTkSegmentedButton(
            selector_frame,
            values=[t("pass_mode_passphrase", self.lang), t("pass_mode_classic", self.lang)],
            selected_color="#6366F1",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_mode_change
        )
        self.mode_segmented.set(t("pass_mode_passphrase", self.lang))
        self.mode_segmented.pack(fill="x")

        self.container = ctk.CTkFrame(
            self,
            fg_color=("white", "#151C2C"),
            border_color=("#E2E8F0", "#334155"),
            border_width=1,
            corner_radius=14
        )
        self.container.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)

        self.setup_generator_controls()

    def on_mode_change(self, val):
        if val == t("pass_mode_passphrase", self.lang):
            self.mode = "passphrase"
        else:
            self.mode = "classic"
        
        for w in self.container.winfo_children():
            w.destroy()
        self.setup_generator_controls()
        self.generate()

    def setup_generator_controls(self):
        disp_frame = ctk.CTkFrame(
            self.container,
            fg_color=("#EEF2FF", "#0F172A"),
            border_color=("#C7D2FE", "#4338CA"),
            border_width=1.5,
            corner_radius=12
        )
        disp_frame.pack(fill="x", padx=16, pady=(16, 10))
        disp_frame.grid_columnconfigure(0, weight=1)

        self.entry_pass = ctk.CTkEntry(
            disp_frame,
            font=ctk.CTkFont(size=18, weight="bold", family="Monospace"),
            height=48,
            fg_color="transparent",
            border_width=0
        )
        self.entry_pass.grid(row=0, column=0, padx=16, pady=6, sticky="ew")

        btn_copy = ctk.CTkButton(
            disp_frame,
            text=t("pass_btn_copy", self.lang),
            font=ctk.CTkFont(size=13, weight="bold"),
            width=115,
            height=40,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8,
            command=self.copy_to_clipboard
        )
        btn_copy.grid(row=0, column=1, padx=(6, 14), pady=6)

        self.lbl_copied = ctk.CTkLabel(
            disp_frame,
            text="",
            text_color="#10B981",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.lbl_copied.grid(row=1, column=0, columnspan=2, padx=16, pady=(0, 6), sticky="w")

        ctrl_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=16, pady=6)
        ctrl_frame.grid_columnconfigure((0, 1), weight=1)

        if self.mode == "passphrase":
            self.lbl_words = ctk.CTkLabel(
                ctrl_frame,
                text=f"{t('pass_word_count', self.lang)} 4",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            self.lbl_words.grid(row=0, column=0, padx=6, pady=(6, 0), sticky="w")

            self.slider_words = ctk.CTkSlider(
                ctrl_frame,
                from_=2,
                to=6,
                number_of_steps=4,
                button_color="#6366F1",
                command=self.on_words_slider
            )
            self.slider_words.set(4)
            self.slider_words.grid(row=1, column=0, padx=6, pady=(0, 12), sticky="ew")

            ctk.CTkLabel(
                ctrl_frame,
                text=t("pass_separator", self.lang),
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(row=0, column=1, padx=6, pady=(6, 0), sticky="w")

            self.opt_sep = ctk.CTkOptionMenu(
                ctrl_frame,
                values=["-", ".", "_", "#", "@", "[Uzay]"],
                button_color="#6366F1",
                command=lambda val: self.generate()
            )
            self.opt_sep.set("-")
            self.opt_sep.grid(row=1, column=1, padx=6, pady=(0, 12), sticky="w")

            self.switch_num = ctk.CTkSwitch(
                ctrl_frame,
                text=t("pass_inc_numbers", self.lang),
                progress_color="#6366F1",
                command=self.generate
            )
            self.switch_num.select()
            self.switch_num.grid(row=2, column=0, padx=6, pady=6, sticky="w")

            self.switch_sym = ctk.CTkSwitch(
                ctrl_frame,
                text=t("pass_inc_symbols", self.lang),
                progress_color="#6366F1",
                command=self.generate
            )
            self.switch_sym.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        else:
            self.lbl_length = ctk.CTkLabel(
                ctrl_frame,
                text=f"{t('pass_length', self.lang)} 16",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            self.lbl_length.grid(row=0, column=0, padx=6, pady=(6, 0), sticky="w")

            self.slider_length = ctk.CTkSlider(
                ctrl_frame,
                from_=8,
                to=32,
                number_of_steps=24,
                button_color="#6366F1",
                command=self.on_length_slider
            )
            self.slider_length.set(16)
            self.slider_length.grid(row=1, column=0, padx=6, pady=(0, 12), sticky="ew")

            self.switch_upper = ctk.CTkSwitch(
                ctrl_frame,
                text=t("pass_inc_uppercase", self.lang),
                progress_color="#6366F1",
                command=self.generate
            )
            self.switch_upper.select()
            self.switch_upper.grid(row=2, column=0, padx=6, pady=6, sticky="w")

            self.switch_classic_sym = ctk.CTkSwitch(
                ctrl_frame,
                text=t("pass_inc_symbols", self.lang),
                progress_color="#6366F1",
                command=self.generate
            )
            self.switch_classic_sym.select()
            self.switch_classic_sym.grid(row=2, column=1, padx=6, pady=6, sticky="w")

        btn_gen = ctk.CTkButton(
            self.container,
            text=t("pass_btn_generate", self.lang),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44,
            fg_color="#F59E0B",
            hover_color="#D97706",
            corner_radius=10,
            command=self.generate
        )
        btn_gen.pack(fill="x", padx=16, pady=16)

        entropy_frame = ctk.CTkFrame(
            self.container,
            fg_color=("#F8FAFC", "#1E293B"),
            corner_radius=12
        )
        entropy_frame.pack(fill="x", padx=16, pady=(0, 16))

        self.lbl_entropy = ctk.CTkLabel(
            entropy_frame,
            text=t("pass_entropy_label", self.lang),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_entropy.pack(anchor="w", padx=16, pady=(12, 6))

        self.progress_entropy = ctk.CTkProgressBar(entropy_frame, height=12, corner_radius=6)
        self.progress_entropy.pack(fill="x", padx=16, pady=6)

        self.lbl_crack_estimate = ctk.CTkLabel(
            entropy_frame,
            text="",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_crack_estimate.pack(anchor="w", padx=16, pady=(0, 12))

    def on_words_slider(self, val):
        cnt = int(val)
        self.lbl_words.configure(text=f"{t('pass_word_count', self.lang)} {cnt}")
        self.generate()

    def on_length_slider(self, val):
        length = int(val)
        self.lbl_length.configure(text=f"{t('pass_length', self.lang)} {length}")
        self.generate()

    def generate(self):
        if self.mode == "passphrase":
            w_cnt = int(self.slider_words.get())
            sep_val = self.opt_sep.get()
            sep = " " if sep_val == "[Uzay]" else sep_val
            inc_num = bool(self.switch_num.get())
            inc_sym = bool(self.switch_sym.get())

            password = self.generator.generate_passphrase(
                word_count=w_cnt,
                separator=sep,
                include_number=inc_num,
                include_symbol=inc_sym,
                lang=self.lang
            )
            entropy_info = self.generator.calculate_entropy(password, is_passphrase=True)
        else:
            length = int(self.slider_length.get())
            inc_upper = bool(self.switch_upper.get())
            inc_sym = bool(self.switch_classic_sym.get())

            password = self.generator.generate_classic_password(
                length=length,
                use_uppercase=inc_upper,
                use_symbols=inc_sym
            )
            entropy_info = self.generator.calculate_entropy(password, is_passphrase=False)

        self.entry_pass.delete(0, "end")
        self.entry_pass.insert(0, password)
        self.lbl_copied.configure(text="")

        status = entropy_info["status"]
        crack_time = entropy_info["crack_time"]

        color_map = {
            "very_weak": ("#F43F5E", 0.15, t("pass_entropy_very_weak", self.lang)),
            "weak": ("#F59E0B", 0.35, t("pass_entropy_weak", self.lang)),
            "good": ("#38BDF8", 0.65, t("pass_entropy_good", self.lang)),
            "strong": ("#10B981", 0.85, t("pass_entropy_strong", self.lang)),
            "ultra": ("#A855F7", 1.0, t("pass_entropy_ultra", self.lang))
        }

        color, progress, desc = color_map.get(status, ("#10B981", 0.8, ""))
        self.progress_entropy.configure(progress_color=color)
        self.progress_entropy.set(progress)
        self.lbl_crack_estimate.configure(
            text=f"{desc}  ({crack_time})",
            text_color=color
        )

    def copy_to_clipboard(self):
        pwd = self.entry_pass.get()
        if pwd:
            self.clipboard_clear()
            self.clipboard_append(pwd)
            self.lbl_copied.configure(text=t("pass_copied_toast", self.lang))
