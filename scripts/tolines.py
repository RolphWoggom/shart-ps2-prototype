#!/bin/python

import json
from pathlib import Path

mangled_map = Path("srr2.map.mangled").read_text().strip().split("\n")
demangled_map = Path("srr2.map.demangled").read_text().strip().split("\n")
print("loaded map files")

lines = list()
for line_number, line in enumerate(demangled_map):
    if line_number < 2:
        continue

    address = int(line[0:8], 16)
    size    = int(line[9:17], 16)
    align   = int(line[18:23], 16)

    if line[24] != " ":
        type_ = "out"
        value = line[24:]

    elif line[32] != " ":
        type_ = "in"
        value = line[32:]

    elif line[40] != " ":
        type_ = "file"
        value = line[40:]

    elif line[48] != " ":
        type_ = "symbol"
        value = {
            "mangled": mangled_map[line_number][48:],
            "demangled": line[48:]
        }

    lines.append({
        "address": address,
        "size": size,
        "align": align,
        "type": type_,
        "value": value
    })

print(f"parsed {len(lines)} lines")

json.dump(lines, open("srr2.lines.json", "w"), indent=2)
print("written to srr2.lines.json")

