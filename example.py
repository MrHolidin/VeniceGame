from data_reader import build_trade_map
import pandas as pd


turn = 3

products = pd.read_csv("data/products.csv")
prices_sell = pd.read_csv(f"data/turn{turn}/sell_prices.csv")
prices_buy = pd.read_csv(f"data/turn{turn}/buy_prices.csv")
routes = pd.read_csv(f"data/turn{turn}/routes.csv")
cities = pd.read_csv(f"data/turn{turn}/cities.csv")

trade_map = build_trade_map(cities, products, prices_buy, prices_sell, routes)
shortest_routes = trade_map.get_shortest_routes(with_water=False)

#### EXAMPLE
max_capital = 500000
max_weight = 1e9
delivery_fee = 1
product_routes = []
for (city_from, city_to), route in shortest_routes.items():
    for product in trade_map.products.keys():
        stat = trade_map.get_stat(route, product, max_weight, max_capital, delivery_fee)
        stat["product"] = product
        product_routes.append(stat)

print(pd.DataFrame(product_routes).reset_index()[:5])
df = pd.DataFrame(product_routes).sort_values("max_profit", ascending=False)
df = df[df["length"] <= 2]
print(df[:20])
