@staticmethod
def get_clean_list_from_string(string: str, separator: str):
    #converts string to list without empty values based on separator
    return [s.strip() for s in string.split(separator) if s.strip()]