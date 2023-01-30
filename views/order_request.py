import sqlite3
import json
from models import Metal
from models import Size
from models import Style
from models import Order
from .metal_requests import get_single_metal

ORDERS = [
    {
        "id": 1,
        "metal_id": 6,
        "size_id": 3,
        "style_id": 2,
        "timestamp": 12345
    }
]

def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp,
            m.metal metal_metal,
            m.price metal_price,
            s.carets size_carets,
            s.price size_price,
            y.style style_style,
            y.price style_price
        FROM Orders o
        JOIN Metals m
            ON m.id = o.metal_id
        JOIN Sizes s
            ON s.id = o.size_id
        JOIN Styles y
            ON y.id = o.style_id
        """)

        orders = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            order = Order(row['id'], row['metal_id'], row['size_id'], row['style_id'],
                            row['timestamp'])
            metal = Metal(row['metal_id'], row['metal_metal'], row['metal_price'])
            size = Size(row['size_id'], row['size_carets'], row['size_price'])
            style = Style(row['style_id'], row['style_style'], row['style_price'])

            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

            orders.append(order.__dict__)

    return orders

def get_single_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.timestamp,
            m.metal metal,
            m.price metal_price,
            s.carets size_carets,
            s.price size_price,
            y.style style,
            y.price style_price
        FROM Orders o
        JOIN Metals m
            ON m.id = o.metal_id
        JOIN Sizes s
            ON s.id = o.size_id
        JOIN Styles y
            ON y.id = o.style_id
        WHERE o.id = ?
        """, ( id, ))

        orders = []

        dataset = db_cursor.fetchall()

        for data in dataset:
            order = Order(data['id'], data['metal_id'], data['size_id'], data['style_id'],
                                data['timestamp'])
            metal = Metal(data['metal_id'], data['metal'], data['metal_price'])
            size = Size(data['size_id'], data['size_carets'], data['size_price'])
            style = Style(data['style_id'], data['style'], data['style_price'])

            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

            orders.append(order.__dict__)

        return order.__dict__


def create_order(new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id, timestamp )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_order['metal_id'],
            new_order['size_id'], new_order['style_id'],
            new_order['timestamp'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the order dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_order['id'] = id


    return new_order


def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Orders
        WHERE id = ?
        """, (id, ))
