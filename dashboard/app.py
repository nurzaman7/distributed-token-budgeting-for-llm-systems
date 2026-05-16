from __future__ import annotations

import streamlit as st
import pandas as pd
import httpx
import plotly.express as px

API_BASE = st.sidebar.text_input("API Base URL", "http://localhost:8080")

st.set_page_config(page_title="Token Budgeting Dashboard", layout="wide")
st.title("Distributed Token Budgeting for LLM Systems")


def fetch(path: str):
    with httpx.Client(timeout=10.0) as c:
        r = c.get(f"{API_BASE.rstrip('/')}{path}")
        r.raise_for_status()
        return r.json()


if st.button("Run 10,000-request Simulation"):
    with httpx.Client(timeout=120.0) as c:
        c.post(f"{API_BASE.rstrip('/')}/simulate", params={"requests": 10000, "seed": 42}).raise_for_status()

metrics = fetch("/metrics")
if not metrics:
    st.info("No data yet. Run simulation first.")
    st.stop()

mdf = pd.DataFrame(metrics)
st.subheader("Strategy Comparison")
st.dataframe(mdf, use_container_width=True)

fig1 = px.bar(mdf, x="strategy", y="avg_latency_ms", title="Average Latency by Strategy")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(mdf, x="strategy", y="p95_latency_ms", title="P95 Latency by Strategy")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(mdf, x="strategy", y="rejection_rate", title="Rejection Rate by Strategy")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.bar(mdf, x="strategy", y="cost_per_1000_req_usd", title="Cost per 1,000 Requests")
st.plotly_chart(fig4, use_container_width=True)

rows = fetch("/results?limit=3000")
df = pd.DataFrame(rows)
if not df.empty:
    h = px.density_heatmap(df, x="total_tokens", y="strategy", z="latency_ms", histfunc="avg", title="Latency Heatmap by Token Budget")
    st.plotly_chart(h, use_container_width=True)
