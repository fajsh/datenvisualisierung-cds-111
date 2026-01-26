import streamlit as st

def compute_kpis(df_monthly_sums):
    numeric_cols = [
        "Nettoerzeugung Total",
        "Landesverbrauch",
        "Verbrauch Speicherpumpen",
        "Ausfuhr",
        "Einfuhr",
        "Wasserführung Rhein",
    ]

    totals = df_monthly_sums[numeric_cols].sum()

    return {
        "Net production": totals["Nettoerzeugung Total"],
        "National consumption": totals["Landesverbrauch"],
        "Pumped storage consumption": totals["Verbrauch Speicherpumpen"],
        "Export": totals["Ausfuhr"],
        "Import": totals["Einfuhr"],
        "Rhine streamflow": totals["Wasserführung Rhein"],
    }


def build_energy_kpis_html(df_monthly_sums):
    kpis = compute_kpis(df_monthly_sums)
    cards = [
        ("⚡", "Net production", kpis["Net production"]),
        ("🇨🇭", "National consumption", kpis["National consumption"]),
        ("💧", "Pumped storage consumption", kpis["Pumped storage consumption"]),
        ("➡️", "Export", kpis["Export"]),
        ("⬅️", "Import", kpis["Import"]),
        ("🌊", "Rhine streamflow", kpis["Rhine streamflow"]),
    ]
    items = []
    for icon, title, value in cards:
        items.append(
            f"""
            <div style="display:flex; align-items:center; gap:0.6rem; padding:0.4rem 0.5rem;
                        border-radius:10px; background-color:#FFFFFF; margin-bottom:0.4rem;">
                <span style="font-size:1.2rem; width:1.6rem; text-align:center;">{icon}</span>
                <div>
                    <div style="font-size:0.8rem; font-weight:600; color:#000000;">{title}</div>
                    <div style="font-size:0.75rem; opacity:0.75; color:#000000;">{value:.1f} GWh</div>
                </div>
            </div>
            """
        )
    return (
        '<div style="display:grid; grid-template-columns:1fr 1fr; gap:0.4rem;">'
        + "".join(items)
        + "</div>"
    )


def _kpi_card(icon, title, value, unit="GWh"):
    """
    Render a single KPI card (internal helper).
    """
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.4rem 0.5rem;
            border-radius: 10px;
            background-color: #FFFFFF;
            min-height: 64px;
            width: 100%;
            box-sizing: border-box;
            margin-bottom: 0.4rem;
        ">
            <span class="material-icons" style="font-size: 1.2rem; width: 1.6rem; text-align: center;">{icon}</span>
            <div>
                <div style="font-size: 0.8rem; font-weight: 600; line-height: 1.2;">{title}</div>
                <div style="font-size: 0.75rem; opacity: 0.75; line-height: 1.2;">{value:.1f} {unit}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_energy_kpis(df_monthly_sums):
    """
    Public function to render the complete KPI block.
    This is the only function that should be called from app.py.
    """

    kpis = compute_kpis(df_monthly_sums)

    icons = {
        "Net production": "bolt",
        "National consumption": "flag",
        "Pumped storage consumption": "water_drop",
        "Export": "north_east",
        "Import": "south_west",
        "Rhine streamflow": "waves",
    }

    cols = st.columns(6)
    with cols[0]:
        _kpi_card(icons["Net production"], "Net production", kpis["Net production"])
    with cols[1]:
        _kpi_card(icons["National consumption"], "National consumption", kpis["National consumption"])
    with cols[2]:
        _kpi_card(icons["Pumped storage consumption"], "Pumped storage consumption", kpis["Pumped storage consumption"])
    with cols[3]:
        _kpi_card(icons["Export"], "Export", kpis["Export"])
    with cols[4]:
        _kpi_card(icons["Import"], "Import", kpis["Import"])
    with cols[5]:
        _kpi_card(icons["Rhine streamflow"], "Rhine streamflow", kpis["Rhine streamflow"])
