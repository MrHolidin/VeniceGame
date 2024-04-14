MAX_PRICE: int = 1_000_000_000
MIN_PRICE: int = 0


class CityInfo:
    def __init__(
        self,
        name: str,
        fee: float,
        country: str,
        product_buy_prices: dict[str, float],
        product_sell_prices: dict[str, float],
        products_capacities: dict[str, float],
    ):
        self.name: str = name
        self.fee: float = fee
        self.country: str = country
        self.product_buy_prices = product_buy_prices
        self.product_sell_prices = product_sell_prices
        self.product_capacities = products_capacities

    def get_buy_prices(self, product_name: str):
        if product_name in self.product_buy_prices.keys():
            return self.product_buy_prices[product_name]
        else:
            return MAX_PRICE

    def get_sell_prices(self, product_name: str):
        if product_name in self.product_sell_prices.keys():
            return self.product_sell_prices[product_name]
        else:
            return MIN_PRICE
