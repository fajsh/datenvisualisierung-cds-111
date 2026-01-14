import streamlit as st

from data.load_data import load_monthly_sums, load_cleaned_dataset
from layout.sidebar import render_sidebar
from layout.header import render_header
from layout.layout_utils import apply_compact_layout
from plots.kpi import plot_kpis
from plots.timeseries import plot_time_series
from plots.heatmap import plot_heatmap_import_export
from plots.production import production_plots
from plots.temperature_scatterplot import temp_scatter
#from plots.consumption import plot_verbrauch
from plots.geography import plot_kantonskarte
from state.session_state import init_state
from plots.kpi_with_icons import render_energy_kpis
from utils.colors import LANDESVERBRAUCH, WASSERFUEHRUNG

st.set_page_config(
    page_title="Energy Dashboard 2025",
    layout="wide"
)

init_state()
apply_compact_layout()
render_sidebar()
render_header()

# Load data
df_monthly = load_monthly_sums()
df_cleaned = load_cleaned_dataset()

scale = st.session_state.get("plot_scale", 0.9)
prod_height = int(220 * scale)
time_height = int(200 * scale)
heat_height = int(200 * scale)
map_width = int(400 * scale)
map_height = int(220 * scale)
temp_height = int(200 * scale)

top_left, top_mid, top_right = st.columns([1.1, 1.4, 1.1], gap="small")
with top_left:
    with st.container(border=True):
        st.markdown("**Energy Overview**")
        render_energy_kpis(df_cleaned)

with top_mid:
    with st.container(border=True):
        st.markdown("**Regionale Analyse**")
        plot_kantonskarte(width=map_width, height=map_height)

with top_right:
    with st.container(border=True):
        st.markdown("**Datenebenen**")
        legend_items = [
            ("Landesverbrauch", LANDESVERBRAUCH),
            ("Wasserfuehrung Rhein", WASSERFUEHRUNG),
            ("Trendlinie (Landesverbrauch)", LANDESVERBRAUCH),
            ("Trendlinie (Wasserfuehrung)", WASSERFUEHRUNG),
            ("Ausreisser Landesverbrauch", "#868D07"),
            ("Ausreisser Rhein", "#C8C36D"),
        ]
        legend_html = "".join(
            f"""
            <div style="display:flex; align-items:center; gap:0.4rem; margin:0.2rem 0;">
                <span style="width:8px; height:8px; border-radius:50%; background:{color}; display:inline-block;"></span>
                <span style="font-size:0.72rem; color:#000000;">{label}</span>
            </div>
            """
            for label, color in legend_items
        )
        st.markdown(legend_html, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**Einfluss der Temperatur auf Landesverbrauch und Wasserfuehrung des Rheins**")
        fig_temp = temp_scatter(
            df_cleaned,
            width=None,
            height=temp_height,
            compact=True,
            show_controls=False,
            show_legend=False,
        )
        st.plotly_chart(fig_temp, use_container_width=True)

mid_left, mid_right = st.columns([2, 1], gap="small")
with mid_left:
    with st.container(border=True):
        st.markdown("**Produktion**")
        production_plots(df_monthly, height=prod_height)
with mid_right:
    with st.container(border=True):
        st.markdown("**Import, Export und Verbrauch pro Monat**")
        plot_heatmap_import_export(df_cleaned, height=heat_height)

bottom_left, bottom_right = st.columns([3, 1], gap="small")
with bottom_left:
    with st.container(border=True):
        st.markdown("**Zeitverlauf- und Energieflussgroessen**")
        plot_time_series(df_cleaned, height=time_height)
with bottom_right:
    with st.container(border=True):
        plot_kpis(df_cleaned)
