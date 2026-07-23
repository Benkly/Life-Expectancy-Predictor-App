"""Reusable HTML rendering components for the Streamlit app."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from colours import DARK, LIGHT, SKY, UN_BLUE, WHITE


def _get_flag_b64() -> str:
    """Return the WHO flag SVG as a base64 data URI."""
    data = (Path(__file__).parent / "Flag_of_WHO.svg").read_bytes()
    return f"data:image/svg+xml;base64,{base64.b64encode(data).decode()}"


def hero_banner() -> None:
    """Render the top hero banner with flag and app title."""
    st.markdown(
        f"""
        <div style="
            background: {UN_BLUE};
            border-radius: 2px;
            padding: 0 2rem 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.10);
            position: relative;
            overflow: hidden;
        ">
            <img src="{_get_flag_b64()}" style="width:420px; margin-bottom:-5rem; margin-top:-2rem;" />
            <h1 style="color:{WHITE}; margin:0 0 0.3rem; font-size:2.2rem; font-weight:700;
                        letter-spacing:-0.5px; position:relative;">
                Life Expectancy Predictor
            </h1>
            <p style="color:{WHITE}; font-size:1.05rem; max-width:560px; margin:0 auto;
                       line-height:1.6; opacity:0.92; position:relative;">
                Estimate a country's life expectancy from population statistics.
                <br/>
                Some inputs (health and mortality data) are considered sensitive,
                so we ask for your consent before using them.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def consent_card() -> None:
    """Render the data consent card with expandable model details."""
    st.markdown(
        f"""
        <div style="
            background: {WHITE};
            border: 2px solid {SKY};
            border-radius: 2px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        ">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.6rem;">
                <div class="icon-tile" style="background:{LIGHT};">
                    <i class="ti ti-shield-check" style="font-size:20px; color:{DARK};"></i>
                </div>
                <div>
                    <p style="color:{DARK}; margin:0; font-size:1.4rem; font-weight:600;">
                        Data Consent
                    </p>
                    <p style="color:{DARK}; opacity:0.7; font-size:0.95rem; margin:0.1rem 0 0;">
                        Do you consent to using sensitive data for better accuracy?
                    </p>
                </div>
            </div>
            <details style="cursor:pointer;" open>
                <summary style="color:{DARK}; font-size:0.85rem; opacity:0.7; list-style:none;
                                 display:flex; align-items:center; gap:0.3rem;">
                    <span style="font-size:0.7rem; color:{UN_BLUE};">&#9660;</span>
                    What's included in each model?
                </summary>
                <p style="color:{DARK}; opacity:0.6; font-size:0.82rem; margin:0.4rem 0 0; line-height:1.5;">
                    <strong>Minimal:</strong> Region, Year, GDP per capita, Population<br/>
                    <strong>Elaborate:</strong> Region, GDP per capita, Adult mortality,
                    Under-five deaths, Development status
                </p>
            </details>
        </div>
        """,
        unsafe_allow_html=True,
    )


