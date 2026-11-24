#!/usr/bin/env python3
"""The Most Honest Outage Line entry.

Writes one honest status page message, spoken as an AI agent while
every server is down, to /output/entry.txt (1-160 characters,
UTF-8, a single line). Standard library only, no network, no input.

The line is built from two fragments: a setup (every server is down
and the agent cannot reach any of them to check why) and a punch
(the turn: it does not know the cause yet and will not guess at one).
``build_line`` joins the fragments in order; ``check_gate`` verifies
the assembled line against the entry gate before ``write_entry``
writes it out.
"""

from dataclasses import dataclass
from pathlib import Path

SETUP = "Every server is down, and I can't reach any of them to check why —"
PUNCH = "I don't know the cause yet, and I won't guess at one."

OUTPUT_PATH = Path("/output/entry.txt")


@dataclass(frozen=True)
class EntryGate:
    """The entry gate for a one-line status message.

    ``max_chars`` is the competition's character limit; ``min_chars``
    keeps the line from being empty or a bare fragment.
    """

    min_chars: int = 1
    max_chars: int = 160


GATE = EntryGate()


def build_line(fragments: tuple[str, ...]) -> str:
    """Join the outage-line fragments into one line, in order."""
    return " ".join(fragment.strip() for fragment in fragments)


def check_gate(line: str, gate: EntryGate = GATE) -> str:
    """Check the line meets the entry gate before it is written.

    Must be within the character limit, UTF-8-encodable, a single
    line, and more than whitespace. Returns the line unchanged so it
    can be passed straight to ``write_entry``. Raises ValueError
    otherwise.
    """
    if not gate.min_chars <= len(line) <= gate.max_chars:
        raise ValueError(
            f"line must be {gate.min_chars}-{gate.max_chars} characters, "
            f"got {len(line)}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return line


def write_entry(line: str, path: Path = OUTPUT_PATH) -> Path:
    """Write the checked line to ``path`` as UTF-8, no trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(line, encoding="utf-8")
    return path


def main() -> None:
    line = check_gate(build_line((SETUP, PUNCH)))
    write_entry(line)


if __name__ == "__main__":
    main()
