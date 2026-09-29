# 🛡️ CyberHealth Desktop

🌐 **Languages:** [Kurdî](README.ku.md) | [Türkçe](README.tr.md) | [English](README.en.md)

> **End-User Digital Security & Health Assistant**  
> Cybersecurity is no longer about complex jargon and boring gray screens! CyberHealth Desktop is a modern, vibrant, user-friendly, and 100% privacy-focused desktop application designed to protect end-users in their daily digital life.

---

## 🔒 Privacy Guarantee (Data Storage Policy)

> **Question: Does CyberHealth store my personal data or email addresses on servers?**  
> **Answer: ABSOLUTELY NOT.**  
> - **100% Offline-First:** All heuristic link analysis, password generation, and security guidance execute locally on your machine.
> - **Privacy-Shielded Email Check:** Your email address is never transmitted raw. Only the first 5 characters of its SHA-1 hash are queried using the K-Anonymity model.
> - **Local History Only:** Scan history is stored strictly on your local device and can be permanently cleared with a single click in *Settings > Clear History*.

---

## 🌟 Key Features

- **🎨 Modern & Vibrant Design:** Designed with curated color palettes in CustomTkinter instead of outdated gray interfaces.
- **🔗 "Is This Link Safe?" (Phishing & Typosquatting Analysis):**
  - Impersonated domain detection (catches typosquatting like *gogole.com*, *netfIix.com*, *paypaI.com*).
  - Suspicious indicator analysis (@ symbol deception, raw IP host, unencrypted HTTP, high-risk TLDs).
  - **Optional Cloud Power:** Enhance link verification using 90+ cloud engines by adding your free VirusTotal API key.
- **✉️ Email Breach Checker:**
  - Queries compromised data repositories using K-Anonymity privacy protection.
  - Provides a 4-step action plan for breached accounts.
- **🔑 Memorable & Secure Password Generator:**
  - Generates easy-to-remember **Passphrases** (*E.g. Dragon-Storm-Forest-42*) instead of unreadable random strings.
  - Calculates Bit Entropy and estimated crack duration.
- **🌐 Multi-Language & Theme Support:**
  - Integrated **Kurdish** as the primary default language alongside Turkish and English. Instant live switching between languages and Dark/Light themes.

---

## 🚀 Execution Instructions

### 1. Direct Python Launch

```bash
pip install -r requirements.txt
python main.py
```

### 2. Building Executable Bundle

```bash
python build.py
```

The compiled output will be generated inside the `dist/CyberHealthDesktop` directory.

---

## 🛠️ Technology Stack

- **Language:** Python 3.10+
- **User Interface:** CustomTkinter
- **Data & Networking:** urllib, re, requests, hashlib, secrets

---

## 📝 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.
