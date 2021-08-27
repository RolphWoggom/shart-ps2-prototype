import json

ctors = set()

lines = json.load(open("srr2.lines.json"))
auto_class_sizes = json.load(open("auto_class_sizes.json"))

not_in_auto_class_sizes = 0

for line in lines:
    if line["type"] == "symbol":
        mangled = line["value"]["mangled"]
        demangled = line["value"]["demangled"]
        if mangled.startswith("__"):
            if mangled[3].isnumeric() or mangled[3] == "Q":
                cleaned_name = demangled.replace(" ", "_").split("(")[0]
                if cleaned_name not in auto_class_sizes:
                    # print(cleaned_name)
                    not_in_auto_class_sizes += 1
                    if "<" not in cleaned_name:
                        ctors.add(cleaned_name)


print("-" * 12)
print(f"{len(ctors)=}")
print(f"{not_in_auto_class_sizes=}")
print(f"{len(auto_class_sizes.keys())=}")
print("-" * 12)

for ctor in ctors:
    print(ctor)

# for key, element in auto_class_sizes.items():
#     if len(element.keys()) > 1:
#         print(key)
#         print(json.dumps(element, indent=2))
#         print()
