import string
import random

ALPHABET = string.ascii_letters + string.digits
_db: dict[str, str] = {}


def generate_code(length: int = 7) -> str:
    """Returns a random base62 for a given length"""
    for _ in range(10):
        code = "".join(random.choices(ALPHABET, k=length))
        if code not in _db:
            return code
    raise RuntimeError("Could not generate a unique code , try on longer length")


def save(code: str, original_url: str) -> None:
    _db[code] = original_url
