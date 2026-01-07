import streamlit as st

from data.load_data import load_monthly_sums, load_cleaned_dataset
from layout.sidebar import render_sidebar
from layout.header import render_header
from plots.production import plot_landeserzeugung
from plots.temperature_scatterplot import temp_scatter
#from plots.consumption import plot_verbrauch
#from plots.geography import plot_kantonskarte
from state.session_state import init_state

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

st.subheader("Produktion")
plot_landeserzeugung(df_monthly)

# st.subheader("Verbrauch")
# plot_verbrauch(df_monthly)

# st.subheader("Regionale Analyse")
# plot_kantonskarte()

# Temperature Scatterplot
st.subheader("Temperatur & Verbrauch")
fig_temp = temp_scatter(df_cleaned)
st.plotly_chart(fig_temp, use_container_width=False)
