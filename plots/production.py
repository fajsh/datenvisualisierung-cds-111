import streamlit as st
import matplotlib.pyplot as plt
from utils.colors import ENERGY_COLORS


def plot_landeserzeugung(df_monthly_sums):
    # ------------------------------------------------------------------
    # DATA PREP
    # ------------------------------------------------------------------
    df = df_monthly_sums.copy()

    df = df.drop(
        columns=['Total Hydraulisch', 'Total Erneuerbar'],
        errors='ignore'
    )

    df_plot = df[df['Monat'] != 'Total']
    df_total = df[df['Monat'] == 'Total']

    energy_sources = [
        'Laufwerke',
        'Speicherwerke',
        'Kernkraftwerke',
        'Thermisch',
        'Windkraft',
        'Photovoltaik'
    ]

    # ------------------------------------------------------------------
    # 1️⃣ STACKED BAR CHART (Monate)
    # ------------------------------------------------------------------
    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))

    (
        df_plot
        .set_index('Monat')[energy_sources]
        .plot(
            kind='bar',
            stacked=True,
            ax=ax_bar,
            color=[ENERGY_COLORS.get(src) for src in energy_sources]
        )
    )

    ax_bar.set_title('Monatliche Summen der Energieerzeugung im Jahr 2025')
    ax_bar.set_xlabel('Monat')
    ax_bar.set_ylabel('Energieerzeugung (in GWh)')
    ax_bar.legend(
        title='Energiequellen',
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )

    plt.tight_layout()
    st.pyplot(fig_bar)

    # ------------------------------------------------------------------
    # 2️⃣ PIE CHART (Total)
    # ------------------------------------------------------------------
    energy_values = df_total[energy_sources].values.flatten()
    
    fig_donut, ax_donut = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax_donut.pie(
        energy_values,
        labels=energy_sources,
        autopct='%1.1f%%',
        startangle=140,
        colors=[ENERGY_COLORS.get(src) for src in energy_sources],
        pctdistance=0.8
    )

    # 🔹 Donut-Loch
    centre_circle = plt.Circle((0, 0), 0.55, fc='white')
    ax_donut.add_artist(centre_circle)

    ax_donut.set_title('Gesamte Energieerzeugung nach Quelle im Jahr 2025')

    st.pyplot(fig_donut)

