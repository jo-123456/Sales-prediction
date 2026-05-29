import pandas as pd
import numpy as np

# Generate sample sales data
np.random.seed(42)
months = pd.date_range(start='2023-01-01', end='2024-12-31', freq='ME')
data = {
    'Month': months,
    'Marketing_Spend': np.random.randint(1000, 5000, len(months)),
    'Customer_Count': np.random.randint(50, 200, len(months)),
    'Season': ['Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', 'Q3', 'Q3', 'Q3', 'Q4', 'Q4', 'Q4'] * 2,
    'Sales': np.random.randint(10000, 50000, len(months))
}

df = pd.DataFrame(data)
df.to_csv('sales_data.csv', index=False)
print("Sample data created: sales_data.csv")
print(df.head())