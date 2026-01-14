import calendar

import pandas as pd
import plotly.express as px
import streamlit as st


def _build_colorscale(colors):
    if len(colors) == 1:
        return [(0.0, colors[0]), (1.0, colors[0])]
    step = 1 / (len(colors) - 1)
    return [(i * step, color) for i, color in enumerate(colors)]


def build_heatmap_import_export_fig(df_cleaned, height=320):
    df = df_cleaned.copy()
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.dropna(subset=["Datum"])

    monthly = (
        df.groupby(df["Datum"].dt.month)[["Einfuhr", "Ausfuhr", "Landesverbrauch"]]
        .sum()
        .reset_index()
        .rename(columns={"Datum": "Monat"})
    )

    month_labels = [calendar.month_abbr[i] for i in range(1, 13)]
    monthly = monthly.set_index("Monat")
    monthly = monthly.reindex(range(1, 13)).fillna(0)

    data = monthly.rename(
        columns={
            "Einfuhr": "Import",
            "Ausfuhr": "Export",
            "Landesverbrauch": "Verbrauch",
        }
    ).T
    data.columns = month_labels

    palette = [
        "#768E78",
        "#C6C09C",
        "#EBDEC0",
        "#E79897",
        "#FCAC83",
        "#FCC88A",
        "#E0C1A6",
        "#8096AD",
    ]

    fig = px.imshow(
        data,
        text_auto=".0f",
        aspect="auto",
        color_continuous_scale=_build_colorscale(palette),
        labels={"x": "Monat", "y": "Kategorie", "color": "GWh"},
    )
    fig.update_layout(
        title="Import, Export und Verbrauch pro Monat",
        title_font={"color": "#000000"},
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
        coloraxis_colorbar={"title": "GWh"},
        height=height,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )
    return fig


def plot_heatmap_import_export(df_cleaned, height=320):
    fig = build_heatmap_import_export_fig(df_cleaned, height=height)
    st.plotly_chart(fig, use_container_width=True)
