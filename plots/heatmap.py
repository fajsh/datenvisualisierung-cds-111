import calendar

import altair as alt
import pandas as pd
import streamlit as st


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
            "Landesverbrauch": "Consumption",
        }
    ).T
    data.columns = month_labels

    df_long = (
        data.reset_index()
        .melt(id_vars="index", var_name="Month", value_name="GWh")
        .rename(columns={"index": "Category"})
    )

    palette = [
        "#F3F1F4",
        "#DDD7DF",
        "#C7BECB",
        "#B0A4B6",
        "#9A8BA2",
        "#7A6883",
        "#6C5D74",
        "#55495B",
        "#3D3441",
        "#252028",
        "#0D0B0E",
    ]

    categories = df_long["Category"].unique().tolist()
    months = df_long["Month"].unique().tolist()
    max_rows = max(len(categories), 1)
    max_cols = max(len(months), 1)
    cell_size = max(12, int(height / max_rows))

    base = alt.Chart(df_long).mark_rect(cornerRadius=2).encode(
        x=alt.X("Month:O", title="Month", sort=month_labels),
        y=alt.Y("Category:O", title="Category", sort=categories),
        color=alt.Color("GWh:Q", scale=alt.Scale(range=palette)),
        tooltip=["Category", "Month", "GWh"],
    )

    text = alt.Chart(df_long).mark_text(fontSize=11, color="#000000").encode(
        x=alt.X("Month:O", sort=month_labels),
        y=alt.Y("Category:O", sort=categories),
        text=alt.Text("GWh:Q", format=".0f"),
    )

    return (
        alt.layer(base, text)
        .properties(
            width=cell_size * max_cols,
            height=cell_size * max_rows,
        )
        .configure_view(strokeWidth=0, fill="transparent")
        .configure(background="transparent")
        .configure_axis(labelColor="#000000", titleColor="#000000")
    )


def plot_heatmap_import_export(df_cleaned, height=320):
    chart = build_heatmap_import_export_fig(df_cleaned, height=height)
    st.altair_chart(chart, use_container_width=True)
