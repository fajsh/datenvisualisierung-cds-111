# Importing libraries
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# 1) Loading the data
data = pd.read_csv("cleaned_dataset.csv")

# Column names
x = data["Mittlere Tagestemperatur"]
y_consumption = data["Landesverbrauch"]
y_rhine = data["Wasserführung Rhein"]

# Outliers
cons_outlier_mask = y_consumption > y_consumption.quantile(0.95)
rhine_outlier_mask = y_rhine < y_rhine.quantile(0.05)   # low-flow outliers

# Trend lines
coef_cons = np.polyfit(x, y_consumption, 1)
coef_rhine = np.polyfit(x, y_rhine, 1)

x_trend = np.linspace(x.min(), x.max(), 50)
y_trend_cons = np.polyval(coef_cons, x_trend)
y_trend_rhine = np.polyval(coef_rhine, x_trend)

# Colours
dark_red = "#880d1e"          # Landesverbrauch
rusty_red= "#dd2d4a"           # Wasserführung / trend
grey = "#d3d3d3"
axis_color = "black"

# 2) Figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Scatter: Landesverbrauch (coloured)
fig.add_trace(
    go.Scatter(
        x=x[~cons_outlier_mask],
        y=y_consumption[~cons_outlier_mask],
        mode="markers",
        name="Landesverbrauch",
        legendgroup="cons",
        marker=dict(color=dark_red, size=9, line=dict(width=1, color=axis_color)),
        opacity=1.0,                       # ON by default
        showlegend=True,                  # explanation lives in the legend block
    ),
    secondary_y=False,
)  # trace 0

# Scatter: Landesverbrauch (grey background when OFF)
fig.add_trace(
    go.Scatter(
        x=x[~cons_outlier_mask],
        y=y_consumption[~cons_outlier_mask],
        mode="markers",
        name="Landesverbrauch (grau)",
        legendgroup="cons",
        marker=dict(color=grey, size=9),
        opacity=0.0,                       # hidden when toggle ON
        hoverinfo="skip",
        showlegend=False,
    ),
    secondary_y=False,
)  # trace 1

# Scatter: Wasserführung Rhein (coloured)
fig.add_trace(
    go.Scatter(
        x=x[~rhine_outlier_mask],
        y=y_rhine[~rhine_outlier_mask],
        mode="markers",
        name="Wasserführung Rhein",
        legendgroup="rhine",
        marker=dict(color=rusty_red, size=9, line=dict(width=1, color=axis_color)),
        opacity=0.0,                       # OFF by default
        showlegend=True,
    ),
    secondary_y=True,
)  # trace 2

# Scatter: Wasserführung Rhein (grey when OFF)
fig.add_trace(
    go.Scatter(
        x=x[~rhine_outlier_mask],
        y=y_rhine[~rhine_outlier_mask],
        mode="markers",
        name="Wasserführung Rhein (grau)",
        legendgroup="rhine",
        marker=dict(color=grey, size=9),
        opacity=0.35,                      # ON (grey) by default
        hoverinfo="skip",
        showlegend=False,
    ),
    secondary_y=True,
)  # trace 3

# Trendline: Landesverbrauch
fig.add_trace(
    go.Scatter(
        x=x_trend,
        y=y_trend_cons,
        mode="lines",
        name="Trend (Landesverbrauch)",
        legendgroup="trend",
        line=dict(color=dark_red, width=2),
        opacity=1.0,                       # ON by default
        showlegend=True,
    ),
    secondary_y=False,
)  # trace 4

# Trendline: Wasserführung Rhein
fig.add_trace(
    go.Scatter(
        x=x_trend,
        y=y_trend_rhine,
        mode="lines",
        name="Trend (Wasserführung Rhein)",
        legendgroup="trend",
        line=dict(color=rusty_red, width=2),
        opacity=1.0,
        showlegend=True,
    ),
    secondary_y=True,
)  # trace 5

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
            line=dict(width=2, color=axis_color),
        ),
        opacity=1.0,                       # ON by default
        showlegend=True,
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
            line=dict(width=2, color=axis_color),
        ),
        opacity=1.0,
        showlegend=True,
    ),
    secondary_y=True,
)  # trace 7

