import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="UAC Care Load Forecasting", page_icon="📊", layout="wide")

DATE_COL = "Date"
HHS_COL = "Children in HHS Care"
DISCHARGE_COL = "Children discharged from HHS Care"

st.title("UAC Care Load & Placement Demand Forecasting")
st.caption("Exploratory dashboard and simple 30-day baseline forecast using the uploaded UAC/HHS dataset.")

st.info(
    "This app uses a simple baseline forecast: the mean of the latest 7 available observations. "
    "It is a learning/portfolio demonstration, not an official operational forecast."
)

uploaded_file = st.file_uploader("Upload your cleaned UAC dataset (CSV)", type=["csv"])

default_path = Path("UAC_Cleaned_Dataset.csv")
df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the uploaded CSV: {exc}")
elif default_path.exists():
    try:
        df = pd.read_csv(default_path)
        st.success(f"Loaded local file: {default_path.name}")
    except Exception as exc:
        st.error(f"Could not read {default_path.name}: {exc}")

if df is None:
    st.warning(
        "Upload your cleaned CSV to start. For automatic loading, place "
        "`UAC_Cleaned_Dataset.csv` in the same folder as `app.py`."
    )
    st.stop()

# Normalize headers and check required columns
df.columns = [str(c).strip() for c in df.columns]
required = [DATE_COL, HHS_COL, DISCHARGE_COL]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Missing required column(s): " + ", ".join(missing))
    st.write("Columns found in this file:", list(df.columns))
    st.stop()

df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
for col in [HHS_COL, DISCHARGE_COL]:
    # Values such as "2,484" contain thousands separators; remove them before conversion.
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"": None, "nan": None, "None": None})
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=[DATE_COL]).sort_values(DATE_COL).reset_index(drop=True)

if df.empty:
    st.error("No valid dates were found in the Date column.")
    st.stop()

min_date = df[DATE_COL].min().date()
max_date = df[DATE_COL].max().date()
st.caption(f"Data range: {min_date} to {max_date} · {len(df):,} rows after removing invalid dates")

# KPI cards
latest_hhs = df[HHS_COL].dropna()
latest_dis = df[DISCHARGE_COL].dropna()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Rows", f"{len(df):,}")
k2.metric("Latest HHS care value", f"{latest_hhs.iloc[-1]:,.0f}" if not latest_hhs.empty else "N/A")
k3.metric("Latest discharge value", f"{latest_dis.iloc[-1]:,.0f}" if not latest_dis.empty else "N/A")
k4.metric("Missing dates in Date column", f"{int(df[DATE_COL].isna().sum()):,}")

st.subheader("Historical trends")
tab1, tab2, tab3 = st.tabs(["HHS Care", "Discharges", "Dataset preview"])

with tab1:
    chart_df = df.dropna(subset=[HHS_COL])
    if not chart_df.empty:
        fig = px.line(chart_df, x=DATE_COL, y=HHS_COL, markers=True, title="Children in HHS Care over time")
        fig.update_layout(xaxis_title="Date", yaxis_title="Children in HHS Care")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric values found for HHS care.")

with tab2:
    chart_df = df.dropna(subset=[DISCHARGE_COL])
    if not chart_df.empty:
        fig = px.line(chart_df, x=DATE_COL, y=DISCHARGE_COL, markers=True, title="Children discharged from HHS Care over time")
        fig.update_layout(xaxis_title="Date", yaxis_title="Children discharged")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric values found for discharges.")

with tab3:
    st.dataframe(df.head(100), use_container_width=True)
    st.download_button(
        "Download data with parsed dates",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="uac_dataset_preview.csv",
        mime="text/csv",
    )

st.subheader("Simple 30-day baseline forecast")
forecast_days = st.slider("Forecast horizon (days)", min_value=7, max_value=60, value=30, step=1)
last_date = df[DATE_COL].max()
future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=forecast_days, freq="D")

def make_forecast(series, output_name):
    values = series.dropna().tail(7)
    if values.empty:
        return None
    avg = float(values.mean())
    return pd.DataFrame({"Date": future_dates, output_name: [avg] * len(future_dates)}), avg, len(values)

forecast1 = make_forecast(df[HHS_COL], "Predicted_HHS_Care")
forecast2 = make_forecast(df[DISCHARGE_COL], "Predicted_Discharges")

fc1, fc2 = st.columns(2)
if forecast1 is not None:
    forecast_df, avg, n = forecast1
    fc1.metric("HHS baseline estimate", f"{avg:,.2f}", help=f"Mean of last {n} available observations")
    fig = px.line(forecast_df, x="Date", y="Predicted_HHS_Care", title="HHS care baseline forecast")
    fc1.plotly_chart(fig, use_container_width=True)
else:
    fc1.warning("Not enough numeric HHS care data to forecast.")

if forecast2 is not None:
    forecast_df2, avg2, n2 = forecast2
    fc2.metric("Discharge baseline estimate", f"{avg2:,.2f}", help=f"Mean of last {n2} available observations")
    fig = px.line(forecast_df2, x="Date", y="Predicted_Discharges", title="Discharge baseline forecast")
    fc2.plotly_chart(fig, use_container_width=True)
else:
    fc2.warning("Not enough numeric discharge data to forecast.")

if forecast1 is not None:
    st.download_button(
        "Download HHS care forecast CSV",
        data=forecast1[0].to_csv(index=False).encode("utf-8"),
        file_name="HHS_Care_Forecast.csv",
        mime="text/csv",
    )
if forecast2 is not None:
    st.download_button(
        "Download discharge forecast CSV",
        data=forecast2[0].to_csv(index=False).encode("utf-8"),
        file_name="HHS_Discharge_Forecast.csv",
        mime="text/csv",
    )

st.subheader("Data quality notes")
st.write(f"- Missing HHS care values: {int(df[HHS_COL].isna().sum()):,}")
st.write(f"- Missing discharge values: {int(df[DISCHARGE_COL].isna().sum()):,}")
st.write("- Missing reporting dates are not automatically filled with zero.")
st.write("- Forecast dates start after the last date in the uploaded dataset, not today's date.")
st.write("- This baseline repeats the recent 7-observation average; it does not model seasonality, uncertainty, or policy changes.")
