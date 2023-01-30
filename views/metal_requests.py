import sqlite3
import json
from models import Metal


METALS = [
    {
        "id": 1,
        "metal": "Sterling Silver",
        "price": 12.42
    },
    {
        "id": 2,
        "metal": "14k Gold",
        "price": 736.4
    },
    {
        "id": 3,
        "metal": "24k Gold",
        "price": 1258.9
    },
    {
        "id": 4,
        "metal": "Platinum",
        "price": 795.45
    },
    {
        "id": 5,
        "metal": "Palladium",
        "price": 1241.0
    }
]


def get_all_metals():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        """)

        metals = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            metal = Metal(row['id'], row['metal'], row['price'])
            
            metals.append(metal.__dict__)


    return metals

def get_single_metal(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        WHERE m.id = ?
        """, (id,))

        data = db_cursor.fetchone()

        metal = Metal(data['id'], data['metal'], data['price'])

        return metal.__dict__


def update_metal(id, new_metal):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Metals
            SET
                metal = ?,
                price = ?
        WHERE id = ?
        """, (new_metal['metal'], new_metal['price'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True