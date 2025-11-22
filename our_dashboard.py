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
    
    columns = df_raw.columns.to_list()

    
    columns_to_process = [
        'Laufwerke', 'Speicherwerke', 'Total Hydraulisch', 'Kernkraftwerke',
        'Thermisch', 'Windkraft', 'Photovoltaik', 'Total Erneuerbar'
    ]

    df_monthly_sums = df_raw.groupby(pd.Grouper(key='Datum', freq='ME'))[columns_to_process].sum().round(2)
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
columns_for_heatmap = ['Einfuhr', 'Ausfuhr', 'Landesverbrauch']

# s)
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
        dcc.Tab(label='Tab 1', value='tab-donut', children=[
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
        dcc.Tab(label='Tab 2', value='tab-bar', children=[
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
       
dcc.Tab(label='Heatmap', value='tab-heatmap', children=[
    html.Div([
        html.Div([
            html.Label('Jahr:'),
            dcc.Dropdown(
                id='year-heatmap',
                options=[{'label': int(y), 'value': int(y)}
                         for y in sorted(df_raw['Datum'].dt.year.unique())],
                value=int(df_raw['Datum'].dt.year.max()),
                clearable=False,
                style={"width":"160px"}
            ),
            dcc.Dropdown(
    id="months",
    options=[{"label": m, "value": i} for i, m in enumerate(
        ["Januar","Februar","März","April","Mai","Juni","Juli",
         "August","September","Oktober","November","Dezember"], start=1)],
    value=list(range(1,13))  
),

            html.Label('Palette:', style={"marginLeft":"12px"}),
            dcc.Dropdown(
                id='palette-heatmap',
                options=[
                    {'label':'Blautöne', 'value':'blue'},
                    {'label':'Rosa→Hellblau', 'value':'rose'},
                    {'label':'Viridis', 'value':'viridis'}
                ],
                value='rose',
                clearable=False,
                style={"width":"200px"}
            ),
        ], style={"display":"flex","gap":"12px","alignItems":"center","marginBottom":"12px"}),

        html.Div([
            html.Div(id="avg-import",  style={"background":"#F3F4F6","borderRadius":"18px","padding":"18px",
                                              "width":"220px","height":"110px","display":"flex","flexDirection":"column",
                                              "justifyContent":"center"}),
            html.Div(id="avg-export",  style={"background":"#F3F4F6","borderRadius":"18px","padding":"18px",
                                              "width":"220px","height":"110px","display":"flex","flexDirection":"column",
                                              "justifyContent":"center"}),
            html.Div(id="avg-landes",  style={"background":"#F3F4F6","borderRadius":"18px","padding":"18px",
                                              "width":"220px","height":"110px","display":"flex","flexDirection":"column",
                                              "justifyContent":"center"}),
        ], style={"display":"flex","gap":"16px","marginBottom":"8px"}),

        dcc.Graph(id='heatmap', config={"displayModeBar": False}, style={"height":"520px"})
    ], style={"padding":"14px"})
]),

        dcc.Tab(label='Zeitverlauf', value='tab-area', children=[
            html.Div([
                html.Label('Year'),
                dcc.Dropdown(
                    id='year-area',
                    options=[{'label': int(y), 'value': int(y)} for y in sorted(df_raw['Datum'].dt.year.unique())],
                    value=int(df_raw['Datum'].dt.year.max()),
                    clearable=False,
                    style={'width': '180px', 'marginBottom': '8px'}
                ),

        dcc.Checklist(
            id='area-series',
            options=[
                {'label': 'Verbrauch Speicherpumpe', 'value': 'Verbrauch Speicherpumpe'},
                {'label': 'Import', 'value': 'Import'},
                {'label': 'Export', 'value': 'Export'},
                {'label': 'Nettoerzeugung', 'value': 'Nettoerzeugung'},
                {'label': 'Landeserzeugung', 'value': 'Landeserzeugung'},
            ],
            value=[
                'Verbrauch Speicherpumpe','Import','Export','Nettoerzeugung','Landeserzeugung'
            ],
            inline=True
        ),
        

        dcc.Graph(id='area-chart')], 
        style={'padding': '12px 18px'})
])

    ])
])

# --- 4. DEFINE CALLBACKS FOR INTERACTIVITY ---

# Callback 

from dash import Input, Output

