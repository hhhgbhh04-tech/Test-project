import random
class PluginManager:
    def get_list(self):
        plugins = [
            "Chrome PDF Plugin", "Chrome PDF Viewer", "Native Client",
            "Shockwave Flash", "Widevine Content Decryption Module",
            "Chrome Remote Desktop Viewer", "QuickTime Plugin"
        ]
        return random.sample(plugins, random.randint(0, 3))
