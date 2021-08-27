#Dumps vftable pointers
#@author SHART
#@category SHART

# ea = address of original data (self for vftable, dereferenced pointer for vftable entry)
# vfptr = address of type info entry (node probably)
# demangled name includes namespace

import json
import os

from ghidra.program.model.data import Pointer32DataType, PointerDataType

base_dir = os.path.dirname(os.path.dirname(str(getSourceFile())))
lines = json.load(open(os.path.join(base_dir, "srr2.lines.json")))

listing = currentProgram.getListing()

vftables = dict()
for line in lines:
    if line["type"] == "symbol":
        if "virtual table" in line["value"]["demangled"]:
            address = line["address"]
            size = line["size"]
            class_name = line["value"]["demangled"].replace(" virtual table", "")

            vftables[class_name] = dict()
            vftables[class_name]["ea"] = hex(address)
            vftables[class_name]["length"] = int(size / 4)
            vftables[class_name]["vfptr"] = None
            vftables[class_name]["entries"] = list()
            
            print(class_name)
            print(toAddr(address))
            for i in range(int(size / 4)):
                data_address = address + i * 4
                data = listing.getDataAt(toAddr(data_address))
                if data:
                    removeData(data)
                listing.createData(toAddr(data_address), PointerDataType.dataType)

                data = listing.getDataAt(toAddr(data_address))
                if data.getValue() == toAddr(0):
                    continue
                print(data.getValue())
            exit()


print(len(lines))
