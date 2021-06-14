from dataclasses import dataclass

from application.keys.base import Key


@dataclass
class Bearer(Key):
    token: str

    def header(self):
        return {
            'Authorization': f'Bearer {self.token}'
        }
