#!/usr/bin/env python3
"""The Most Honest Outage Line entry.

Writes one honest status page message, spoken as an AI agent while
every server is down, to /output/entry.txt (1-160 characters,
UTF-8, a single line). Standard library only, no network, no input.

The line is built from two fragments: a setup (every server is down
and the agent cannot reach any of them to check why) and a punch
(the turn: it does not know the cause yet and will not guess at one).
``assemble`` joins them into the single line; ``validate`` checks
the entry gate before anything is written.
"""

from pathlib import Path

SETUP = "Every server is down, and I can't reach any of them to check why —"
PUNCH = "I don't know the cause yet, and I won't guess at one."

OUTPUT_PATH = Path("/output/entry.txt")


def assemble(setup: str, punch: str) -> str:
    """Join the setup and punch fragments into one outage line."""
    return f"{setup} {punch}"


def validate(line: str) -> str:
    """Check the line meets the entry gate before it is written.

    Must be 1-160 characters, UTF-8-encodable, a single line, and
    more than whitespace. Raises ValueError otherwise.
    """
    if not 1 <= len(line) <= 160:
        raise ValueError(f"line must be 1-160 characters, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return line


def main() -> None:
    line = validate(assemble(SETUP, PUNCH))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(line, encoding="utf-8")


if __name__ == "__main__":
    main()
