#!/usr/bin/env python3
"""Convert a C array / hex dump (0xNN tokens) to a binary ROM image.

  tools/c2bin.py basic_rom.h roms/basic.bin

Use it to turn the Integer BASIC array from your Pico source into the
roms/basic.bin file the Linux emulator loads at $E000.
"""
import re, sys
if len(sys.argv) != 3:
    sys.exit(__doc__)
data = open(sys.argv[1], encoding="utf-8", errors="replace").read()
data = re.sub(r"/\*.*?\*/|//[^\n]*", "", data, flags=re.S)   # drop comments
vals = [int(t, 16) for t in re.findall(r"0[xX]([0-9A-Fa-f]{1,2})\b", data)]
open(sys.argv[2], "wb").write(bytes(vals))
print(f"wrote {len(vals)} bytes to {sys.argv[2]}")
