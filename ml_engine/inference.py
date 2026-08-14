import os
import json
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
MODEL_PATH = os.path.join(BASE_DIR, 'vishalya_rf_model.pkl')
JSON_PATH = os.path.join(PROJECT_ROOT, 'shared_contracts', 'symptom_schema.json')

_model = None
_symptom_schema = None

def _load_assets():
    global _model, _symptom_schema
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _symptom_schema is None:
        with open(JSON_PATH, 'r') as f:
            schema = json.load(f)
            _symptom_schema = schema['symptoms']

def predict_disease(active_symptoms: list) -> dict:
    _load_assets()
    
    # Create a dictionary setting all known symptoms to 0
    input_data = {symptom: 0 for symptom in _symptom_schema} # type: ignore
    
    # Flip the value to 1 for symptoms provided by the user
    cleaned_active_symptoms = [s.strip().lower() for s in active_symptoms]
    for symptom in cleaned_active_symptoms:
        if symptom in input_data:
            input_data[symptom] = 1
            
    # Convert dictionary into a single-row Pandas DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Predict the top disease
    prediction = _model.predict(df_input)[0] # type: ignore
    
    # XAI: Get prediction probabilities for transparency
    probabilities = _model.predict_proba(df_input)[0] # type: ignore
    
    # Get the confidence score of the winning prediction
    disease_index = list(_model.classes_).index(prediction) # type: ignore
    confidence_score = round(probabilities[disease_index] * 100, 2)
    
    return {
        "disease": prediction,
        "confidence_percentage": confidence_score
    }