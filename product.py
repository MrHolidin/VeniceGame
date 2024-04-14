from enum import Enum
import numpy as np


class ProductDemand(Enum):
    HIGH = "Высокая"
    MEDIUM = "Средняя"
    LOW = "Низкая"


class ProductInfo:
    def __init__(self, name: str, weight: float, standard_price: int, standard_capacity: int, demand: ProductDemand):
        self.name = name
        self.weight = weight
        self.standard_price = standard_price
        self.standard_capacity = standard_capacity
        self.demand = demand

    def max_amount_by_weight(self, allowed_weight: float):
        return np.inf if self.weight == 0 else allowed_weight / self.weight


def get_capacity_estimations(
    products: list[ProductInfo], capacity_by_demand: dict[ProductDemand, int]
) -> dict[str, float]:
    sorted_capacities = sorted([product.standard_capacity for product in products])
    capacity_multiplyer = {
        ProductDemand.HIGH: capacity_by_demand[ProductDemand.HIGH] / sorted_capacities[-1],
        ProductDemand.MEDIUM: capacity_by_demand[ProductDemand.MEDIUM] / sorted_capacities[len(products) // 2],
        ProductDemand.LOW: capacity_by_demand[ProductDemand.LOW] / sorted_capacities[0],
    }
    return {product.name: product.standard_capacity * capacity_multiplyer[product.demand] for product in products}
