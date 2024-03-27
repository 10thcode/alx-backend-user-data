#!/usr/bin/env python3
"""
defines filter_datum function
"""
from typing import List, Tuple
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records.
        """
        record.msg = filter_datum(self._fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return (super().format(record))


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


PII_FIELDS: Tuple = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Gets a logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)

    return logger
