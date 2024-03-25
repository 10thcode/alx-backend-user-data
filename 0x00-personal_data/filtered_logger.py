#!/usr/bin/env python3
"""
defines filter_datum function
"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """
    Replace occurrences of certain field values in a message
    """
    new_message: str = message

    for field in fields:
        new_message = re.sub("{}=(.*?){}".format(field, separator),
                             "{}={}{}".format(field, redaction, separator),
                             new_message)

    return new_message
