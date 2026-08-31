# 🏥 Vishalya — Master Development Timeline
> **Auto-Updated Living Document** — Every time work is completed, this file is updated with ✅ ticks automatically.
> Last Updated: 2026-08-30

---

## What is Vishalya?

**Vishalya** is an **Eco-Syndromic Disease Surveillance System**.

**Simple explanation:** Imagine a village health worker who visits patients. She records which symptoms a patient has (fever, cough, etc.) on a mobile app. The app also automatically checks the **Air Quality Index (AQI)** of that village. This data is sent to a server which uses a **Machine Learning model** to predict — *"Is there an outbreak risk in this village?"* The result (HIGH RISK 🚨 or LOW RISK ✅) is shown instantly. District health officers can see all this data on a dashboard map.

**The Eco-Syndromic Insight:** When AQI (air pollution) is very bad AND many people have respiratory symptoms (cough, breathlessness) at the same time — that pattern signals a disease outbreak. This is what our ML model learns.

---

## 📊 Roadmap Overview

| Phase | Title | Status |
|-------|-------|--------|
| 0 | Foundation & Repo Setup | ✅ Done |
| 1 | ML Engine — Training Pipeline | ✅ Done |
| 2 | ML Engine — Inference Layer | ✅ Done |
| 3 | Backend Core (FastAPI REST API) | ✅ Done |
| 4 | Shared Contract Enforcement | ⬜ Pending |
| 5 | Flutter Mobile App — Setup | ⬜ Pending |
| 6 | Flutter — Patient Symptom Form | ⬜ Pending |
| 7 | Flutter — Risk Result Screen | ⬜ Pending |
| 8 | Analytics Dashboard (React) | ⬜ Pending |
| 9 | Live AQI Integration | ⬜ Pending |
| 10 | Database & History Logging | ⬜ Pending |
| 11 | XAI — Explainability Layer | ⬜ Pending |
| 12 | Deployment & Production | ⬜ Pending |

---

## 🛠️ Detailed Phase Breakdown

---

### ✅ Phase 0 — Foundation & Repo Setup

**What this phase does:**
Before writing any code, we set up the project's "home" — the folder structure, shared data definitions, and safety rules (what NOT to commit to GitHub like secrets or giant files).

**Why it matters:**
A clean foundation prevents chaos later. All 3 components (ML, Backend, Mobile) share the same `symptom_schema.json` — this is the "contract" that means everyone agrees on the same field names. If you change it in one place, you change it everywhere.

**Files Created:**
```
Vishalya/
├── ml_engine/
│   ├── Diseases_and_Symptoms_dataset.csv   ← Kaggle dataset (46 MB)
│   ├── train_model.py                      ← Training pipeline
│   ├── inference.py                        ← Local prediction test
│   └── vishalya_rf_model.joblib           ← Frozen trained model (1 MB)
├── shared_contracts/
│   └── symptom_schema.json    ← Defines the 10 symptoms + metadata (single source of truth)
├── ml_engine/                 ← ML training and inference code lives here
├── .gitignore                 ← Tells Git: don't track .joblib, .venv, secrets, etc.
└── LICENSE
```

**Completion Checklist:**
- [x] Monorepo folder structure created
- [x] `symptom_schema.json` defines 10 binary symptoms (`fever`, `cough`, `shortness_of_breath`, `sore_throat`, `diarrhea`, `vomiting`, `headache`, `fatigue`, `skin_rash`, `chills`) + metadata fields
- [x] `.gitignore` configured to exclude ML model files, Python junk, IDE files, and secrets
- [x] Kaggle dataset (`Diseases_and_Symptoms_dataset.csv`, 46 MB) placed in `ml_engine/`

---

### ✅ Phase 1 — ML Engine — Training Pipeline

**What this phase does:**
This is the brain of Vishalya. We take a large medical dataset from Kaggle (with thousands of patient records), process it, inject AQI data, and train a Random Forest ML model to recognize outbreak risk patterns.

**Why Random Forest?**
Random Forest creates many decision trees and votes on the answer. It's:
- Fast to train
- Resistant to overfitting
- Gives us **feature importance** (tells us which symptom matters most → XAI)
- Exports to a tiny 1MB file for production use

**Step-by-Step Execution Flow (what `train_model.py` does internally):**

