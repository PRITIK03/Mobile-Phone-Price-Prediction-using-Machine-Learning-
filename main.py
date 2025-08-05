import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)
import pickle
import os

# Load dataset
file_path = r"C:\Users\SHAHID MULANI\OneDrive\Documents\Desktop\Y M Z\phones_data.csv"
data = pd.read_csv(file_path)

# Drop unnecessary columns
data_cleaned = data.drop(columns=["Unnamed: 0", "os", "popularity", "sellers_amount"])

# Handle missing values for price columns at the same time
imputer_price = SimpleImputer(strategy="mean")
data_cleaned[["lowest_price", "highest_price"]] = imputer_price.fit_transform(data_cleaned[["lowest_price", "highest_price"]])

# Handle missing values for other columns
imputer_screen = SimpleImputer(strategy="mean")
data_cleaned["screen_size"] = imputer_screen.fit_transform(data_cleaned[["screen_size"]])

imputer_memory = SimpleImputer(strategy="mean")
data_cleaned["memory_size"] = imputer_memory.fit_transform(data_cleaned[["memory_size"]])

imputer_battery = SimpleImputer(strategy="mean")
data_cleaned["battery_size"] = imputer_battery.fit_transform(data_cleaned[["battery_size"]])

# Handle `release_date`
data_cleaned["release_date"] = pd.to_datetime(data_cleaned["release_date"], errors="coerce").fillna(pd.Timestamp("1970-01-01"))
data_cleaned["release_date"] = data_cleaned["release_date"].astype(int) / 10**9  # Convert to UNIX timestamp

# Encode categorical features
label_encoder = LabelEncoder()
data_cleaned["model_name"] = label_encoder.fit_transform(data_cleaned["model_name"])
data_cleaned["brand_name"] = label_encoder.fit_transform(data_cleaned["brand_name"])

# Extract features (X) and targets (y)
X = data_cleaned[["battery_size", "brand_name", "memory_size"]]
y = data_cleaned[["model_name", "lowest_price", "highest_price", "release_date", "screen_size"]]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Extract `model_name` separately for classification
y_train_model_name = y_train["model_name"]
y_test_model_name = y_test["model_name"]

# Regression task: Train a multi-output regressor
regressor = MultiOutputRegressor(RandomForestRegressor(random_state=42))
regressor.fit(X_train, y_train[["lowest_price", "highest_price", "release_date", "screen_size"]])

# Predict and evaluate regression
y_pred_reg = regressor.predict(X_test)
mae = mean_absolute_error(y_test[["lowest_price", "highest_price", "release_date", "screen_size"]], y_pred_reg)
mse = mean_squared_error(y_test[["lowest_price", "highest_price", "release_date", "screen_size"]], y_pred_reg)
r2 = r2_score(y_test[["lowest_price", "highest_price", "release_date", "screen_size"]], y_pred_reg)

print("Regression Metrics:")
print(f"MAE: {mae}, MSE: {mse}, R2: {r2}")

# Classification task: Train a classifier for `model_name`
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train_model_name)

# Predict and evaluate classification
y_pred_model_name = clf.predict(X_test)
accuracy = accuracy_score(y_test_model_name, y_pred_model_name)
precision = precision_score(y_test_model_name, y_pred_model_name, average="weighted")
recall = recall_score(y_test_model_name, y_pred_model_name, average="weighted")
f1 = f1_score(y_test_model_name, y_pred_model_name, average="weighted")

print("\nClassification Metrics:")
print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

# Confusion matrix
conf_matrix = confusion_matrix(y_test_model_name, y_pred_model_name)
print("\nConfusion Matrix:")
print(conf_matrix)

# Save models
output_dir = "models"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "regressor.pkl"), "wb") as f:
    pickle.dump(regressor, f)

with open(os.path.join(output_dir, "classifier.pkl"), "wb") as f:
    pickle.dump(clf, f)

# Save the label encoder for `model_name`
with open(os.path.join(output_dir, "label_encoder.pkl"), "wb") as f:
    pickle.dump(label_encoder, f)

print("\nModels saved successfully!")
