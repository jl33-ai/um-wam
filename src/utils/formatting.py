import re
from typing import List


def to_list(text) -> List:
    """Extracts all numbers from a blob of text"""
    if not text:
        return []

    matches = re.findall(r'\d+', str(text))
    return [int(match) for match in matches]
