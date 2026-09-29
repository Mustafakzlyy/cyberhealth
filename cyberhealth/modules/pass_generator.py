import math
import secrets
import string
from typing import Dict, Any, List

KURDISH_WORDS = [
    "roşên", "ejdeha", "bahoz", "hêlîn", "pêlîvan", "qehwe", "rûbar", "stêrk",
    "daristan", "derya", "ewr", "şêr", "helq", "şahîn", "delfîn", "dar",
    "berû", "zêtûn", "çinar", "êvar", "beyanî", "şev", "bihar", "keskesor",
    "yaqût", "safîr", "zümrüt", "almas", "pûsula", "fener", "qeyik", "kaptan",
    "destan", "efsane", "çîrok", "helbest", "awaz", "rîtim", "stran", "deng",
    "ronahî", "sêwî", "agir", "volkan", "gopît", "gelî", "kanyon", "şefeq", "hêvroş"
]

TURKISH_WORDS = [
    "güneş", "ejderha", "fırtına", "pusula", "kelebek", "kaplan", "samanyolu", "kahve",
    "nehir", "rüzgar", "yıldız", "orman", "deniz", "bulut", "şelale", "çağlayan",
    "aslan", "kartal", "martı", "yunus", "çam", "meşe", "zeytin", "çınar",
    "akşam", "sabah", "gece", "bahar", "gökkuşağı", "yakut", "safir", "zümrüt",
    "elmas", "kehribar", "pusula", "fener", "yelken", "kaptan", "destan", "efsane",
    "masal", "şiir", "beste", "melodi", "ritim", "harmoni", "yankı", "ışık",
    "gölge", "alev", "volkan", "zirve", "vadi", "kanyon", "şafak", "mehtap"
]

ENGLISH_WORDS = [
    "dragon", "storm", "compass", "butterfly", "tiger", "galaxy", "coffee", "river",
    "breeze", "star", "forest", "ocean", "cloud", "waterfall", "eagle", "dolphin",
    "pine", "oak", "olive", "sunset", "sunrise", "spring", "rainbow", "ruby",
    "sapphire", "emerald", "diamond", "amber", "beacon", "sail", "captain", "legend",
    "rhythm", "harmony", "echo", "light", "shadow", "flame", "volcano", "summit",
    "canyon", "dawn", "moonlight", "thunder", "comet", "meteor", "crystal", "prism"
]

class PasswordGenerator:
    def __init__(self):
        self.ku_words = KURDISH_WORDS
        self.tr_words = TURKISH_WORDS
        self.en_words = ENGLISH_WORDS

    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        capitalize: bool = True,
        include_number: bool = True,
        include_symbol: bool = False,
        lang: str = "ku"
    ) -> str:
        if lang == "ku":
            words_pool = self.ku_words
        elif lang == "tr":
            words_pool = self.tr_words
        else:
            words_pool = self.en_words

        selected_words = [secrets.choice(words_pool) for _ in range(word_count)]

        if capitalize:
            selected_words = [w.capitalize() for w in selected_words]
        else:
            selected_words = [w.lower() for w in selected_words]

        passphrase = separator.join(selected_words)

        if include_number:
            num = secrets.randbelow(90) + 10
            passphrase += f"{separator}{num}"

        if include_symbol:
            sym = secrets.choice(["!", "@", "#", "$", "%", "*", "?"])
            passphrase += sym

        return passphrase

    def generate_classic_password(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        chars = ""
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if exclude_ambiguous:
            for amb in ["l", "1", "I", "O", "0"]:
                chars = chars.replace(amb, "")

        if not chars:
            chars = string.ascii_letters + string.digits

        return "".join(secrets.choice(chars) for _ in range(length))

    def calculate_entropy(self, password: str, is_passphrase: bool = False) -> Dict[str, Any]:
        if not password:
            return {"entropy": 0, "status": "very_weak", "crack_time": "Instant"}

        length = len(password)

        if is_passphrase:
            entropy = length * 2.5
        else:
            pool_size = 0
            if any(c in string.ascii_lowercase for c in password):
                pool_size += 26
            if any(c in string.ascii_uppercase for c in password):
                pool_size += 26
            if any(c in string.digits for c in password):
                pool_size += 10
            if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                pool_size += 32

            if pool_size == 0:
                pool_size = 26

            entropy = length * math.log2(pool_size)

        entropy = round(entropy, 1)

        if entropy < 30:
            status = "very_weak"
            crack_time = "< 1 Saniye"
        elif entropy < 50:
            status = "weak"
            crack_time = "~ Birkaç Dakika"
        elif entropy < 70:
            status = "good"
            crack_time = "~ Birkaç Yıl"
        elif entropy < 90:
            status = "strong"
            crack_time = "~ Yüzyıllarca"
        else:
            status = "ultra"
            crack_time = "~ Evrenin Ömrü Kadar!"

        return {
            "entropy": entropy,
            "status": status,
            "crack_time": crack_time
        }
