#Find class sizes
#@author SHART
#@category SHART

from ghidra.program.model.data import PointerDataType, Pointer, IntegerDataType
from ghidra.program.model.symbol import SourceType
from ghidra.util.task import TaskMonitor
from ghidra.program.model.lang import RegisterValue

log_lines = False
log_calling_funcs = True

# these need their parameters to be set already
new_operators = [
    [0x00166b78, "operator new(unsigned int, GameMemoryAllocator)"],
    [0x00183db0, "AnimatedIcon::operator new(unsigned int)"],
    [0x00183e20, "AnimatedIcon::operator new(unsigned int, GameMemoryAllocator)"],
    [0x0032d870, "tRefCountedTemp::operator new(unsigned int)"],
    [0x003c4900, "radTimer::operator new(unsigned int, radTimerList *)"],
    [0x003c6be0, "ExternalMemoryHeap::operator new(unsigned int, int)"],
    [0x003c8c38, "MemorySpaceAsyncRequest::operator new(unsigned int, char const *)"],
    [0x003ca180, "MemoryPool::operator new(unsigned int, int)"],
    [0x003e2830, "radRequest::operator new(unsigned int)"],
    [0x003e5448, "radFile::operator new(unsigned int)"],
    [0x003e6390, "radInstanceDrive::operator new(unsigned int)"],
    [0x003ed548, "radLoadObject::operator new(unsigned int)"],
    [0x003ed568, "radLoadObject::operator new(unsigned int, int)"],
    [0x00166938, "__builtin_new(unsigned int)"],

    # size as second arg
    [0x003c7a28, "radMemoryAlloc(int, unsigned int)"],
]

import time

function_manager = currentProgram.getFunctionManager()

decomp_interface = ghidra.app.decompiler.DecompInterface()
decomp_interface.openProgram(currentProgram)

def decompile_function(function):
    decompiled = decomp_interface.decompileFunction(
        function,
        12,
        TaskMonitor.DUMMY
    )
    while not decompiled.decompileCompleted():
        time.sleep(1)
    return decompiled

def get_c(function):
    return decompile_function(function).getDecompiledFunction().getC()

def get_function_body(function):
    function_string = decompile_function(function).getCCodeMarkup().getClangFunction().toString()
    function_body = "{" + "{".join(function_string.split("{")[1:])
    for c in [";", "{", "}"]:
        function_body = (c + "\n").join(function_body.split(c))
    function_body_lines = function_body.split("\n")

    function_body = ""
    indent = 0
    for line in function_body_lines:
        if "}" in line:
            indent -= 1
        if "LAB_" in line:
            label = line.split(":")[0] + ":"
            function_body += label + "\n"
            line = line.replace(label, "")
        function_body += indent * "  "
        function_body += line
        function_body += "\n"
        if "{" in line:
            indent += 1
    function_body.strip()
    
    return function_body

# for addr, name in new_operators:
#     print(name)
#     op_new_func = decomp_interface.decompileFunction(
#         function_manager.getFunctionAt(toAddr(addr)),
#         99999999,
#         TaskMonitor.DUMMY
#     )
#     while not op_new_func.decompileCompleted():
#         time.sleep(1)

#     calling_funcs = list(set(op_new_func.getCallingFunctions(TaskMonitor.DUMMY)))
#     for calling_func in calling_funcs:
#         c_code = calling_func.getDecompiledFunction().getC()
#         c_lines = c_code.split("\n")
#         print(c_lines)
#         break

#     break
#     print()
#     # print(op_new_func.getDecompiledFunction().getC())

#     c_code_markup = op_new_func.getCCodeMarkup()
#     for i in range(c_code_markup.numChildren()):
#         print(c_code_markup.Child(i))

#     break

# exit()

results = dict()

