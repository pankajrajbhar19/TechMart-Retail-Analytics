import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

base_dir = "data"
os.makedirs(base_dir, exist_ok=True)

n_customers = 5000
n_products = 150
n_stores = 20
n_transactions = 50000

cities = ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
states = ["Delhi", "Maharashtra", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal", "Maharashtra", "Gujarat"]
categories = ["Smartphone", "Laptop", "Accessory", "Tablet", "TV"]
price_ranges = {
    "Smartphone": (12000, 60000),
    "Laptop":     (35000, 120000),
    "Accessory":  (300, 5000),
    "Tablet":     (8000, 45000),
    "TV":         (15000, 90000),
}
discount_levels = [0.0, 0.05, 0.10, 0.15, 0.20]
regions = ["North", "South", "East", "West"]

# 1) Customers
customers = pd.DataFrame({
    "customer_id": np.arange(1, n_customers + 1),
    "city": np.random.choice(cities, n_customers),
    "state": np.random.choice(states, n_customers),
    "age": np.random.randint(18, 60, n_customers),
    "gender": np.random.choice(["M", "F"], n_customers),
})
customers.to_csv(os.path.join(base_dir, "customers.csv"), index=False)

# 2) Products
products = pd.DataFrame({
    "product_id": np.arange(1, n_products + 1),
    "category": np.random.choice(categories, n_products, p=[0.35, 0.25, 0.25, 0.10, 0.05]),
    "brand": np.random.choice(["TechPro", "SmartX", "Nova", "Zenith", "Electra"], n_products),
})
products["unit_price"] = products["category"].apply(
    lambda c: np.random.randint(*price_ranges[c])
)
products.to_csv(os.path.join(base_dir, "products.csv"), index=False)

# 3) Stores
stores = pd.DataFrame({
    "store_id": np.arange(1, n_stores + 1),
    "city": np.random.choice(cities, n_stores),
    "region": np.random.choice(regions, n_stores),
})
stores.to_csv(os.path.join(base_dir, "stores.csv"), index=False)

# 4) Transactions
start_date = datetime(2023, 1, 1)
order_dates = [
    start_date + timedelta(days=int(x))
    for x in np.random.randint(0, 365, n_transactions)
]

transactions = pd.DataFrame({
    "order_id": np.arange(1, n_transactions + 1),
    "order_date": order_dates,
    "customer_id": np.random.choice(customers["customer_id"], n_transactions),
    "product_id": np.random.choice(products["product_id"], n_transactions),
    "store_id": np.random.choice(stores["store_id"], n_transactions),
    "quantity": np.random.randint(1, 5, n_transactions),
    "discount_pct": np.random.choice(discount_levels, n_transactions),
})

transactions = transactions.merge(
    products[["product_id", "unit_price", "category"]],
    on="product_id",
    how="left"
)
transactions["selling_price"] = (
    transactions["unit_price"] * (1 - transactions["discount_pct"])
).round(2)
transactions.drop(columns=["unit_price"], inplace=True)

transactions.to_csv(os.path.join(base_dir, "transactions.csv"), index=False)

print("✅ Data generated successfully in ./data folder")

