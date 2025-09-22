import re


def string_is_printable_characters_plus_nontrailingleading_space(string: str) -> bool:
    # there must be no leading or trailing whitespace
    if re.search(r"^\s", string) or re.search(r"\s$", string):
        return False

    return bool(re.fullmatch(r"^[\S ]+$", string))


def string_is_printable_lowercase_ascii_characters(string: str) -> bool:
    return bool(re.fullmatch(r"^[\x21-\x7e]+$", string))


def string_is_printable_lowercase_ascii_characters_or_space(string: str) -> bool:
    return bool(re.fullmatch(r"^[\x20-\x7e]+$", string))
