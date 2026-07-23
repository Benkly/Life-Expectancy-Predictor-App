"""WHO Life Expectancy Predictor - main Streamlit app."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent

from colours import DARK, GOLD, GOLD_DARK, MOSS, SKY, UN_BLUE, WHITE, REGION_LIST
from components import (
    about_estimate, confidence_bar, consent_card, hero_banner,
    metrics_row, model_info_card, population_stats_header, result_card,
)
from helpers import load_data
from styles import apply_styles

st.set_page_config(page_title="World Health Organisation", page_icon="🌍", layout="centered")
apply_styles()


@st.cache_resource
def load_bundle(name: str) -> dict:
    return joblib.load(APP_DIR / "models" / f"{name}.pkl")


df = load_data()

# --- Hero ---
hero_banner()

# --- Consent ---
consent_card()

# manage consent state early so CSS can reflect it
if "use_elaborate" not in st.session_state:
    st.session_state.use_elaborate = None

_use = st.session_state.use_elaborate
if _use is None:
    _min_bg, _elab_bg = SKY, SKY
elif _use:
    _min_bg, _elab_bg = SKY, UN_BLUE
else:
    _min_bg, _elab_bg = UN_BLUE, SKY

# button styling (dynamic selected state + predict button)
st.markdown(
    f"""
    <style>
    .st-key-btn_predict button {{
        background-color: {UN_BLUE} !important;
        color: {WHITE} !important;
        border: none !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }}
    .st-key-btn_predict button p,
    .st-key-btn_predict button span,
    .st-key-btn_predict button div {{
        color: {WHITE} !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }}
    .st-key-btn_minimal button:hover,
    .st-key-btn_elaborate button:hover,
    .st-key-btn_predict button:hover {{
        background-color: {UN_BLUE} !important;
    }}
    .st-key-btn_minimal button {{
        background-color: {_min_bg} !important;
        color: {WHITE} !important;
        border: none !important;
    }}
    .st-key-btn_elaborate button {{
        background-color: {_elab_bg} !important;
        color: {WHITE} !important;
        border: none !important;
    }}
    [data-testid="stExpander"] {{
        border: none !important;
        background: transparent !important;
    }}
    [data-testid="stExpander"] details {{
        border: none !important;
    }}
    [data-testid="stExpander"] summary {{
        border: none !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# consent buttons
consent_col1, consent_col2 = st.columns(2)
with consent_col1:
    minimal_selected = st.button(
        "**No, don't use sensitive data**\n\nMinimal model",
        use_container_width=True, key="btn_minimal",
    )
with consent_col2:
    elaborate_selected = st.button(
        "**Yes, use sensitive data**\n\nElaborate model",
        use_container_width=True, key="btn_elaborate",
    )

if minimal_selected:
    st.session_state.use_elaborate = False
if elaborate_selected:
    st.session_state.use_elaborate = True

use_elaborate = st.session_state.use_elaborate
if use_elaborate is None:
    st.stop()

# --- Model info ---
model_name = "elaborate" if use_elaborate else "minimal"
bundle = load_bundle(model_name)
pipeline = bundle["pipeline"]
test_rmse = bundle["test_metrics"]["rmse"]
test_adj_r2 = bundle["test_metrics"]["adj_r2"]

if use_elaborate:
    _box_bg = GOLD
    _box_border = GOLD_DARK
    _box_heading = DARK
    _box_subtitle = "#8D7100"
    _metric_color = "#8D7100"
    _accent_color = GOLD
else:
    _box_bg = MOSS
    _box_border = "#5A9456"
    _box_heading = DARK
    _box_subtitle = "#3D7539"
    _metric_color = "#3D7539"
    _accent_color = MOSS

model_info_card(model_name, use_elaborate, _box_bg, _box_border, _box_heading, _box_subtitle)
metrics_row(test_rmse, test_adj_r2, _metric_color, _box_bg)

# --- Input form ---
population_stats_header()

with st.container():
    region = st.selectbox("Region", REGION_LIST, key="input_region")

    if use_elaborate:
        inp_col1, inp_col2 = st.columns(2)
        with inp_col1:
            gdp = st.number_input(
                "GDP per Capita (USD)",
                min_value=float(df["GDP_per_capita"].min()),
                max_value=float(df["GDP_per_capita"].max()),
                value=float(df["GDP_per_capita"].median()),
                format="%.2f", key="input_gdp_elaborate",
            )
            adult_mortality = st.number_input(
                "Adult Mortality (per 1000)",
                min_value=0.0, max_value=float(df["Adult_mortality"].max()),
                value=float(df["Adult_mortality"].median()), format="%.2f",
                help="Probability of dying between 15-60 years per 1000 population",
            )
        with inp_col2:
            under_five_deaths = st.number_input(
                "Under-Five Deaths (per 1000)",
                min_value=0.0, max_value=float(df["Under_five_deaths"].max()),
                value=float(df["Under_five_deaths"].median()), format="%.2f",
                help="Deaths of children under five per 1000 live births",
            )
            economy_status = st.selectbox("Economy Status", ["Developing", "Developed"], index=0)
            developed = 1 if economy_status == "Developed" else 0

        input_df = pd.DataFrame([{
            "Region": region, "GDP_per_capita": gdp,
            "Adult_mortality": adult_mortality,
            "Under_five_deaths": under_five_deaths,
            "Economy_status_Developed": developed,
        }])
    else:
        inp_col1, inp_col2 = st.columns(2)
        with inp_col1:
            year = st.number_input("Year", min_value=2000, max_value=2030, value=2015, step=1, key="input_year")
            gdp = st.number_input(
                "GDP per Capita (USD)",
                min_value=float(df["GDP_per_capita"].min()),
                max_value=float(df["GDP_per_capita"].max()),
                value=float(df["GDP_per_capita"].median()),
                format="%.2f", key="input_gdp_minimal",
            )
        with inp_col2:
            population = st.number_input(
                "Population (millions)",
                min_value=float(df["Population_mln"].min()),
                max_value=float(df["Population_mln"].max()),
                value=float(df["Population_mln"].median()), format="%.2f",
            )

        input_df = pd.DataFrame([{
            "Region": region, "Year": year,
            "log_GDP": np.log(gdp), "log_Population": np.log(population),
        }])

# --- Prediction ---
st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

if st.button("Predict Life Expectancy", type="primary", use_container_width=True, key="btn_predict"):
    prediction = pipeline.predict(input_df)[0]
    lower = prediction - test_rmse
    upper = prediction + test_rmse

    result_card(prediction, lower, upper, _accent_color)

    bar_min = float(df["Life_expectancy"].min())
    bar_max = float(df["Life_expectancy"].max())
    confidence_bar(prediction, lower, upper, bar_min, bar_max, _accent_color)

    about_estimate(
        model_name, len(df), df["Country"].nunique(),
        df["Year"].min(), df["Year"].max(),
        test_rmse, test_adj_r2, _metric_color,
    )
