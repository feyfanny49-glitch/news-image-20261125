#!/usr/bin/env python3
"""Validate entry.png exactly as a whole-image gate would, using the stdlib.

Checks: PNG signature, IHDR shape, every chunk's CRC, IDAT and IEND, no trailing
bytes, at most 1 MiB and at most 1024 by 1024 pixels. Prints bytes, dimensions
and sha256 on success.
"""

import hashlib
import struct
import sys
import zlib
from pathlib import Path

SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def check(path):
    data = Path(path).read_bytes()
    if len(data) > MAX_BYTES:
        fail(f"file is {len(data)} bytes, cap is {MAX_BYTES}")
    if not data.startswith(SIGNATURE):
        fail("bad PNG signature")

    pos = len(SIGNATURE)
    chunks = []
    saw_iend = False
    while pos < len(data):
        if pos + 12 > len(data):
            fail(f"truncated chunk header at {pos}")
        length = struct.unpack_from(">I", data, pos)[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            fail(f"chunk {kind!r} runs past end of file")
        payload = data[pos + 8:pos + 8 + length]
        stated = struct.unpack_from(">I", data, pos + 8 + length)[0]
        actual = zlib.crc32(kind + payload) & 0xFFFFFFFF
        if stated != actual:
            fail(f"CRC mismatch in {kind!r}: {stated:08x} != {actual:08x}")
        chunks.append((kind, length))
        pos = end
        if kind == b"IEND":
            saw_iend = True
            if length != 0:
                fail("IEND must have zero length")
            if pos != len(data):
                fail(f"{len(data) - pos} trailing bytes after IEND")
            break

    if not saw_iend:
        fail("no IEND chunk")
    if not chunks or chunks[0][0] != b"IHDR" or chunks[0][1] != 13:
        fail("first chunk must be a 13-byte IHDR")
    if not any(kind == b"IDAT" for kind, _ in chunks):
        fail("no IDAT chunk")

    ihdr = data[len(SIGNATURE) + 8:len(SIGNATURE) + 21]
    width, height, depth, colour, comp, filt, interlace = struct.unpack(">IIBBBBB", ihdr)
    if width == 0 or height == 0 or width > MAX_SIDE or height > MAX_SIDE:
        fail(f"dimensions {width}x{height} exceed {MAX_SIDE}x{MAX_SIDE}")
    if depth not in (1, 2, 4, 8, 16) or colour not in (0, 2, 3, 4, 6):
        fail("unsupported IHDR depth or colour type")
    if comp != 0 or filt != 0 or interlace not in (0, 1):
        fail("unsupported IHDR compression, filter or interlace")

    digest = hashlib.sha256(data).hexdigest()
    print(f"PASS  bytes={len(data)}  dimensions={width}x{height}  "
          f"chunks={len(chunks)}  sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1] if len(sys.argv) > 1 else "entry.png"))
