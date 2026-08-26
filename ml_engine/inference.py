import joblib
import numpy as np
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

print("2. Simulating incoming data from FastAPI...")
# Example 1: High Risk Patient (Respiratory syndrome in bad air quality)
# fever=1, cough=1, breath=1, fatigue=1, aqi=320. Rest are 0.
patient_1 = np.array([[1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 320]]) 

# Example 2: Low Risk Patient (Just a mild headache, clean air)
# headache=1, aqi=80. Rest are 0.
patient_2 = np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 80]])

print("\n3. Running Predictions...")
risk_1 = model.predict(patient_1)
risk_2 = model.predict(patient_2)

print(f"Patient 1 Risk: {'HIGH DANGER (1) 🚨' if risk_1[0] == 1 else 'LOW (0) ✅'}")
print(f"Patient 2 Risk: {'HIGH DANGER (1) 🚨' if risk_2[0] == 1 else 'LOW (0) ✅'}")