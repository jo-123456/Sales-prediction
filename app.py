from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

app = Flask(__name__)

# ===== LOAD AND TRAIN MODEL =====
print("Loading data and training model...")

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'Walmart_Sales.csv')

try:
    df = pd.read_csv(csv_path)
    print(f"✅ CSV loaded from: {csv_path}")
except FileNotFoundError:
    print(f"❌ CSV not found at: {csv_path}")
    print("Available files:", os.listdir(BASE_DIR))
    # Create sample data as fallback
    df = pd.DataFrame({
        'Store': np.random.randint(1, 50, 100),
        'Dept': np.random.randint(1, 100, 100),
        'Weekly_Sales': np.random.randint(10000, 100000, 100)
    })

print("Available columns:", df.columns.tolist())

# Get all numeric columns automatically
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"Numeric columns found: {numeric_cols}")

# Remove the target column
if 'Weekly_Sales' in numeric_cols:
    feature_cols = [col for col in numeric_cols if col != 'Weekly_Sales']
    target_col = 'Weekly_Sales'
else:
    feature_cols = numeric_cols[:-1]
    target_col = numeric_cols[-1]

print(f"Features: {feature_cols}")
print(f"Target: {target_col}")

# Prepare data
X = df[feature_cols].dropna()
y = df[target_col][X.index]

print(f"X shape: {X.shape}, y shape: {y.shape}")

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Calculate accuracy
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred) * 100

print(f"✅ Model trained!")
print(f"   Features: {len(feature_cols)}")
print(f"   Accuracy: {accuracy:.2f}%")

# ===== ROUTES =====

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html', accuracy=f"{accuracy:.2f}")

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction"""
    try:
        data = request.json
        
        # Get values for each feature
        input_values = []
        for feature in feature_cols:
            if feature in data:
                input_values.append(float(data[feature]))
            else:
                return jsonify({
                    'success': False,
                    'error': f'Missing feature: {feature}'
                }), 400
        
        # Make prediction
        prediction = model.predict([input_values])[0]
        
        return jsonify({
            'success': True,
            'prediction': f"${prediction:,.2f}",
            'input': {col: val for col, val in zip(feature_cols, input_values)}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stats')
def stats():
    """Get model statistics"""
    return jsonify({
        'total_records': len(df),
        'accuracy': f"{accuracy:.2f}%",
        'avg_sales': f"${y.mean():,.2f}",
        'max_sales': f"${y.max():,.2f}",
        'min_sales': f"${y.min():,.2f}",
        'features': feature_cols
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Calculate accuracy
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred) * 100

print(f"✅ Model trained!")
print(f"   Features: {len(feature_cols)}")
print(f"   Accuracy: {accuracy:.2f}%")

# ===== ROUTES =====

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html', accuracy=f"{accuracy:.2f}")

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction"""
    try:
        data = request.json
        
        # Get values for each feature
        input_values = []
        for feature in feature_cols:
            if feature in data:
                input_values.append(float(data[feature]))
            else:
                return jsonify({
                    'success': False,
                    'error': f'Missing feature: {feature}'
                }), 400
        
        # Make prediction
        prediction = model.predict([input_values])[0]
        
        return jsonify({
            'success': True,
            'prediction': f"${prediction:,.2f}",
            'input': {col: val for col, val in zip(feature_cols, input_values)}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stats')
def stats():
    """Get model statistics"""
    return jsonify({
        'total_records': len(df),
        'accuracy': f"{accuracy:.2f}%",
        'avg_sales': f"${y.mean():,.2f}",
        'max_sales': f"${y.max():,.2f}",
        'min_sales': f"${y.min():,.2f}",
        'features': feature_cols
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
