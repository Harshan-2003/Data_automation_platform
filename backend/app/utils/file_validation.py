ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json"}

def is_allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = "." + filename.split(".")[-1].lower()
    return ext in ALLOWED_EXTENSIONS
