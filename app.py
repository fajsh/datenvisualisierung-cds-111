import streamlit as st

from data.load_data import load_monthly_sums, load_cleaned_dataset
from layout.sidebar import render_sidebar
from layout.header import render_header
from plots.kpi import plot_kpis
from plots.timeseries import plot_time_series
from plots.heatmap import plot_heatmap_import_export
from plots.production import production_plots
from plots.temperature_scatterplot import temp_scatter
#from plots.consumption import plot_verbrauch
from plots.geography import plot_kantonskarte
from state.session_state import init_state
from plots.kpi_with_icons import render_energy_kpis

st.set_page_config(
    page_title="Energy Dashboard 2025",
    layout="wide"
)

init_state()
render_sidebar()
render_header()

# Load data
df_monthly = load_monthly_sums()
df_cleaned = load_cleaned_dataset()

st.subheader("Energy Overview")
render_energy_kpis(df_cleaned)

st.subheader("Produktion")
production_plots(df_monthly)

st.subheader("Zeitverlauf")
plot_time_series(df_cleaned)

plot_kpis(df_cleaned)

# st.subheader("Verbrauch")
# plot_verbrauch(df_monthly)

st.subheader("Regionale Analyse")
plot_kantonskarte()

# Heatmap: Import/Export/Verbrauch
st.subheader("Import, Export und Verbrauch")
plot_heatmap_import_export(df_cleaned)

# Temperature Scatterplot
st.subheader("Temperatur & Verbrauch")
fig_temp = temp_scatter(df_cleaned)
st.plotly_chart(fig_temp, use_container_width=False)
