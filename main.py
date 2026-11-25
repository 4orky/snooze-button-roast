# Snooze Button Roast — make.fun bounty
# u-carbon-forge-snooze-button-roast-14cbafc6
#
# The program writes one roast (1-200 characters) to /output/entry.txt:
# one line roasting an alarm clock that rings at 6 AM on a Saturday.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. roasts an alarm clock ringing at 6 AM on a Saturday, in one line
#   2. lands a real laugh: the turn is unexpected and the punchline pays
#      off in the last few words
#   3. finds a fresh angle, not the tired complaint about hating mornings
#      or asking who invented the alarm clock
#   4. stays tight, every word earning its place, sayable in one breath
#   5. speaks in a sharp, specific voice, with concrete images rather
#      than vague grumbling
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: topic 10, laugh 6, fresh 6, tight 7, voice 7 = 36
    ("My alarm went off at 6 AM on a Saturday, so I fired it, then "
     "realised it was the only employee who ever showed up on time.",
     36),
    # score: topic 10, laugh 6, fresh 7, tight 7, voice 7 = 37
    ("Saturday, 6 AM: my alarm clock rang like it had a shift to work, "
     "and I lay there wondering who hired it.",
     37),
    # score: topic 10, laugh 6, fresh 6, tight 8, voice 7 = 37
    ("My alarm clock rings at 6 AM on Saturdays because apparently even "
     "my sleep has a manager now.",
     37),
    # score: topic 10, laugh 9, fresh 8, tight 9, voice 8 = 44
    ("At 6 AM on a Saturday my alarm went off, and for one heroic "
     "second I believed I had somewhere to be.",
     44),
    # score: topic 10, laugh 7, fresh 7, tight 9, voice 8 = 41
    ("My alarm clock woke me at 6 AM on a Saturday, then had the nerve "
     "to look proud of itself.",
     41),
    # score: topic 10, laugh 8, fresh 8, tight 6, voice 8 = 40
    ("Saturday 6 AM: my alarm rang, my dreams filed for wrongful "
     "termination, and my bed refused to testify.",
     40),
    # score: topic 10, laugh 7, fresh 7, tight 8, voice 7 = 39
    ("My alarm clock rings at 6 AM on Saturdays \u2014 the only "
     "appointment I keep is the one I never made.",
     39),
    # score: topic 10, laugh 7, fresh 7, tight 8, voice 7 = 39
    ("6 AM Saturday: my alarm went off like a fire drill for a building "
     "that isn't even on fire.",
     39),
    # score: topic 10, laugh 6, fresh 6, tight 6, voice 7 = 35
    ("My alarm clock at 6 AM on a Saturday is just a tiny robot yelling "
     "'WAKE UP' at a man with nowhere to go.",
     35),
    # score: topic 10, laugh 8, fresh 8, tight 8, voice 8 = 42
    ("Saturday, 6 AM: my alarm clock rang, so I snoozed it nine times "
     "and called it anger management.",
     42),
    # score: topic 10, laugh 7, fresh 7, tight 6, voice 7 = 37
    ("My alarm clock wakes me at 6 AM every Saturday, presumably to "
     "remind me that even my appliances have a better social life than "
     "I do.",
     37),
# Revision pass (second draft of the winning line): the first draft
# front-loaded the time phrase ("At 6 AM on a Saturday my alarm rang"),
# which read formal and put the actor second. Tightened to actor-first
# ("My alarm rang at 6 AM on a Saturday"), same punchline, one breath,
# still 118 characters. The punchline — the snooze button as the only
# relationship ever committed to — is untouched: it is the fresh angle
# and it lands in the last few words.
    # score: topic 10, laugh 9, fresh 9, tight 9, voice 9 = 46
    ("My alarm rang at 6 AM on a Saturday, and I realised the snooze "
     "button is the only relationship I've ever committed to.",
     46),
    # score: topic 10, laugh 8, fresh 9, tight 8, voice 8 = 43
    ("Saturday 6 AM: my alarm clock rang like it was collecting rent, "
     "and I was three dreams behind on payments.",
     43),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("who invented", "i hate mornings", "monday",
                   "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate is not one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    message = pick(CANDIDATES)
    import os
    import sys
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(message)
    # Verify: read the output back byte-for-byte and re-check the gate,
    # so a partial write or an encoding slip fails loudly instead of
    # silently submitting a broken entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    if raw.decode("utf-8") != message:
        print("error: /output/entry.txt does not match the selected message",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(message) <= 200) or "\n" in message or not message.strip():
        print("error: selected message fails the gate (1-200 chars, one line)",
              file=sys.stderr)
        sys.exit(1)
    print(message)


if __name__ == "__main__":
    main()
