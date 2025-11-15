import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- 1. DATA PREPARATION ---
try:
    df_raw = pd.read_csv('cleaned_dataset.csv')
    df_raw['Datum'] = pd.to_datetime(df_raw['Datum'], format='%Y-%m-%d')

    columns_to_process = [
        'Laufwerke', 'Speicherwerke', 'Total Hydraulisch', 'Kernkraftwerke',
        'Thermisch', 'Windkraft', 'Photovoltaik', 'Total Erneuerbar'
    ]

    df_monthly_sums = df_raw.groupby(pd.Grouper(key='Datum', freq='M'))[columns_to_process].sum().round(2)
    df_monthly_sums = df_monthly_sums.reset_index()
    # Keep a numeric month for filtering later
    df_monthly_sums['Monat_Num'] = df_monthly_sums['Datum'].dt.month
    df_monthly_sums['Datum'] = df_monthly_sums['Datum'].dt.strftime('%B')
    df_monthly_sums.rename(columns={'Datum': 'Monat'}, inplace=True)

    total_row = pd.DataFrame(df_monthly_sums[columns_to_process].sum()).T
    total_row['Monat'] = 'Total'
    df_monthly_sums = pd.concat([df_monthly_sums, total_row], ignore_index=True)

except FileNotFoundError:
    print("Error: 'cleaned_dataset.csv' not found. Please make sure the file is in the correct directory.")
    exit()

# --- Data for visualizations ---
df = df_monthly_sums.copy()
df = df.drop(columns=['Laufwerke', 'Speicherwerke', 'Total Erneuerbar'])

energy_sources = ['Total Hydraulisch', 'Kernkraftwerke', 'Photovoltaik', 'Thermisch', 'Windkraft']

# Data for bar chart (percentages)
df_plot = df[df['Monat'] != 'Total'].copy()
df_percent = df_plot.copy()
df_percent[energy_sources] = df_percent[energy_sources].div(df_percent[energy_sources].sum(axis=1), axis=0) * 100

# Colors
colors = {
    'Total Hydraulisch': '#d9534f', 'Kernkraftwerke': '#b71c1c',
    'Photovoltaik': '#f48fb1', 'Thermisch': '#ffcccb', 'Windkraft': '#c0e7f7'
}

# --- 2. INITIALIZE DASH APP ---
app = dash.Dash(__name__)
server = app.server

# --- 3. DEFINE APP LAYOUT ---
app.layout = html.Div(children=[
    html.H1(children='Dashboard Energieerzeugung Schweiz 2025', style={'textAlign': 'center'}),

    dcc.Tabs(id="tabs-charts", value='tab-donut', children=[
        dcc.Tab(label='Gesamtübersicht nach Monat', value='tab-donut', children=[
            html.Div([
                html.Label('Monat auswählen:'),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': i, 'value': i} for i in df_monthly_sums['Monat'].unique()],
                    value='Total'
                ),
            ], style={'width': '50%', 'margin': 'auto', 'paddingTop': '20px'}),
            dcc.Graph(id='donut-chart')
        ]),
        dcc.Tab(label='Monatliche Aufteilung (Prozent)', value='tab-bar', children=[
            html.Div([
                html.Label('Monatsbereich auswählen:'),
                dcc.RangeSlider(
                    id='month-slider',
                    min=1,
                    max=12,
                    step=1,
                    value=[1, 12],
                    marks={i: month for i, month in enumerate(df_plot['Monat'], 1)}
                ),
            ], style={'padding': '20px 50px'}),
            dcc.Graph(id='stacked-bar-chart')
        ]),
    ])
])

# --- 4. DEFINE CALLBACKS FOR INTERACTIVITY ---

# Callback for Donut Chart
@app.callback(
    Output('donut-chart', 'figure'),
    Input('month-dropdown', 'value')
)
def update_donut_chart(selected_month):
    filtered_df = df[df['Monat'] == selected_month]
    values_total = filtered_df[energy_sources].values.flatten()

    fig_donut = go.Figure(data=[go.Pie(
        labels=energy_sources,
        values=values_total,
        hole=.55,
        marker_colors=[colors[src] for src in energy_sources],
        hoverinfo='label+percent',
        textinfo='percent',
        textfont_size=14
    )])

    fig_donut.update_layout(
        title_text=f'Energieerzeugung für: {selected_month}',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        margin=dict(t=50, b=50, l=50, r=50) # Adjust margin for title
    )
    return fig_donut

# Callback for Stacked Bar Chart
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    Input('month-slider', 'value')
)
def update_bar_chart(month_range):
    filtered_df = df_percent[(df_percent['Monat_Num'] >= month_range[0]) & (df_percent['Monat_Num'] <= month_range[1])]
    
    df_percent_long = filtered_df.melt(id_vars='Monat', value_vars=energy_sources, var_name='Energiequelle', value_name='Prozent')

    fig_bar = px.bar(
        df_percent_long,
        x='Monat',
        y='Prozent',
        color='Energiequelle',
        title='Landeserzeugung nach Typ',
        color_discrete_map=colors,
        text=df_percent_long['Prozent'].apply(lambda x: f'{x:.0f}%' if x > 5 else ''),
        labels={'Prozent': 'Prozent (%)', 'Monat': 'Monat', 'Energiequelle': 'Energiequellen'}
    )
    fig_bar.update_layout(
        barmode='stack',
        yaxis_range=[0, 100],
        legend_title='Energiequellen',
        legend=dict(traceorder='normal')
    )
    fig_bar.update_traces(textposition='inside')
    return fig_bar

# --- 5. RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True)