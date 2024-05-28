#!/usr/bin/env python3
""" Module that obuscates a log message"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
      Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: string representing fields to obuscate
        message: a string representing the log line
        separator: character separating fields
      Return:
        the log message obuscated
    """
    pattern = f'({"|".join(map(re.escape, fields))})=.*?{re.escape(separator)}'
    return re.sub(pattern,
                  lambda m: f'{m.group(1)}={redaction}{separator}', message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)
