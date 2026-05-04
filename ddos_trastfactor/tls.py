import ssl
import random

class TLSFingerprint:
    def create_ssl_context(self):
        context = ssl.create_default_context()
        ciphers = [
            'ECDHE-ECDSA-AES128-GCM-SHA256',
            'ECDHE-RSA-AES128-GCM-SHA256',
            'ECDHE-ECDSA-AES256-GCM-SHA384',
            'ECDHE-RSA-AES256-GCM-SHA384',
            'ECDHE-ECDSA-CHACHA20-POLY1305',
            'ECDHE-RSA-CHACHA20-POLY1305'
        ]
        random.shuffle(ciphers)
        context.set_ciphers(':'.join(ciphers))
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
