import re

from pathvalidate import is_valid_filename, Platform

from package_validation.top_level_keys import string_is_valid_url
from package_validation.strings import (
    string_is_printable_characters_plus_nontrailingleading_space,
    string_is_printable_lowercase_ascii_characters,
    string_is_printable_lowercase_ascii_characters_or_space,
)

# ref https://github.com/Quaddicted/quaddicted-data/wiki/Tags


def explode_tag(tag: str) -> tuple[str, list[str], str]:
    """Splits a tag string to its key, key qualifiers and its value.

    The key part is exploded into the key and optional qualifiers, delimited by ":".

    If the tag is malformed, a ValueError is raised.

    >>> explode_tag("foo=bar")
    ("foo", [], "bar")
    >>> explode_tag("foo:bar=baz")
    ("foo", ["bar"], "baz")
    >>> explode_tag("foo:bar=baz=qux")
    ("foo", ["bar"], "baz=qux")
    >>> explode_tag("foo")
    ValueError
    """
    # foo, =foo or foo= are malformed tags. foo=bar= would be ok.
    if "=" not in tag or tag.startswith("=") or (tag.count("=") == 1 and tag.endswith("=")):
        raise ValueError("Tag must contain key and value, separated by a '='.")

    separator_index = tag.index("=")  # the left-most "="
    key_string, value = tag[:separator_index], tag[separator_index + 1 :]

    key_parts = key_string.split(":")
    key = key_parts[0]
    qualifiers = key_parts[1:]

    return key, qualifiers, value


# Keys and qualifiers
def string_is_valid_key(string: str) -> bool:
    """A key (opt. with qualifiers) must start with a-z, may contain any of a-z, 0-9, _, : and must not end with a :"""
    # Catch *trailing* ":" in the string. Adding a [^:]* in the regex did not...
    if string.endswith(":"):
        return False

    return bool(re.fullmatch(r"^[a-z]+[a-z0-9_:]*$", string))


def string_is_valid_key_without_qualifiers(string: str) -> bool:
    return bool(re.fullmatch(r"^[a-z]+[a-z0-9_]*$", string))


def string_is_valid_qualifier(string: str) -> bool:
    # same as key for now, except no ":" is allowed
    return bool(re.fullmatch(r"^[a-z]+[a-z0-9_]*$", string))


# Main tags
def string_is_valid_author(string: str) -> bool:
    return string_is_printable_characters_plus_nontrailingleading_space(string)


def string_is_valid_filename(string: str) -> bool:
    # A filename is valid if it is valid on ANY reasonable operating system
    # Yeah, probably not a good idea. You are invited to make a reasonable suggestion for a better approach!
    if string in (".", ".."):
        # for some reason pathvalidate does not consider those invalid...
        # https://github.com/thombashi/pathvalidate/issues/19
        return False
    return any(
        (
            is_valid_filename(string, platform=Platform.LINUX),
            is_valid_filename(string, platform=Platform.MACOS),
            is_valid_filename(string, platform=Platform.POSIX),
            is_valid_filename(string, platform=Platform.WINDOWS),
        )
    )


def string_is_valid_game(string: str) -> bool:
    return string_is_printable_lowercase_ascii_characters(string)


def string_is_valid_game_mode(string: str) -> bool:
    return string_is_printable_lowercase_ascii_characters(string)


def string_is_valid_release_date(string: str) -> bool:
    return any(
        (
            re.match(r"^\d{4}$", string),  # YYYY
            re.match(r"^\d{4}-\d{2}$", string),  # YYYY-MM
            re.match(r"^\d{4}-\d{2}-\d{2}$", string),  # YYYY-MM-DD
        )
    )


def string_is_valid_title(string: str) -> bool:
    return string_is_printable_characters_plus_nontrailingleading_space(string)


def string_is_valid_type(string: str) -> bool:
    return string_is_printable_lowercase_ascii_characters(string)


# Other tags
def string_is_valid_commandline(string: str) -> bool:
    # better safe than sorry, this is quite restrictive for now
    # we should not allow special characters like ;, &, <>, | etc. or bad things might happen in some shells
    return bool(re.fullmatch(r"^[a-zA-Z0-9 ._+-/]+$", string))


def string_is_valid_link(string: str) -> bool:
    # links can use markdown syntax to specify a title...
    match = re.fullmatch(r"^\[(.*)\]\((.*)\)$", string)
    if match:
        title = match.group(1)
        url = match.group(2)
    else:
        title = None
        url = string

    if title:
        if not string_is_printable_characters_plus_nontrailingleading_space(title):
            return False

    if not string_is_valid_url(url):
        return False

    return True


def string_is_valid_startmap(string: str) -> bool:
    # I guess this is a decent start, but surely it could be more restrictive than this?
    return string_is_printable_lowercase_ascii_characters(string)


def string_is_valid_theme(string: str) -> bool:
    return string_is_printable_lowercase_ascii_characters_or_space(string)
    # TODO nope, ö too... how to allow any umlauts and accents?


# TODOs:
"""
"depends",
"provides",
"release_group",
"version",
"dependency",
"current_main_group_package",
"patch",
"nuked",
"zipbasedir",
"exceeds_quake_limits",
"exceedslimits",
"source",
"bsp_format",
"style",
"playstyle",
"map_size",
"map_layout",
"size",
"mod",
"music",
"nonspecific_tag",
"""
