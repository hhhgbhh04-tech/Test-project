import asyncio
import aiohttp
import random
import time
import json
from urllib.parse import urlparse
from .browser import BrowserEmulator
from .fingerprint import FingerprintGenerator
from .headers import HeaderBuilder
from .cookies import CookieManager
from .storage import LocalStorage
from .history import BrowserHistory
from .trust import TrustFactor
from .captcha import CaptchaSolver
from .tls import TLSFingerprint
from .behavior import BehaviorSimulator

class TrastClient:
    def __init__(self, trust_level="high", proxy=None):
        self.browser = BrowserEmulator()
        self.fingerprint = FingerprintGenerator()
        self.headers = HeaderBuilder()
        self.cookies = CookieManager()
        self.storage = LocalStorage()
        self.history = BrowserHistory()
        self.trust = TrustFactor(level=trust_level)
        self.captcha = CaptchaSolver()
        self.tls = TLSFingerprint()
        self.behavior = BehaviorSimulator()
        self.proxy = proxy
        self.session = None
        self.request_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.start_time = time.time()
    
    async def _create_session(self):
        connector = aiohttp.TCPConnector(
            ssl=self.tls.create_ssl_context(),
            limit=100,
            limit_per_host=10,
            enable_cleanup_closed=True
        )
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers.build(self.fingerprint, self.browser)
        )
    
    async def get(self, url, retry=3):
        self.request_count += 1
        start_time = time.time()
        await self.behavior.before_request()
        
        headers = self.headers.build(self.fingerprint, self.browser)
        cookies = self.cookies.get_for_domain(url)
        trust_score = self.trust.get_score()
        headers["X-Trust-Score"] = str(trust_score)
        
        for attempt in range(retry):
            try:
                if not self.session or self.session.closed:
                    await self._create_session()
                
                async with self.session.get(url, headers=headers, cookies=cookies, proxy=self.proxy) as resp:
                    content = await resp.text()
                    self.success_count += 1
                    self.history.add(url, resp.status, time.time() - start_time)
                    self.cookies.update_from_response(resp)
                    self.trust.record_request(resp.status)
                    
                    if self.captcha.detect(content):
                        content = await self.captcha.solve(content, url)
                    
                    await self.behavior.after_request(time.time() - start_time)
                    return content
                    
            except Exception as e:
                self.fail_count += 1
                if attempt == retry - 1:
                    return f"ERROR: {str(e)}"
        
        return "ERROR: Max retries exceeded"
    
    async def post(self, url, data=None, retry=3):
        self.request_count += 1
        await self.behavior.before_request()
        
        headers = self.headers.build(self.fingerprint, self.browser)
        cookies = self.cookies.get_for_domain(url)
        headers["X-Trust-Score"] = str(self.trust.get_score())
        
        for attempt in range(retry):
            try:
                if not self.session or self.session.closed:
                    await self._create_session()
                
                async with self.session.post(url, json=data, headers=headers, cookies=cookies, proxy=self.proxy) as resp:
                    content = await resp.text()
                    self.success_count += 1
                    self.history.add(url, resp.status)
                    self.cookies.update_from_response(resp)
                    self.trust.record_request(resp.status)
                    
                    if self.captcha.detect(content):
                        content = await self.captcha.solve(content, url)
                    
                    return content
                    
            except Exception as e:
                self.fail_count += 1
                if attempt == retry - 1:
                    return f"ERROR: {str(e)}"
        
        return "ERROR: Max retries exceeded"
    
    def get_stats(self):
        return {
            "requests": self.request_count,
            "success": self.success_count,
            "fail": self.fail_count,
            "trust_score": self.trust.get_score(),
            "uptime": time.time() - self.start_time
        }
    
    async def close(self):
        if self.session:
            await self.session.close()
