

def get_charset(option: str) -> str:
    # e.g., "lower", "upper", "digits", "all"
    charsets = {
        "lower": "abcdefghijklmnopqrstuvwxyz",
        "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digits": "0123456789",
        "all": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    }
    return charsets.get(option, charsets["all"])