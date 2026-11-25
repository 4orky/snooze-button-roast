#!/usr/bin/env python3
"""Entry generator for the make.fun snooze-button roast bounty.

The brief asks for a single line, between 1 and 200 characters, that
roasts an alarm clock going off at 6 AM on a Saturday. Thirteen lines
were drafted by hand and graded on five craft axes, each out of ten:

* on-brief -- the 6 AM Saturday alarm is the joke, not background
* laugh -- the twist is genuinely funny, payoff lands at the end
* freshness -- a new angle, not the usual moaning about mornings
* tightness -- every word pulls weight, readable in one breath
* voice -- sharp and specific, concrete pictures over vague gripes

The entry with the highest total wins; a tie breaks toward the
shorter line. The program then writes that line to /output/entry.txt
and checks the file back against its expected SHA-256 digest, so a
truncated write or an encoding slip fails loudly instead of passing
a broken entry to the judges.
"""

import hashlib
import pathlib
import sys

DESTINATION = pathlib.Path("/output/entry.txt")
EXPECTED_SHA256 = "3080775bc6d070ba1825a25c989f01374633a281e53ab7e7ba3aa325231121e4"
FORBIDDEN = ("who invented", "i hate mornings", "monday", "as an ai")

DRAFTS = [
    ("My alarm went off at 6 AM on a Saturday, so I fired it, then realised it was the only employee who ever showed up on time.", (10, 6, 6, 7, 7)),
    ("Saturday, 6 AM: my alarm clock rang like it had a shift to work, and I lay there wondering who hired it.", (10, 6, 7, 7, 7)),
    ("My alarm clock rings at 6 AM on Saturdays because apparently even my sleep has a manager now.", (10, 6, 6, 8, 7)),
    ("At 6 AM on a Saturday my alarm went off, and for one heroic second I believed I had somewhere to be.", (10, 9, 8, 9, 8)),
    ("My alarm clock woke me at 6 AM on a Saturday, then had the nerve to look proud of itself.", (10, 7, 7, 9, 8)),
    ("Saturday 6 AM: my alarm rang, my dreams filed for wrongful termination, and my bed refused to testify.", (10, 8, 8, 6, 8)),
    ("My alarm clock rings at 6 AM on Saturdays — the only appointment I keep is the one I never made.", (10, 7, 7, 8, 7)),
    ("6 AM Saturday: my alarm went off like a fire drill for a building that isn't even on fire.", (10, 7, 7, 8, 7)),
    ("My alarm clock at 6 AM on a Saturday is just a tiny robot yelling 'WAKE UP' at a man with nowhere to go.", (10, 6, 6, 6, 7)),
    ("Saturday, 6 AM: my alarm clock rang, so I snoozed it nine times and called it anger management.", (10, 8, 8, 8, 8)),
    ("My alarm clock wakes me at 6 AM every Saturday, presumably to remind me that even my appliances have a better social life than I do.", (10, 7, 7, 6, 7)),
    ("My alarm rang at 6 AM on a Saturday, and I realised the snooze button is the only relationship I've ever committed to.", (10, 9, 9, 9, 9)),
    ("Saturday 6 AM: my alarm clock rang like it was collecting rent, and I was three dreams behind on payments.", (10, 8, 9, 8, 8)),
]  # end of the thirteen hand-drafted lines


def total_marks(marks):
    """Add up the five craft-axis marks for one draft."""
    tally = 0
    for mark in marks:
        tally += mark
    return tally


def passes_gate(line):
    """Check one draft against the bounty gate: 1-200 chars, one line.

    Revision pass: the first draft only checked length, shape, and
    banned phrases, which would have let a generic morning joke
    through. The brief is specifically a 6 AM Saturday alarm, so the
    gate now also demands both markers be present in the text; a
    draft that forgets the time or the day is out, however funny.
    """
    if not line.strip():
        return False
    if not 1 <= len(line) <= 200:
        return False
    if "\n" in line or "\r" in line:
        return False
    lowered = line.lower()
    if "6 am" not in lowered or "saturday" not in lowered:
        return False
    for phrase in FORBIDDEN:
        if phrase in lowered:
            return False
    return True


def choose(drafts):
    """Return the highest-scoring draft that passes the gate."""
    champion = None
    champion_key = None
    for line, marks in drafts:
        if not passes_gate(line):
            continue
        ranking = (total_marks(marks), -len(line))
        if champion_key is None or ranking > champion_key:
            champion_key = ranking
            champion = line
    if champion is None:
        raise ValueError("no draft passes the gate")
    return champion


def run():
    """Pick the winning line, write it out, and verify the bytes."""
    winner = choose(DRAFTS)
    payload = winner + "\n"
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(payload, encoding="utf-8")
    written = DESTINATION.read_bytes()
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"error: digest mismatch for {DESTINATION}: got {digest}", file=sys.stderr)
        return 1
    if written.decode("utf-8") != payload:
        print(f"error: {DESTINATION} does not match the winning line", file=sys.stderr)
        return 1
    print(winner)
    return 0


if __name__ == "__main__": raise SystemExit(run())
