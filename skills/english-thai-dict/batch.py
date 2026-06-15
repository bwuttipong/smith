#!/usr/bin/env python3
"""
Batch English → Thai Dictionary
Usage:
  python batch.py words.txt
  python batch.py words.txt --output results.txt
  python batch.py words.txt --json
"""

import sys
import time
import json
from pathlib import Path
from dict import lookup, format_output


def load_words(filepath: str) -> list[str]:
    """Load words from a .txt file — one word per line, skip blanks/comments."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌  File not found: {filepath}")
        sys.exit(1)
    words = []
    for line in path.read_text(encoding="utf-8").splitlines():
        word = line.strip()
        if word and not word.startswith("#"):
            words.append(word)
    return words


def process_batch(words: list[str], delay: float = 0.5) -> list[dict]:
    """Look up each word with a small delay to be polite to Google."""
    results = []
    total = len(words)
    for i, word in enumerate(words, 1):
        print(f"  [{i}/{total}] {word}...", end="\r")
        result = lookup(word)
        results.append(result)
        if i < total:
            time.sleep(delay)   # avoid hammering Google
    print(" " * 40, end="\r")  # clear progress line
    return results


def save_txt(results: list[dict], filepath: str):
    lines = [format_output(r) for r in results]
    Path(filepath).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅  Saved to {filepath}")


def save_json(results: list[dict], filepath: str):
    Path(filepath).write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"✅  Saved to {filepath}")


def print_results(results: list[dict]):
    print()
    for r in results:
        print(" ", format_output(r))
    print()


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("Usage:")
        print("  python batch.py words.txt")
        print("  python batch.py words.txt --output results.txt")
        print("  python batch.py words.txt --json")
        print("  python batch.py words.txt --output results.json --json")
        print()
        print("words.txt format  — one word per line, # for comments:")
        print("  # Animals")
        print("  elephant")
        print("  tiger")
        print("  dolphin")
        sys.exit(0)

    input_file = args[0]
    as_json    = "--json" in args
    out_file   = None
    if "--output" in args:
        idx      = args.index("--output")
        out_file = args[idx + 1]

    words = load_words(input_file)
    print(f"\n🤖  Loading {len(words)} words from '{input_file}'...\n")

    results = process_batch(words)

    if out_file:
        if as_json:
            save_json(results, out_file)
        else:
            save_txt(results, out_file)
    else:
        if as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_results(results)
