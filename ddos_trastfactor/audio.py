import hashlib
import random
class AudioSpoofer:
    def get_hash(self):
        return hashlib.md5(str(random.random()).encode()).hexdigest()
