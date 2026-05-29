import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# ===== LOAD REAL DATA =====
print("Loading real data from Walmart...")
df = pd.read_csv('Walmart_Sales.csv')

print("\n--- Dataset Information ---")
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\nFirst few rows:")
print(df.head())

# ===== DATA EXPLORATION =====
print("\n--- Data Statistics ---")
print(df.describe())

# ===== PREPARE DATA =====
print("\n--- Preparing Data ---")

# Select relevant columns - adjust based on your CSV columns
# Check what columns you have with df.columns
# Common column names: Sales, Revenue, Store, Weekly_Sales, etc.

# Try these column names (change if your CSV has different names)
try:
    X = df[['Store', 'Dept']]  # Features
    y = df['Weekly_Sales']  # Target
except KeyError:
    print("Column names don't match. Your columns are:")
    print(df.columns.tolist())
    print("\nTrying alternative columns...")
    # If above fails, try any numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        X = df[numeric_cols[:-1]]
        y = df[numeric_cols[-1]]
    else:
        print("Not enough numeric columns!")
        exit()

# Remove missing values
X = X.dropna()
y = y[X.index]

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# ===== SPLIT DATA =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ===== TRAIN MODEL =====
print("\n--- Training Model ---")
model = LinearRegression()
model.fit(X_train, y_train)

print(f"Model Coefficients: {model.coef_}")
print(f"Model Intercept: {model.intercept_:.4f}")

# ===== MAKE PREDICTIONS =====
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# ===== EVALUATE MODEL =====
print("\n--- Model Performance ---")
mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2 = r2_score(y_test, y_pred_test)

print(f"Mean Absolute Error (MAE): ${mae:,.2f}")
print(f"Root Mean Squared Error (RMSE): ${rmse:,.2f}")
print(f"R² Score: {r2:.4f}")

# ===== VISUALIZATIONS =====
print("\n--- Creating Visualizations ---")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Actual vs Predicted
axes[0, 0].scatter(y_test, y_pred_test, alpha=0.6, color='blue', s=30)
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0, 0].set_xlabel('Actual Sales ($)')
axes[0, 0].set_ylabel('Predicted Sales ($)')
axes[0, 0].set_title(f'Actual vs Predicted\nR² Score: {r2:.4f}')
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Distribution of Sales
axes[0, 1].hist(y, bins=30, color='green', alpha=0.7, edgecolor='black')
axes[0, 1].set_xlabel('Sales ($)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Distribution of Sales')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Residuals
residuals = y_test - y_pred_test
axes[1, 0].scatter(y_pred_test, residuals, alpha=0.6, color='orange', s=30)
axes[1, 0].axhline(y=0, color='r', linestyle='--', lw=2)
axes[1, 0].set_xlabel('Predicted Sales ($)')
axes[1, 0].set_ylabel('Residuals ($)')
axes[1, 0].set_title('Residual Plot')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Error Distribution
axes[1, 1].hist(residuals, bins=30, color='purple', alpha=0.7, edgecolor='black')
axes[1, 1].set_xlabel('Prediction Error ($)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Error Distribution')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('walmart_prediction_results.png', dpi=300, bbox_inches='tight')
print("✅ Visualizations saved as 'walmart_prediction_results.png'")
plt.show()

print("\n" + "="*50)
print("WALMART SALES PREDICTION - SUMMARY")
print("="*50)
print(f"Dataset: Walmart Sales (Real Data)")
print(f"Total Records: {len(df)}")
print(f"Performance - MAE: ${mae:,.2f}")
print(f"Performance - R² Score: {r2:.4f}")
print("="*50)