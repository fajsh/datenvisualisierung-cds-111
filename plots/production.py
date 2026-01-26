import calendar
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from utils.colors import ENERGY_COLORS


ENERGY_SOURCES = [
    "Laufwerke",
    "Speicherwerke",
    "Kernkraftwerke",
    "Thermisch",
    "Windkraft",
    "Photovoltaik",
]


def production_plots(
    df_monthly,
    height=220,
    selected_month="Total",
    show_bar=True,
    show_donut=True,
):
    """
    Flexible production plot renderer.
    Can render stacked bar, donut, or both depending on flags.
    """

    df = df_monthly.copy()

    # -----------------------------
    # Month mapping: Zahl → Name
    # -----------------------------
    month_map = {f"{i:02d}": calendar.month_name[i] for i in range(1, 13)}
    month_map["Total"] = "Total"

    # Convert selected_month Zahl (z.B. "01") in Namen (z.B. "January")
    if selected_month in month_map:
        selected_month = month_map[selected_month]

    # -----------------------------
    # BAR CHART (stacked)
    # -----------------------------
    if show_bar:
        df_bar = df[df["Monat"] != "Total"].copy()
        df_bar["Monat_Name"] = df_bar["Monat"].map(month_map)

        if selected_month != "Total":
            df_bar = df_bar[df_bar["Monat_Name"] == selected_month]

        fig_bar = go.Figure()

        for src in ENERGY_SOURCES:
            fig_bar.add_trace(
                go.Bar(
                    x=df_bar["Monat_Name"],
                    y=df_bar[src],
                    name=src,
                    marker_color=ENERGY_COLORS.get(src),
                )
            )

        fig_bar.update_layout(
            height=height,
            barmode="stack",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title=None,
            yaxis_title="GWh",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10),
            ),
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # -----------------------------
    # DONUT CHART
    # -----------------------------
    if show_donut:
        if selected_month == "Total":
            df_donut = df[df["Monat"] == "Total"]
        else:
            df_donut = df[df["Monat"] != "Total"].copy()
            df_donut["Monat_Name"] = df_donut["Monat"].map(month_map)
            df_donut = df_donut[df_donut["Monat_Name"] == selected_month]

        if df_donut.empty:
            st.warning("No data available for selected month.")
            return

        # Werte der einen Zeile extrahieren (nur wenn genau eine Zeile da ist)
        row = df_donut.iloc[0]
        values = [row[src] for src in ENERGY_SOURCES]

        donut_df = pd.DataFrame(
            {
                "Energiequelle": ENERGY_SOURCES,
                "Wert": values,
            }
        )

        fig_donut = px.pie(
            donut_df,
            names="Energiequelle",
            values="Wert",
            hole=0.6,
            color="Energiequelle",
            color_discrete_map=ENERGY_COLORS,
        )

        fig_donut.update_layout(
            height=height,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )

        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>%{value:.1f} GWh<extra></extra>",
        )

        st.plotly_chart(fig_donut, use_container_width=True)

