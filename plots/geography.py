import json
from pathlib import Path

import folium
import pandas as pd
import streamlit as st
from branca.colormap import LinearColormap
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium


@st.cache_data
def _load_timeseries(path, sheet_name):
    return pd.read_excel(path, sheet_name=sheet_name, skiprows=[1])


def _extract_canton_codes(column_name, metric):
    if "\n" in column_name:
        column_name = column_name.split("\n", 1)[0].strip()

    singular = f"{metric} Kanton "
    plural = f"{metric} Kantone "

    if column_name.startswith(singular):
        return [column_name.replace(singular, "").strip()]
    if column_name.startswith(plural):
        tail = column_name.replace(plural, "").strip()
        return [code.strip() for code in tail.split(",") if code.strip()]
    return []


def _build_canton_totals(df, metric, split_mode):
    totals = {}

    candidate_cols = [
        col for col in df.columns
        if isinstance(col, str) and col.startswith(f"{metric} Kanton")
    ]
    candidate_cols += [
        col for col in df.columns
        if isinstance(col, str) and col.startswith(f"{metric} Kantone")
    ]

    for col in candidate_cols:
        codes = _extract_canton_codes(col, metric)
        if not codes:
            continue

        value = pd.to_numeric(df[col], errors="coerce").sum()
        if split_mode == "equal" and len(codes) > 1:
            value = value / len(codes)

        for code in codes:
            totals[code] = totals.get(code, 0) + value

    return pd.DataFrame({"Kanton": sorted(totals), "Wert": [totals[k] for k in sorted(totals)]})


def _guess_feature_key(geojson_obj):
    feature = geojson_obj.get("features", [{}])[0]
    props = feature.get("properties", {})
    for key in ("NAME", "name", "KANTON", "kanton", "abbr", "code", "id"):
        if key in props:
            return f"properties.{key}"
    if "id" in feature:
        return "id"
    return None


def _map_codes_to_names(df):
    code_to_name = {
        "AG": "Aargau",
        "AI": "Appenzell Innerrhoden",
        "AR": "Appenzell Ausserrhoden",
        "BE": "Bern",
        "BL": "Basel-Landschaft",
        "BS": "Basel-Stadt",
        "FR": "Fribourg",
        "GE": "Gen\u00e8ve",
        "GL": "Glarus",
        "GR": "Graub\u00fcnden",
        "JU": "Jura",
        "LU": "Luzern",
        "NE": "Neuch\u00e2tel",
        "NW": "Nidwalden",
        "OW": "Obwalden",
        "SG": "St. Gallen",
        "SH": "Schaffhausen",
        "SO": "Solothurn",
        "SZ": "Schwyz",
        "TG": "Thurgau",
        "TI": "Ticino",
        "UR": "Uri",
        "VD": "Vaud",
        "VS": "Valais",
        "ZG": "Zug",
        "ZH": "Z\u00fcrich",
    }

    df = df.copy()
    df["Kanton"] = df["Kanton"].map(code_to_name).fillna(df["Kanton"])
    return df


def _merge_geojson_by_property(geojson_obj, feature_key):
    if not feature_key or not feature_key.startswith("properties."):
        return geojson_obj

    prop_key = feature_key.split(".", 1)[1]
    merged = {}

    for feat in geojson_obj.get("features", []):
        props = feat.get("properties", {})
        name = props.get(prop_key)
        if not name:
            continue

        geom = feat.get("geometry", {})
        geom_type = geom.get("type")
        coords = geom.get("coordinates", [])
        if geom_type == "Polygon":
            polygons = [coords]
        elif geom_type == "MultiPolygon":
            polygons = coords
        else:
            continue

        entry = merged.setdefault(
            name,
            {
                "type": "Feature",
                "properties": {prop_key: name},
                "geometry": {"type": "MultiPolygon", "coordinates": []},
            },
        )
        entry["geometry"]["coordinates"].extend(polygons)

    return {"type": "FeatureCollection", "features": list(merged.values())}


