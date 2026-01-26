import streamlit as st
import streamlit.components.v1 as components


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


def _kpi_card_html(icon, title, value, unit="GWh", icon_color="#111111"):
    return f"""
    <div style="
        display:flex;
        align-items:center;
        gap:0.6rem;
        padding:0.45rem 0.55rem;
        border-radius:12px;
        background:#FFFFFF;
        border: 1px solid rgba(17,17,17,0.15);
        border-color: #FFFFFF;
        width:100%;
        box-sizing:border-box;
        min-height:64px;
    ">
        <span class="material-icons" style="
            font-size:2rem;
            width:1.8rem;
            text-align:center;
            color:{icon_color};
            line-height:1;
        ">{icon}</span>

        <div style="min-width:0;">
            <div style="
                font-size:1rem;
                font-weight:600;
                color:#111111;
                line-height:1.15;
                white-space:normal;
                overflow:visible;
                text-overflow:unset;
                word-break:break-word;
            ">{title}</div>

            <div style="
                font-size:1rem;
                color:#111111;
                opacity:0.72;
                line-height:1.15;
                margin-top:0.15rem;
            ">{value:.1f} {unit}</div>
        </div>
    </div>
    """


def render_energy_kpis(df_monthly_sums):
    kpis = compute_kpis(df_monthly_sums)

    icons = {
        "Net production": "bolt",
        "National consumption": "flag",
        "Pumped storage consumption": "water_drop",
        "Export": "north_east",
        "Import": "south_west",
        "Rhine streamflow": "waves",
    }

    icon_colors = {
        "Net production": "#F4B400",              # gelb
        "National consumption": "#F2994A",        # orange
        "Pumped storage consumption": "#2D9CDB",  # blau (wasser)
        "Export": "#27AE60",                      # grün
        "Import": "#EB5757",                      # rot
        "Rhine streamflow": "#2BB3B1",            # türkis
    }

    # HTML Grid für alle KPI-Cards (statt st.columns + markdown)
    grid_html = f"""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

    <style>
    /* Streamlit nutzt standardmäßig "Source Sans Pro" (bzw. ähnliche System-Fonts).
        Wir setzen das hier explizit, damit es gleich aussieht. */
    * {{
        font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif;
    }}
    </style>

    <div style="
        display:grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap:0.6rem;
        width:100%;
    ">
        {_kpi_card_html(icons["Net production"], "Net production", kpis["Net production"],
                        icon_color=icon_colors["Net production"])}

        {_kpi_card_html(icons["National consumption"], "National consumption", kpis["National consumption"],
                        icon_color=icon_colors["National consumption"])}

        {_kpi_card_html(icons["Pumped storage consumption"], "Pumped storage consumption", kpis["Pumped storage consumption"],
                        icon_color=icon_colors["Pumped storage consumption"])}

        {_kpi_card_html(icons["Export"], "Export", kpis["Export"],
                        icon_color=icon_colors["Export"])}

        {_kpi_card_html(icons["Import"], "Import", kpis["Import"],
                        icon_color=icon_colors["Import"])}

        {_kpi_card_html(icons["Rhine streamflow"], "Rhine streamflow", kpis["Rhine streamflow"],
                        icon_color=icon_colors["Rhine streamflow"])}
    </div>
    """

    # components.html rendert stabil (kein "als Text angezeigt")
    components.html(grid_html, height=90, scrolling=False)
