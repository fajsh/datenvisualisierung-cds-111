import streamlit as st

from data.load_data import load_monthly_sums, load_cleaned_dataset
from layout.header import render_header
from layout.layout_utils import apply_compact_layout
from plots.kpi import plot_kpis
from plots.timeseries import plot_time_series
from plots.heatmap import plot_heatmap_import_export
from plots.production import production_plots
from plots.temperature_scatterplot import temp_scatter
# from plots.consumption import plot_consumption
from plots.geography import plot_kantonskarte
from state.session_state import init_state
from plots.kpi_with_icons import render_energy_kpis
from utils.colors import LANDESVERBRAUCH, WASSERFUEHRUNG

#----------------------------------
# SET  BACKGROUND COLORS
#----------------------------------

# App Background


css = """
.st-key-container1{
    background: #FFFFFF;
}
.st-key-container2{
    background: #FFFFFF;
}
.st-key-container3{
    background: #FFFFFF;
}
.st-key-container4{
    background: #FFFFFF;
}
.st-key-container5{
    background: #FFFFFF;
}
.st-key-container6{
    background: #FFFFFF;
}

"""
st.html(f"<style>{css}</style>")

#----------------------------------

st.set_page_config(
    page_title="Energy Dashboard 2025",
    layout="wide"
)

st.markdown(
    """
<style>
/* Make checkbox rows smaller without negative margin overlap */
div[data-testid="stCheckbox"]{
  transform: scale(0.85);
  transform-origin: left center;
  margin: 0 !important;
  padding: 0 !important;
}

/* Remove built-in padding/min-height that creates tall rows */
div[data-testid="stCheckbox"] label{
  padding: 0 !important;
  margin: 0 !important;
  min-height: 0 !important;
  line-height: 1.0 !important;
}

/* If Streamlit adds vertical spacing between elements in a block */
div[data-testid="stVerticalBlock"]{
  gap: 0.25rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

apply_compact_layout()
init_state()
render_header()

# Load data
df_monthly = load_monthly_sums()
df_cleaned = load_cleaned_dataset()

scale = st.session_state.get("plot_scale", 0.9)
prod_height = int(190 * scale)
time_height = int(200 * scale)
heat_height = prod_height
heat_container_height = int(138 * scale)
map_width = int(400 * scale)
map_height = int(220 * scale)
temp_height = int(260 * scale)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
with st.container(key="container1",border=True):
    render_energy_kpis(df_cleaned)

# ─────────────────────────────────────────────
# REST ROW
# ─────────────────────────────────────────────

col1, col2 = st.columns([1.6, 1.2], gap="small")

## ─────────────────────────────────────────────
# COLUMN LEFT
## ─────────────────────────────────────────────

with col1:
    with st.container(key="container2",border=True):
        st.markdown("##### Regional Analysis")
        plot_kantonskarte()       

    with st.container(key="container3",border=True):
        st.markdown("##### Impact of temperature on national electricity consumption and Rhine river flow ")

        def legend_toggle(label: str, color: str, key: str, default=True, marker="dot"):
            c_marker, c_label, c_toggle = st.columns([0.10, 0.72, 0.18], vertical_alignment="center", gap="small")

            with c_marker:
                if marker == "line":
                    st.markdown(
                        f"<div style='width:16px;height:2px;background:{color};border-radius:2px;margin-top:8px;'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div style='width:9px;height:9px;border-radius:50%;background:{color};margin-top:6px;'></div>",
                        unsafe_allow_html=True,
                    )

            with c_label:
                st.markdown(
                    f"<div style='font-size:0.72rem;line-height:1.0;margin:0;padding:0;'>{label}</div>",
                    unsafe_allow_html=True,
                )

            with c_toggle:
                return st.checkbox("", value=default, key=key, label_visibility="collapsed")

        # Wrap the toggle/legend stack to scope CSS compression
        st.markdown('<div class="legend-panel">', unsafe_allow_html=True)

        show_cons = legend_toggle("National consumption", LANDESVERBRAUCH, "dl_cons", marker="dot")
        show_rhine = legend_toggle("Rhine river flow", WASSERFUEHRUNG, "dl_rhine", marker="dot")
        show_trend_cons = legend_toggle(
            "Trend line (national consumption)", LANDESVERBRAUCH, "dl_trend_cons", marker="line"
        )
        show_trend_rhine = legend_toggle(
            "Trend line (Rhine river flow)", WASSERFUEHRUNG, "dl_trend_rhine", marker="line"
        )
        show_out_cons = legend_toggle("Outliers - national consumption", "#868D07", "dl_out_cons", marker="dot")
        show_out_rhine = legend_toggle("Outliers - Rhine", "#C8C36D", "dl_out_rhine", marker="dot")

        st.markdown("</div>", unsafe_allow_html=True)

        fig_temp = temp_scatter(
            df_cleaned,
            width=None,
            height=temp_height,
            compact=True,
            show_controls=False,
            show_legend=False,
        )

        fig_temp.data[0].visible = show_cons
        fig_temp.data[1].visible = (not show_cons)

        fig_temp.data[2].visible = show_rhine
        fig_temp.data[3].visible = (not show_rhine)

        fig_temp.data[4].visible = show_trend_cons
        fig_temp.data[5].visible = show_trend_rhine

        fig_temp.data[6].visible = show_out_cons
        fig_temp.data[7].visible = show_out_rhine

        st.plotly_chart(fig_temp, use_container_width=True)

## ─────────────────────────────────────────────
# COLUMN RIGHT
## ─────────────────────────────────────────────

with col2:
    with st.container(key="container4",border=True):
        st.markdown("##### Production")

        selected_month = st.selectbox(
            "Month",
            label_visibility = 'collapsed',
            options=["Total"] + sorted(df_monthly["Monat"].unique().tolist()),
            index=0,
            key="prod_month",
        )

        production_plots(
            df_monthly,
            height=prod_height,
            selected_month=selected_month,
            show_bar=True,
            show_donut=False,
        )

        production_plots(
            df_monthly,
            height=prod_height,
            selected_month=selected_month,
            show_bar=False,
            show_donut=True,
        )

    with st.container(key="container5",border=True):
        st.markdown("##### Import, Export and Consumption")
        plot_heatmap_import_export(df_cleaned, height=heat_height)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container(key="container6",border=True):
        st.markdown("##### Time Series and Energy Flow Metrics")
        plot_time_series(df_cleaned, height=time_height)
