from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float

@dataclass
class Order:
    id: int
    product_ids: list[int]
    total_price: float