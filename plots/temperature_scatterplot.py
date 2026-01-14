# Importing Libraries
# import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# importing color codes
from utils.colors import (
    LANDESVERBRAUCH,
    WASSERFUEHRUNG,
    GRAU,
    ACHSE,
    PLOT_HINTERGRUND,
    LEGENDE_HINTERGRUND,
    TOGGLE_HINTERGRUND,
    TOGGLE_TEXT
)

# function to build scatterplot
def temp_scatter(
    df: pd.DataFrame,
    width=1000,
    height=650,
    compact=False,
    show_controls=True,
    show_legend=True,
) -> go.Figure:
    axis_lw = 1.5 if compact else 2
    # Assigning column names
    x = df["Mittlere Tagestemperatur"]
    y_consumption = df["Landesverbrauch"]
    y_rhine = df["Wasserführung Rhein"]

    # Assigning outliers
    cons_outlier_mask = y_consumption > y_consumption.quantile(0.95)
    rhine_outlier_mask = y_rhine < y_rhine.quantile(0.05)  # low-flow outliers

    # Assigning Trend lines
    coef_cons = np.polyfit(x, y_consumption, 1)
    coef_rhine = np.polyfit(x, y_rhine, 1)

    x_trend = np.linspace(x.min(), x.max(), 50)
    y_trend_cons = np.polyval(coef_cons, x_trend)
    y_trend_rhine = np.polyval(coef_rhine, x_trend)

    # Creating figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Scatter dots: Landesverbrauch (coloured)
    fig.add_trace(
        go.Scatter(
            x=x[~cons_outlier_mask],
            y=y_consumption[~cons_outlier_mask],
            mode="markers",
            name="Landesverbrauch",
            marker=dict(
                color=LANDESVERBRAUCH,
                size=9,
                line=dict(width=1, color="white"),
            ),
            hovertemplate=(
                "Temp: %{x:.1f} °C<br>"
                "Verbrauch: %{y:.0f} GWh"
                "<extra></extra>"
            ),
            opacity=1.0,
        ),
        secondary_y=False
    )

    # Scatter dots: Landesverbrauch (grey background when off)
    fig.add_trace(
        go.Scatter(
            x=x[~cons_outlier_mask],
            y=y_consumption[~cons_outlier_mask],
            mode="markers",
            name="Landesverbrauch (grau)",
            # legendgroup="cons",
            marker=dict(color=GRAU, size=9),
            opacity=0.0,  # hidden when toggle on
            # hoverinfo="skip",
            showlegend=False,
        ),
        secondary_y=False)  # trace 1

    # Scatter dots: Wasserführung Rhein (coloured)
    fig.add_trace(
        go.Scatter(
            x=x[~rhine_outlier_mask],
            y=y_rhine[~rhine_outlier_mask],
            mode="markers",
            name="Wasserführung Rhein",
            marker=dict(
                color=WASSERFUEHRUNG,
                size=9,
                line=dict(width=1, color="white"),
            ),
            hovertemplate=(
                "Temp: %{x:.1f} °C<br>"
                "Rhein: %{y:.0f} m³/s"
                "<extra></extra>"
            ),
            opacity=1.0,
        ),
        secondary_y=True
    )

    # Scatter dots: Wasserführung Rhein (grey when off)
    fig.add_trace(
        go.Scatter(
            x=x[~rhine_outlier_mask],
            y=y_rhine[~rhine_outlier_mask],
            mode="markers",
            name="Wasserführung Rhein (grau)",
            # legendgroup="rhine",
            marker=dict(color=GRAU, size=9),
            opacity=0.0,  # off by default
            # hoverinfo="skip",
            showlegend=False,
        ),
        secondary_y=True)  # trace 3

    # Trendline: Landesverbrauch
    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=y_trend_cons,
            mode="lines",
            name="Trend (Landesverbrauch)",
            # legendgroup="trend",
            line=dict(color=LANDESVERBRAUCH, width=2),
            # opacity=1.0,                       # on by default
            # showlegend=True,
        ),
        secondary_y=False)  # trace 4

    # Trendline: Wasserführung Rhein
    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=y_trend_rhine,
            mode="lines",
            name="Trend (Wasserführung Rhein)",
            # legendgroup="trend",
            line=dict(color=WASSERFUEHRUNG, width=2),
            # opacity=1.0,
            # showlegend=True,
        ),
        secondary_y=True)  # trace 5

    # Outliers: Landesverbrauch
    fig.add_trace(
        go.Scatter(
            x=x[cons_outlier_mask],
            y=y_consumption[cons_outlier_mask],
            mode="markers",
            name="Ausreisser Landesverbrauch",
            legendgroup="outliers",
            marker=dict(
                symbol="circle-open",
                size=12,
                color="#868D07",
                line=dict(width=2, color="#868D07"),
            ),
            opacity=1.0,  # on by default
            # showlegend=True,
        ),
        secondary_y=False,
    )  # trace 6

    # Outliers: Wasserführung Rhein
    fig.add_trace(
        go.Scatter(
            x=x[rhine_outlier_mask],
            y=y_rhine[rhine_outlier_mask],
            mode="markers",
            name="Ausreisser Rhein",
            legendgroup="outliers",
            marker=dict(
                symbol="circle-open",
                size=12,
                color="#C8C36D",
                line=dict(width=2, color="#C8C36D"),
            ),
            opacity=1.0,
            # showlegend=True,
        ),
        secondary_y=True)  # trace 7

    # Axes styling (x, and 2 y axes)
    fig.update_xaxes(
        title_text="Average Daily Temperatures (°C) - Basel/Bern/Lausanne/Zurich",
        zeroline=False,
        showgrid=False,
        linecolor=ACHSE,
        linewidth=2,
        title_font=dict(size=12, color=ACHSE),
        tickfont=dict(color=ACHSE)
    )

    fig.update_yaxes(
        title_text="National Consumption (GWh)",
        secondary_y=False,
        showgrid=False,
        linecolor=ACHSE,
        linewidth=2,
        title_standoff=18,
        title_font=dict(size=11, color=ACHSE),
        tickfont=dict(color=ACHSE)
    )

    fig.update_yaxes(
        title_text="Rhine River Flow (m³/s)",
        secondary_y=True,
        showgrid=False,
        linecolor=ACHSE,
        linewidth=2,
        title_standoff=8,
        title_font=dict(size=11, color=ACHSE),
        tickfont=dict(color=ACHSE)
    )

    toggle_box = dict(x0=1.15, x1=1.55, y0=0.01, y1=0.42)
    toggle_x = 1.35
    legend_cfg = dict(
        x=1.15,
        y=0.98,
        xanchor="left",
        yanchor="top",
        bgcolor=LEGENDE_HINTERGRUND,
        bordercolor="black",
        borderwidth=2,
        font=dict(size=14),
    )
    toggle_font = dict(color=TOGGLE_TEXT, family="Courier New", size=16)

    if compact:
        toggle_box = dict(x0=0.67, x1=0.98, y0=0.02, y1=0.46)
        toggle_x = 0.83
        legend_cfg = dict(
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
            bgcolor=LEGENDE_HINTERGRUND,
            bordercolor="black",
            borderwidth=1,
            font=dict(size=11),
        )
        toggle_font = dict(color=TOGGLE_TEXT, family="Courier New", size=11)

    if show_legend:
        fig.update_layout(legend=legend_cfg)

    # Legend settings
    fig.update_layout(showlegend=show_legend)

    # Rectangle around the toggles area
    if show_controls:
        fig.add_shape(
            type="rect",
            xref="paper", yref="paper",
            x0=toggle_box["x0"], x1=toggle_box["x1"],
            y0=toggle_box["y0"], y1=toggle_box["y1"],
            fillcolor="white",
            opacity=1,
            layer="above"
        )

    # Toggle buttons
    updatemenus = [
        # Landesverbrauch toggle
        dict(
            type="buttons",
            x=toggle_x, y=0.32, xanchor="center", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=toggle_font,  # toggle text
            showactive=True,
            # direction="down",
            buttons=[
                dict(
                    label="Landesverbrauch" + "\u00A0"*4,
                    method="restyle",
                    args=[{"opacity": [1.0, 0.0]}, [0, 1]],
                    args2=[{"opacity": [0.0, 0.35]}, [0, 1]],
                )
            ],
        ),
        # Wasserführung Rhein toggle
        dict(
            type="buttons",
            x=toggle_x, y=0.24, xanchor="center", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=toggle_font,  # toggle text
            showactive=True,
            direction="down",
            buttons=[
                dict(
                    label="Wasserführung Rhein",
                    method="restyle",
                    args=[{"opacity": [1.0, 0.0]}, [2, 3]],
                    args2=[{"opacity": [0.0, 0.35]}, [2, 3]],
                )
            ],
        ),
        # Trendlines toggle
        dict(
            type="buttons",
            x=toggle_x, y=0.16, xanchor="center", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=toggle_font,  # toggle text
            showactive=True,
            # direction="down",
            buttons=[
                dict(
                    label="Trendlinien" + "\u00A0"*8,
                    method="restyle",
                    args=[{"opacity": [1.0, 1.0]}, [4, 5]],
                    args2=[{"opacity": [0.0, 0.0]}, [4, 5]],
                )
            ],
        ),
        # Outliers toggle
        dict(
            type="buttons",
            x=toggle_x, y=0.08, xanchor="center", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=toggle_font,  # toggle text
            showactive=True,
            # direction="down",
            buttons=[
                dict(
                    label="Ausreisser" + "\u00A0"*9,
                    method="restyle",
                    args=[{"opacity": [1.0, 1.0]}, [6, 7]],
                    args2=[{"opacity": [0.0, 0.0]}, [6, 7]],
                )
            ],
        ),
    ]

    # Figure layout configurations
    layout_kwargs = dict(
        showlegend=show_legend,
        updatemenus=updatemenus if show_controls else [],        
        template="simple_white",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        autosize=True,
        margin=dict(l=120, r=360, t=80, b=80),
    )
    if compact:
        layout_kwargs["margin"] = dict(l=60, r=90, t=30, b=70)
    if width is not None:
        layout_kwargs["width"] = width
    if height is not None:
        layout_kwargs["height"] = height

    fig.update_layout(**layout_kwargs)
    return fig
