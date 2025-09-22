import re

from pathlib import Path


def extract_sha256_from_path(path: str | Path) -> str:
    # path should end in ...(sha256).json
    path = Path(path)

    if path.suffix != ".json":
        raise ValueError("Path does not end with '.json'.")

    sha256 = path.stem
    if not string_is_valid_sha256(sha256):
        raise ValueError("Does not look like a SHA256.")

    return sha256


def string_is_valid_sha256(string: str) -> bool:
    return bool(re.match(r"^[a-z0-9]{64}$", string))
