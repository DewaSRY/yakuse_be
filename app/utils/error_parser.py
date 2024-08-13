import re


def find_errr_from_args(domain: str, message: str):
    result = re.findall(f"{domain}\\.(\\w+)", message)
    if len(result) == 0:
        return ""
    return result[0]
