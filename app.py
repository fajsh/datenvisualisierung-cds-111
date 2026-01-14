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


st.set_page_config(
    page_title="Energy Dashboard 2025",
    layout="wide"
)

init_state()
apply_compact_layout()
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
temp_height = int(260 * scale)

# ─────────────────────────────────────────────
# TOP ROW
# ─────────────────────────────────────────────
top_left, top_mid, top_right = st.columns([1.2, 1.6, 1.2], gap="small")

with top_left:
    with st.container(border=True):
        st.markdown("**Energy Overview**")
        render_energy_kpis(df_cleaned)

with top_mid:
    with st.container(border=True):
        st.markdown("**Regional Analysis**")
        plot_kantonskarte()

with top_right:
    with st.container(border=True):
        st.markdown("**Impact of temperature on national electricity consumption and Rhine river flow**")

        def legend_toggle(label: str, color: str, key:str, default=True, marker="dot"):
            c_marker, c_label, c_toggle = st.columns([0.10, 0.72, 0.18], vertical_alignment="center", gap="small")

            with c_marker:
                if marker == "line":
                    st.markdown(
                    f"<div style='width:16px;height:2px;background:{color};border-radius:2px;margin-top:8px;'></div>",
                    unsafe_allow_html=True,
                )
                else:
                    st.markdown(f"<div style='width:9px;height:9px;border-radius:50%;background:{color};margin-top:6px;'></div>",
                    unsafe_allow_html=True,
                )

            with c_label:
                st.markdown(
                    f"<div style='font-size:0.72rem;line-height:1.1;margin:0;padding:0;'>{label}</div>",
                    unsafe_allow_html=True,
                )

            with c_toggle:
                return st.checkbox("", value=default, key=key)

        show_cons = legend_toggle("National consumption", LANDESVERBRAUCH, "dl_cons", marker="dot")
        show_rhine = legend_toggle("Rhine river flow", WASSERFUEHRUNG, "dl_rhine", marker="dot")
        show_trend_cons = legend_toggle("Trend line (national consumption)", LANDESVERBRAUCH, "dl_trend_cons", marker="line")
        show_trend_rhine = legend_toggle("Trend line (Rhine river flow)", WASSERFUEHRUNG, "dl_trend_rhine", marker="line")
        show_out_cons = legend_toggle("Outliers - national consumption", "#868D07", "dl_out_cons", marker="dot")
        show_out_rhine = legend_toggle("Outliers - Rhine", "#C8C36D", "dl_out_rhine", marker="dot")

    # with st.container(border=True):
    #    st.markdown(
    #        "**Impact of temperature on national electricity consumption and Rhine river flow**"
    #    )

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

# ─────────────────────────────────────────────
# MIDDLE ROW
# ─────────────────────────────────────────────
mid_left, mid_right = st.columns([2.2, 1], gap="small")

with mid_left:
    with st.container(border=True):
        st.markdown("### Production")

        selected_month = st.selectbox(
            "Choose month",
            options=["Total"] + sorted(df_monthly["Monat"].unique().tolist()),
            index=0,
            key="prod_month",
        )

        bar_col, donut_col = st.columns([1.4, 1])

        with bar_col:
            production_plots(
                df_monthly,
                height=prod_height,
                selected_month=selected_month,
                show_bar=True,
                show_donut=False,
            )

        with donut_col:
            production_plots(
                df_monthly,
                height=prod_height,
                selected_month=selected_month,
                show_bar=False,
                show_donut=True,
            )

with mid_right:
    with st.container(border=True):
        st.markdown("### Import, Export and Consumption")
        plot_heatmap_import_export(df_cleaned, height=heat_height)

# ─────────────────────────────────────────────
# BOTTOM ROW
# ─────────────────────────────────────────────
bottom_left, bottom_right = st.columns([3, 1.2], gap="small")

with bottom_left:
    with st.container(border=True):
        st.markdown("**Time Series and Energy Flow Metrics**")
        plot_time_series(df_cleaned, height=time_height)

with bottom_right:
    with st.container(border=True):
        plot_kpis(df_cleaned)
