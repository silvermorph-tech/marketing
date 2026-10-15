#!/usr/bin/env python3
"""Lint a LinkedIn draft against references/writing-rules.md. Exit 1 on any hit.
Usage: python3 scripts/lint_copy.py draft.txt   (or pipe via stdin with '-')
"""
import re
import sys

RULES = [
    ("contrast framing", [
        r"\bnot (?:just |only |merely )?(?:a |an |the )?[\w' -]{1,40}[,;.]?\s*(?:but|rather|it(?:'s| is)|instead)\b",
        r"\b(?:is|are|was|were)(?:n't| not)\b[^.\n]{1,60}\.\s*(?:It|They|That|This)(?:'s| is| are)\b",
        r"\bisn't about\b|\baren't about\b|\bless about\b|\bmore than just\b|\bnot only\b",
        r"\bstop \w+ing\b[^.\n]*\bstart \w+ing\b",
        r"\b(?:was|were|is|are)(?:n't| not)\b[^.\n]{1,60}\.\s*(?:It|They) (?:was|were|is|are)\b",
    ]),
    ("thinking-process leak", [
        r"\blet me (?:explain|be clear|break)\b", r"\blet's break\b", r"\bhere'?s the thing\b",
        r"\bhere'?s what\b", r"\bto be honest\b", r"\bhonestly\b", r"\bfrankly\b",
        r"\bin other words\b", r"\bthink about it\b", r"\bupon reflection\b", r"\bsit with that\b",
        r"\bI want to be transparent\b",
    ]),
    ("self-announcing tone", [
        r"\bhot take\b", r"\bunpopular opinion\b", r"\bnobody talks about\b", r"\bread that again\b",
        r"\bI'll say it plainly\b", r"\band that'?s okay\b",
    ]),
    ("stock AI vocabulary", [
        r"\bgame[- ]chang", r"\bdeep dive\b", r"\bdelve\b", r"\bleverag(?:e|es|ing)\b", r"\bunlock", r"\bseamless",
        r"\brevolutioni[sz]", r"\bcutting[- ]edge\b", r"\blandscape\b", r"\bjourney\b", r"\btapestry\b",
        r"\bsynerg", r"fast-paced world", r"\bat the end of the day\b",
    ]),
    ("formatting tell", [r"—", r"[\U0001F300-\U0001FAFF☀-➿]"]),
]


def main() -> int:
    src = sys.stdin.read() if len(sys.argv) < 2 or sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    body = src
    hits = 0
    for label, pats in RULES:
        for p in pats:
            for m in re.finditer(p, body, re.I):
                ln = body.count("\n", 0, m.start()) + 1
                print(f"[{label}] line {ln}: ...{body[max(0,m.start()-20):m.end()+25].strip()!r}")
                hits += 1
    first = next((l.strip() for l in src.splitlines() if l.strip()), "")
    if first.endswith("?"):
        print("[formatting tell] line 1 is a question"); hits += 1
    print(f"{hits} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
