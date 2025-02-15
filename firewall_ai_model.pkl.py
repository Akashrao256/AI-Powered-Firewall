import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Example dataset (replace with real network traffic data)
# Features: [request_rate, payload_size, header_anomalies]
X = np.array([[1, 100, 0], [2, 200, 0], [1, 150, 0], [3, 300, 1], [5, 500, 1], [4, 400, 1]])
# Labels: 0 = benign, 1 = malicious
y = np.array([0, 0, 0, 1, 1, 1])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train_scaled, y_train)

# Evaluate the model
accuracy = model.score(X_test_scaled, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model and scaler
model_path = r"d:\Python\firewall_ai_model.pkl"
joblib.dump({'model': model, 'scaler': scaler}, model_path)
print(f"Model saved successfully to {model_path}")
