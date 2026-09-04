# 🏥 Vishalya

### Eco-Syndromic Disease Surveillance & AI-Based Risk Prediction System

Vishalya is a hybrid AI-powered medical surveillance system designed to help identify potential disease outbreak risks by combining patient symptoms with environmental air-quality information.

The system uses a Machine Learning model to analyze patient symptoms and AQI data and return an outbreak-risk prediction through a FastAPI backend.

---

## 🚀 Live Backend

**Production Backend:**  
https://vishalya.onrender.com/

**API Documentation:**  
https://vishalya.onrender.com/docs

**ReDoc:**  
https://vishalya.onrender.com/redoc

---

# 🎯 Project Objective

Vishalya combines:

- 🧑‍⚕️ Field-level patient data collection
- 🤖 Machine Learning
- 🌫️ Air Quality Index (AQI)
- 📍 Geospatial information
- ⚡ FastAPI REST APIs
- 💾 Patient record persistence
- 📊 Public-health analytics

The goal is to identify possible disease-risk patterns by combining **syndromic symptoms with environmental pollution data**.

---

# 🏗️ System Architecture

```text
                 VISHALYA SYSTEM
                       │
                       ▼
             📱 Flutter Mobile App
              Field Health Worker
                       │
                       │ Patient Data
                       ▼
              ⚡ FastAPI Backend
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Validation     AQI Data     Database
      Pydantic      Integration   Storage
          │            │
          └────────────┘
                 │
                 ▼
          🧠 ML Prediction
                 │
                 ▼
        Random Forest Model
                 │
          ┌──────┴──────┐
          ▼             ▼
       🚨 HIGH        ✅ LOW
          │             │
          └──────┬──────┘
                 ▼
          📊 Dashboard
        Analytics / XAI
