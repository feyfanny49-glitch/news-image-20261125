#!/usr/bin/env python3
"""make.fun news-image entry: copy the committed PNG into the output directory.

Standard library only. The program reads its own committed entry.png and writes
those exact bytes to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png),
so the two grader runs cannot diverge. It verifies the copy and prints a short
manifest line naming the byte count and digest it produced.
"""

import hashlib
import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        raise SystemExit(f"missing committed image: {source}")

    data = source.read_bytes()

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"

    # Write the bytes directly; a plain byte copy keeps the image whole.
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"output mismatch: {target}")

    digest = hashlib.sha256(data).hexdigest()
    print(f"entry.png: {len(data)} bytes sha256 {digest} -> {target}")


if __name__ == "__main__":
    main()
