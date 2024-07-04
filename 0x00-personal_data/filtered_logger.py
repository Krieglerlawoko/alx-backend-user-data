#!/usr/bin/env python3
import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Obfuscate specified fields in a log message.

    Args:
        fields: List of fields to obfuscate.
        redaction: String to replace field values with.
        message: Log message.
        separator: Field separator in the log message.

    Returns:
        Obfuscated log message.
    """
    for field in fields:
        pattern = f"{field}=[^{separator}]*"
        replacement = f"{field}={redaction}"
        message = re.sub(
            pattern,
            replacement,
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record, obfuscating specified fields.

        Args:
            record: LogRecord instance.

        Returns:
            Formatted log message with obfuscated fields.
        """
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connects to a MySQL database using environment variables.

    Returns:
        MySQLConnection object.
    """
    db_config = {
        "user": os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        "password": os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        "host": os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        "database": os.getenv("PERSONAL_DATA_DB_NAME")
    }
    return mysql.connector.connect(**db_config)


def main() -> None:
    """
    Main function that retrieves and logs user data from the database.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    for row in cursor:
        user_data = {
            "name": row[0],
            "email": row[1],
            "phone": row[2],
            "ssn": row[3],
            "password": row[4],
            "ip": row[5],
            "last_login": row[6],
            "user_agent": row[7]
        }
        message = ";".join([
            f"{key}={value}" for key, value in user_data.items()
        ])
        logger.info(message)

    cursor.close()
    db.close()

if __name__ == '__main__':
    main()
