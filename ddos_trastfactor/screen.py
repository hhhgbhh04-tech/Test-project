import random
class ScreenSpoofer:
    def get_resolution(self):
        return f"{random.choice([1920, 1366, 1536, 2560, 3440])}x{random.choice([1080, 768, 864, 1440, 1600])}"
