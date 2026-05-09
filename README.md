# PV String Performance Analysis Tool

**Solar Portfolio Analytics Portfolio Project**

A complete end-to-end data tool that transforms raw SCADA telemetry and wiring plans into actionable insights for detecting underperforming PV strings.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://solar-string-analytics.streamlit.app/)

### Project Objective
Build a reliable data pipeline to identify underperforming components in a solar plant and help Operations & Maintenance teams prioritize work.

### Key Features
- Full data pipeline: Raw SCADA → clean per-string time series
- String-to-inverter mapping using wiring plans
- Performance metrics (Performance Ratio, temperature normalized power)
- Automated detection of underperformance and clipping
- Interactive Streamlit dashboard with maintenance priority list

### Live Demo
**👉 [Open Live Dashboard](https://solar-string-analytics.streamlit.app/)**

### Tech Stack
- Python, pandas, NumPy
- Plotly (interactive visualizations)
- Streamlit (web dashboard)
- Parquet for efficient data storage

### Screenshots

*(Add your 3–4 screenshots here after you take them)*

![Dashboard Overview](images/overview.png)
![Power Analysis](images/string_comparison.png)
![Maintenance Priority](images/maintanence_priority.png)

### How to Run Locally

```bash
conda activate solar_analysis
streamlit run dashboards/app.py


Results & Business Impact

Successfully created clean per-string time series from raw data
Detected underperforming strings (e.g. STR_07 showing only ~6% of expected performance)
Built a clear maintenance priority ranking
Demonstrated full data lifecycle: ingestion → cleaning → analysis → visualization

This project shows my ability to handle real-world solar data challenges and deliver practical tools that support asset management decisions.


