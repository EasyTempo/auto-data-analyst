import pandas as pd
import numpy as np

# 1. Text Data: ecommerce_reviews.csv
reviews = [
    {"review_id": 1, "product_id": "P001", "rating": 5, "review_text": "Absolutely love this product! The quality is amazing and it arrived so fast. Excellent."},
    {"review_id": 2, "product_id": "P001", "rating": 2, "review_text": "Not what I expected. The material feels cheap, completely disappointed."},
    {"review_id": 3, "product_id": "P002", "rating": 4, "review_text": "Good value for the price. Works perfectly but the packaging was damaged."},
    {"review_id": 4, "product_id": "P003", "rating": 5, "review_text": "Amazing experience, definitely recommend to everyone. Best purchase ever."},
    {"review_id": 5, "product_id": "P002", "rating": 1, "review_text": "Terrible. Broke after one use. Do not buy this garbage."},
    {"review_id": 6, "product_id": "P001", "rating": 5, "review_text": "Excellent quality, fast shipping, amazing price. Perfect!"},
    {"review_id": 7, "product_id": "P004", "rating": 3, "review_text": "It is okay. Not great but not terrible. Average product."},
]
pd.DataFrame(reviews).to_csv("data/ecommerce_reviews.csv", index=False)

# 2. Time-series Data: stock_timeseries.csv
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
prices = 100 + np.cumsum(np.random.randn(100) * 2)
volume = np.random.randint(1000, 5000, size=100)
prices[10:15] = np.nan # Add missing values
df_stock = pd.DataFrame({"date": dates, "price": prices, "volume": volume})
df_stock.to_csv("data/stock_timeseries.csv", index=False)

# 3. High-dimensional Data: housing_features.csv
n_samples = 200
sqft = np.random.normal(1500, 500, n_samples)
age = np.random.randint(1, 50, n_samples)
distance_to_center = np.random.exponential(5, n_samples)
rooms = np.round(sqft / 400 + np.random.normal(0, 0.5, n_samples)).clip(1, 10)
price = sqft * 300 - age * 1000 - distance_to_center * 5000 + np.random.normal(0, 20000, n_samples)
df_housing = pd.DataFrame({
    "sqft_living": sqft,
    "house_age_years": age,
    "distance_to_center_km": distance_to_center,
    "num_bedrooms": rooms,
    "price_usd": price
})
df_housing.to_csv("data/housing_features.csv", index=False)

# 4. Multi-table relational: orders.csv & customers.xlsx
customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104],
    "name": ["Alice", "Bob", "Charlie", "David"],
    "region": ["North", "South", "East", "West"],
    "email": ["alice@email.com", "bob@email.com", "charlie@email.com", "david@email.com"]
})
customers.to_excel("data/customers.xlsx", index=False)

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "customer_id": [101, 102, 101, 104, 105], # 105 is an orphan
    "amount": [250.0, 150.5, 300.0, 50.0, 400.0],
    "order_date": ["2023-05-01", "2023-05-02", "2023-05-03", "2023-05-04", "2023-05-05"]
})
orders.to_csv("data/orders.csv", index=False)

print("Generated all advanced datasets in data/ folder!")
