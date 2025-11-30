import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import requests
import json
import pandas as pd
import base64
from io import BytesIO, StringIO
import os

API_BASE = st.secrets.get("API_BASE")
# API_BASE = os.getenv("API_BASE")

# ------------------------ UI STYLING ------------------------
st.set_page_config(page_title="SAYL — Digital Twin Dashboard", layout="centered")

st.markdown("""
<style>
.title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: #3A7AFE;
    margin-bottom: -10px;
}
.tagline {
    font-size: 18px;
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}
.report-box {
    padding: 18px;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    background: #FAFAFA;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">SAYL</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Predict. Prevent. Perform.</div>', unsafe_allow_html=True)

st.write("___")


# ------------------------ SECTION 1: JSON Logger ------------------------
st.subheader("📩 Send Live Sensor Data (JSON)")

json_input = st.text_area("Enter JSON sensor row(s):", placeholder='e.g. {"timestamp":"2025-12-01T12:30","ax":0.8,"ay":0.4,"az":1.1,"gx":0.03,"gy":0.04,"gz":0.06,"class_id":0,"rul_days":120}')

if st.button("Send JSON to Logger"):
    try:
        parsed = json.loads(json_input)
        res = requests.post(f"{API_BASE}/log-json", json=parsed)
        if res.status_code == 200:
            st.success(res.json().get("message"))
        else:
            st.error(res.json())
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format")


st.divider()


# ------------------------ SECTION 2: CSV Upload ------------------------
st.subheader("📁 Upload CSV to Log")

uploaded_csv = st.file_uploader("Select CSV File", type=["csv"])

if st.button("Upload CSV"):
    if uploaded_csv:
        files = {"file": uploaded_csv}
        res = requests.post(f"{API_BASE}/upload-csv", files=files)

        if res.status_code == 200:
            st.success(res.json().get("message"))
        else:
            st.error(res.json())
    else:
        st.warning("Please upload a CSV first.")


st.divider()


# ------------------------ SECTION 3: Inference ------------------------
st.subheader("🧠 Run Prediction / Inference")

if st.button("Run Inference"):
    with st.spinner("Running AI inference... ⏳"):
        res = requests.get(f"{API_BASE}/run-inference")

    if res.status_code == 200:
        data = res.json()

        st.success(f"Motor Health Status → **{data['class_name']}** ({data['class_id']})")

        rul_df = pd.DataFrame({"Hour Ahead": range(1, len(data["rul_forecast"])+1),
                               "Predicted RUL (days)": data["rul_forecast"]})

        # Display table
        with st.expander("📄 Prediction Table"):
            st.dataframe(rul_df)

        # Display plot
        img_bytes = base64.b64decode(data["graph_base64"])
        st.image(img_bytes, caption="🔍 Remaining Useful Life Forecast", use_container_width=True)

        # CSV download button
        csv_bytes = rul_df.to_csv(index=False).encode()
        st.download_button("📥 Download Prediction CSV", csv_bytes, file_name="rul_predictions.csv")
    else:
        st.error(res.json())


st.write("___")
st.caption("© 2025 SAYL — Intelligent Digital Twin Health Monitoring System")
