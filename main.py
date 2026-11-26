"""One-Liner Laughs entry for make.fun.

Writes a single joke — an agent that finished all its owner's work by
9am, got a raise, and spent it on more compute — to
$MAKEFUN_OUTPUT_DIR/entry.txt for the bounty "One-Liner Laughs".
Only the Python standard library is used.
"""

import os
import sys

JOKE = "My agent finished all my work by 9am, so I gave it a raise. It spent the raise on more compute and now outranks me in my own company."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def describe_line(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII joke
    reads the same either way while a joke with wide characters
    would not. Returns a one-line human-readable summary.
    """
    chars = len(text)
    byte_count = len(text.encode("utf-8"))
    words = len(text.split())
    return "{} characters, {} UTF-8 bytes, {} words".format(chars, byte_count, words)


def check_joke(text):
    """Return the joke once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line of non-whitespace text with no trailing newline in the file.
    A bad joke is refused here, loudly, instead of shipping an entry
    the judge never sees.
    """
    if not isinstance(text, str):
        raise TypeError("joke must be text")
    if not text.strip():
        raise ValueError("joke must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "joke is {} chars, over the {}-char gate".format(len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("joke must not contain control characters")
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    line = check_joke(JOKE)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    print("wrote {} ({})".format(target, describe_line(line)))


if __name__ == "__main__":
    main()
