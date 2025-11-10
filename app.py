import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# -----------------------
# Page setup
# -----------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")
DATA_FILE = "sales_data.csv"

# -----------------------
# Header (logo + title + short summary)
# -----------------------
# Try loading a local logo.png if present
logo_path = Path("logo.png")
col_logo, col_title, col_meta = st.columns([1, 6, 2])

with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=80)
    else:
        st.write("")  # keep column empty if no logo

with col_title:
    st.markdown("<h1 style='margin:0; padding:0;'>Sales Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color: #666; margin-top:6px;'>Interactive dashboard showing monthly sales trends, KPIs and exportable reports.</div>", unsafe_allow_html=True)

with col_meta:
    st.write("")  # reserve space for possible quick links or small info

st.write("---")

# -----------------------
# Load & clean data
# -----------------------
data = pd.read_csv(DATA_FILE)

# Convert Sales to numeric (remove commas/spaces if any)
data["Sales"] = data["Sales"].astype(str).str.replace(",", "").str.strip()
data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")
data = data.dropna(subset=["Sales"]).reset_index(drop=True)

# -----------------------
# Sidebar filters & info
# -----------------------
st.sidebar.header("🔍 Filter Options")
months = st.sidebar.multiselect(
    "Select Month(s):",
    options=list(data["Month"].unique()),
    default=list(data["Month"].unique())
)
st.sidebar.markdown("*Data: Sample sales CSV\nTools*: Python, Pandas, Plotly, Streamlit")

filtered_data = data[data["Month"].isin(months)]

# -----------------------
# KPIs (formatted)
# -----------------------
if len(filtered_data) > 0:
    total_sales = int(filtered_data["Sales"].sum())
    avg_sales = round(filtered_data["Sales"].mean(), 2)
    max_idx = filtered_data["Sales"].idxmax()
    best_month = filtered_data.loc[max_idx, "Month"]
else:
    total_sales = 0
    avg_sales = 0
    best_month = "N/A"

k_col1, k_col2, k_col3 = st.columns([2, 2, 2])
k_col1.metric("💰 Total Sales", f"₹{total_sales:,}")
k_col2.metric("📈 Average Sales", f"₹{avg_sales:,.2f}")
k_col3.metric("🏆 Best Month", best_month)

st.write("")  # small gap

# -----------------------
# Charts (nice white theme)
# -----------------------
st.subheader("📈 Monthly Sales Trend")
fig_line = px.line(filtered_data, x="Month", y="Sales", markers=True, template="plotly_white")
fig_line.update_layout(margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("📊 Sales by Month (Bar)")
fig_bar = px.bar(filtered_data, x="Month", y="Sales", title="", template="plotly_white")
fig_bar.update_layout(margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------
# Table and CSV download
# -----------------------
st.subheader("📄 Filtered Data")
st.dataframe(filtered_data.reset_index(drop=True), use_container_width=True)

csv = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇ Download filtered data (CSV)",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

# -----------------------
# Small footer / project note
# -----------------------
st.write("---")
st.caption("Built with Python, Pandas, Plotly and Streamlit — great for portfolio & interviews.")