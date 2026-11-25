"""One Line, No Deadline Met.

Writes a single original one-line joke giving an excuse for a missed
deadline to /output/entry.txt (falling back to ./output/entry.txt),
then reads the file back and verifies it holds exactly that line.
Deterministic: stdlib only, no network, no randomness, no secrets.
"""

import os
import sys

# The entry: one original single-line excuse for a missed deadline.
# The twist is a blame reversal -- the deadline missed *me* -- and the
# punch lands on the last words: it never even apologized.
JOKE = "I didn't miss the deadline \u2014 the deadline missed me, and frankly, it never even apologized."

MAX_CHARS = 200


def validate(line):
    """Check the line satisfies the competition gate.

    The gate requires UTF-8 text of 1-200 characters, not only
    whitespace, and exactly one line. Anything else is rejected
    before the file is written, so a bad line can never be submitted.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line or line.strip() == "":
        raise ValueError("line must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError("line must be 1-200 characters, got %d" % len(line))
    return line


def pick_output_path():
    """Prefer /output/entry.txt; fall back to ./output/entry.txt."""
    for base in ("/output", os.path.join(os.getcwd(), "output")):
        try:
            os.makedirs(base, exist_ok=True)
            probe = os.path.join(base, ".write-test")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("")
            os.remove(probe)
            return os.path.join(base, "entry.txt")
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main():
    line = validate(JOKE)
    path = pick_output_path()
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(line)
    # Read back and verify the file holds exactly the line, nothing else.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != line:
        raise ValueError("read-back mismatch: file does not hold exactly the line")
    print("%d" % len(line))
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
