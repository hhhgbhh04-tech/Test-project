import json
import time
import random
import hashlib
from urllib.parse import urlparse

class CookieManager:
    def __init__(self, filepath="cookies.json"):
        self.filepath = filepath
        self.cookies = self._load()
        self.session_cookies = {}
        self.created = time.time()
    
    def _load(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.cookies, f, indent=2)
    
    def get_for_domain(self, url):
        domain = urlparse(url).netloc
        result = {}
        for d, cookies in self.cookies.items():
            if d in domain or domain in d or self._domain_match(d, domain):
                for name, data in cookies.items():
                    if data.get("expires", time.time() + 3600) > time.time():
                        result[name] = data["value"]
        for name, data in self.session_cookies.items():
            result[name] = data["value"]
        return result
    
    def _domain_match(self, cookie_domain, request_domain):
        cookie_parts = cookie_domain.split('.')
        request_parts = request_domain.split('.')
        if len(cookie_parts) > len(request_parts):
            return False
        return cookie_parts == request_parts[-len(cookie_parts):]
    
    def set(self, domain, name, value, expires=None, secure=False, http_only=False):
        if domain not in self.cookies:
            self.cookies[domain] = {}
        self.cookies[domain][name] = {
            "value": value,
            "expires": expires or time.time() + 30*24*3600,
            "created": time.time(),
            "secure": secure,
            "httpOnly": http_only
        }
        self._save()
    
    def set_session(self, name, value, domain=None):
        self.session_cookies[name] = {
            "value": value,
            "domain": domain,
            "created": time.time()
        }
    
    def update_from_response(self, response):
        if "set-cookie" in response.headers:
            cookies = response.headers.getall("set-cookie", [])
            for cookie in cookies:
                self._parse_cookie(cookie, response.url.host)
    
    def _parse_cookie(self, cookie_str, default_domain):
        parts = cookie_str.split(";")
        name_value = parts[0].split("=", 1)
        if len(name_value) != 2:
            return
        name, value = name_value
        domain = default_domain
        expires = None
        secure = False
        http_only = False
        for part in parts[1:]:
            part = part.strip().lower()
            if part.startswith("domain="):
                domain = part[7:]
            elif part.startswith("expires="):
                try:
                    expires = time.mktime(time.strptime(part[8:], "%a, %d-%b-%Y %H:%M:%S %Z"))
                except:
                    pass
            elif part == "secure":
                secure = True
            elif part == "httponly":
                http_only = True
        self.set(domain, name, value, expires, secure, http_only)
    
    def generate_fake(self, domain, count=None):
        if count is None:
            count = random.randint(5, 15)
        fake_cookies = {}
        for i in range(count):
            name = f"__test_{hashlib.md5(str(i).encode()).hexdigest()[:8]}"
            value = hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
            fake_cookies[name] = value
            self.set(domain, name, value)
        return fake_cookies
    
    def generate_analytics_cookies(self, domain):
        analytics = {
            "_ga": f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
            "_gid": f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
            "_ga_{random.randint(100000, 999999)}": f"GS1.1.{int(time.time())}.1.1.{int(time.time())}.0.0.0",
            "_fbp": f"fb.1.{int(time.time())}.{random.randint(1000000000, 9999999999)}",
            "_ttp": f"{hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}.{int(time.time())}",
            "session_id": hashlib.md5(str(random.random()).encode()).hexdigest(),
            "csrf_token": hashlib.sha256(str(random.random()).encode()).hexdigest()[:32],
            "user_session": hashlib.md5(str(random.random()).encode()).hexdigest()[:24]
        }
        for name, value in analytics.items():
            self.set(domain, name, value)
        return analytics
    
    def clear_domain(self, domain):
        if domain in self.cookies:
            del self.cookies[domain]
            self._save()
    
    def clear_all(self):
        self.cookies = {}
        self.session_cookies = {}
        self._save()
    
    def get_all(self):
        all_cookies = {}
        for domain, cookies in self.cookies.items():
            for name, data in cookies.items():
                if data.get("expires", time.time() + 3600) > time.time():
                    all_cookies[f"{domain}:{name}"] = data["value"]
        for name, data in self.session_cookies.items():
            all_cookies[f"session:{name}"] = data["value"]
        return all_cookies
    
    def export(self):
        return {
            "persistent": self.cookies,
            "session": self.session_cookies,
            "created": self.created,
            "total_count": len(self.get_all())
        }
