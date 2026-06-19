"""Tests for release version bumping."""

from __future__ import annotations

import pytest

from scripts.bump_project_version import VersionBumpError, bump_version


def test_patch_bump_replaces_entire_semver() -> None:
    text = 'name = "study-os-thesis"\nversion = "0.1.0"\ndescription = "x"\n'

    new_text, version = bump_version(text, "patch")

    assert version == "0.1.1"
    assert 'version = "0.1.1"' in new_text
    assert "0.1.1.1.0" not in new_text


@pytest.mark.parametrize(
    ("bump", "expected"),
    [
        ("minor", "0.2.0"),
        ("major", "1.0.0"),
    ],
)
def test_minor_and_major_bumps_reset_lower_segments(bump: str, expected: str) -> None:
    new_text, version = bump_version('version = "0.1.9"\n', bump)

    assert version == expected
    assert f'version = "{expected}"' in new_text


def test_rejects_non_semver_project_version() -> None:
    with pytest.raises(VersionBumpError):
        bump_version('version = "0.1"\n', "patch")
