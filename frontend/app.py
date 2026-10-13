import os
import requests
import streamlit as st

st.set_page_config(page_title="Machinery Health Monitor", page_icon="⚙️", layout="wide")
api = os.getenv("API_URL", "http://backend:8000").rstrip("/")
st.title("⚙️ Cloud-Secure Predictive Maintenance")
st.caption("Streamlit + FastAPI + Docker + AWS EC2")
st.warning("Educational prototype only. Do not use for safety-critical industrial decisions.")

with st.sidebar:
    st.header("Machine parameters")
    vibration = st.slider("Vibration (mm/s)", 0.0, 100.0, 15.0, 0.5)
    temperature = st.slider("Temperature (°C)", 0.0, 150.0, 50.0, 1.0)
    rpm = st.slider("Rotational speed (RPM)", 500, 3500, 1400, 50)
    torque = st.slider("Torque", 5.0, 100.0, 40.0, 1.0)
    wear = st.slider("Tool wear (minutes)", 0.0, 250.0, 80.0, 5.0)
    run = st.button("Assess machine health", type="primary")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Sensor readings")
    st.metric("Vibration", f"{vibration:.1f} mm/s")
    st.metric("Temperature", f"{temperature:.1f} °C")
    st.metric("RPM", str(rpm))
with c2:
    st.subheader("Service status")
    try:
        r = requests.get(f"{api}/health", timeout=3)
        st.success("FastAPI connected") if r.ok else st.error("Backend error")
    except requests.RequestException:
        st.error("Backend unreachable; check Docker services.")

if run:
    payload = {"vibration": vibration, "temperature": temperature, "rpm": rpm, "torque": torque, "tool_wear": wear}
    try:
        r = requests.post(f"{api}/predict", json=payload, timeout=10)
        r.raise_for_status()
        result = r.json()
        st.divider()
        a, b = st.columns(2)
        a.metric("Risk score", f"{result['risk_score']:.1f}/100")
        b.progress(min(max(result["risk_score"]/100, 0), 1))
        if result["risk_score"] >= 70: st.error(result["status"])
        elif result["risk_score"] >= 40: st.warning(result["status"])
        else: st.success(result["status"])
        st.write("**Recommended action:**", result["recommended_action"])
        st.write("**Explanation:**")
        for reason in result["explanation"]: st.write("- " + reason)
        with st.expander("Raw API response"): st.json(result)
    except requests.RequestException as e:
        st.error(f"Prediction failed: {e}")
