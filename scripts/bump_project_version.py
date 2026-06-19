"""Bump the project SemVer in pyproject.toml."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PYPROJECT = REPO_ROOT / "pyproject.toml"
VERSION_PATTERN = re.compile(r'(?m)^(version = ")(\d+)\.(\d+)\.(\d+)(")$')


class VersionBumpError(RuntimeError):
    """Raised when the project version cannot be bumped."""


def bump_version(text: str, bump: str) -> tuple[str, str]:
    match = VERSION_PATTERN.search(text)
    if not match:
        raise VersionBumpError('pyproject.toml must contain a SemVer [project].version like version = "0.1.0"')

    major, minor, patch = map(int, match.group(2, 3, 4))
    if bump == "major":
        major, minor, patch = major + 1, 0, 0
    elif bump == "minor":
        minor, patch = minor + 1, 0
    elif bump == "patch":
        patch += 1
    else:
        raise VersionBumpError(f"unsupported bump type: {bump}")

    new_version = f"{major}.{minor}.{patch}"
    new_text = text[: match.start()] + f'{match.group(1)}{new_version}{match.group(5)}' + text[match.end() :]
    return new_text, new_version


def bump_pyproject(pyproject_path: Path, bump: str) -> str:
    text = pyproject_path.read_text(encoding="utf-8")
    new_text, new_version = bump_version(text, bump)
    pyproject_path.write_text(new_text, encoding="utf-8")
    return new_version


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump [project].version in pyproject.toml.")
    parser.add_argument("bump", choices=["patch", "minor", "major"])
    parser.add_argument("--pyproject", type=Path, default=DEFAULT_PYPROJECT)
    args = parser.parse_args()

    try:
        print(bump_pyproject(args.pyproject, args.bump))
    except VersionBumpError as error:
        parser.exit(status=1, message=f"error: {error}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
