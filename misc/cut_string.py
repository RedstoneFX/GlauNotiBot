def cut_string(string: str, max_chars: int):
    if len(string) <= max_chars:
        return string
    else:
        return string[max_chars-3] + "..."

