import pandas as pd
import streamlit as st


def _safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def plot_kpis(df_cleaned):
    df = df_cleaned.copy()
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.dropna(subset=["Datum"])

    required = ["Landesverbrauch", "Nettoerzeugung Total"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        st.info("KPIs: Spalten fehlen: " + ", ".join(missing))
        return

    df["Landesverbrauch"] = _safe_numeric(df["Landesverbrauch"])
    df["Nettoerzeugung Total"] = _safe_numeric(df["Nettoerzeugung Total"])

    winter_months = {12, 1, 2}
    summer_months = {6, 7, 8}

    winter = df[df["Datum"].dt.month.isin(winter_months)]
    summer = df[df["Datum"].dt.month.isin(summer_months)]

    winter_avg = winter["Landesverbrauch"].mean()
    summer_prod = summer["Nettoerzeugung Total"].mean()

    peak_row = df.loc[df["Nettoerzeugung Total"].idxmax()]
    peak_value = peak_row["Nettoerzeugung Total"]
    peak_date = peak_row["Datum"].strftime("%d.%m")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Winterverbrauch (Ø)", f"{winter_avg:,.0f} GWh".replace(",", "'"))
    with col2:
        st.metric("Sommerproduktion", f"{summer_prod:,.0f} GWh".replace(",", "'"))
    with col3:
        st.metric("Leistungs-Peak", f"{peak_value:,.0f} GWh".replace(",", "'"))
        st.caption(f"am {peak_date}")
