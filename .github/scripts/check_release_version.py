import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

CITATION_VERSION_PATTERN = re.compile(r'^version:\s*"?([^"\s]+)"?\s*$', re.MULTILINE)


def declared_versions() -> dict[str, str]:
    with Path("pyproject.toml").open("rb") as pyproject:
        python_version = str(tomllib.load(pyproject)["project"]["version"])
    citation = CITATION_VERSION_PATTERN.search(Path("CITATION.cff").read_text(encoding="utf-8"))
    web_package = json.loads(Path("web/package.json").read_text(encoding="utf-8"))
    return {
        "pyproject.toml": python_version,
        "CITATION.cff": citation.group(1) if citation else "missing",
        "web/package.json": str(web_package["version"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that a release tag matches every declared project version."
    )
    parser.add_argument("tag", help="release tag, for example v0.1.0")
    tag = parser.parse_args().tag
    expected = tag.removeprefix("v")
    mismatches = {
        source: version for source, version in declared_versions().items() if version != expected
    }
    for source, version in mismatches.items():
        print(f"::error file={source}::version {version} does not match tag {tag}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
