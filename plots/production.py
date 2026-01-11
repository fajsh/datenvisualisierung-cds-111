import streamlit as st
import matplotlib.pyplot as plt
from utils.colors import ENERGY_COLORS
import pandas as pd
import plotly.express as px
import calendar
import streamlit as st
import plotly.graph_objects as go
from utils.colors import ENERGY_COLORS


def plot_stacked_bar_interactive(df_monthly_sums):
    # -------------------------------------------------
    # DATA PREP
    # -------------------------------------------------
    df = df_monthly_sums.copy()

    # Total-Zeile entfernen
    df = df[df['Monat'] != 'Total']

    energy_sources = [
        'Laufwerke',
        'Speicherwerke',
        'Kernkraftwerke',
        'Thermisch',
        'Windkraft',
        'Photovoltaik'
    ]

    months = df['Monat'].tolist()

    # -------------------------------------------------
    # PLOTLY STACKED BAR
    # -------------------------------------------------
    fig = go.Figure()

    for source in energy_sources:
        fig.add_trace(
            go.Bar(
                x=months,
                y=df[source],
                name=source,
                marker_color=ENERGY_COLORS.get(source),
                hovertemplate=(
                    f"<b>{source}</b><br>"
                    "Monat: %{x}<br>"
                    "%{y:.1f} GWh<extra></extra>"
                )
            )
        )

    fig.update_layout(
        title="Monatliche Energieerzeugung nach Quelle (2025)",
        xaxis_title="Monat",
        yaxis_title="Energieerzeugung (GWh)",
        barmode="stack",
        legend_title_text="Energiequelle",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_donut_with_month_selector(df_monthly_sums):
    # -------------------------------------------------
    # DATA PREP
    # -------------------------------------------------
    df = df_monthly_sums.copy()

    energy_sources = [
        'Laufwerke',
        'Speicherwerke',
        'Kernkraftwerke',
        'Thermisch',
        'Windkraft',
        'Photovoltaik'
    ]

    # -------------------------------------------------
    # Monat-Mapping: numerisch -> Name
    # -------------------------------------------------
    month_map = {
        f"{i:02d}": calendar.month_name[i]
        for i in range(1, 13)
    }
    month_map["Total"] = "Total"

    # verfügbare Monate (numerisch)
    months_numeric = df['Monat'].tolist()

    # Anzeige-Namen
    months_display = [month_map[m] for m in months_numeric]

    # -------------------------------------------------
    # UI: Dropdown
    # -------------------------------------------------
    selected_display = st.selectbox(
        "Monat wählen",
        months_display,
        index=months_display.index("Total") if "Total" in months_display else 0
    )

    # Rückübersetzung Display → numerisch
    reverse_map = {v: k for k, v in month_map.items()}
    selected_month = reverse_map[selected_display]

    # -------------------------------------------------
    # Filter für gewählten Monat
    # -------------------------------------------------
    df_selected = df[df['Monat'] == selected_month]

    values = df_selected[energy_sources].values.flatten()

    df_donut = pd.DataFrame({
        "Energiequelle": energy_sources,
        "Wert_TWh": values
    })

    total = df_donut["Wert_TWh"].sum()
    df_donut["Prozent"] = (df_donut["Wert_TWh"] / total * 100).round(1)

    # -------------------------------------------------
    # DONUT (Plotly)
    # -------------------------------------------------
    fig = px.pie(
        df_donut,
        names="Energiequelle",
        values="Wert_TWh",
        hole=0.55,
        color="Energiequelle",
        color_discrete_map=ENERGY_COLORS
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{value:.1f} TWh<br>"
            "%{percent:.1%}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Energieerzeugung nach Quelle ({selected_display})",
        legend_title_text="Energiequelle"
    )

    st.plotly_chart(fig, use_container_width=True)
