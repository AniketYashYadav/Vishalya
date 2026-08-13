import os
import json
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Dynamically resolve paths so this script works on any computer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

CSV_PATH = os.path.join(BASE_DIR, 'Diseases_and_Symptoms_dataset.csv')
JSON_PATH = os.path.join(PROJECT_ROOT, 'shared_contracts', 'symptom_schema.json')
MODEL_PATH = os.path.join(BASE_DIR, 'vishalya_rf_model.pkl')

def train():
    print("Loading shared symptom schema...")
    with open(JSON_PATH, 'r') as f:
        schema = json.load(f)
    symptom_features = schema['symptoms']

    print("Loading training dataset...")
    df = pd.read_csv(CSV_PATH)

    # Standardize dataset column names to exactly match the JSON format
    df.columns = df.columns.str.strip().str.lower()
    
    # Identify the target column (Kaggle sets this as 'diseases' or 'disease')
    target_col = 'diseases' if 'diseases' in df.columns else 'disease'
    
    # Extract features (X) and target (y)
    X = df[symptom_features]
    y = df[target_col]

    # Split data for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier on 96k+ instances...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    # Validate the model
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Model Training Complete. Validation Accuracy: {acc * 100:.2f}%")

    # Export the frozen model
    joblib.dump(clf, MODEL_PATH)
    print(f"Success: Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()