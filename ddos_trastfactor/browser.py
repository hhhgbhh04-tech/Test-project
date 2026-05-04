import random
import time
import hashlib
from .extensions import ExtensionManager
from .plugins import PluginManager
from .cache import CacheEmulator

class BrowserEmulator:
    def __init__(self):
        self.name = random.choice(["Chrome", "Firefox", "Edge", "Safari"])
        self.version = self._get_version()
        self.extensions = ExtensionManager()
        self.plugins = PluginManager()
        self.cache = CacheEmulator()
        self.start_time = time.time()
        self.tabs = []
        self.active_tab = 0
        self.downloads = []
        self.bookmarks = []
        self._init_fake_bookmarks()
    
    def _get_version(self):
        versions = {
            "Chrome": ["120", "119", "118", "121", "122", "123"],
            "Firefox": ["121", "120", "119", "122", "123"],
            "Edge": ["120", "119", "121", "122"],
            "Safari": ["17.0", "16.5", "17.1", "17.2", "18.0"]
        }
        return random.choice(versions.get(self.name, ["120"]))
    
    def _init_fake_bookmarks(self):
        fake_sites = [
            "https://google.com", "https://youtube.com", "https://github.com",
            "https://reddit.com", "https://twitter.com", "https://facebook.com"
        ]
        self.bookmarks = random.sample(fake_sites, random.randint(3, 6))
    
    def new_tab(self, url=None):
        tab = {
            "id": len(self.tabs),
            "url": url,
            "created": time.time(),
            "history": [],
            "scroll_position": random.randint(0, 5000)
        }
        self.tabs.append(tab)
        self.active_tab = len(self.tabs) - 1
        return tab
    
    def close_tab(self, tab_id):
        if 0 <= tab_id < len(self.tabs):
            closed = self.tabs.pop(tab_id)
            if self.active_tab >= len(self.tabs):
                self.active_tab = len(self.tabs) - 1
            return closed
        return None
    
    def switch_tab(self, tab_id):
        if 0 <= tab_id < len(self.tabs):
            self.active_tab = tab_id
            return True
        return False
    
    def record_download(self, url, filename):
        self.downloads.append({
            "url": url,
            "filename": filename,
            "time": time.time(),
            "size": random.randint(100000, 10000000)
        })
    
    def get_user_agent(self):
        platforms = {
            "Chrome": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.version}.0.0.0 Safari/537.36",
            "Chrome_Mac": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.version}.0.0.0 Safari/537.36",
            "Chrome_Linux": f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.version}.0.0.0 Safari/537.36",
            "Firefox": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{self.version}.0) Gecko/20100101 Firefox/{self.version}.0",
            "Edge": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.version}.0.0.0 Safari/537.36 Edg/{self.version}.0.0",
            "Safari": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{self.version} Safari/605.1.15"
        }
        os_choice = random.choice(["", "_Mac", "_Linux"]) if self.name == "Chrome" else ""
        key = self.name + os_choice
        return platforms.get(key, platforms["Chrome"])
    
    def get_browser_info(self):
        return {
            "name": self.name,
            "version": self.version,
            "user_agent": self.get_user_agent(),
            "extensions": self.extensions.get_active(),
            "plugins": self.plugins.get_list(),
            "cache_size": self.cache.get_size(),
            "uptime": time.time() - self.start_time,
            "tabs_count": len(self.tabs),
            "bookmarks_count": len(self.bookmarks),
            "downloads_count": len(self.downloads)
        }
    
    def generate_browser_id(self):
        data = f"{self.name}{self.version}{self.start_time}{len(self.tabs)}"
        return hashlib.md5(data.encode()).hexdigest()[:16]
