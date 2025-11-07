#!/usr/bin/python3
import seed


def stream_users():
    """Generator that yields rows one by one from user_data."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    for row in cursor:
        yield row  # yields one dictionary per user

    cursor.close()
    connection.close()
