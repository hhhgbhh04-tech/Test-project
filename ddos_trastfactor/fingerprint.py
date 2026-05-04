import random
import hashlib
import time

class FingerprintSpoofer:
    def __init__(self):
        self.fake_id = hashlib.md5(str(random.random()).encode()).hexdigest()
    
    def get_headers(self):
        browsers = [
            ("Chrome", "120", "Windows NT 10.0; Win64; x64"),
            ("Edge", "119", "Windows NT 10.0; Win64; x64"),
            ("Firefox", "121", "Windows NT 10.0; Win64; x64; rv:109.0"),
            ("Safari", "605.1.15", "Macintosh; Intel Mac OS X 14_0"),
        ]
        
        browser, version, platform = random.choice(browsers)
        
        if browser == "Safari":
            ua = f"Mozilla/5.0 ({platform}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        elif browser == "Firefox":
            ua = f"Mozilla/5.0 ({platform}) Gecko/20100101 Firefox/{version}.0"
        else:
            ua = f"Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/{version}.0.0.0 Safari/537.36"
        
        return {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "ru-RU,ru;q=0.8", "de-DE,de;q=0.7", "fr-FR,fr;q=0.9"]),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Ch-Ua": f'"Not_A Brand";v="8", "{browser}";v="{version}"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": f'"{platform.split(";")[0]}"',
            "Cache-Control": "max-age=0",
            "DNT": random.choice(["0", "1"]),
        }
    
    def get_canvas_fingerprint(self):
        return {
            "winding": True,
            "data": hashlib.sha256(str(random.random()).encode()).hexdigest(),
        }
    
    def get_webgl_fingerprint(self):
        vendors = ["Intel Inc.", "NVIDIA Corporation", "AMD", "Apple", "Google Inc."]
        renderers = ["ANGLE", "Metal", "OpenGL", "DirectX"]
        return {
            "vendor": random.choice(vendors),
            "renderer": random.choice(renderers),
            "version": f"{random.randint(1,5)}.{random.randint(0,9)}",
        }
    
    def get_audio_fingerprint(self):
        return hashlib.md5(str(random.random()).encode()).hexdigest()
    
    def get_webrtc_ip(self):
        return f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
    
    def get_font_fingerprint(self):
        fonts = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Calibri"]
        random.shuffle(fonts)
        return fonts[:random.randint(3, 6)]
    
    def get_media_devices(self):
        return {
            "videoinput": random.choice(["FaceTime HD Camera", "HD Webcam", "Integrated Camera"]),
            "audioinput": random.choice(["Built-in Microphone", "External Mic", "USB Audio Device"]),
        }
    
    def get_full_fingerprint(self):
        return {
            "id": self.fake_id,
            "canvas": self.get_canvas_fingerprint(),
            "webgl": self.get_webgl_fingerprint(),
            "audio": self.get_audio_fingerprint(),
            "fonts": self.get_font_fingerprint(),
            "webrtc_ip": self.get_webrtc_ip(),
            "media": self.get_media_devices(),
            "timezone_offset": random.randint(-720, 720),
            "language": random.choice(["en-US", "ru-RU", "de-DE", "fr-FR", "ja-JP"]),
            "platform": random.choice(["Win32", "MacIntel", "Linux x86_64", "iPhone", "Android"]),
            "hardware_cores": random.choice([2, 4, 6, 8, 10, 12, 16]),
            "device_memory": random.choice([2, 4, 8, 16, 32]),
            "touch_support": random.choice([0, 1]),
            "adblock": random.choice([0, 1]),
        }