@app.callback(
    Output('area-chart', 'figure'),
    Input('year-area', 'value'),
    Input('area-series', 'value')  
)
def update_area_chart(selected_year, selected_series):
    d = df_raw.copy()
    d['Datum'] = pd.to_datetime(d['Datum'], errors='coerce')
    d = d[d['Datum'].dt.year == selected_year].copy()
    d['Monat'] = d['Datum'].dt.month

    series_order_raw = [
        "Verbrauch Speicherpumpen", "Einfuhr", "Ausfuhr",
        "Nettoerzeugung Total", "Total Erneuerbar",
    ]
    rename_map = {
        "Verbrauch Speicherpumpen": "Verbrauch Speicherpumpe",
        "Einfuhr": "Import",
        "Ausfuhr": "Export",
        "Nettoerzeugung Total": "Nettoerzeugung",
        "Total Erneuerbar": "Landeserzeugung",
    }
    monthly = (
        d.groupby('Monat')[series_order_raw].sum()
         .reindex(range(1, 13))
         .rename(columns=rename_map)
    )
    month_names = {1:"Jan",2:"Feb",3:"Mär",4:"Apr",5:"Mai",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Okt",11:"Nov",12:"Dez"}
    x_order = [month_names[m] for m in range(1,13)]
    monthly.index = x_order

    colors = {
        "Verbrauch Speicherpumpe": "#b91c1c",
        "Import": "#ef4444",
        "Export": "#f472b6",
        "Nettoerzeugung": "#f9a8d4",
        "Landeserzeugung": "#cbeef3",
    }

    import plotly.graph_objects as go
    fig = go.Figure()
    order = ["Verbrauch Speicherpumpe","Import","Export","Nettoerzeugung","Landeserzeugung"]

    for name in order:
        y = monthly[name].to_list()
        fig.add_scatter(
            x=x_order, y=y, name=name,
            mode="lines+markers",
            line=dict(color=colors[name], width=2),
            marker=dict(size=5, color=colors[name]),
            stackgroup="one",
            connectgaps=False,
            hovertemplate=f"{name}<br>%{{x}}: %{{y:.0f}}<extra></extra>",
            
            visible=True if (name in (selected_series or [])) else "legendonly"
        )

    fig.update_layout(
        title="Zeitverlauf- und Energieflussgrössen",
        hovermode="x unified",
        plot_bgcolor="white",
        margin=dict(l=40, r=20, t=50, b=60),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.25, x=0, xanchor="left",
            itemclick="toggle", itemdoubleclick="toggleothers"  # 👈 Legend-Interaktion
        )
    )
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=x_order,
                     title="", showgrid=True, gridcolor="#e5e7eb")
    fig.update_yaxes(title="", showgrid=True, gridcolor="#e5e7eb", zeroline=False, rangemode="tozero")
    return fig



from dash.exceptions import PreventUpdate
import numpy as np
import plotly.graph_objects as go

columns_for_heatmap = ['Einfuhr', 'Ausfuhr', 'Landesverbrauch']

@app.callback(
    Output('heatmap', 'figure'),
    Output('avg-import', 'children'),
    Output('avg-export', 'children'),
    Output('avg-landes', 'children'),
    Input('year-heatmap', 'value'),
    Input('palette-heatmap', 'value'),
)
def update_heatmap(selected_year, palette):
    if selected_year is None:
        raise PreventUpdate


    d = df_raw[df_raw['Datum'].dt.year == selected_year].copy()
    d['Monat'] = d['Datum'].dt.month
    hm = (
        d.groupby('Monat')[columns_for_heatmap]
         .sum()
         .reindex(range(1, 13))  
         .T                      
    )

    # Labels
    month_map = {1:'Januar',2:'Februar',3:'März',4:'April',5:'Mai',6:'Juni',
                 7:'Juli',8:'August',9:'September',10:'Oktober',11:'November',12:'Dezember'}
    x_labels = [month_map[i] for i in hm.columns]
    y_labels = hm.index.tolist()
    Z = hm.values.astype(float)


    if palette == 'blue':
        colorscale = [[0.00,"#E6F7FF"],[0.25,"#BAECFE"],[0.50,"#8EE2FD"],[0.75,"#63D8FC"],[1.00,"#37CEFB"]]
    elif palette == 'viridis':
        colorscale = 'Viridis'
    else: 
        colorscale = [[0.00,"#880d1e"],[0.25,"#dd2d4a"],[0.50,"#f26a8d"],[0.75,"#f49cbb"],[1.00,"#cbeef3"]]


    fig = go.Figure(go.Heatmap(
        z=Z, x=x_labels, y=y_labels,
        colorscale=colorscale,
        zmin=np.nanmin(Z), zmax=np.nanmax(Z),
        showscale=False, xgap=6, ygap=14
    ))
    fig.update_layout(plot_bgcolor="#F3F4F6", paper_bgcolor="white")


    annotations = []
    for i, cat in enumerate(y_labels):
        for j, mon in enumerate(x_labels):
            val = Z[i, j]
            txt = "" if np.isnan(val) else f"{val:.0f}"
            annotations.append(dict(x=mon, y=cat, text=txt, showarrow=False,
                                    font=dict(size=12, color="#0c4a6e")))
    fig.update_layout(
        annotations=annotations,
        title=f'Import, Export und Verbrauch pro – {selected_year}',
        xaxis_title='', yaxis_title='',
        margin=dict(l=70, r=20, t=40, b=50)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

  
    means = hm.mean(axis=1, skipna=True) 
    def card(title, value):
        return html.Div([
            html.Div(f"{value:.0f}", style={"fontSize":"28px","fontWeight":"800","lineHeight":"1","color":"#0f172a"}),
            html.Div(f"{title} (Average)", style={"fontSize":"14px","fontWeight":"600","color":"#111827"})
        ])

    avg_import = card("Import",         float(means.get('Einfuhr', np.nan)))
    avg_export = card("Export",         float(means.get('Ausfuhr', np.nan)))
    avg_landes = card("Landesverbrauch",float(means.get('Landesverbrauch', np.nan)))

    return fig, avg_import, avg_export, avg_landes



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