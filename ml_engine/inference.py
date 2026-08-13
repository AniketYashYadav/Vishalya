import os
import json
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

JSON_PATH = os.path.join(PROJECT_ROOT, 'shared_contracts', 'symptom_schema.json')
MODEL_PATH = os.path.join(BASE_DIR, 'vishalya_rf_model.pkl')

# Global variables to hold the model in memory
_model = None
_symptom_schema = None

def _load_assets():
    """Private function to load the model and schema into memory only once."""
    global _model, _symptom_schema
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _symptom_schema is None:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
            _symptom_schema = data['symptoms']

def predict_disease(active_symptoms: list) -> str:
    """
    Public function for the FastAPI backend.
    Takes a list of symptoms and returns the predicted disease.
    """
    _load_assets()
    
    # Create a dictionary setting all known symptoms to 0
    input_data = {symptom: 0 for symptom in _symptom_schema}
    
    # Flip the value to 1 for symptoms provided by the user
    cleaned_active_symptoms = [s.strip().lower() for s in active_symptoms]
    for symptom in cleaned_active_symptoms:
        if symptom in input_data:
            input_data[symptom] = 1
            
    # Convert dictionary into a single-row Pandas DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Predict and return the string result
    prediction = _model.predict(df_input)
    return prediction[0]