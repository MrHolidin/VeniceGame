from product import ProductInfo
from city import CityInfo
from route import Route, RouteType, connect_routes
import numpy as np


class TradeMap:
    def __init__(
        self,
        cities: dict[str, CityInfo],
        products: dict[str, ProductInfo],
        routes: list[Route],
    ):
        self.cities: dict[str, CityInfo] = cities
        self.products: dict[str, ProductInfo] = products
        self.routes: list[Route] = routes

    def get_shortest_routes(self, with_land=True, with_water=True) -> dict[tuple[str, str], Route]:
        def is_good_route(type: RouteType):
            if with_land and type == RouteType.LAND:
                return True
            if with_water and type == RouteType.WATER:
                return True
            if with_land and with_water and type == RouteType.MIXED:
                return True
            return False

        simple_routes = filter(lambda route: is_good_route(route.route_type), self.routes)
        expanded_routes: dict[tuple[str, str], Route] = {
            (route.city_from, route.city_to): route for route in simple_routes
        }
        # Floyd-Warshall algorithm
        for mid_name in self.cities.keys():
            for from_name in self.cities.keys():
                for to_name in self.cities.keys():
                    if (from_name, mid_name) in expanded_routes and (mid_name, to_name) in expanded_routes:
                        united_route = connect_routes(
                            expanded_routes[(from_name, mid_name)], expanded_routes[(mid_name, to_name)]
                        )
                        if (from_name, to_name) not in expanded_routes or expanded_routes[
                            (from_name, mid_name)
                        ].length > united_route.length:
                            expanded_routes[(from_name, mid_name)] = united_route

        return expanded_routes

    def add_city(self, city: CityInfo):
        self.cities[city.name] = city

    def add_product(self, product: ProductInfo):
        self.products[product.name] = product

    def add_route(self, route: Route):
        self.routes.append(route)

    def get_stat(
        self, route: Route, product: str, max_weight: float, max_capital: float, delivery_fee_by_unit: float = 0
    ) -> dict[str, float | str]:
        price_to = self.cities[route.city_to].get_sell_prices(product)
        price_from = self.cities[route.city_from].get_buy_prices(product)
        effective_price_diff = price_from * (1 - self.cities[route.city_to].fee) - price_to
        max_product_amount = min(
            self.cities[route.city_from].product_capacities[product],
            self.cities[route.city_to].product_capacities[product],
            max_capital / (delivery_fee_by_unit * self.products[product].weight + price_from),
            self.products[product].max_amount_by_weight(max_weight),
        )
        max_profit = max(0, max_product_amount * effective_price_diff)
        return {
            "city_from": route.city_from,
            "city_to": route.city_to,
            "route_type": str(route.route_type),
            "effective_price_diff": effective_price_diff,
            "max_amount": max_product_amount,
            "max_profit": max_profit,
            "profitness": max_profit / max_product_amount,
        }
