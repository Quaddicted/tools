import logging

import package_validation.tags

from package_validation.strings import string_is_printable_characters_plus_nontrailingleading_space
from package_validation.tags import (
    explode_tag,
    string_is_valid_qualifier,
    string_is_valid_key_without_qualifiers,
)


class Tag:
    def __init__(self, string: str) -> None:
        # some most basic checks to weed out strings that are definitely not valid tags
        if not "=" in string:
            raise ValueError("Tag does not contain a '='.")
        if len(string) < 3:
            raise ValueError("Tag cannot be shorter than 3 characters ('k=v').")

        key, qualifiers, value = explode_tag(string)

        # some quick checks on general validity of key, qualifiers and value
        if not string_is_valid_key_without_qualifiers(key):
            raise ValueError("Tag does not contain a valid key.")
        for qualifier in qualifiers:
            if not string_is_valid_qualifier(qualifier):
                raise ValueError("Tag key contains an invalid qualifier.")
        if not string_is_printable_characters_plus_nontrailingleading_space(value):
            raise ValueError("Tag value contains disallowed characters.")

        # all looks good, let's set up the object
        self.key = key
        self.qualifiers = qualifiers
        self.value = value

    def has_valid_value(self) -> bool:
        # Note: Validation for tag values does not consider any key qualifiers yet
        validate_value_for_key = getattr(package_validation.tags, f"string_is_valid_{self.key}", None)
        if not validate_value_for_key:
            logging.warning(f"No validation function found for tag key {self.key!r}, considering '{self}' to be valid!")
        else:
            if validate_value_for_key(self.value) is False:
                return False

        return True

    def __str__(self):
        return f"{self.key}{':'.join(self.qualifiers) if self.qualifiers else ''}={self.value}"

    def __repr__(self):
        return f"Tag({str(self)})"
