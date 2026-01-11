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
    LEGENDE_HINTERGRUND,
    TOGGLE_HINTERGRUND,
    TOGGLE_TEXT
)

# function to build scatterplot
def temp_scatter(df: pd.DataFrame) -> go.Figure:
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
            # legendgroup="cons",
            marker=dict(color=LANDESVERBRAUCH, size=9  # ,line=dict(width=1, color=axis_color)
                        ),
            opacity=1.0,  # on by default
            # showlegend=True,
        ),
        secondary_y=False)  # trace 0

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
            # legendgroup="rhine",
            marker=dict(color=WASSERFUEHRUNG, size=9  # , line=dict(width=1, color=axis_color)
                        ),
            opacity=1.0,  # on by default
            # showlegend=True,
        ),
        secondary_y=True)  # trace 2

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
                line=dict(width=2, color=ACHSE),
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
                line=dict(width=2, color=ACHSE),
            ),
            opacity=1.0,
            # showlegend=True,
        ),
        secondary_y=True)  # trace 7

    # Axes styling (x, and 2 y axes)
    fig.update_xaxes(
        title_text="MITTLERE TAGESTEMPERATUR BASEL, BERN, LAUSANNE, ZÜRICH (°C)",
        zeroline=False,
        showgrid=False,
        linecolor=ACHSE,
        linewidth=2,
        title_font=dict(size=14),
    )

    fig.update_yaxes(
        title_text="LANDESVERBRAUCH (GWh)",
        secondary_y=False,
        showgrid=False,
        linecolor=ACHSE,
        linewidth=2,
        title_standoff=20,
        title_font=dict(size=14),
    )

    fig.update_yaxes(
        title_text="WASSERFÜHRUNG RHEIN IN RHEINFELDEN TAGESMITTEL (m³/s)",
        secondary_y=True,
        showgrid=False,
        linecolor=ACHSE,
        linewidth=2,
        title_standoff=30,
        title_font=dict(size=14),
    )

    # Legend block (top-right)
    fig.update_layout(
        legend=dict(
            x=1.15,
            y=0.98,
            xanchor="left",
            yanchor="top",
            bgcolor=LEGENDE_HINTERGRUND,
            bordercolor="grey",
            borderwidth=3,
            font=dict(size=14),
            # orientation="v",
        )
    )

    # Legend settings
    fig.update_layout(showlegend=True)  # switching on classical legend

    # Rectangle around the toggles area
    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=1.15, x1=1.55,
        y0=0.01, y1=0.42,
        # xanchor="left",
        # yanchor="top",
        line=dict(color=ACHSE, width=3),
        fillcolor="black",
    )

    # Toggle buttons
    updatemenus = [
        # Landesverbrauch toggle
        dict(
            type="buttons",
            x=1.17, y=0.32, xanchor="left", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=dict(color=TOGGLE_TEXT),  # toggle text
            showactive=True,
            # direction="down",
            buttons=[
                dict(
                    label="Landesverbrauch",
                    method="restyle",
                    args=[{"opacity": [1.0, 0.0]}, [0, 1]],
                    args2=[{"opacity": [0.0, 0.35]}, [0, 1]],
                )
            ],
        ),
        # Wasserführung Rhein toggle
        dict(
            type="buttons",
            x=1.17, y=0.24, xanchor="left", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=dict(color=TOGGLE_TEXT),  # toggle text
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
            x=1.17, y=0.16, xanchor="left", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=dict(color=TOGGLE_TEXT),  # toggle text
            showactive=True,
            # direction="down",
            buttons=[
                dict(
                    label="Trendlinien",
                    method="restyle",
                    args=[{"opacity": [1.0, 1.0]}, [4, 5]],
                    args2=[{"opacity": [0.0, 0.0]}, [4, 5]],
                )
            ],
        ),
        # Outliers toggle
        dict(
            type="buttons",
            x=1.17, y=0.08, xanchor="left", yanchor="middle",
            bgcolor=TOGGLE_HINTERGRUND,  # toggle background
            bordercolor="black",  # toggle border
            font=dict(color=TOGGLE_TEXT),  # toggle text
            showactive=True,
            # direction="down",
            buttons=[
                dict(
                    label="Ausreisser",
                    method="restyle",
                    args=[{"opacity": [1.0, 1.0]}, [6, 7]],
                    args2=[{"opacity": [0.0, 0.0]}, [6, 7]],
                )
            ],
        ),
    ]

    # Figure layout configurations
    fig.update_layout(
        showlegend=True,
        updatemenus=updatemenus,
        # title configurations
        title=dict(
            text="EINFLUSS DER TEMPERATUR AUF LANDESVERBRAUCH UND WASSERFÜHRUNG DES RHEINS",
            x=0.75,
            y=0.97,
            xanchor="right",
            yanchor="top",
            font=dict(size=18)
        ),
        # plot configurations
        template="simple_white",
        width=1000,
        height=650,
        plot_bgcolor=LEGENDE_HINTERGRUND,
        # font=dict(
        #    family="Comic Sans MS, Patrick Hand, Arial",
        #    size=16,
        #),
        margin=dict(l=120, r=360, t=80, b=80),
    )
    return fig
