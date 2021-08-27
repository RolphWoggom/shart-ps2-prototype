#!/bin/python

import json

from elftools.elf.elffile import ELFFile

with open("data/SLUS_206.24", 'rb') as f:
    rodata = ELFFile(f).get_section_by_name(".rodata")
    rodata_address = rodata.header["sh_addr"]
    rodata_data = rodata.data()

map_lines = json.load(open("srr2.lines.json"))
map_lines_by_address = dict()
for line in map_lines:
    map_lines_by_address[hex(line["address"])] = line

vftables = dict()
for line in map_lines:
    if line["type"] == "symbol":
        if "virtual table" in line["value"]["demangled"]:
            address = line["address"]
            size = line["size"]
            length = int(size / 4)
            class_name = line["value"]["demangled"].replace(" virtual table", "")

            vftables[class_name] = {
                "ea": address,
                "length": length,
                "vftptr": None, # Virtual Function Type PoinTeR ? Virtual Function Table PoinTeR
                "entries": list()
            }

            print()
            print(hex(address).rjust(8), class_name)
            for i in range(length):
                pointer_address = (address + i * 4) - rodata_address
                pointer_bytes = rodata_data[pointer_address:pointer_address + 4]
                pointer = int.from_bytes(pointer_bytes, "little")
                if pointer:
                    pointer_line = map_lines_by_address[hex(pointer)] if hex(pointer) in map_lines_by_address else None
                    if pointer_line:
                        if pointer_line["type"] == "symbol":
                            name = pointer_line["value"]["mangled"]
                            demangled_name = pointer_line["value"]["demangled"]
                            print("    ", str(i).rjust(3), hex(pointer).rjust(8), "   ", demangled_name)
                        else:
                            name = ""
                            demangled_name = ""
                    # else:
                    #     print("   weird shit:", pointer, hex(pointer))
                    vftables[class_name]["entries"].append({
                        "ea": pointer,
                        "offset": i,
                        "name": name,
                        "demangled_name": demangled_name,
                        "import": False,
                        "type": "meth"
                    })

json.dump(vftables, open("srr2.vftables.json", "w"), indent=2)

vftables = dict()
for line in map_lines:
    if line["type"] == "symbol":
        if "virtual table" in line["value"]["demangled"]:
            address = line["address"]
            vftable_address = address - rodata_address
            vftables[address] = rodata_data[vftable_address:vftable_address + line["size"]].hex()

json.dump(vftables, open("srr2.vftables2.json", "w"), indent=2)

ctors = list()
for line in map_lines:
    if line["type"] == "symbol":
        mangled = line["value"]["mangled"]
        demangled = line["value"]["demangled"]
        if mangled.startswith("__"):
            if mangled == demangled:
                continue
            if mangled.startswith("__ti"):
                continue
            if mangled.startswith("__tf"):
                continue
            print(mangled)
            print(demangled)
            print(hex(line["address"]))
            print()
