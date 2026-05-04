import asyncio
import aiohttp
import ssl
import socket
from .tls import TLSBypass
from .challenge import ChallengeBypass
from .fingerprint import FingerprintSpoofer

class TrastClient:
    def __init__(self):
        self.tls = TLSBypass()
        self.challenge = ChallengeBypass()
        self.spoofer = FingerprintSpoofer()
        self.session = None
    
    async def get(self, url, proxy=None):
        headers = self.spoofer.get_headers()
        conn = aiohttp.TCPConnector(
            ssl=self.tls.create_ssl_context(),
            family=socket.AF_INET,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(connector=conn, timeout=timeout, headers=headers)
        
        try:
            async with self.session.get(url, proxy=proxy) as resp:
                text = await resp.text()
                
                if "cf_challenge" in text or "challenge-platform" in text:
                    return await self.challenge.solve(text, url)
                
                return text
        except Exception as e:
            return f"Error: {e}"
        finally:
            await self.session.close()
    
    async def post(self, url, data=None, proxy=None):
        headers = self.spoofer.get_headers()
        conn = aiohttp.TCPConnector(ssl=self.tls.create_ssl_context())
        self.session = aiohttp.ClientSession(connector=conn, headers=headers)
        
        async with self.session.post(url, json=data, proxy=proxy) as resp:
            return await resp.text()
    
    async def close(self):
        if self.session:
            await self.session.close()
