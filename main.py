#!/usr/bin/env python3
"""Entrypoint: copy the shipped entry.png to the output directory.

Standard library only, no network. Deterministic: two runs write
identical bytes. Never deletes the output directory.
"""

import hashlib
import os
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    with open(dest, "wb") as fh:
        fh.write(data)
    with open(dest, "rb") as fh:
        verify = hashlib.sha256(fh.read()).hexdigest()
    if verify != digest:
        print("verification failed: copy hash mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dest}: {len(data)} bytes sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
