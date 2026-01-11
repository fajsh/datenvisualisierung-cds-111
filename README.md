# Energy Dashboard 2025

## Projektbeschreibung
Interaktives Dashboard zur Analyse von Energieproduktion und -verbrauch sowie die regionalen Unterschieden in der Schweiz.

Die Daten basieren auf der offiziellen Elektrizitätsstatistik des Bundesamts für Energie (BFE), welche detaillierte Informationen zur Stromerzeugung in der Schweiz nach Energiequellen bereitstellt.

Bundesamt für Energie (BFE):
https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/energiestatistiken/elektrizitaetsstatistik.html

## Architektur
- Datenimport: /data
- Visualisierungen: /plots
- Layout & UI: /layout
- Globale Zustände: /state

## Starten
streamlit run app.py