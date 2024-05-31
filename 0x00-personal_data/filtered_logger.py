#!/usr/bin/env python3
""" Module that obuscates a log message"""
from mysql.connector import connection
import mysql.connector
from typing import List
import re
import logging
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        """Intializes the class with correct arguments"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """This method filters data using the filter_datum method"""
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates and returns a logger named 'user_data
    with specific configuration"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MYSQLConnection:
    """REturns a connector to the database"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    if not database:
        raise ValueError(
            "Database name must be set in PERSONAL_DATA_DB_NAME environment variable")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
