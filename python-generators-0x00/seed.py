#!/usr/bin/python3
import mysql.connector
import csv
import uuid


def connect_db():
    """Connects to MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"  # change to your local MySQL password if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()


def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # change this if needed
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Creates the user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()


def insert_data(connection, csv_file):
    """Inserts CSV data into the user_data table if not already inserted."""
    cursor = connection.cursor()
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            cursor.execute(
                "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, age)
            )
    connection.commit()
    cursor.close()
