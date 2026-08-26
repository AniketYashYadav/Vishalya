import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==========================================
# 1. PATH RESOLUTION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

CSV_PATH = os.path.join(BASE_DIR, 'Diseases_and_Symptoms_dataset.csv')
JSON_PATH = os.path.join(PROJECT_ROOT, 'shared_contracts', 'symptom_schema.json')
# FIX: Save as .joblib to avoid GitHub limits and improve server load speed
MODEL_PATH = os.path.join(BASE_DIR, 'vishalya_rf_model.joblib')

def train():
    print("1. Loading shared symptom schema...")
    with open(JSON_PATH, 'r') as f:
        schema = json.load(f)
    
    json_symptoms_list = list(schema['symptoms'].keys())

    print("2. Loading Kaggle dataset...")
    df = pd.read_csv(CSV_PATH)

    print("3. Preprocessing & Mapping IHIP Schema...")
    
    ihip_mapping = {
        'fever': 'fever',
        'cough': 'cough',
        'shortness of breath': 'shortness_of_breath',
        'sore throat': 'sore_throat',
        'diarrhea': 'diarrhea',
        'vomiting': 'vomiting',
        'headache': 'headache',
        'fatigue': 'fatigue',
        'skin rash': 'skin_rash',
        'chills': 'chills'
    }
    
    df_optimized = df[list(ihip_mapping.keys())].copy()
    df_optimized.rename(columns=ihip_mapping, inplace=True)
    df_optimized.fillna(0, inplace=True)

    print("4. Applying Eco-Syndromic Logic (Adding AQI)...")
    np.random.seed(42)
    df_optimized['aqi_level'] = np.random.randint(50, 450, size=len(df_optimized))

    def calculate_risk(row):
        if (row['aqi_level'] >= 250) and (row['shortness_of_breath'] == 1 or row['cough'] == 1):
            return 1
        elif (row['fever'] == 1 and row['cough'] == 1 and row['fatigue'] == 1):
            return 1
        else:
            return 0

    df_optimized['outbreak_risk'] = df_optimized.apply(calculate_risk, axis=1)

    print("5. Preparing Data for Training...")
    final_features = json_symptoms_list + ['aqi_level']
    X = df_optimized[final_features]
    y = df_optimized['outbreak_risk']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("6. Training Random Forest Classifier on optimized features...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"\n✅ Model Training Complete. Validation Accuracy: {acc * 100:.2f}%")

    print("7. Exporting the frozen model...")
    joblib.dump(clf, MODEL_PATH)
    print(f"✅ Success: Optimized model saved to {MODEL_PATH}")
    
    print("\nFeature Importances (For XAI dashboard):")
    for name, imp in zip(final_features, clf.feature_importances_):
        print(f" - {name}: {imp*100:.1f}%")

if __name__ == "__main__":
    train()