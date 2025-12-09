from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Global Power Plant Explorer", layout="wide")

BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "global_power_plant_database.csv"
LOGO_PATH = BASE_PATH / "logo.png"


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(subset=["latitude", "longitude"])

    fuel_cols = ["other_fuel1", "other_fuel2", "other_fuel3"]
    df["other_fuels"] = (
        df[fuel_cols]
        .apply(lambda row: ", ".join([str(x) for x in row if pd.notna(x)]), axis=1)
        .replace("", pd.NA)
    )

    # Keep year numeric but allow missing values.
    df["commissioning_year"] = (
        pd.to_numeric(df["commissioning_year"], errors="coerce").round().astype("Int64")
    )

    return df


def build_hover_text(row: pd.Series) -> str:
    lines = [
        f"<b>{row['name']}</b>",
        f"Country: {row['country_long']}",
        f"Capacity: {row['capacity_mw']:,} MW" if pd.notna(row["capacity_mw"]) else "Capacity: N/A",
        f"Primary fuel: {row['primary_fuel']}",
    ]

    if pd.notna(row["other_fuels"]):
        lines.append(f"Other fuels: {row['other_fuels']}")

    if pd.notna(row["commissioning_year"]):
        lines.append(f"Commissioned: {int(row['commissioning_year'])}")

    if pd.notna(row["owner"]):
        lines.append(f"Owner: {row['owner']}")

    return "<br>".join(lines)


df = load_data(DATA_PATH)

st.title("Global Power Plant Explorer")
st.write(
    "Visualize the Global Power Plant Database on an interactive map. "
    "Filter by country and primary fuel, then inspect each plant's details."
)

with st.sidebar:
    st.header("Filters")
    countries = sorted(df["country_long"].dropna().unique().tolist())
    fuels = sorted(df["primary_fuel"].dropna().unique().tolist())

    country_choice = st.selectbox(
        "Country",
        ["All countries"] + countries,
        help="Choose a country to display (or show all).",
    )
    fuel_choice = st.selectbox(
        "Primary fuel",
        ["All fuels"] + fuels,
        help="Color and filter plants by their primary fuel (or show all).",
    )

if country_choice == "All countries":
    country_mask = df["country_long"].notna()
else:
    country_mask = df["country_long"] == country_choice

if fuel_choice == "All fuels":
    fuel_mask = df["primary_fuel"].notna()
else:
    fuel_mask = df["primary_fuel"] == fuel_choice

filtered = df[country_mask & fuel_mask].copy()

tab_map, tab_info, tab_estimate = st.tabs(
    ["Map explorer", "Infographic", "Estimating Power Plant Generation"]
)

with tab_map:
    if filtered.empty:
        st.warning("No plants match the current filters.")
    else:
        filtered["hover_text"] = filtered.apply(build_hover_text, axis=1)

        fig = px.scatter_mapbox(
            filtered,
            lat="latitude",
            lon="longitude",
            color="primary_fuel",
            size="capacity_mw",
            size_max=14,
            hover_name="name",
            zoom=1,
            height=600,
        )
        fig.update_traces(hovertemplate="%{text}<extra></extra>", text=filtered["hover_text"])
        fig.update_layout(
            mapbox_style="open-street-map",
            legend_title_text="Primary fuel",
            margin=dict(l=0, r=0, t=0, b=0),
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Plants in current selection")
        display_cols = [
            "country_long",
            "name",
            "capacity_mw",
            "primary_fuel",
            "other_fuels",
            "commissioning_year",
            "owner",
        ]
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

with tab_info:
    if (BASE_PATH / "infographic.png").exists():
        st.image(str(BASE_PATH / "infographic.png"), caption="Global Power Plant Overview", use_container_width=True)
    else:
        st.info("Add infographic.png next to this app to display it here.")

with tab_estimate:
    estimation_imgs = [BASE_PATH / f"{i}.jpeg" for i in range(1, 9)]
    available_imgs = [p for p in estimation_imgs if p.exists()]

    if available_imgs:
        for img_path in available_imgs:
            st.image(str(img_path), use_container_width=True)
    else:
        st.info("Add 1.jpeg through 8.jpeg next to this app to display the estimation visuals.")

st.markdown("---")
footer = st.container()
with footer:
    left, right = st.columns([0.7, 0.3])
    with left:
        st.write("Thanks for exploring!")
    with right:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=False, width=160)
        else:
            st.info("Add a logo.png next to this app to display it here.")
