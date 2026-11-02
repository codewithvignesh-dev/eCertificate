from pathlib import Path
import zipfile
import fnmatch
import os
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.name
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
ZIP_PATH = PROJECT_DIR / f"{PROJECT_NAME}_{TIMESTAMP}.zip"

EXTRA_EXCLUDE_DIRS = {
    ".git",
    ".pytest_cache",
    "myenv",
    "venv",
    "env",
    ".venv",
    "__pycache__",
    "node_modules",
    "tests",
}

EXTRA_EXCLUDE_FILES = {
    ".gitignore",
    "package.json",
    "package-lock.json",
    "README.md",
}

EXTRA_EXCLUDE_PATTERNS = {"*.zip"}


def load_gitignore():
    gitignore = PROJECT_DIR / ".gitignore"

    if not gitignore.exists():
        print("WARNING: .gitignore not found")
        return []

    with gitignore.open("r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]


def matches_gitignore(path, is_dir=False):
    relative = path.relative_to(PROJECT_DIR).as_posix()
    parts = relative.split("/")

    for pattern in GITIGNORE_PATTERNS:
        if not pattern or pattern.startswith("!"):
            continue

        directory_pattern = pattern.endswith("/")
        pattern = pattern.rstrip("/")

        if pattern.startswith("/"):
            pattern = pattern.lstrip("/")

            if fnmatch.fnmatch(relative, pattern):
                return True

            if is_dir and fnmatch.fnmatch(relative + "/", pattern + "/"):
                return True

        elif (
            fnmatch.fnmatch(relative, pattern)
            or fnmatch.fnmatch(path.name, pattern)
            or any(fnmatch.fnmatch(part, pattern) for part in parts)
        ):
            return True

    return False


def should_exclude(path):
    if path.is_dir() and path.name in EXTRA_EXCLUDE_DIRS:
        return True

    if path.is_file() and path.name in EXTRA_EXCLUDE_FILES:
        return True

    if path.is_file() and any(
        fnmatch.fnmatch(path.name, pattern)
        for pattern in EXTRA_EXCLUDE_PATTERNS
    ):
        return True

    return matches_gitignore(path, path.is_dir())


def create_zip():
    global GITIGNORE_PATTERNS
    GITIGNORE_PATTERNS = load_gitignore()

    print("=" * 70)
    print("PROJECT ZIP CREATOR")
    print("=" * 70)
    print(f"Project : {PROJECT_DIR}")
    print(f"ZIP     : {ZIP_PATH}")
    print(f"Rules   : {len(GITIGNORE_PATTERNS)}")
    print("-" * 70)

    included = 0
    excluded = 0

    with zipfile.ZipFile(
        ZIP_PATH,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zip_file:
        for root, dirs, files in os.walk(PROJECT_DIR):
            root_path = Path(root)

            excluded_dirs = [
                directory
                for directory in dirs
                if should_exclude(root_path / directory)
            ]

            excluded += len(excluded_dirs)
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in excluded_dirs
            ]

            for filename in files:
                file_path = root_path / filename

                if should_exclude(file_path):
                    excluded += 1
                    continue

                archive_path = file_path.relative_to(PROJECT_DIR).as_posix()
                zip_file.write(file_path, arcname=archive_path)

                included += 1
                print(f"ADD  {archive_path}")

    print("-" * 70)
    print("ZIP CREATED")
    print("=" * 70)
    print(f"Included : {included} files")
    print(f"Excluded : {excluded} files/folders")
    print(f"Size     : {ZIP_PATH.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"Output   : {ZIP_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    create_zip()