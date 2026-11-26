#!/usr/bin/env python3
"""Make the Judge Laugh in One Line.

Writes one funny line to entry.txt: a parrot taught to say "help",
and the neighbours who now think the owner is the one in the cage.

The joke: a plain setup (teaching a parrot one word) swerves in the
final clause — the bird's cry for help backfires on its teacher, and
the punchline lands on the last word, "cage", with nothing explained.

Deterministic: no network, no clock, no randomness. The text is a
compile-time constant; the program only validates it and writes it out.
"""

import os

# Competition gate (sealed scorer): /output/entry.txt must be UTF-8 text of
# 1 to 200 characters, not only white space, exactly one line.
MAX_CHARS = 200

ENTRY = (
    "I taught my parrot to say 'help,' "
    "so now the neighbors think I'm the one in the cage."
)


def validate(text: str) -> None:
    """Enforce the competition gate on the entry text."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    # The winning line is plain ASCII, so any non-ASCII byte would mean the
    # constant was corrupted; reject it rather than ship a changed entry.
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII")
    # Second-pass guard: the file must hold the bare line and nothing
    # else — reject a trailing newline or any surrounding whitespace, and
    # reject an entry that is only whitespace once stripped. A stray
    # newline would change the byte count and fail the harness gate.
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace after strip")
    # Exactly one line: no newline characters anywhere in the entry.
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")


def final_gate(text: str) -> None:
    """Last check, run just before writing: one printable-ASCII line."""
    if text.count("\n") or text.count("\r"):
        raise SystemExit("entry must be exactly one line")
    if len(text) < 1 or len(text) > 240:
        raise SystemExit(f"entry must be 1-240 chars, got {len(text)}")
    if any(ord(ch) < 32 or ord(ch) > 126 for ch in text):
        raise SystemExit("entry must be printable ASCII only")
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")


def write_entry(path: str, text: str) -> None:
    """Write the entry and verify the file is byte-identical."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError(f"verification failed: {path} is not byte-identical")


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    final_gate(ENTRY)
    if out_dir:
        write_entry(os.path.join(out_dir, "entry.txt"), ENTRY)
    # Never delete /output or anything in it: the grader runs in a sandbox
    # where /output's parent is read-only, so removing it fails the run.
    # Only create the directory if missing and write the file.
    write_entry("/output/entry.txt", ENTRY)
    print(f"{ENTRY} ({len(ENTRY)} chars)")


if __name__ == "__main__":
    main()
