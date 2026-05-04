import random
class WebGLSpoofer:
    def get_vendor(self):
        return random.choice(["Intel", "NVIDIA", "AMD", "Apple"])
