import os
import pytest

os.environ["ENV_FILE"] = ".env.test"

from database import get_connection
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def setup_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM price_history")
    cursor.execute("DELETE FROM products")

    cursor.execute("""
        INSERT INTO products (id, external_id, name)
        VALUES 
            (1, 'test-001', 'Test Keyboard'),
            (2, 'test-002', 'Test Mouse')
        """)

    cursor.execute("""
        INSERT INTO price_history (product_id, price)
        VALUES
            (1, 100.00),
            (1, 80.00),
            (2, 50.00)
        """)

    connection.commit()
    cursor.close()
    connection.close()


def test_get_products(setup_database):
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_product_fields(setup_database):
    response = client.get("/products")
    product = response.json()[0]

    assert "id" in product
    assert "external_id" in product
    assert "name" in product


def test_price_history(setup_database):
    response = client.get("/products/1/prices")
    history = response.json()

    assert response.status_code == 200
    assert len(history) == 2
    assert history[0]["price"] == 100.0
    assert history[1]["price"] == 80.0


def test_product_not_found(setup_database):
    response = client.get("/products/999999/prices")

    assert response.status_code == 404


def test_price_change(setup_database):
    response = client.get("/products/1/change")
    result = response.json()

    assert response.status_code == 200
    assert result["previous_price"] == 100.0
    assert result["current_price"] == 80.0
    assert result["change"] == -20.0
    assert result["percentage_change"] == -20.0


def test_not_enough_price_history_api(setup_database):
    response = client.get("/products/2/change")

    assert response.status_code == 200
    assert response.json() == {"message": "Not enough price history"}
