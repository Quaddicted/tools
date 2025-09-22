import json
import logging

from pathlib import Path
from typing import Optional

from package_validation.sha256s import extract_sha256_from_path, string_is_valid_sha256
from classes.tag import Tag
from package_validation.top_level_keys import string_is_valid_url, value_is_valid_bytes


def validate_package(package: dict) -> dict[str, str]:
    package_validation_errors = {}

    # bytes
    if "bytes" not in package.keys():
        package_validation_errors["bytes"] = "Missing 'bytes' value."
    else:
        if not value_is_valid_bytes(package["bytes"]):
            package_validation_errors["bytes"] = "Malformed 'bytes' value."

    # sha256
    if "sha256" not in package.keys():
        package_validation_errors["sha256"] = "Missing 'sha256' value."
    else:
        if not string_is_valid_sha256(package["sha256"]):
            package_validation_errors["sha256"] = "Malformed 'sha256' value."

    # urls
    for url in package.get("urls", []):
        if not string_is_valid_url(url):
            package_validation_errors["url"] = url

    for key in ("description", "files", "install", "notes"):
        value = package.get(key)
        if value:
            logging.warning(f"TODO top-level key: {key!r}")  # TODO add validators for these

    # Any unknown toplevel keys? -> fail!
    known_keys = {
        # mandatory:
        "bytes",
        "sha256",
        # optional:
        "description",
        "files",
        "install",
        "json_version",
        "notes",
        "tags",
        "urls",
        # deprecated, remove later:
        "authors",
        "current_main_group_package",
        "depends",
        "provides",
        "release_date",
        "release_group",
        "title",
        "version",
    }
    unknown_keys = package.keys() - known_keys
    if unknown_keys:
        package_validation_errors["unknown keys"] = unknown_keys

    # tags
    for tag_string in package.get("tags", []):
        try:
            tag = Tag(tag_string)
        except ValueError as e:
            package_validation_errors["invalid tag"] = str(e)
            continue

        if not tag.has_valid_value():
            package_validation_errors[tag.key] = tag.value

    return package_validation_errors


def validate_json(json_file_path: str | Path) -> Optional[dict[str, str]]:
    # open and read the file, errors on this level are fatal
    try:
        with open(json_file_path, encoding="utf-8") as f:
            try:
                package = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                return {"json": str(e)}
    except OSError as e:
        return {"file": str(e)}

    file_level_package_validation_errors = {}

    # small sanity check to see if the path's sha256 matches the sha256 in the json itself
    try:
        sha256_from_file_path = extract_sha256_from_path(json_file_path)
    except ValueError as e:
        file_level_package_validation_errors["path"] = str(e)
    else:
        if sha256_from_file_path != package.get("sha256"):
            file_level_package_validation_errors["sha256"] = "SHA256 mismatch between file path and file contents"

    # content validation
    package_validation_errors = validate_package(package)

    # merge errors collected here with those collected in the validation function(s)
    package_validation_errors = package_validation_errors | file_level_package_validation_errors

    return package_validation_errors
