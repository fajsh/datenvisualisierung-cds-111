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


def _kpi_card(icon, title, value, unit="GWh"):
    """
    Render a single KPI card (internal helper).
    """
    st.markdown(
        f"""
        <div style="
            padding: 1rem;
            border-radius: 12px;
            background-color: #f7f7f7;
            margin-bottom: 1rem;
        ">
            <span style="font-size: 1.8rem;">{icon}</span><br>
            <strong>{title}</strong><br>
            {value:.1f} {unit}
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

    col1, col2 = st.columns(2)

    with col1:
        _kpi_card("⚡", "Net production", kpis["Net production"])
        _kpi_card("🇨🇭", "National consumption", kpis["National consumption"])
        _kpi_card("💧", "Pumped storage consumption", kpis["Pumped storage consumption"])
        

    with col2:
        _kpi_card("➡️", "Export", kpis["Export"])
        _kpi_card("⬅️", "Import", kpis["Import"])
        _kpi_card("🌊", "Rhine streamflow", kpis["Rhine streamflow"])
