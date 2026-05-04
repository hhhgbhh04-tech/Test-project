import random
import time
from urllib.parse import urlparse

class HeaderBuilder:
    def __init__(self):
        self.referer_cache = []
    
    def build(self, fingerprint, browser):
        ua = browser.get_user_agent()
        platform = fingerprint.get_navigator_properties()["platform"]
        
        sec_ch_ua = f'"Chromium";v="{random.randint(100, 123)}", "Google Chrome";v="{random.randint(100, 123)}"'
        if "Firefox" in ua:
            sec_ch_ua = f'"Firefox";v="{random.randint(100, 123)}"'
        elif "Edg" in ua:
            sec_ch_ua = f'"Chromium";v="{random.randint(100, 123)}", "Microsoft Edge";v="{random.randint(100, 123)}"'
        
        accept_langs = [
            "en-US,en;q=0.9", "ru-RU,ru;q=0.8,en-US;q=0.5", 
            "de-DE,de;q=0.9,en-US;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8",
            "ja-JP,ja;q=0.9,en-US;q=0.8", "zh-CN,zh;q=0.9,en;q=0.8"
        ]
        
        referer = self._get_referer()
        
        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": random.choice(accept_langs),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "DNT": random.choice(["0", "1"]),
            "Sec-GPC": random.choice(["0", "1"]),
            "Sec-Ch-Ua": sec_ch_ua,
            "Sec-Ch-Ua-Mobile": "?0" if "Android" not in platform and "iPhone" not in platform else "?1",
            "Sec-Ch-Ua-Platform": f'"{platform.split()[0] if " " in platform else platform}"',
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            "Client-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            "X-Requested-With": random.choice(["XMLHttpRequest", ""]),
            "Priority": random.choice(["u=0, i", "u=1", "u=2"]),
            "Referer": referer,
            "Origin": self._extract_origin(referer) if referer else "null",
            "Save-Data": random.choice(["on", "off"])
        }
        
        if self._should_add_push():
            headers["Accept-Push-Policy"] = random.choice(["load", "manual"])
        
        if random.random() > 0.7:
            headers["If-None-Match"] = f'W/"{hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}"'
        
        return headers
    
    def _get_referer(self):
        referers = [
            "https://google.com", "https://yandex.ru", "https://bing.com", 
            "https://duckduckgo.com", "https://yahoo.com", "https://facebook.com",
            "https://twitter.com", "https://reddit.com", "https://youtube.com",
            "https://wikipedia.org", "https://amazon.com", "https://github.com",
            ""
        ]
        
        if self.referer_cache and random.random() > 0.3:
            return random.choice(self.referer_cache)
        
        ref = random.choice(referers)
        if ref:
            self.referer_cache.append(ref)
            if len(self.referer_cache) > 10:
                self.referer_cache.pop(0)
        return ref
    
    def _extract_origin(self, url):
        if not url:
            return "null"
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _should_add_push(self):
        return random.random() > 0.85
    
    def rotate(self, fingerprint, browser):
        return self.build(fingerprint, browser)