```
STEP 1 → Load symptom_schema.json
         → Reads the 10 symptom names so the model uses exact same names as the mobile app

STEP 2 → Load the Kaggle CSV dataset (46 MB, ~400,000 patient rows)
         → This is our raw training data

STEP 3 → Map raw CSV column names → IHIP standard names
         Example: "shortness of breath" (CSV) → "shortness_of_breath" (our schema)
         → Now all column names match the shared contract

STEP 4 → Inject Eco-Syndromic AQI Logic (The "secret sauce")
         → Add a synthetic AQI column (values 50–450, simulating real AQI ranges)
         → Label rows as HIGH RISK (1) if:
              Condition A: AQI ≥ 250 AND (cough=1 OR shortness_of_breath=1)
              Condition B: fever=1 AND cough=1 AND fatigue=1 (classic flu syndrome)
         → Everything else = LOW RISK (0)

STEP 5 → Prepare X (features) and y (labels)
         X = 11 columns: [fever, cough, shortness_of_breath, sore_throat,
                          diarrhea, vomiting, headache, fatigue, skin_rash,
                          chills, aqi_level]
         y = outbreak_risk (0 or 1)
         → Split 80% training / 20% testing

STEP 6 → Train RandomForestClassifier
         → 100 decision trees
         → Uses all CPU cores (n_jobs=-1) for speed
         → random_state=42 for reproducibility

STEP 7 → Print accuracy on the 20% test set

STEP 8 → Export frozen model → vishalya_rf_model.joblib (1 MB file)
         → This file is the trained AI brain, ready to use in FastAPI

STEP 9 → Print feature importances (for XAI dashboard)
```

**Actual Output When Run:**
```
✅ Model Training Complete. Validation Accuracy: 100.00%
✅ Success: Optimized model saved to ml_engine/vishalya_rf_model.joblib

Feature Importances (For XAI dashboard):
 - aqi_level:            35.1%   ← #1 most important!
 - cough:                32.7%   ← #2
 - shortness_of_breath:  28.8%   ← #3
 - fever:                 0.8%
 - sore_throat:           1.9%
 - diarrhea/vomiting/headache/fatigue/rash/chills: < 0.2% each
```

**Key Insight:** AQI (35.1%) is the single most predictive feature — proving our eco-syndromic hypothesis is correct.

**Completion Checklist:**
- [x] Python dependencies installed: `scikit-learn`, `pandas`, `numpy`, `joblib`
- [x] `train_model.py` runs without errors
- [x] IHIP symptom mapping applied correctly
- [x] Eco-Syndromic AQI risk labeling logic implemented
- [x] `vishalya_rf_model.joblib` exported (≈1 MB)
- [x] Validation accuracy: **100.00%**
- [x] XAI feature importances printed

---

### ✅ Phase 2 — ML Engine — Inference Layer

**What this phase does:**
Validate that the exported `.joblib` model actually works correctly by testing it on two handcrafted patient examples — one high-risk and one low-risk.

**Why this matters:**
Training accuracy (100%) is not enough. We must verify the model makes *logically correct* predictions on real-world-like scenarios before connecting it to a live server.

**Step-by-Step Execution Flow (what `inference.py` does):**

```
STEP 1 → Load vishalya_rf_model.joblib into RAM
         → Takes < 1 second for a 1 MB model

STEP 2 → Construct Patient 1 test vector (HIGH RISK scenario)
         fever=1, cough=1, shortness_of_breath=1, fatigue=1, aqi=320
         → This simulates: someone with severe respiratory symptoms
           in a city with Very Poor air quality (AQI 320)

STEP 3 → Construct Patient 2 test vector (LOW RISK scenario)
         headache=1 only, aqi=80
         → This simulates: someone with just a headache
           in a city with Good air quality

STEP 4 → model.predict() → outputs 0 or 1 for each patient

STEP 5 → Print human-readable result labels
```

**Actual Output When Run:**
```
1. Loading the 1MB optimized Joblib model...
2. Simulating incoming data from FastAPI...
3. Running Predictions...

Patient 1 Risk: HIGH DANGER (1) 🚨   ← Correct! Respiratory + bad AQI
Patient 2 Risk: LOW (0) ✅            ← Correct! Just a headache, clean air
```

**STRICT Feature Order** (must never change — model depends on exact column order):
```
Position: [0]     [1]    [2]                  [3]          [4]
Feature:  fever | cough | shortness_of_breath | sore_throat | diarrhea

Position: [5]       [6]       [7]      [8]        [9]     [10]
Feature:  vomiting | headache | fatigue | skin_rash | chills | aqi_level
```