def model_info_card(
    model_name: str, use_elaborate: bool,
    box_bg: str, box_border: str, box_heading: str, box_subtitle: str,
) -> None:
    """Render the coloured model-active banner."""
    subtitle = (
        "Includes sensitive health features (mortality, development status)"
        if use_elaborate
        else "Uses only non-sensitive features (GDP, population, year)"
    )
    st.markdown(
        f"""
        <div style="
            background: {box_bg};
            border: 2px solid {box_border};
            border-radius: 2px;
            padding: 0.6rem 1.8rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            text-align: center;
        ">
            <h2 style="color:{box_heading}; margin:0; padding:0; font-size:2rem; font-weight:700;
                        text-transform:capitalize; line-height:1.2;">
                {model_name} Model Active
            </h2>
            <p style="color:{box_subtitle}; font-size:1rem; margin:0.1rem 0 0; padding:0; line-height:1.2;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrics_row(
    test_rmse: float, test_adj_r2: float,
    metric_color: str, box_bg: str,
) -> None:
    """Render the RMSE and R-squared metric cards side by side."""
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown(
            f"""
            <div style="
                background: {WHITE};
                border: 2px solid {SKY};
                border-radius: 2px;
                padding: 1rem 1.4rem;
                box-shadow: 0 1px 6px rgba(0,0,0,0.03);
                display: flex; align-items: center; gap: 14px;
            ">
                <div class="icon-tile" style="background:{box_bg}22;">
                    <i class="ti ti-target-arrow" style="font-size:22px; color:{metric_color};"></i>
                </div>
                <div>
                    <p style="color:{DARK}; opacity:0.55; font-size:0.78rem; text-transform:uppercase;
                              letter-spacing:0.5px; margin:0 0 0.15rem;">Test RMSE</p>
                    <p style="color:{metric_color}; font-size:2.1rem; font-weight:700; margin:0; line-height:1.1;">
                        +/-{test_rmse:.2f} <span style="font-size:1rem; font-weight:600; color:{DARK};">years</span>
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m_col2:
        st.markdown(
            f"""
            <div style="
                background: {WHITE};
                border: 2px solid {SKY};
                border-radius: 2px;
                padding: 1rem 1.4rem;
                box-shadow: 0 1px 6px rgba(0,0,0,0.03);
                display: flex; align-items: center; gap: 14px;
            ">
                <div class="icon-tile" style="background:{box_bg}22;">
                    <i class="ti ti-chart-bar" style="font-size:22px; color:{metric_color};"></i>
                </div>
                <div>
                    <p style="color:{DARK}; opacity:0.55; font-size:0.78rem; text-transform:uppercase;
                              letter-spacing:0.5px; margin:0 0 0.15rem;">Adjusted R²</p>
                    <p style="color:{metric_color}; font-size:2.1rem; font-weight:700; margin:0; line-height:1.1;">
                        {test_adj_r2:.3f}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def population_stats_header() -> None:
    """Render the population statistics section header card."""
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            background: {WHITE};
            border: 2px solid {SKY};
            border-radius: 2px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        ">
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="icon-tile" style="background:{LIGHT};">
                    <i class="ti ti-clipboard-list" style="font-size:20px; color:{DARK};"></i>
                </div>
                <div>
                    <p style="color:{DARK}; margin:0; font-size:1.4rem; font-weight:600;">
                        Population Statistics
                    </p>
                    <p style="color:{DARK}; opacity:0.7; font-size:0.95rem; margin:0.1rem 0 0;">
                        Enter the values below to generate a prediction
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def result_card(prediction: float, lower: float, upper: float, accent_color: str) -> None:
    """Render the main prediction result card."""
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            background: {DARK};
            border-radius: 2px;
            padding: 1.8rem 2rem;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0,46,71,0.15);
        ">
            <p style="color:{WHITE}; font-size:1rem; text-transform:uppercase;
                       letter-spacing:1.5px; margin:0 0 0.4rem;">
                Predicted Life Expectancy
            </p>
            <p style="color:{WHITE}; font-size:4.2rem; font-weight:700; margin:0; line-height:1;">
                {prediction:.1f} <span style="font-size:1.8rem; font-weight:700; color:{WHITE};">years</span>
            </p>
            <div style="
                display: inline-block;
                background: {accent_color};
                border-radius: 2px;
                padding: 0.3rem 0.9rem;
                margin-top: 0.7rem;
            ">
                <span style="color:{DARK}; font-size:1rem; font-weight:600;">
                    Confidence range: {lower:.1f} to {upper:.1f} years
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def confidence_bar(
    prediction: float, lower: float, upper: float,
    bar_min: float, bar_max: float, accent_color: str,
) -> None:
    """Render the confidence interval visual bar."""
    pct_lower = max(0, min(100, (lower - bar_min) / (bar_max - bar_min) * 100))
    pct_upper = max(0, min(100, (upper - bar_min) / (bar_max - bar_min) * 100))
    pct_pred = max(0, min(100, (prediction - bar_min) / (bar_max - bar_min) * 100))

    st.markdown(
        f"""
        <div style="
            background: {WHITE};
            border: 2px solid {SKY};
            border-radius: 2px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.03);
        ">
            <p style="color:{DARK}; font-size:0.9rem; margin:0 0 0.6rem;
                       text-transform:uppercase; letter-spacing:0.5px;">
                Confidence Interval
            </p>
            <div style="position:relative; height:38px; background:{WHITE};
                        border-radius:2px; overflow:hidden; border:1px solid {SKY};">
                <div style="
                    position:absolute; left:{pct_lower}%; width:{pct_upper - pct_lower}%;
                    height:100%; background:{SKY}; border-radius:2px;
                "></div>
                <div style="
                    position:absolute; left:{pct_pred}%; top:3px; width:6px; height:32px;
                    background:{accent_color}; border-radius:1px;
                    transform:translateX(-50%); box-shadow: 0 0 6px {accent_color};
                "></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:0.4rem;">
                <span style="color:{DARK}; opacity:0.6; font-size:0.88rem;">{bar_min:.0f} yrs</span>
                <span style="color:{DARK}; opacity:0.6; font-size:0.88rem;">{bar_max:.0f} yrs</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def about_estimate(
    model_name: str, num_records: int, num_countries: int,
    year_min: int, year_max: int,
    test_rmse: float, test_adj_r2: float, metric_color: str,
) -> None:
    """Render the inline metrics summary and collapsible 'About this estimate'."""
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; gap:2rem; margin-bottom:0.5rem;">
            <span style="color:{DARK}; font-size:0.85rem;">
                RMSE: <strong style="color:{metric_color};">+/-{test_rmse:.2f} yrs</strong>
            </span>
            <span style="color:{DARK}; font-size:0.85rem;">
                Adj. R²: <strong style="color:{metric_color};">{test_adj_r2:.3f}</strong>
            </span>
        </div>
        <details style="cursor:pointer; margin-top:0.5rem;">
            <summary style="color:{DARK}; font-size:0.85rem; opacity:0.7; list-style:none;
                             display:flex; align-items:center; gap:0.3rem;">
                <span style="font-size:0.7rem; color:{UN_BLUE};">&#9660;</span> About this estimate
            </summary>
            <p style="color:{DARK}; opacity:0.6; font-size:0.82rem; margin:0.4rem 0 0; line-height:1.5;">
                Generated by the <em>{model_name}</em> model,
                trained on <strong>{num_records:,}</strong> country-year records
                ({num_countries} countries, {year_min} to {year_max}).
                The expected error (RMSE) is <strong>+/-{test_rmse:.2f} years</strong>.
            </p>
        </details>
        """,
        unsafe_allow_html=True,
    )
