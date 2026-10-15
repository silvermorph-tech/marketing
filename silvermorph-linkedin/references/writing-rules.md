# Voice core (owner, 2026-10-14): applies to every category

1. **Talk like a friend who knows the field.** Plain, direct, warm. No corporate announcement voice.
2. **Never empty.** Each post gives the reader something they can take away: a fact they did not have, a way to see a problem, a decision they can make. If a post could be written by any company in the sector, it is not ready.
3. **First principles.** Go to the root cause. Say what actually drives the problem (cost, time, incentives, structure) before saying what we built. Strip every sentence that only decorates.
4. **Test before approval:** (a) What does the reader know after 20 seconds that they did not know before? (b) Could a competitor post this unchanged? If (a) is "nothing" or (b) is "yes", rewrite.

# Writing rules: banned patterns (owner's list + upstream tells)

Run `python3 scripts/lint_copy.py <draft.txt>` before every approval card. Any hit = rewrite, not "explain why it is fine".

## 1. Contrast framing (the most obvious AI tell)
Banned: "not X, but Y" / "X is not Y. It is Z." / "isn't about X, it's about Y" / "less about X than Y" / "more than just X" / "not only X but also Y" / "stop doing X, start doing Y".
Fix: state Y directly. Drop X unless the reader actually holds X as a belief, and then say it as a plain claim ("Most dashboards record events; they do not move work.").

## 2. Thinking process leaking into the post
Banned: "Let me explain", "Let's break it down", "Here's the thing", "Here's what I learned", "Let me be clear", "To be honest", "Honestly", "Frankly", "I want to be transparent", "In other words", "Think about it", "Upon reflection", "Sit with that".
The post shows the conclusion, never the drafting.

## 3. Self-validating or self-announcing tone
Banned: "Hot take", "Unpopular opinion", "Nobody talks about", "I'll say it plainly", "and that's okay", "This is important", "Read that again", announced candor of any kind.
Claims earn attention with a fact. They do not announce themselves.

## 4. Stock AI vocabulary
game-changer, deep dive, delve, leverage (verb), unlock, seamless, revolutionize, transform (as hype), cutting-edge, landscape, journey, tapestry, ecosystem (unless naming a partner ecosystem), synergy, "in today's fast-paced world", "at the end of the day".

## 5. Formatting tells
No em dashes. No emojis. No "Here's why:" bullet stacks. No question as line 1. No more than one rhetorical question per post (the closing one). No three-item rhythm lists used as filler.

## 6. Facts
Every number, name, date and quote comes from `inputs/00-facts/facts-bank.md` or from the user in this conversation. If missing: ask. Never fill a gap with a plausible sentence.
