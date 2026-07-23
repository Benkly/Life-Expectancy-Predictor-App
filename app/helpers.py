"""Shared helper functions for data loading and simple UI components."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from colours import DARK, LIGHT, UN_BLUE

APP_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the WHO life expectancy dataset, cached across reruns."""
    return pd.read_csv(APP_DIR / "Life Expectancy Data.csv")


def section_header(title: str, subtitle: str | None = None) -> None:
    """Render a consistent section heading with an optional subtitle."""
    st.markdown(
        f"<h2 style='color:{DARK}; margin-bottom:0;'>{title}</h2>",
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f"<p style='color:{DARK}; opacity:0.7; margin-top:0.2rem;'>{subtitle}</p>",
            unsafe_allow_html=True,
        )


def metric_card(label: str, value: str, help_text: str | None = None) -> None:
    """Thin wrapper around st.metric for consistent styling."""
    st.metric(label=label, value=value, help=help_text)


def insight_box(text: str, colour: str = UN_BLUE) -> None:
    """Render a highlighted callout box."""
    st.markdown(
        f"""
        <div style="background-color:{LIGHT};
                    padding:0.8rem 1rem; border-radius:2px; margin:0.6rem 0; color:{DARK};">
        {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
