import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(page_title="AVDP Final Impact Dashboard", layout="wide")
st.title("🌾 AVDP Final Performance & Impact Dashboard")
st.markdown("### Climate-Smart Agriculture & Value Chain Impact (2019–2025)")

# Sample Data
data = {
    "Region": ["Bo", "Kenema", "Kono", "Kailahun", "Tonkolili", "Port Loko"],
    "Value Chain": ["Rice", "Cocoa", "Oil Palm", "Vegetables", "Rice", "Vegetables"],
    "CSA Practice": [
        "Bunds & Compost", "Improved Seedlings", "Mulching & Drainage",
        "Drip Irrigation", "Raised Beds", "Shading & Mulching"
    ],
    "Farmers Trained": [1500, 1200, 1100, 1800, 1300, 1600],
    "Women (%)": [42, 38, 36, 55, 48, 53],
    "Youth (%)": [30, 25, 28, 50, 40, 45],
    "Yield Before (t/ha)": [1.2, 0.8, 1.0, 2.5, 1.1, 2.2],
    "Yield After (t/ha)": [2.1, 1.6, 1.8, 4.2, 2.3, 3.8]
}

df = pd.DataFrame(data)
df["Yield Increase (%)"] = ((df["Yield After (t/ha)"] - df["Yield Before (t/ha)"]) / df["Yield Before (t/ha)"]) * 100

# Filters
region_filter = st.selectbox("Filter by Region", options=["All"] + list(df["Region"].unique()))
value_chain_filter = st.selectbox("Filter by Value Chain", options=["All"] + list(df["Value Chain"].unique()))

filtered_df = df.copy()
if region_filter != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region_filter]
if value_chain_filter != "All":
    filtered_df = filtered_df[filtered_df["Value Chain"] == value_chain_filter]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("👨‍🌾 Total Farmers Trained", f"{filtered_df['Farmers Trained'].sum():,}")
col2.metric("📈 Avg Yield Increase", f"{filtered_df['Yield Increase (%)'].mean():.1f}%")
col3.metric("👩 Women Participation", f"{filtered_df['Women (%)'].mean():.1f}%")

# Charts
st.markdown("### 📊 Yield Improvement by Region")
fig1 = px.bar(filtered_df, x="Region", y="Yield Increase (%)", color="Value Chain", barmode="group", height=400)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 🌱 CSA Practices by Value Chain")
fig2 = px.sunburst(filtered_df, path=["Value Chain", "CSA Practice"], values="Farmers Trained", color="Yield Increase (%)", height=400)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 👥 Gender & Youth Participation")
fig3 = px.scatter(filtered_df, x="Women (%)", y="Youth (%)", size="Farmers Trained", color="Value Chain", hover_name="Region")
st.plotly_chart(fig3, use_container_width=True)

# Data Table
st.markdown("### 📄 Detailed Intervention Data")
st.dataframe(filtered_df)
