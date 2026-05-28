# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import numpy as np
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI(
    title="Clinical Decision Support System",
    description="XGBoost-based treatment and dosage recommendation system with SHAP explanations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models at startup
MODEL_PATH = "models"

try:
    treatment_model = joblib.load(f"{MODEL_PATH}/xgb_treatment_model.pkl")
    dosage_model = joblib.load(f"{MODEL_PATH}/xgb_dosage_model.pkl")
    label_encoder = joblib.load(f"{MODEL_PATH}/label_encoder.pkl")
    feature_columns = joblib.load(f"{MODEL_PATH}/feature_columns.pkl")
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    treatment_model = None
    dosage_model = None
    label_encoder = None
    feature_columns = None

# Define request schema
class PatientData(BaseModel):
    age: float
    gender: int
    gender_male: int
    weight_kg: float
    height_cm: float
    bmi: float
    bp_systolic: float
    bp_diastolic: float
    heart_rate: float
    temperature: float
    respiratory_rate: float
    creatinine: float
    egfr: float
    diagnosis: int
    allergies: int
    has_diabetes: int
    has_hypertension: int
    has_ckd: int
    has_chf: int
    has_copd: int
    has_liver_disease: int

    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "gender": 1,
                "gender_male": 1,
                "weight_kg": 85,
                "height_cm": 175,
                "bmi": 27.8,
                "bp_systolic": 145,
                "bp_diastolic": 90,
                "heart_rate": 78,
                "temperature": 37.2,
                "respiratory_rate": 16,
                "creatinine": 1.4,
                "egfr": 52,
                "diagnosis": 0,
                "allergies": 0,
                "has_diabetes": 1,
                "has_hypertension": 1,
                "has_ckd": 0,
                "has_chf": 0,
                "has_copd": 0,
                "has_liver_disease": 0
            }
        }

# Define response schema
class RecommendationResponse(BaseModel):
    treatment: str
    dosage_mg: int
    confidence: float
    disclaimer: str = "Clinical decision support only. Final decision rests with physician."

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Clinical Decision Support System API",
        "status": "healthy",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
def health_check():
    if treatment_model is None or dosage_model is None:
        return {"status": "unhealthy", "error": "Models not loaded"}
    return {"status": "healthy", "models_loaded": True}

# Prediction endpoint
@app.post("/predict", response_model=RecommendationResponse)
def predict(patient: PatientData):
    """
    Get treatment and dosage recommendation for a patient
    """
    if treatment_model is None or dosage_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    try:
        # Convert patient data to DataFrame
        input_dict = patient.dict()
        input_df = pd.DataFrame([input_dict])[feature_columns]
        
        # Predict treatment
        treatment_encoded = treatment_model.predict(input_df)[0]
        treatment = label_encoder.inverse_transform([treatment_encoded])[0]
        
        # Predict dosage
        dosage = int(dosage_model.predict(input_df)[0])
        
        # Get prediction confidence
        proba = treatment_model.predict_proba(input_df)[0]
        confidence = float(max(proba))
        
        return RecommendationResponse(
            treatment=treatment,
            dosage_mg=dosage,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Batch prediction endpoint
@app.post("/predict/batch")
def predict_batch(patients: List[PatientData]):
    """
    Get recommendations for multiple patients
    """
    if treatment_model is None or dosage_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    results = []
    for patient in patients:
        try:
            input_dict = patient.dict()
            input_df = pd.DataFrame([input_dict])[feature_columns]
            
            treatment_encoded = treatment_model.predict(input_df)[0]
            treatment = label_encoder.inverse_transform([treatment_encoded])[0]
            dosage = int(dosage_model.predict(input_df)[0])
            
            results.append({
                "treatment": treatment,
                "dosage_mg": dosage,
                "success": True
            })
        except Exception as e:
            results.append({
                "error": str(e),
                "success": False
            })
    
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)