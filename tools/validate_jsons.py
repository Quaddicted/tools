import glob
import logging
import os
import sys

from package_validation.validation import validate_json

logging.basicConfig(level=logging.INFO)

quaddicted_data_repo_path = os.environ["QUADDICTED_DATA"]  # root directory of the quaddicted-data repository


if __name__ == "__main__":
    packages_validation_errors: dict[str, dict] = {}

    for json_file_path in glob.glob(quaddicted_data_repo_path + "/json/by-sha256/*/*"):
        logging.info(f"Checking {json_file_path}...")
        package_validation_errors = validate_json(json_file_path)
        if package_validation_errors:
            packages_validation_errors[json_file_path] = package_validation_errors

    logging.info(f"Error(s) in {len(packages_validation_errors)} file(s).")
    for sha256, error in packages_validation_errors.items():
        logging.error(f"{sha256}: {dict(error)}")

    if packages_validation_errors:
        sys.exit(1)

    logging.info("JSON/Package validation finished without errors.")