def plot_kantonskarte(
    data_path="data/raw/EnergieUebersichtCH-2025-2.xlsx",
    geojson_path="data/geo/swissBOUNDARIES3D_1_3_TLM_KANTONSGEBIET.geojson",
    sheet_name="Zeitreihen0h15",
    metric_label="Produktion",
    split_mode="equal",
    feature_key="properties.NAME",
):
    data_file = Path(data_path)
    if not data_file.exists():
        st.info(f"Daten nicht gefunden: {data_file.as_posix()}")
        return

    geo_file = Path(geojson_path)
    if not geo_file.exists():
        st.info(
            "GeoJSON fehlt. Lege die Datei hier ab: "
            f"{geo_file.as_posix()}"
        )
        return

    if metric_label is None:
        metric_label = st.selectbox("Kennzahl", ["Produktion", "Verbrauch"], index=0)

    df = _load_timeseries(str(data_file), sheet_name)

    if "Zeitstempel" in df.columns:
        df["Zeitstempel"] = pd.to_datetime(df["Zeitstempel"], dayfirst=True, errors="coerce")
        month_options = (
            df["Zeitstempel"]
            .dropna()
            .dt.to_period("M")
            .astype(str)
            .unique()
        )
        month_options = sorted(month_options)
        selected_month = st.selectbox("Monat waehlen", ["Gesamt"] + month_options)
        if selected_month != "Gesamt":
            df = df[df["Zeitstempel"].dt.to_period("M").astype(str) == selected_month]

    totals = _build_canton_totals(df, metric_label, split_mode)
    totals = _map_codes_to_names(totals)

    with geo_file.open("r", encoding="utf-8") as handle:
        geojson_obj = json.load(handle)

    feature_key = feature_key or _guess_feature_key(geojson_obj)
    if not feature_key:
        st.info("GeoJSON-Feature-Key nicht erkannt. Bitte feature_key setzen.")
        return

    geojson_obj = _merge_geojson_by_property(geojson_obj, feature_key)

    if feature_key.startswith("properties."):
        prop_key = feature_key.split(".", 1)[1]
        geo_names = {f.get("properties", {}).get(prop_key) for f in geojson_obj.get("features", [])}
        data_names = set(totals["Kanton"].unique())
        missing = sorted(n for n in data_names if n not in geo_names)
        if missing:
            st.warning("Kantone im Datensatz fehlen im GeoJSON: " + ", ".join(missing))
    else:
        st.info("GeoJSON-Feature-Key muss properties.<name> sein.")
        return

    value_map = {row["Kanton"]: row["Wert"] for _, row in totals.iterrows()}
    display_map = {
        k: f"{value_map[k]:,.0f}".replace(",", "'")
        for k in value_map
    }
    if feature_key.startswith("properties."):
        prop_key = feature_key.split(".", 1)[1]
        for feat in geojson_obj.get("features", []):
            name = feat.get("properties", {}).get(prop_key)
            if name in display_map:
                feat["properties"]["Wert_kwh"] = display_map[name]

    map_center = [46.8, 8.3]
    m = folium.Map(location=map_center, zoom_start=7, tiles="CartoDB positron")

    palette = [
        "#768E78",
        "#C6C09C",
        "#EBDEC0",
        "#E79897",
        "#FCAC83",
        "#FCC88A",
        "#E0C1A6",
        "#8096AD",
    ]
    colormap = LinearColormap(
        palette,
        vmin=totals["Wert"].min(),
        vmax=totals["Wert"].max(),
    )
    colormap.caption = f"{metric_label} (kWh)"
    colormap.add_to(m)

    def style_function(feature):
        name = feature.get("properties", {}).get(prop_key)
        value = value_map.get(name)
        fill = colormap(value) if value is not None else "#f2f2f2"
        return {
            "fillColor": fill,
            "color": "#555555",
            "weight": 0.7,
            "fillOpacity": 0.85,
        }

    tooltip = GeoJsonTooltip(
        fields=[prop_key, "Wert_kwh"],
        aliases=["Kanton:", f"{metric_label} (kWh):"],
        localize=True,
        sticky=False,
    )
    folium.GeoJson(geojson_obj, style_function=style_function, tooltip=tooltip).add_to(m)

    st_folium(m, width=900, height=650)
