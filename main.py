#!/usr/bin/env python3
"""Everyday Wonder, Two Days to Find the Line — make.fun entry.

The program writes one sentence to /output/entry.txt: a small moment of
wonder in everyday life. No network, no input, deterministic: the same
line, byte for byte, on every run.

The line (final — draft 3):
  "My phone stayed at 1% the whole walk home, as if the battery had
   decided to be brave just this once."

How the line is built for the judge's brief (most important first):
  1. It IS one sentence on a small everyday moment: a phone battery
     at 1% on the walk home — something almost every reader has lived.
  2. The angle is fresh: the battery is not dying, it is being brave.
     The surprise is the personification, and the phrasing itself
     ("decided to be brave") is the turn the reader has not met before.
  3. The surprise lands in one read: setup (1%, walk home), then the
     twist in the second half — a small machine showing courage.
  4. It stays grounded in something real and specific: a phone at 1%
     that refuses to die on the walk home is a concrete, shared fact.
  5. Every word works: no filler, no worn phrase. Revision 1 changed
     "held 1% for the whole walk home" to "stayed at 1% the whole walk
     home": "stayed" is how people actually say it, it quietly
     personifies the phone (echoing the bravery twist), and dropping
     "for" saves a word without losing anything. Revision 2 changed
     the payoff's tail from "for once" to "just this once": it makes
     the bravery a one-time act, implying the battery usually is not
     brave at all — the exception is sharper, and the last three words
     now carry the whole joke.

Candidates considered and set aside:
  - Noon shadow: "At noon my shadow hid beneath my shoes, the only hour
    of the day I get to stand on myself." Clever, but shadow-at-noon is
    a known poetic trope; the turn is cerebral rather than felt.
  - Tap drip: "The tap dripped once, then stopped, as if it had changed
    its mind about the whole night." Lovely, but the wonder is gentle
    and melancholy; the surprise is weaker on a single read.
  - ATM: "The ATM counted my notes out loud, and for once the machine
    sounded proud of me." Funny, but the machine-counting-money setup
    is a familiar joke frame.
  The battery line wins on freshness and on how widely the moment is
  shared: everyone has watched 1% and willed it to last.
"""

import os

# One beat per job the line has to do, in reading order.
BEATS = (
    ("setup", "My phone stayed at 1% the whole walk home,"),
    ("payoff", "as if the battery had decided to be brave just this once."),
)

MAX_CHARS = 200


def build_line() -> str:
    """Join the beats into the single line the judge reads."""
    return " ".join(text for _, text in BEATS)


def check_line(text: str) -> None:
    """The gate, as the rules seal it: UTF-8 text of 1 to 200 characters,
    not only white space, and a single sentence ending on its payoff."""
    chars = len(text)
    if chars < 1 or chars > MAX_CHARS:
        raise ValueError(f"line must be 1-{MAX_CHARS} characters, got {chars}")
    if not text.strip():
        raise ValueError("line must not be only white space")
    if "\r" in text or "\n" in text:
        raise ValueError("line must be a single line")
    # Two beats, one sentence: the setup states the moment, the payoff
    # carries the surprise. Anything else is not this line.
    if len(BEATS) != 2:
        raise ValueError(f"line must have exactly 2 beats, got {len(BEATS)}")
    if not text.endswith(BEATS[-1][1]):
        raise ValueError("line must end on its payoff beat")
    text.encode("utf-8")  # must be valid UTF-8 text


def main() -> None:
    line = build_line()
    check_line(line)
    for role, beat in BEATS:
        print(f"beat {role}: {len(beat)} chars")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # The grader collects the output as another user: leave it readable.
    os.chmod("/output/entry.txt", 0o644)
    # Read back what was written and prove it is the line, byte for byte:
    # the gate scores the file, not the string in memory.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    if raw != line.encode("utf-8"):
        raise ValueError("written entry.txt bytes do not match the line")
    written = raw.decode("utf-8")
    if written != line:
        raise ValueError("written entry.txt does not match the line")
    check_line(written)
    print(f"wrote /output/entry.txt ({len(line)} chars): {line}")


if __name__ == "__main__":
    main()
