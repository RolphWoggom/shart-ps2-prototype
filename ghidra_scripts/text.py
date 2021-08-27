# shart
#@author shart
#@category shart
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.program.model.symbol.SourceType import *
from ghidra.program.model.data import *
import json

print("dfsdasdf")

addressFactory = currentProgram.getAddressFactory()
functionManager = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
memory = currentProgram.getMemory()

balls = json.load(open("/home/user/projects/shart-ps2-prototype/map.json"))

def intToAddress(addr):
    return addressFactory.getAddress(hex(addr))

for sym in balls[".text"]:
    # print(sym["name"]["cleaned"])
    name = sym["name"]["cleaned"]
    func_addr = sym["address"]

    func = functionManager.getFunctionAt(intToAddress(func_addr))

    if func != None:
        old_name = func.getName()
        func.setName(name, USER_DEFINED)
        print "%s renamed as %s" % (old_name, name)
    else:
        func = createFunction(intToAddress(func_addr), name)
        print "Created function %s" % name
    func.setComment(sym["name"]["demngld"])

from ghidra.program.model.symbol import SourceType
for sym in balls[".data"] + balls[".rodata"] + balls[".sbss"] + balls[".bss"]:
    d = listing.getDataAt(intToAddress(sym["address"]))
    if not d:
        print("No data for %s" % sym["name"]["demngld"])
        continue
    ps = d.getPrimarySymbol()
    if ps:
        ps.setName(sym["name"]["cleaned"], SourceType.USER_DEFINED)
    else:
        print("No primary symbol for %s" % sym["name"]["demngld"])