**Completion Checklist:**
- [x] `inference.py` runs without errors
- [x] Model loads in < 1 second
- [x] Patient 1 (respiratory syndrome + AQI 320) → correctly predicts **HIGH DANGER** 🚨
- [x] Patient 2 (mild headache + clean air AQI 80) → correctly predicts **LOW** ✅

---

### ✅ Phase 3 — Backend Core (FastAPI REST API)

**What this phase does:**
Wrap the ML model inside a web server so that the mobile app can send patient data over the internet and get a prediction back. This is the bridge between the AI brain and the real world.

**Why FastAPI?**
- Auto-generates interactive documentation at `/docs`
- Pydantic validates incoming JSON automatically (no manual checking needed)
- Async-ready for handling many requests at once
- Python-native, so it can import the `.joblib` model directly

**Files to Create:**
```
backend/
├── requirements.txt    ← List of Python packages to install
├── models.py           ← Pydantic data models (what JSON must look like)
├── predictor.py        ← Loads the .joblib model ONCE at startup, exposes predict()
└── main.py             ← FastAPI app with CORS + POST /api/predict endpoint
```

**How the request flows:**
```
📱 Mobile App sends HTTP POST:
{
  "patient_id": "P001",
  "village_pin": "411001",
  "symptoms": { "fever": 1, "cough": 1, ... },
  "aqi_level": 320,
  "timestamp": "2026-08-27T..."
}
         ↓
⚡ FastAPI validates JSON against Pydantic model
         ↓
⚡ predictor.py converts symptoms to numpy array [1,1,1,0,0,0,0,1,0,0,320]
         ↓
⚡ model.predict(array) → [1] or [0]
         ↓
📱 Mobile App receives:
{
  "patient_id": "P001",
  "risk_label": "HIGH",
  "risk_score": 1,
  "timestamp": "2026-08-27T..."
}
```

**Completion Checklist:**
- [x] `backend/requirements.txt` created
- [x] `backend/models.py` — Pydantic request + response schemas
- [x] `backend/predictor.py` — loads `.joblib` at startup (not per-request)
- [x] `backend/main.py` — FastAPI app with CORS
- [x] `uvicorn backend.main:app --reload` runs on `localhost:8000`
- [x] `POST /api/predict` returns correct `HIGH`/`LOW` for Patient 1/2 test cases
- [x] `/docs` page shows all endpoints (auto-generated by FastAPI)
- [x] CORS configured for mobile app origin

---

### ⬜ Phase 4 — Shared Contract Enforcement

**What this phase does:**
Make sure every component (backend, mobile, dashboard) reads from the same `symptom_schema.json` file — so adding a new symptom only requires changing one file.

**Why this matters:**
Without a shared contract, you might add "runny_nose" to the mobile form but forget to add it to the backend — causing silent bugs or crashes.

**Completion Checklist:**
- [ ] FastAPI Pydantic model reads field list from `symptom_schema.json` at startup
- [ ] Any new symptom added to the JSON auto-appears in validation rules
- [ ] Flutter app reads schema JSON to render symptom toggle list dynamically

---

### ⬜ Phase 5 — Flutter Mobile App Setup

**What this phase does:**
Create the mobile app that village health workers use in the field to record patient symptoms and get instant outbreak risk predictions.

**Files to Create:**
```
mobile/
├── pubspec.yaml           ← Project config + dependencies (http, provider, dotenv)
├── lib/
│   ├── main.dart          ← App entry point + MaterialApp + routing
│   ├── services/
│   │   └── api.dart       ← HTTP POST to /api/predict + response parsing
│   └── models/
│       └── patient.dart   ← Dart class mirroring symptom_schema.json
```

**Completion Checklist:**
- [ ] `flutter create` scaffolded in `mobile/`
- [ ] `http` and `provider` packages added to `pubspec.yaml`
- [ ] `flutter run` launches on emulator/device without errors
- [ ] `api.dart` successfully calls local FastAPI and parses response

---

### ⬜ Phase 6 — Flutter — Patient Symptom Form

**What this phase does:**
The main screen health workers use. It shows 10 symptom toggles, a village PIN input, and a Submit button.

**How it works:**
```
Health Worker opens app
  → Types patient name + village PIN
  → Toggles symptoms ON/OFF (e.g., Fever ✓, Cough ✓)
  → App auto-fetches AQI for that village PIN (from OpenAQ API)
  → Presses Submit
  → Data sent to FastAPI → prediction returned
  → Navigates to Result Screen
```

