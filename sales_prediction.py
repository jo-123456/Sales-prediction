import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('Walmart_sales.csv')
print("Data loaded successfully!")
print(f"Total records: {len(df)}")
print("\nFirst few rows:")
print(df.head())

# Step 1: Prepare data
# Select features (inputs) and target (output)
X = df[['Marketing_Spend', 'Customer_Count']]  # Features
y = df['Sales']  # Target (what we want to predict)

print("\n--- Data Preparation ---")
print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Step 2: Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Step 3: Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)
print("\n--- Model Trained ---")
print(f"Model coefficients: {model.coef_}")
print(f"Model intercept: {model.intercept_}")

# Step 4: Make predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Step 5: Evaluate model
mae = mean_absolute_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)

print("\n--- Model Performance ---")
print(f"Mean Absolute Error: ${mae:,.2f}")
print(f"R² Score: {r2:.4f} (closer to 1 is better)")

# Step 6: Predict future sales
print("\n--- Future Predictions ---")
future_data = np.array([
    [3000, 100],  # Marketing Spend: $3000, Customers: 100
    [4500, 150],  # Marketing Spend: $4500, Customers: 150
    [2000, 75]    # Marketing Spend: $2000, Customers: 75
])

future_predictions = model.predict(future_data)
for i, pred in enumerate(future_predictions):
    print(f"Scenario {i+1}: Predicted Sales = ${pred:,.2f}")

# Step 7: Visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Actual vs Predicted (Test Data)
axes[0, 0].scatter(y_test, y_pred_test, alpha=0.6, color='blue')
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0, 0].set_xlabel('Actual Sales')
axes[0, 0].set_ylabel('Predicted Sales')
axes[0, 0].set_title('Actual vs Predicted Sales')
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Sales over time
axes[0, 1].plot(df['Month'], df['Sales'], marker='o', label='Actual Sales')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Sales ($)')
axes[0, 1].set_title('Sales Trend Over Time')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].legend()

# Plot 3: Marketing Spend vs Sales
axes[1, 0].scatter(df['Marketing_Spend'], df['Sales'], alpha=0.6, color='green')
axes[1, 0].set_xlabel('Marketing Spend ($)')
axes[1, 0].set_ylabel('Sales ($)')
axes[1, 0].set_title('Marketing Spend vs Sales')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Residuals (errors)
residuals = y_test - y_pred_test
axes[1, 1].scatter(y_pred_test, residuals, alpha=0.6, color='orange')
axes[1, 1].axhline(y=0, color='r', linestyle='--')
axes[1, 1].set_xlabel('Predicted Sales')
axes[1, 1].set_ylabel('Residuals')
axes[1, 1].set_title('Residual Plot')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('prediction_results.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualizations saved as 'prediction_results.png'")
plt.show()