import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="PV String Performance Tool", layout="wide")
st.title("☀️ PV String Performance Analysis Tool")

# Load data
@st.cache_data
def load_data():
    df = pd.read_parquet('data/processed/per_string_data.parquet')
    summary = pd.read_csv('reports/string_performance_summary.csv')
    return df, summary

df, summary = load_data()

# Sidebar
st.sidebar.header("Filters")
selected_strings = st.sidebar.multiselect("Select Strings", df['string_id'].unique(), default=df['string_id'].unique()[:5])

# Main Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Strings", df['string_id'].nunique())
col2.metric("Underperforming", summary['is_underperforming'].sum())
col3.metric("Avg Performance Ratio", f"{summary['avg_pr'].mean():.3f}")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "String Comparison", "Maintenance Priority"])

with tab1:
    st.subheader("Power Output Over Time")
    fig = px.line(df[df['string_id'].isin(selected_strings)], 
                  x='timestamp', y='power_kw', color='string_id',
                  title="Power Production by String")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Performance Ratio Comparison")
    fig2 = px.bar(summary, x=summary.index, y='avg_pr', 
                  color='is_underperforming',
                  title="Average Performance Ratio per String",
                  labels={'avg_pr': 'Avg Performance Ratio'})
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("🔥 Maintenance Priority List")
    display_summary = summary.copy()
    display_summary['Recommendation'] = display_summary['is_underperforming'].apply(
        lambda x: "High Priority - Investigate" if x else "Normal"
    )
    st.dataframe(display_summary.style.highlight_max(axis=0, color='lightcoral'), use_container_width=True)

st.caption("Portfolio Project • End-to-End PV String Analysis Pipeline")