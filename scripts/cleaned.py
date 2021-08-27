    symbol = line[48:]
    symbol_mangled = mangled_map[line_number][48:]

    cleaned = symbol.split("(")[0]
    cleaned = cleaned.replace(" type_info ", "::__type_info__")
    cleaned = cleaned.replace(" virtual table", "::__virtual_table")
    if "operator" in cleaned:
        cleaned = cleaned.replace(" ", "_")
    if "global" in cleaned:
        if "deconstructors" in cleaned:
            de = True
        else:
            de = False
        cleaned = cleaned.split(" ")[-1]
        cleaned += "__global_"
        if de:
            cleaned += "de"
        cleaned += "constructors"
    cleaned = cleaned.replace(" ", "")

    if " " in cleaned and "<" not in cleaned:
        print(size, cleaned)

    if "(" in symbol:
        args = symbol.split("(")[1].split(")")[0].split(",")
        if len(args):
            args = [arg.strip() for arg in args]
            for arg in args:
                unique_args.add(arg)

    symbols[section].append({
        "address": address,
        "size": size,
        "align": align,
        "filename": filename,
        "name": {
            "mangled": symbol_mangled,
            "demngld": symbol,
            "cleaned": cleaned
        }
    })

