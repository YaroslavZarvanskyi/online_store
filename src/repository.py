import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from domain import Product

class ProductRepository:
    def __init__(self):
        # Ініціалізуємо тестовими даними
        self._products = {
            1: Product(1, "Ноутбук", 25000.0),
            2: Product(2, "Мишка", 500.0),
            3: Product(3, "Клавіатура", 1500.0)
        }

    def get_all(self):
        return list(self._products.values())
    
    def get_by_id(self, product_id):
        return self._products.get(product_id)
    
class CartRepository:
    def __init__(self):
        self._items = []

    def add(self, product: Product):
        self._items.append(product)

    def remove(self, product_id):
        for i, item in enumerate(self._items):
            if item.id == product_id:
                self._items.pop(i)
                break

    def get_all(self):
        return self._items
    
    def get_total(self):
        total = sum(item.price for item in self._items)
        # Логіка: знижка 10% якщо товарів > 3
        if len(self._items) > 3:
            return total * 0.9
        return total