import joblib
import pandas as pd
import os

# Resolve path automatically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'vishalya_rf_model.joblib')

print("1. Loading the 1MB optimized Joblib model...")
model = joblib.load(MODEL_PATH)

# =====================================================================
# THE FEATURE MAP (Strict Order)
# Order MUST be: fever, cough, shortness_of_breath, sore_throat, 
# diarrhea, vomiting, headache, fatigue, skin_rash, chills, aqi_level
# =====================================================================
FEATURE_ORDER = [
    "fever", "cough", "shortness_of_breath", "sore_throat",
    "diarrhea", "vomiting", "headache", "fatigue",
    "skin_rash", "chills", "aqi_level"
]

print("2. Simulating incoming data from FastAPI...")
# Example 1: High Risk Patient (Respiratory syndrome in bad air quality)
patient_1 = pd.DataFrame([[1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 320]], columns=FEATURE_ORDER) 

# Example 2: Low Risk Patient (Just a mild headache, clean air)
patient_2 = pd.DataFrame([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 80]], columns=FEATURE_ORDER)

print("\n3. Running Predictions...")
risk_1 = model.predict(patient_1)
risk_2 = model.predict(patient_2)

print(f"Patient 1 Risk: {'HIGH DANGER (1) 🚨' if risk_1[0] == 1 else 'LOW (0) ✅'}")
print(f"Patient 2 Risk: {'HIGH DANGER (1) 🚨' if risk_2[0] == 1 else 'LOW (0) ✅'}")