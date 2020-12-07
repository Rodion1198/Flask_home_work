import os
import sqlite3
from faker import Faker


fake = Faker()

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def generate_user(count=0):
    for _ in range(count):
        name = fake.name()
        yield name


def init_database():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS customers
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL)"""
            )
            # for user in generate_user(15):
            #     cursor.execute(
            #         """INSERT INTO customers(name) VALUES (?)""",
            #         [user]
            #     )
            cursor.execute("""CREATE TABLE IF NOT EXISTS tracks
                (id_track INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT NOT NULL,
                track TEXT NOT NULL,
                duration REAL NOT NULL)"""
                           )


def exec_query(query, *args):
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            qs = cursor.execute(query, args)
            results = qs.fetchall()
    return results


if __name__ == "__main__":
    init_database()