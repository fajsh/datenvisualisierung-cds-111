import pandas as pd
import streamlit as st


def _safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def build_summary_kpis_html(df_cleaned):
    df = df_cleaned.copy()
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.dropna(subset=["Datum"])

    required = ["Landesverbrauch", "Nettoerzeugung Total"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        return "<div style='color:#000000;'>KPIs: Spalten fehlen.</div>"

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

    cards = [
        ("Winterverbrauch (Ø)", f"{winter_avg:,.0f} GWh".replace(",", "'"), "#6F896F"),
        ("Sommerproduktion", f"{summer_prod:,.0f} GWh".replace(",", "'"), "#C9C39D"),
        ("Leistungs-Peak", f"{peak_value:,.0f} GWh am {peak_date}".replace(",", "'"), "#F2C58B"),
    ]
    items = []
    for title, value, color in cards:
        items.append(
            f"""
            <div style="background-color:{color}; color:#FFFFFF !important; padding:0.8rem 1rem;
                        border-radius:10px; margin-bottom:0.6rem; display:flex;
                        justify-content:space-between; align-items:center; font-weight:600;">
                <span>{title}</span>
                <span>{value}</span>
            </div>
            """
        )
    return "".join(items)


def _summary_card(title, value, bg_color):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            color: #FFFFFF !important;
            padding: 0.8rem 1rem;
            border-radius: 10px;
            margin-bottom: 0.6rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
        ">
            <span>{title}</span>
            <span>{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

    winter_text = f"{winter_avg:,.0f} GWh".replace(",", "'")
    summer_text = f"{summer_prod:,.0f} GWh".replace(",", "'")
    peak_text = f"{peak_value:,.0f} GWh on {peak_date}".replace(",", "'")

    _summary_card("Winter Consumption (Ø)", winter_text, "#6F896F")
    _summary_card("Summer Production", summer_text, "#C9C39D")
    _summary_card("Energy Peak", peak_text, "#F2C58B")
