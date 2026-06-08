import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.repository import ProductRepository, CartRepository
from src.domain import Product
from src.app import app
from src.app import repo

# 1. Тести для Domain Model
def test_product_creation():
    p = Product(1, "Test", 100.0)
    assert p.id == 1
    assert p.name == "Test"
    assert p.price == 100.0

# 2. Тести для логіки знижок
@pytest.mark.parametrize("quantity, price, expected_total", [
    (1, 100, 100), (2, 100, 200), (3, 100, 300),  # Без знижки
    (4, 100, 360), (5, 100, 450), (10, 100, 900), # Зі знижкою
    (0, 100, 0), (100, 10, 900)                   # Граничні випадки
])
def test_cart_discount_logic(quantity, price, expected_total):
    cart = CartRepository()
    for _ in range(quantity):
        cart.add(Product(1, "Item", price))
    assert cart.get_total() == expected_total

# 3. Тести для додавання/видалення товарів
@pytest.mark.parametrize("add_count, remove_id, expected_len", [
    (1, 1, 0), (2, 1, 1), (5, 1, 4), (1, 99, 1) 
])
def test_cart_add_remove(add_count, remove_id, expected_len):
    cart = CartRepository()
    for i in range(add_count):
        cart.add(Product(i+1, f"Item{i}", 100))
    cart.remove(remove_id)
    assert len(cart.get_all()) == expected_len

# 4. Тести репозиторію
@pytest.mark.parametrize("prod_id", range(1, 151))
def test_repository_get_by_id(prod_id):
    repo = ProductRepository()
    product = Product(prod_id, f"Prod{prod_id}", 10.0)
    repo._products[prod_id] = product 
    found = repo.get_by_id(prod_id)
    assert found is not None
    assert found.id == prod_id

# 5. Тести граничних випадків
@pytest.mark.parametrize("price, name", [
    (0.01, "Cheap"), (999999.99, "Expensive"), (123.45, "Normal"),
    (0.0, "Free"), (-10.0, "Negative")
])
def test_product_boundary_cases(price, name):
    p = Product(1, name, price)
    assert p.name == name
    assert p.price == price

# 6. Тести комбінацій
@pytest.mark.parametrize("val", range(100, 150))
def test_cart_total_combinations(val):
    cart = CartRepository()
    cart.add(Product(1, "Test", float(val)))
    assert cart.get_total() == float(val)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 7. Тести для маршрутів Flask (додають покриття app.py)
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_cart_route(client):
    response = client.get('/cart')
    assert response.status_code == 200

def test_add_to_cart_route(client):
    # 1. SETUP: Додаємо тестовий товар в репозиторій перед тестом
    # Якщо твій репозиторій використовує словник:
    repo._products[1] = Product(1, "TestItem", 100) 
    
    # 2. Виконуємо запит
    response = client.get('/add_to_cart/1', follow_redirects=True)
    
    # 3. Перевіряємо
    assert response.status_code == 200
    assert b'TestItem' in response.data # Тепер ми точно знаємо, що шукати

def test_remove_from_cart_route(client):
    # Спочатку додаємо товар, потім видаляємо
    client.get('/add_to_cart/1', follow_redirects=True)
    response = client.get('/remove_from_cart/1', follow_redirects=True)
    assert response.status_code == 200