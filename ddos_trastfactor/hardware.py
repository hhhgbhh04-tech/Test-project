import random
class HardwareSpoofer:
    def get_cores(self):
        return random.choice([2, 4, 6, 8, 12, 16])
    def get_memory(self):
        return random.choice([4, 8, 16, 32, 64])
