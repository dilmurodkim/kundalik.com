def clean_name(name: str) -> str:
    name = name.lower().strip()
    suffixes = ["jon", "xon", "bek"]
    for suf in suffixes:
        if name.endswith(suf):
            name = name[:-len(suf)]
    return name.strip()