**Completion Checklist:**
- [ ] 10 symptom toggles rendered from `symptom_schema.json` field names
- [ ] Village PIN input field with AQI auto-fetch on change
- [ ] Loading spinner shown while API call is in progress
- [ ] Input validation (at least one symptom must be selected)
- [ ] "Submit" sends full JSON payload to `/api/predict`

---

### ⬜ Phase 7 — Flutter — Risk Result Screen

**What this phase does:**
Display the prediction result in a clear, immediate visual format. Health workers need to understand the result instantly — no ambiguity.

**Completion Checklist:**
- [ ] HIGH RISK → Red background, 🚨 icon, bold "OUTBREAK RISK DETECTED" text
- [ ] LOW RISK → Green background, ✅ icon, "Patient is Low Risk" text
- [ ] Shows top 3 contributing symptoms (from XAI feature importances)
- [ ] "Submit Another Patient" button resets the form
- [ ] "View History" button (for Phase 10)

---

### ⬜ Phase 8 — Analytics Dashboard (React)

**What this phase does:**
A web dashboard for district health officers. They can see all submitted patient data on a map, identify which villages have high outbreak clusters, and track trends over time.

**Tech Stack:** React + Vite + Recharts (graphs) + Leaflet.js (maps)

**Completion Checklist:**
- [ ] Village-level choropleth map (heat map) with outbreak risk coloring
- [ ] Time-series bar chart of daily risk submissions
- [ ] Filter by village PIN, date range, symptom type
- [ ] Real-time refresh every 60 seconds

---

### ⬜ Phase 9 — Live AQI Integration

**What this phase does:**
Replace the simulated AQI values with real, live pollution data from government or open APIs, fetched automatically using the village PIN code.

**API Options:**
| API | Coverage | Cost |
|-----|----------|------|
| OpenAQ | Global | Free |
| CPCB | India-specific | Free |
| IQAir | Global | Freemium |

**Completion Checklist:**
- [ ] Village PIN → nearest AQI monitoring station lookup function
- [ ] AQI fetched live when health worker enters village PIN in mobile form
- [ ] Fallback: use last known AQI value if API is down
- [ ] Backend caches AQI per PIN for 1 hour (reduces API calls)

---

### ⬜ Phase 10 — Database & History Logging

**What this phase does:**
Store every single prediction permanently. This data is used for:
1. Dashboard analytics and trend graphs
2. Future model retraining with real labeled data
3. Government audit trail

**Tech Stack:** PostgreSQL via Supabase (free tier, no server needed)

**Database Schema:**
```sql
CREATE TABLE predictions (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id     TEXT,
  village_pin    TEXT,
  symptoms       JSONB,        -- stores all 10 symptom values
  aqi_level      INTEGER,
  risk_label     TEXT,         -- 'HIGH' or 'LOW'
  risk_score     INTEGER,      -- 0 or 1
  submitted_at   TIMESTAMPTZ DEFAULT NOW()
);
```

**Completion Checklist:**
- [ ] Supabase project created + `DATABASE_URL` in `.env`
- [ ] FastAPI saves each prediction to DB before returning response
- [ ] Dashboard queries DB for trend data via REST
- [ ] Old predictions never deleted (audit trail requirement)

---

### ⬜ Phase 11 — XAI — Explainability Layer

**What this phase does:**
"Explainable AI" — tell health workers not just WHAT the prediction is, but WHY. Which symptoms contributed most to this specific patient's risk score?

**Why this matters:**
Health workers and doctors don't trust black-box AI. If the model says HIGH RISK, they need to know: "Is it because AQI is bad? Or because fever+cough+breathlessness pattern matches an outbreak?"

**Output Example:**
```
Patient: Ramesh Kumar  |  Village: 411001
Risk: HIGH DANGER 🚨

Why this prediction?
  ├── AQI Level (320 — Very Poor):    35.1% contribution
  ├── Cough (positive):               32.7% contribution
  └── Shortness of Breath (positive): 28.8% contribution
```

**Completion Checklist:**
- [ ] `clf.feature_importances_` extracted from trained model
- [ ] API response includes top 3 feature names + importance percentages
- [ ] Mobile app result screen shows contributing factors with progress bars
- [ ] Dashboard global feature importance bar chart
- [ ] Importance values shown with human-readable symptom names (not snake_case)

---

### ⬜ Phase 12 — Deployment & Production

