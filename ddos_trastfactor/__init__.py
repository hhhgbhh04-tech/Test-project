from .client import TrastClient
from .browser import BrowserEmulator
from .fingerprint import FingerprintGenerator
from .headers import HeaderBuilder
from .cookies import CookieManager
from .storage import LocalStorage
from .history import BrowserHistory
from .extensions import ExtensionManager
from .plugins import PluginManager
from .cache import CacheEmulator
from .webrtc import WebRTCSpoofer
from .canvas import CanvasSpoofer
from .webgl import WebGLSpoofer
from .audio import AudioSpoofer
from .fonts import FontSpoofer
from .timezone import TimezoneSpoofer
from .language import LanguageSpoofer
from .screen import ScreenSpoofer
from .hardware import HardwareSpoofer
from .trust import TrustFactor
from .captcha import CaptchaSolver
from .tls import TLSFingerprint
from .behavior import BehaviorSimulator

__version__ = "7.0.0"
__all__ = [
    "TrastClient", "BrowserEmulator", "FingerprintGenerator",
    "HeaderBuilder", "CookieManager", "LocalStorage", "BrowserHistory",
    "ExtensionManager", "PluginManager", "CacheEmulator", "WebRTCSpoofer",
    "CanvasSpoofer", "WebGLSpoofer", "AudioSpoofer", "FontSpoofer",
    "TimezoneSpoofer", "LanguageSpoofer", "ScreenSpoofer", "HardwareSpoofer",
    "TrustFactor", "CaptchaSolver", "TLSFingerprint", "BehaviorSimulator"
]
