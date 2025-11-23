#!/usr/bin/python3
import seed


def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from the DB in batches.
    Uses yield to return one batch (list of dicts) at a time.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    batch = []
    for row in cursor:   # loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch   # yield each full batch
            batch = []

    if batch:
        yield batch       # yield remaining rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Generator that processes each batch and yields users over 25.
    Uses yield to stream processed users instead of storing all in memory.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:                             # loop 3
            if user["age"] > 25:
                yield user  

def batch_processing(batch_size):
    """Processes users in batches and prints users older than 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
