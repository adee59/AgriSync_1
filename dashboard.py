import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

st.set_page_config(page_title="AgriSync Command Center", layout="wide")

st.title("🚜 AgriSync Multi-Agent Operations Console")
st.caption("Cloud Live Feed Mode")

placeholder = st.empty()

# Simulated database log store for cloud presentation
if "cloud_logs" not in st.session_state:
    st.session_state.cloud_logs = []

while True:
    # Generate continuous test telemetry
    soil_val = random.randint(15, 45)
    weather_val = random.randint(10, 90)
    
    if soil_val < 30 and weather_val < 70:
        decision = "ACTIVATE_IRRIGATION"
        reason = "Soil moisture critical (<30%). Low rain probability."
    elif soil_val < 30 and weather_val >= 70:
        decision = "DEFER_IRRIGATION"
        reason = "Soil dry, but rain probability high (>=70%)."
    else:
        decision = "IDLE"
        reason = "Optimal moisture levels maintained."

    # Prepend new log
    st.session_state.cloud_logs.insert(0, {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "decision": decision,
        "reason": reason,
        "context": {"soil": soil_val, "weather": weather_val}
    })
    
    # Keep last 10 records
    st.session_state.cloud_logs = st.session_state.cloud_logs[:10]
    df = pd.DataFrame(st.session_state.cloud_logs)

    with placeholder.container():
        if not df.empty:
            last_entry = df.iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Current Action", last_entry['decision'])
            c2.metric("Soil Moisture", f"{last_entry['context']['soil']}%")
            c3.metric("Rain Probability", f"{last_entry['context']['weather']}%")

            st.subheader("Decision Audit Trail")
            st.dataframe(df[['timestamp', 'decision', 'reason', 'context']], use_container_width=True)

    time.sleep(2)
