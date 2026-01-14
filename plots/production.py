import streamlit as st
import pandas as pd
import calendar
import plotly.express as px
import plotly.graph_objects as go
from utils.colors import ENERGY_COLORS

def build_stacked_bar_interactive(df_monthly_sums, selected_month, height=320):
    df = df_monthly_sums.copy()
    df = df[df['Monat'] != 'Total']

    energy_sources = [
        'Laufwerke',
        'Speicherwerke',
        'Kernkraftwerke',
        'Thermisch',
        'Windkraft',
        'Photovoltaik'
    ]

    month_map = {
        f"{i:02d}": calendar.month_name[i]
        for i in range(1, 13)
    }

    df["Monat_Name"] = df["Monat"].map(month_map)

    # Filter für Balkendiagramm, falls Monat gewählt (außer "Total")
    if selected_month != "Total":
        df_filtered = df[df["Monat"] == selected_month]
        months_display = [month_map[selected_month]]
    else:
        df_filtered = df
        months_display = df_filtered["Monat_Name"].tolist()

    fig = go.Figure()

    for source in energy_sources:
        fig.add_trace(
            go.Bar(
                x=months_display,
                y=df_filtered[source],
                name=source,
                marker_color=ENERGY_COLORS.get(source),
                hovertemplate=(
                    f"<b>{source}</b><br>"
                    "Month: %{x}<br>"
                    "%{y:.1f} GWh<extra></extra>"
                )
            )
        )

    fig.update_layout(
        title="Monthly energy production by source",
        title_font={"color": "#000000"},
        xaxis_title="Month",
        yaxis_title="Energy production (GWh)",
        barmode="stack",
        legend_title_text="Energy source",
        hovermode="x unified",
        height=height,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )
    return fig


def plot_stacked_bar_interactive(df_monthly_sums, selected_month, height=320):
    fig = build_stacked_bar_interactive(df_monthly_sums, selected_month, height=height)
    st.plotly_chart(fig, use_container_width=True)

def build_donut(df_monthly_sums, selected_month, height=320):
    df = df_monthly_sums.copy()

    energy_sources = [
        'Laufwerke',
        'Speicherwerke',
        'Kernkraftwerke',
        'Thermisch',
        'Windkraft',
        'Photovoltaik'
    ]

    month_map = {
        f"{i:02d}": calendar.month_name[i]
        for i in range(1, 13)
    }
    month_map["Total"] = "Total"

    # Filter für Donut
    df_selected = df[df['Monat'] == selected_month]

    values = df_selected[energy_sources].values.flatten()

    df_donut = pd.DataFrame({
        "Energiequelle": energy_sources,
        "Wert_TWh": values
    })

    total = df_donut["Wert_TWh"].sum()
    df_donut["Prozent"] = (df_donut["Wert_TWh"] / total * 100).round(1)

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
        title=None,
        height=height,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        title_font={"color": "#000000"},
    )
    return fig


def plot_donut(df_monthly_sums, selected_month, height=320):
    fig = build_donut(df_monthly_sums, selected_month, height=height)
    st.plotly_chart(fig, use_container_width=True)

def production_plots(df_monthly_sums, height=320):
    # Monat-Mapping für Dropdown
    month_map = {
        f"{i:02d}": calendar.month_name[i]
        for i in range(1, 13)
    }
    month_map["Total"] = "Total"

    months_numeric = df_monthly_sums['Monat'].tolist()
    months_display = [month_map[m] for m in months_numeric]

    # Dropdown oberhalb des Balkendiagramms
    selected_display = st.selectbox(
        "Choose month",
        months_display,
        index=months_display.index("Total") if "Total" in months_display else 0
    )

    reverse_map = {v: k for k, v in month_map.items()}
    selected_month = reverse_map[selected_display]

    col1, col2 = st.columns(2)

    with col1:
        plot_stacked_bar_interactive(df_monthly_sums, selected_month, height=height)

    with col2:
        plot_donut(df_monthly_sums, selected_month, height=height)


"""
für app.py:

st.subheader("Energy Overview")
render_energy_kpis(df_cleaned)

st.subheader("Produktion")
production_plots(df_monthly)
"""