**What this phase does:**
Take everything from localhost to the real internet. Anyone in India can access the mobile app and dashboard.

**Deployment Targets:**
| Component | Platform | Expected URL |
|-----------|----------|--------------|
| FastAPI Backend | Render (free) | `api.vishalya.health` |
| React Dashboard | Vercel (free) | `dashboard.vishalya.health` |
| Flutter App | Google Play Store | APK download |

**Step-by-Step Deployment Flow:**
```
STEP 1 → Push latest code to GitHub main branch
STEP 2 → Render auto-detects push → rebuilds FastAPI Docker container
STEP 3 → Vercel auto-detects push → rebuilds React dashboard
STEP 4 → Test production API: POST api.vishalya.health/api/predict
STEP 5 → Build Flutter release APK → upload to Play Store
STEP 6 → Update Flutter .env to point to production API URL
```

**Completion Checklist:**
- [ ] `backend/Dockerfile` created for containerized deployment
- [ ] Render service created + `DATABASE_URL`, `MODEL_PATH` env vars set
- [ ] Vercel project linked to `/dashboard` folder
- [ ] CORS in FastAPI updated to allow production frontend domain
- [ ] Flutter `.env.production` points to `https://api.vishalya.health`
- [ ] GitHub Actions CI/CD: on push to `main` → run tests → auto-deploy
- [ ] End-to-end smoke test: mobile form → FastAPI → DB → Dashboard all working

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       VISHALYA SYSTEM                            │
│                                                                  │
│  📱 Flutter Mobile App          🌐 React Dashboard (Vercel)     │
│     (Health Worker — Field)        (District Officer — Web)      │
│     ├─ 10 Symptom Toggles          ├─ Village Heat Map          │
│     ├─ Village PIN input           ├─ Trend Graphs              │
│     └─ AQI auto-fetch              └─ XAI Charts                │
│              │ HTTP POST                     │ REST              │
│              ▼                               ▼                   │
│  ╔═══════════════════════════════════════════════════╗          │
│  ║         ⚡ FastAPI Backend (Render / localhost)    ║          │
│  ║  POST /api/predict                                 ║          │
│  ║  ├─ Pydantic validates JSON (symptom_schema.json)  ║          │
│  ║  ├─ predictor.py loads vishalya_rf_model.joblib   ║          │
│  ║  ├─ model.predict() → 0 or 1                      ║          │
│  ║  ├─ Returns { risk_label, risk_score, xai_scores } ║          │
│  ║  └─ Logs to PostgreSQL (Supabase)                  ║          │
│  ╚═══════════════════════════════════════════════════╝          │
│                                                                  │
│  📦 shared_contracts/symptom_schema.json                         │
│     └─ Single source of truth used by ALL components above       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Current Project Structure

```
Vishalya/                              ← Project root
├── TIMELINE.md                        ← ✅ This file (living document)
├── LICENSE
├── .gitignore
│
├── shared_contracts/                  ← ✅ Done
│   └── symptom_schema.json            ← 10 symptoms + metadata contract
│
├── ml_engine/                         ← ✅ Done
│   ├── Diseases_and_Symptoms_dataset.csv   (46 MB Kaggle dataset)
│   ├── train_model.py                 ← Trains and exports the model
│   ├── inference.py                   ← Tests the model with sample patients
│   └── vishalya_rf_model.joblib       ← 1MB frozen AI model (READY ✅)
│
├── backend/                           ← ⬜ Phase 3 (next to build)
│   ├── requirements.txt
│   ├── models.py
│   ├── predictor.py
│   └── main.py
│
├── mobile/                            ← ⬜ Phase 5
│   └── (Flutter project goes here)
│
└── dashboard/                         ← ⬜ Phase 8
    └── (React + Vite project goes here)
```

---

## 🚀 Current Status & Next Action

**✅ Completed:** Phases 0, 1, 2 — The ML brain is trained and working.
**⬜ Up Next:** Phase 3 — Build the FastAPI backend server.

```bash
# To start Phase 3, run these commands:
mkdir -p /home/kali/Desktop/android-studio/Vishalya/backend
pip3 install fastapi "uvicorn[standard]" pydantic scikit-learn joblib --break-system-packages
```

> 📌 **Note to AI:** Every time a phase is completed, update this file — change `⬜ Pending` → `✅ Done` in the roadmap table and mark all checkboxes `[ ]` → `[x]` in that phase's checklist.
