#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")

    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()


def average_age():
    """Compute average age using generator (no full dataset in memory)."""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    avg = total / count if count else 0
    print(f"Average age of users: {avg:.2f}")
    return avg
