import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

ENV_FILE = os.getenv("ENV_FILE", ".env")
load_dotenv(ENV_FILE)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row,
    )


def save_product(external_id, name, price):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE external_id = %s
        """,
        (external_id,),
    )

    product = cursor.fetchone()

    if product:
        product_id = product["id"]

    else:
        cursor.execute(
            """
            INSERT INTO products (external_id, name)
            VALUES (%s, %s)
            RETURNING id
            """,
            (external_id, name),
        )
        product_id = cursor.fetchone()["id"]

    cursor.execute(
        """
        INSERT INTO price_history (product_id, price)
        VALUES (%s, %s)
        """,
        (product_id, price),
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM products
    """)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


def get_price_history(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM price_history
        WHERE product_id = %s
        ORDER BY recorded_at
        """,
        (product_id,),
    )

    price_history = cursor.fetchall()

    cursor.close()
    connection.close()

    return price_history


def get_product(product_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id = %s
        """,
        (product_id,),
    )

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return product