# 3) Axes styling
fig.update_xaxes(
    title_text="MITTLERE TAGESTEMPERATUR BASEL, BERN, LAUSANNE, ZÜRICH (°C)",
    zeroline=False,
    showgrid=False,
    linecolor=axis_color,
    linewidth=2,
    title_font=dict(size=14),
)

fig.update_yaxes(
    title_text="LANDESVERBRAUCH (GWh)",
    secondary_y=False,
    showgrid=False,
    linecolor=axis_color,
    linewidth=2,
    title_standoff=10,
    title_font=dict(size=14),
)

fig.update_yaxes(
    title_text="WASSERFÜHRUNG RHEIN IN RHEINFELDEN TAGESMITTEL (m³/s)",
    secondary_y=True,
    showgrid=False,
    linecolor=axis_color,
    linewidth=2,
    title_standoff=40,
    title_font=dict(size=14),
)

# 4) Legend block (top-right)
fig.update_layout(
    legend=dict(
        x=1.12,
        y=0.98,
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="black",
        borderwidth=1,
        font=dict(size=14),
        orientation="v",
    )
)

# Legend settings
fig.update_layout(showlegend=True)  # turn off classical legend

'''
# Marker “bullets” + explanations
legend_annotations = [
    dict(
        x=1.28, y=0.98, xref="paper", yref="paper",
        text="<b>Landesverbrauch<br>anhand steigender<br>Temperatur</b>",
        showarrow=False, align="left"
    ),
    dict(
        x=1.28, y=0.84, xref="paper", yref="paper",
        text="<b>Wasserführung<br>anhand steigender<br>Temperatur</b>",
        showarrow=False, align="left"
    ),
    dict(
        x=1.41, y=0.62, xref="paper", yref="paper",
        text="<b>Trend Linie (Landesverbrauch<br>anhand steigender Temperatur)</b>",
        showarrow=False, align="left"
    ),
    dict(
        x=1.41, y=0.50, xref="paper", yref="paper",
        text="<b>Trend Linie (Wasserführung<br>anhand steigender Temperatur)</b>",
        showarrow=False, align="left"
    ),
]
'''

fig.update_layout(annotations=[
    # Box headline
    dict(
        x=1.40, y=0.40, xref="paper", yref="paper",
        text="<b>DATENEBENEN AUSWÄHLEN</b>",
        showarrow=False, align="center", font=dict(size=15),
    )
])

# Rectangle around the toggles area
fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=1.12, x1=1.42,
    y0=0.02, y1=0.42,
    line=dict(color="black", width=2),
    fillcolor="rgba(255,255,255,0.95)",
)

# 5) Toggle buttons
updatemenus = [
    # Landesverbrauch toggle
    dict(
        type="buttons",
        x=1.15, y=0.32, xanchor="left", yanchor="middle",
        showactive=True,
        direction="down",
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
        x=1.15, y=0.24, xanchor="left", yanchor="middle",
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
        x=1.15, y=0.16, xanchor="left", yanchor="middle",
        showactive=True,
        direction="down",
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
        x=1.15, y=0.08, xanchor="left", yanchor="middle",
        showactive=True,
        direction="down",
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

fig.update_layout(
    updatemenus=updatemenus,
    title="EINFLUSS DER TEMPERATUR AUF LANDESVERBRAUCH UND WASSERFÜHRUNG DES RHEINS",
    template="simple_white",
    width=1300,
    height=650,
    plot_bgcolor="white",
    font=dict(
        family="Comic Sans MS, Patrick Hand, Arial",
        size=16,
    ),
    margin=dict(l=120, r=360, t=80, b=80),
)

fig.show()
