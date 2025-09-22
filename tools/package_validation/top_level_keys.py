import urllib.parse

from typing import Any


def string_is_valid_url(string: str) -> bool:
    """
    Returns True if the string parses to a URL with at least scheme and 'netloc'.

    >>> string_is_valid_url("https://www.quaddicted.com")  # <3
    True
    >>> string_is_valid_url("xyz://www.quaddicated.null")  # scheme and netloc are not validated in any way
    True
    >>> string_is_valid_url("https://www.example.com/foo bar!§$%&/()=?`")
    True
    >>> string_is_valid_url("https:/www.quaddicted.com")  # only one slash
    False
    >>> string_is_valid_url("foo")
    False
    """
    parsed_url = urllib.parse.urlparse(string)
    return bool(parsed_url.scheme and parsed_url.netloc)


def value_is_valid_bytes(value: Any) -> bool:
    try:
        int_value = int(value)
    except ValueError:
        return False

    if int_value < 1:
        return False

    return True
