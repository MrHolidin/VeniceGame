import pandas as pd
from enum import Enum
from product import ProductInfo, ProductDemand, get_capacity_estimations
from city import CityInfo
from route import Route, RouteType, connect_routes
from trade_map import TradeMap


def convert_prices(prices: pd.DataFrame):
    prices = prices.rename(columns={"Товары": "Product"})
    melted_data = pd.melt(prices, id_vars=["Product"], var_name="City", value_name="Price")
    melted_data = melted_data.dropna(subset=["Price"])
    # Converting prices to float, ensuring correct data type
    melted_data["Price"] = pd.to_numeric(melted_data["Price"].astype(str).str.replace(",", "."), errors="coerce")
    melted_data_clean = melted_data.dropna(subset=["Price"])

    # Now, creating the dictionary with the clean data
    prices_dict_clean = {
        (row["City"], row["Product"]): float(row["Price"]) for index, row in melted_data_clean.iterrows()
    }
    return prices_dict_clean


def build_trade_map(
    cities_df: pd.DataFrame,
    products_df: pd.DataFrame,
    prices_buy: pd.DataFrame,
    prices_sell: pd.DataFrame,
    routes_df: pd.DataFrame,
) -> TradeMap:
    products: dict[str, ProductInfo] = {}
    for _, row in products_df.iterrows():
        products[row["Продукт"]] = ProductInfo(
            row["Продукт"],
            float(row["Вес"]),
            row["Стандартная цена"],
            row["Стандартная вместимость"],
            ProductDemand(row["Востребованность"]),
        )
    buy_dict = convert_prices(prices_buy)
    sell_dict = convert_prices(prices_sell)
    cities: dict[str, CityInfo] = {}

    for _, row in cities_df.iterrows():
        city_name = row["Город"]
        cities[city_name] = CityInfo(
            city_name,
            float(row["Торговый сбор, %"]) * 0.01,
            row["Страна"],
            product_buy_prices={product: price for ((city, product), price) in buy_dict.items() if city == city_name},
            product_sell_prices={product: price for ((city, product), price) in sell_dict.items() if city == city_name},
            products_capacities=get_capacity_estimations(
                list(products.values()),
                {
                    ProductDemand.HIGH: row["Вместимость высоких"],
                    ProductDemand.MEDIUM: row["Вместимость средних"],
                    ProductDemand.LOW: row["Вместимость низких"],
                },
            ),
        )
    routes: list[Route] = []
    for _, row in routes_df.iterrows():
        route = Route(
            row["A"],
            row["B"],
            float(row["Время"].replace(",", ".")),
            row["Тип"],
            disaster_risk_per_unit=row["Disaster risk"],
            assault_risk_per_unit=row["Assault risk"],
        )
        routes.append(route)
        routes.append(route.get_reverse())
    trade_map = TradeMap(cities, products, routes)
    return trade_map


turn = 3

products = pd.read_csv("data/products.csv")
prices_sell = pd.read_csv(f"data/turn{turn}/sell_prices.csv")
prices_buy = pd.read_csv(f"data/turn{turn}/buy_prices.csv")
routes = pd.read_csv(f"data/turn{turn}/routes.csv")
cities = pd.read_csv(f"data/turn{turn}/cities.csv")

trade_map = build_trade_map(cities, products, prices_buy, prices_sell, routes)
