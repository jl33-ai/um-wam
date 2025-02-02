import re


def to_list(text):
    """Extracts all numbers from a blob of text"""
    return re.findall(r'\d+', text)
