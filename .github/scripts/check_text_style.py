import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

EXCLUDED_FILES = frozenset(
    {
        ".github/scripts/check_text_style.py",
        "CODE_OF_CONDUCT.md",
        "dataset/LICENSE",
        "hardware/LICENSE",
        "web/package-lock.json",
    }
)
BINARY_SUFFIXES = frozenset({".bin", ".gbr", ".jpg", ".parquet", ".pdf", ".png", ".zip"})
MARKETING_WORDS = ("comprehensive", "cutting-edge", "empower", "leverage", "robust", "seamless")

EM_DASH = "—"
EMOJI_CODE_POINT_RANGES = (
    (0x1F000, 0x1FAFF),
    (0x2600, 0x27BF),
    (0x2B00, 0x2BFF),
    (0xFE0F, 0xFE0F),
)
MARKETING_WORD_PATTERN = re.compile(
    r"\b(?:" + "|".join(re.escape(word) for word in MARKETING_WORDS) + r")\w*", re.IGNORECASE
)


def tracked_files() -> list[Path]:
    listing = subprocess.run(["git", "ls-files", "-z"], check=True, capture_output=True).stdout
    return [Path(name) for name in listing.decode("utf-8").split("\0") if name]


def is_emoji(character: str) -> bool:
    code_point = ord(character)
    return any(low <= code_point <= high for low, high in EMOJI_CODE_POINT_RANGES)


def style_violations(path: Path) -> Iterator[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    for line_number, line in enumerate(text.splitlines(), start=1):
        for column, character in enumerate(line, start=1):
            if character == EM_DASH:
                yield f"{path}:{line_number}:{column}: em dash"
            elif is_emoji(character):
                yield f"{path}:{line_number}:{column}: emoji U+{ord(character):04X}"
        for match in MARKETING_WORD_PATTERN.finditer(line):
            yield f"{path}:{line_number}:{match.start() + 1}: marketing word '{match.group(0)}'"


def main() -> int:
    violations = [
        violation
        for path in tracked_files()
        if path.as_posix() not in EXCLUDED_FILES and path.suffix not in BINARY_SUFFIXES
        for violation in style_violations(path)
    ]
    for violation in violations:
        print(violation)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
