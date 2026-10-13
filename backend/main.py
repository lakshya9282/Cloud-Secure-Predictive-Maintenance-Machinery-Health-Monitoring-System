import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

app = FastAPI(title="Predictive Maintenance API", version="1.0.0")
rng = np.random.default_rng(42)
n = 6000
vibration = rng.uniform(2, 100, n)
temperature = rng.uniform(20, 150, n)
rpm = rng.uniform(500, 3500, n)
torque = rng.uniform(5, 100, n)
wear = rng.uniform(0, 250, n)
score = .32*vibration/100 + .27*temperature/150 + .18*rpm/3500 + .13*torque/100 + .10*wear/250
y = (score > .49).astype(int)
X = np.column_stack([vibration, temperature, rpm, torque, wear])
model = make_pipeline(MinMaxScaler(), RandomForestClassifier(n_estimators=120, max_depth=10, class_weight="balanced", random_state=42))
model.fit(X, y)

class MachineInput(BaseModel):
    vibration: float = Field(ge=0, le=200)
    temperature: float = Field(ge=-20, le=250)
    rpm: float = Field(ge=0, le=10000)
    torque: float = Field(ge=0, le=500)
    tool_wear: float = Field(default=100, ge=0, le=1000)

@app.get("/")
def root():
    return {"message": "Predictive Maintenance API", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}

@app.post("/predict")
def predict(data: MachineInput):
    vals = np.array([[data.vibration, data.temperature, data.rpm, data.torque, data.tool_wear]])
    risk = round(float(model.predict_proba(vals)[0][1]) * 100, 1)
    if risk >= 70:
        status, action = "CRITICAL: Maintenance Required!", "Stop and inspect the machine"
    elif risk >= 40:
        status, action = "Warning: Inspection Recommended", "Schedule maintenance inspection"
    else:
        status, action = "Normal Operation", "Continue monitoring"
    reasons = []
    if data.vibration >= 50: reasons.append("Elevated vibration")
    if data.temperature >= 90: reasons.append("High operating temperature")
    if data.rpm >= 2800: reasons.append("High rotational speed")
    if data.torque >= 75: reasons.append("High torque")
    if data.tool_wear >= 180: reasons.append("High tool wear")
    if not reasons: reasons.append("No individual input crossed demo warning thresholds")
    return {"risk_score": risk, "status": status, "recommended_action": action,
            "explanation": reasons, "model_note": "Demo model trained on simulated data; not validated for industrial safety."}
