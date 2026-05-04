import random
class ExtensionManager:
    def get_active(self):
        extensions = [
            "AdBlock", "Tampermonkey", "Grammarly", "LastPass", "Honey",
            "uBlock Origin", "Dark Reader", "Privacy Badger", "Ghostery",
            "HTTPS Everywhere", "NoScript", "Dashlane", "Bitwarden"
        ]
        return random.sample(extensions, random.randint(0, 5))
