import hmac
import hashlib
import binascii
from urllib.parse import urlencode

from dataclasses import dataclass

from application.keys.base import Key


@dataclass
class ClientKey(Key):
    token: str
    secret: str

    def header(self):
        return {
            'X-MBX-APIKEY': self.token
        }

    def get_signature(self, params: dict):
        return hmac.new(
            self.secret.encode(),
            urlencode(params, doseq=False).encode(),
            hashlib.sha256
        ).hexdigest()

