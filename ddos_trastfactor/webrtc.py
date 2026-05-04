import random
class WebRTCSpoofer:
    def get_ip(self):
        return f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
