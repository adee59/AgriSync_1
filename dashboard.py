import streamlit as st
import pandas as pd
from pymongo import MongoClient
import time

st.set_page_config(page_title="AgriSync Command Center", layout="wide")
client = MongoClient("mongodb://admin:password123@localhost:27017/")
db = client.agrisync_records

st.title("?? AgriSync Multi-Agent Operations Console")

placeholder = st.empty()

while True:
    with placeholder.container():
        cursor = db.logs.find().sort("_id", -1).limit(10)
        df = pd.DataFrame(list(cursor))

        if not df.empty:
            last_entry = df.iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Current Action", last_entry['decision'])
            c2.metric("Soil Moisture", f"{last_entry['context']['soil']}%")
            c3.metric("Rain Probability", f"{last_entry['context']['weather']}%")

            st.subheader("Decision Audit Trail")
            st.dataframe(df[['decision', 'reason', 'context']], use_container_width=True)
        else:
            st.info("Awaiting telemetry data stream...")

    time.sleep(2)
