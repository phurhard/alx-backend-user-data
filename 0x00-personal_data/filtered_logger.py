#!/usr/bin/env python3
""" User dataPII
"""
import logging
import typing
import re


def filter_datum(fields: typing.List[str]=None, redaction: str="", message: str="",
        separator: str="") -> str:
    """Returns a log message upon which some certain parts are obfuscated
    """
    return re.sub(fr'(?<={separator})(?P<field>{"|".join(fields)})=(?=[^{separator}]+)', fr'\1{redaction}', message)



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: typing.List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        pass