function_manager = currentProgram.getFunctionManager()
for addr, name in new_operators:
    print("\n------- %s -------\n" % name)
    op_new_func = function_manager.getFunctionAt(toAddr(addr))
    op_new_func.setReturnType(PointerDataType.dataType, SourceType.USER_DEFINED)

    op_new_func.setComment(name)

    # op_new_func_name = name.split("(")[0].replace(" ", "_")
    op_new_func_name = "tmpname" + hex(addr)
    # print(op_new_func_name)
    # print

    op_new_func.setName(op_new_func_name, SourceType.USER_DEFINED)

    op_new_func_name_decomp = op_new_func_name.replace(":", "_")

    # op_new_func.updateFunction(None, None, newparams, asd, False, None)

    calling_funcs = list(set(op_new_func.getCallingFunctions(TaskMonitor.DUMMY)))
    # print("calling func count:", len(calling_funcs))
    # print(calling_funcs)

    for calling_func in calling_funcs:
        if log_calling_funcs:
            print
            print(">>>>>>>calling func: %s" % calling_func)
            print

        # print(get_function_body(calling_func))
        # exit()

        # c_code = get_c(calling_func).split("{")
        # c_code_skip = len(c_code[0].split("\n"))
        # c_code = "{".join(c_code[1:])
        # c_lines = c_code.split("\n")
        # print("************ c code")
        # print(c_code)
        var = None
        size = None
        # for line_num, line in enumerate(c_lines, c_code_skip):
        for line_num, line in enumerate(get_function_body(calling_func).split("\n")):
            if var:
                # print(line)
                # print(var, size)
                if var in line:
                    if "Allocate" in line or "goto" in line:
                        continue
                    # print(line_num, line)
                    # print
                    if log_lines:
                        print(line)
                        print

                    # assignemnts
                    for segment in line.split("="):
                        if var in segment:
                            target_class = segment.strip()
                    
                    # casts
                    if target_class[0] == "(":
                        target_class = target_class.split(")")[1].strip()
                    
                    # parameters
                    target_class = target_class.split("(")[0]

                    # target_class = target_class.split(var)[0]
                    # target_class = target_class.split("(")[-2]
                    # target_class = target_class.split(" ")[-1]
                    # target_class = target_class.replace("*)", "")

                    # print(op_new_func_name, target_class, var, size)

                    if target_class == "":
                        print("TARGETCLASSEMPTY TARGETCLASSEMPTY TARGETCLASSEMPTY TARGETCLASSEMPTY ")
                        var = None
                        size = None
                        continue

                    # print(".......... %s ..........size: %s" % (target_class, hex(size)))

                    func_addresses = getGlobalFunctions(target_class)

                    if len(func_addresses) > 1:
                        address = "MULTIFUN"
                    elif len(func_addresses) == 1:
                        address = func_addresses[0].getEntryPoint()
                    else:
                        # if target_class in ["*", "puVar1;", "piVar2[3]"]:
                        #     # ps2context[0x104] ??? what is it, some kind of lookup table?
                        #     # tLoadRequest::tLoadRequest
                        #     # pddiBaseContext::BuildMatrixStacks
                        #     var = None
                        #     size = None
                        #     continue
                        # else:
                        #     print("ERROR FINDING %s" % target_class)
                        #     exit()
                        if name == "__builtin_new(unsigned int)":
                            print "FAIL FAILE FAIL FAIL __builtin_new %s" % calling_func
                            var = None
                            size = None
                            continue
                        else:
                            print "FAAAAAAAAAAAAAAIIIIIIIIL %s " % calling_func
                            var = None
                            size = None
                            continue
                        

                    # print("%s %s - %s " % (hex(size).rjust(6), address, target_class))

                    if target_class not in results:
                        results[target_class] = dict()
                    if hex(size) not in results[target_class]:
                        results[target_class][hex(size)] = 1
                    else:
                        results[target_class][hex(size)] += 1


                    var = None
                    size = None
            else:
                if op_new_func_name_decomp in line:
                    if log_lines:
                        print(line)

                    var = line.split("=")[0].strip()
                    if "radMemoryAlloc" not in name:
                        size = line.split(op_new_func_name_decomp + "(")[1].split(")")[0].split(",")[0]
                    else:
                        size = line.split(op_new_func_name_decomp + "(")[1].split(",")[1].replace(");", "")

                    # size = int(size, 16)
                    
                    if "(" in size:
                        # print("SKIPSKIPSKIPSKIP", line)
                        var = None
                        size = None
                    else:
                        try:
                            size = int(size, 16)
                        except:
                            print("SIZE SKIP SIZE SKIP SIZE SKIP %s" % line)
                            var = None
                            size = None
                        # print("debug: set size and var", size, var)
                elif op_new_func_name in line:
                    print("NAMENAMENAMENAMENAMENAME", line)
        # break

    # break
    # continue
    # print(op_new_func.getSignature())
    # # continue
    # # print(calling_funcs)

    

    # for calling_func in calling_funcs:
    #     print("op new func:", op_new_func)
    #     print("calling func:", calling_func)

    #     for called_func in calling_func.getCalledFunctions(TaskMonitor.DUMMY):
    #         # find op new usage
    #         if called_func.getEntryPoint() == op_new_func.getEntryPoint():
    #             size = called_func.getParameters()[0]
    #             print(size)
    #             print(RegisterValue(size.getRegister()))
    #             # print(size.getFormalDataType().getValue())

    # # get size from it
    # # get return param
    # # get return param usage
    # # save usage funcation and size
    # print("\n\n")

results_sorted = dict()
for key in sorted(results.keys(), key=unicode.lower):
    results_sorted[key] = results[key]
results = results_sorted

# print("-----------------")
# for target_class in results:
#     for size in results[target_class]:
#         print("%s %s %u" % (target_class, size, results[target_class][size]))
#     print("-----------------")
print("classes count: %u" % len(results.keys()))

import os
import json

base_dir = os.path.dirname(os.path.dirname(str(getSourceFile())))
results_json_file = os.path.join(base_dir, "auto_class_sizes.json")
json.dump(results, open(results_json_file, "w"), indent=2)