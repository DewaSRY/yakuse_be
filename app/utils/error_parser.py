import re


def find_errr_from_args(domain: str, message: str):
    result = re.findall("users\\.(\\w+)", message)
    return result[0]
