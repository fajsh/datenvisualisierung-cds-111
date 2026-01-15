import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def build_time_series_fig(df_cleaned, height=320):
    df = df_cleaned.copy()
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.dropna(subset=["Datum"])

    metrics = {
        "Einfuhr": "Import",
        "Ausfuhr": "Export",
        "Nettoerzeugung Total": "Net Production",
        "Landesverbrauch": "National Consumption",
    }
    missing = [col for col in metrics if col not in df.columns]
    if missing:
        st.info("Zeitverlauf: Spalten fehlen: " + ", ".join(missing))
        return

    df = df.set_index("Datum")
    monthly = df[list(metrics.keys())].resample("M").sum()
    monthly = monthly.reindex(pd.date_range(monthly.index.min(), monthly.index.max(), freq="M"))
    monthly = monthly.fillna(0)
    month_labels = [d.strftime("%b") for d in monthly.index]

    palette = [
        "#83686F",
        "#A76E7D",
        "#ECDAC7",
        "#E18262",
        "#F69E6C",
        "#FCC88A",
        "#E0C1A6",
        "#8096AD",
    ]

    fig = go.Figure()
    for idx, (key, label) in enumerate(metrics.items()):
        color = palette[idx % len(palette)]
        fig.add_trace(
            go.Scatter(
                x=month_labels,
                y=monthly[key],
                name=label,
                stackgroup="one",
                mode="lines",
                line={"color": color},
                fillcolor=color,
                hovertemplate=f"{label}: %{{y:.0f}} kWh<extra></extra>",
            )
        )

    fig.update_layout(
        xaxis_title="Monat",
        yaxis_title="kWh",
        hovermode="x unified",
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
        height=height,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )
    return fig


def plot_time_series(df_cleaned, height=320):
    fig = build_time_series_fig(df_cleaned, height=height)
    st.plotly_chart(fig, use_container_width=True)
