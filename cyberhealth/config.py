import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".cyberhealth"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "virustotal_api_key": "",
    "language": "ku",
    "theme": "Dark",
    "auto_check_vt": True,
    "url_history": [],
    "email_history": []
}

class ConfigManager:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        try:
            if not self.config_dir.exists():
                self.config_dir.mkdir(parents=True, exist_ok=True)
            
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, val in DEFAULT_CONFIG.items():
                        self.config[key] = data.get(key, val)
            else:
                self.save_config()
        except Exception:
            self.config = DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            if not self.config_dir.exists():
                self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def add_url_history(self, url: str, status: str, score: int):
        history = self.config.get("url_history", [])
        entry = {"url": url, "status": status, "score": score}
        history.insert(0, entry)
        self.config["url_history"] = history[:20]
        self.save_config()

    def add_email_history(self, email: str, is_breached: bool, breach_count: int):
        history = self.config.get("email_history", [])
        entry = {"email": email, "is_breached": is_breached, "breach_count": breach_count}
        history.insert(0, entry)
        self.config["email_history"] = history[:20]
        self.save_config()

    def clear_history(self):
        self.config["url_history"] = []
        self.config["email_history"] = []
        self.save_config()

config_manager = ConfigManager()
