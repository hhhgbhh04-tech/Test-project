import hashlib
import random
class CanvasSpoofer:
    def get_hash(self):
        return hashlib.sha256(str(random.random()).encode()).hexdigest()
