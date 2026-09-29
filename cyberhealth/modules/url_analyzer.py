import re
import base64
import requests
from urllib.parse import urlparse
from typing import Dict, List, Any, Tuple

POPULAR_BRANDS = [
    "google", "netflix", "paypal", "amazon", "microsoft", "apple",
    "facebook", "instagram", "twitter", "binance", "whatsapp", "spotify",
    "youtube", "steam", "ziraatbank", "garanti", "akbank", "isbank",
    "yapikredi", "enpara", "trendyol", "hepsiburada", "turkiye.gov.tr",
    "papara", "sahibinden", "linkedin", "telegram", "discord", "tiktok",
    "github", "outlook", "gmail", "bankofamerica", "chase", "wellsfargo"
]

HIGH_RISK_TLDS = {
    ".xyz", ".top", ".tk", ".ml", ".cf", ".gq", ".ga", ".click", ".buzz",
    ".work", ".fit", ".rest", ".cam", ".zip", ".mov", ".icu", ".monster",
    ".cfd", ".sbs", ".cyou", ".cc", ".su", ".pw", ".bid"
}

SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "verification", "secure-login", "account-update",
    "banking", "bank", "free-gift", "claim", "bonus", "reward", "password-reset",
    "confirm-details", "security-check", "billing-update", "credential"
]

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def normalize_visually(text: str) -> str:
    replacements = {
        "I": "l", "0": "o", "1": "i", "vv": "w", "rn": "m", "cl": "d",
        "@": "a", "$": "s", "3": "e", "5": "s"
    }
    res = text.lower()
    for src, dst in replacements.items():
        res = res.replace(src, dst)
    return res

class URLAnalyzer:
    def __init__(self, vt_api_key: str = ""):
        self.vt_api_key = vt_api_key.strip()

    def set_api_key(self, api_key: str):
        self.vt_api_key = api_key.strip()

    def check_typosquatting(self, domain: str) -> List[Tuple[str, str]]:
        findings = []
        domain_clean = domain.lower().split(":")[0]
        parts = domain_clean.split(".")
        
        main_part = parts[-2] if len(parts) >= 2 else parts[0]
        normalized_main = normalize_visually(main_part)

        for brand in POPULAR_BRANDS:
            if main_part == brand:
                continue

            dist = levenshtein_distance(normalized_main, brand)
            if 1 <= dist <= 2 and len(main_part) >= 4:
                findings.append(("typosquatting", brand))
                break

            if len(parts) > 2 and brand in domain_clean and not domain_clean.endswith(f".{brand}.com"):
                if main_part != brand:
                    findings.append(("subdomain_brand_impersonation", brand))
                    break
        return findings

    def analyze_heuristics(self, url: str) -> Dict[str, Any]:
        raw_url = url.strip()
        if not raw_url.startswith(("http://", "https://")):
            parsed_url_str = "http://" + raw_url
        else:
            parsed_url_str = raw_url

        try:
            parsed = urlparse(parsed_url_str)
        except Exception:
            return {
                "score": 90,
                "status": "danger",
                "findings": [("invalid_url", "URL format invalid.")],
                "details": []
            }

        hostname = parsed.netloc.split(":")[0].lower()
        path_and_query = (parsed.path + "?" + parsed.query).lower()

        score = 0
        findings = []

        if parsed.scheme == "http":
            score += 15
            findings.append(("no_https", ""))

        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if re.match(ip_pattern, hostname):
            score += 40
            findings.append(("ip_host", hostname))

        if "@" in parsed.netloc:
            score += 45
            findings.append(("at_symbol", ""))

        typos = self.check_typosquatting(hostname)
        for typo_type, brand in typos:
            score += 45
            findings.append((typo_type, brand))

        for tld in HIGH_RISK_TLDS:
            if hostname.endswith(tld):
                score += 25
                findings.append(("suspicious_tld", tld))
                break

        if "xn--" in hostname:
            score += 30
            findings.append(("punycode", ""))

        subdomains = hostname.split(".")
        if len(subdomains) > 3:
            score += 20
            findings.append(("many_subdomains", str(len(subdomains))))

        detected_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in path_and_query]
        if detected_keywords:
            score += 15
            findings.append(("suspicious_keywords", ", ".join(detected_keywords[:3])))

        if ":" in parsed.netloc:
            port = parsed.netloc.split(":")[-1]
            if port not in ("80", "443"):
                score += 15

        score = min(score, 100)

        if score < 20:
            status = "safe"
        elif score < 50:
            status = "caution"
        else:
            status = "danger"

        return {
            "score": score,
            "status": status,
            "findings": findings,
            "hostname": hostname,
            "scheme": parsed.scheme
        }

    def analyze_virustotal(self, url: str) -> Dict[str, Any]:
        if not self.vt_api_key:
            return {"active": False, "error": "No API key"}

        try:
            url_id = base64.urlsafe_b64encode(url.strip().encode()).decode().strip("=")
            endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
            headers = {"x-apikey": self.vt_api_key, "accept": "application/json"}

            response = requests.get(endpoint, headers=headers, timeout=8)
            if response.status_code == 200:
                data = response.json().get("data", {}).get("attributes", {})
                stats = data.get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                harmless = stats.get("harmless", 0)
                undetected = stats.get("undetected", 0)
                total = malicious + suspicious + harmless + undetected

                return {
                    "active": True,
                    "malicious": malicious,
                    "suspicious": suspicious,
                    "harmless": harmless,
                    "total": total,
                    "reputation": data.get("reputation", 0)
                }
            elif response.status_code == 404:
                return {"active": True, "not_scanned": True, "malicious": 0, "total": 0}
            else:
                return {"active": False, "error": f"API HTTP {response.status_code}"}
        except Exception as e:
            return {"active": False, "error": str(e)}

    def analyze(self, url: str) -> Dict[str, Any]:
        result = self.analyze_heuristics(url)
        vt_result = self.analyze_virustotal(url)
        result["vt"] = vt_result

        if vt_result.get("active") and vt_result.get("malicious", 0) > 0:
            vt_malicious = vt_result["malicious"]
            result["score"] = max(result["score"], min(100, 50 + vt_malicious * 10))
            if result["score"] >= 50:
                result["status"] = "danger"

        return result
