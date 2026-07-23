"""Global CSS injection for the Streamlit app."""

import streamlit as st

from colours import DARK, GOLD, LIGHT, NEUTRAL, SKY, UN_BLUE, WHITE


def apply_styles() -> None:
    """Inject WHO-branded CSS into the Streamlit app."""
    st.markdown(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <style>
        /* ===== BASE & LAYOUT ===== */
        .stApp {{
            background-color: {NEUTRAL};
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 52rem;
        }}

        [data-testid="stVerticalBlock"] {{
            gap: 1rem !important;
        }}

        /* ===== TYPOGRAPHY ===== */
        h1, h2, h3, h4 {{
            color: {DARK};
            font-weight: 600;
        }}

        p, span, label {{
            color: {DARK};
        }}

        /* ===== BUTTONS ===== */
        .stButton > button {{
            background-color: {UN_BLUE};
            color: {WHITE};
            border: none;
            border-radius: 2px;
            padding: 0.7rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.2px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 158, 219, 0.25);
        }}

        .stButton > button:hover {{
            background-color: {GOLD};
            color: {DARK};
            box-shadow: 0 4px 14px rgba(253, 157, 36, 0.3);
            transform: translateY(-1px);
        }}

        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: 0 1px 4px rgba(0, 158, 219, 0.2);
        }}

        /* ===== SELECTBOX & INPUTS ===== */
        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] > div > div {{
            background-color: {WHITE} !important;
            border: 1px solid {SKY} !important;
            border-radius: 2px !important;
            color: {DARK} !important;
            transition: border-color 0.2s ease;
        }}

        div[data-baseweb="select"] > div:hover {{
            border-color: {UN_BLUE} !important;
        }}

        ul[data-baseweb="menu"] {{
            background-color: {WHITE} !important;
            border-radius: 2px !important;
        }}

        ul[data-baseweb="menu"] li {{
            color: {DARK} !important;
        }}

        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [data-baseweb="menu"],
        [data-baseweb="listbox"],
        [role="listbox"],
        [role="listbox"] > li,
        [data-baseweb="menu"] > li {{
            background-color: {WHITE} !important;
            color: {DARK} !important;
        }}

        [data-baseweb="menu"] li:hover,
        [role="listbox"] li:hover {{
            background-color: {LIGHT} !important;
        }}

        .stNumberInput > div > div > input,
        .stTextInput > div > div > input,
        input[type="number"],
        input[type="text"] {{
            background-color: {WHITE} !important;
            border: 1px solid {SKY} !important;
            border-radius: 2px !important;
            color: {DARK} !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}

        .stNumberInput > div > div > input:focus,
        .stTextInput > div > div > input:focus,
        input[type="number"]:focus,
        input[type="text"]:focus {{
            border-color: {UN_BLUE} !important;
            box-shadow: 0 0 0 3px rgba(0, 158, 219, 0.1);
        }}

        .stNumberInput button {{
            background-color: {SKY} !important;
            color: {DARK} !important;
            border: 1px solid {SKY} !important;
            border-radius: 2px !important;
        }}

        .stNumberInput button:hover {{
            background-color: {UN_BLUE} !important;
            color: {WHITE} !important;
        }}

        .stNumberInput button svg {{
            color: {DARK} !important;
            fill: {DARK} !important;
        }}

        .stNumberInput button:hover svg {{
            color: {WHITE} !important;
            fill: {WHITE} !important;
        }}

        [data-baseweb="input"],
        [data-baseweb="input"] > div {{
            border-radius: 2px !important;
            border-color: {SKY} !important;
        }}

        .stSelectbox > div > div,
        .stNumberInput > div {{
            border-radius: 2px !important;
        }}

        .stNumberInput div[data-baseweb] {{
            border-color: {SKY} !important;
            border-radius: 2px !important;
        }}

        .stSelectbox div[data-baseweb] {{
            border-color: {SKY} !important;
            border-radius: 2px !important;
        }}

        .stSelectbox [data-baseweb="select"] > div:last-child,
        div[data-baseweb="select"] > div > div:last-child {{
            background-color: {LIGHT} !important;
            border-radius: 2px !important;
        }}

        .stSelectbox [data-baseweb="select"] > div:last-child:hover,
        div[data-baseweb="select"] > div > div:last-child:hover {{
            background-color: {SKY} !important;
        }}

        .stSelectbox svg,
        div[data-baseweb="select"] svg {{
            color: {DARK} !important;
            fill: {DARK} !important;
        }}

        div[data-baseweb="select"] > div > div:last-child {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 0.5rem !important;
        }}

        [data-testid="stNumberInput"] div,
        [data-testid="stSelectbox"] div {{
            border-color: {SKY} !important;
        }}

        div[data-baseweb="select"] span {{
            color: {DARK} !important;
        }}

        .stNumberInput label,
        .stSelectbox label,
        .stTextInput label {{
            color: {DARK} !important;
            font-weight: 500;
            font-size: 0.88rem;
        }}

        /* ===== TOGGLE ===== */
        .stToggle label span {{
            color: {DARK};
            font-weight: 500;
        }}

        /* ===== METRICS ===== */
        div[data-testid="stMetric"] {{
            background-color: {WHITE};
            border: 1px solid {LIGHT};
            border-radius: 2px;
            padding: 1rem 1.2rem;
            box-shadow: 0 1px 6px rgba(0,0,0,0.03);
        }}

        div[data-testid="stMetricValue"] {{
            color: {UN_BLUE};
            font-weight: 700;
        }}

        /* ===== CONTAINERS ===== */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 2px;
            border-color: transparent;
        }}

        /* ===== EXPANDER ===== */
        .streamlit-expanderHeader {{
            background-color: {WHITE};
            border-radius: 2px;
            font-weight: 500;
        }}

        details[data-testid="stExpander"] svg,
        [data-testid="stExpander"] svg,
        .st-emotion-cache-p5msec svg,
        details summary svg {{
            color: {UN_BLUE} !important;
            fill: {UN_BLUE} !important;
        }}

        details[data-testid="stExpander"] summary {{
            padding: 0.5rem 1rem;
        }}

        details[data-testid="stExpander"],
        details[data-testid="stExpander"] > summary,
        [data-testid="stExpander"],
        [data-testid="stExpander"] > div {{
            border: none !important;
            border-radius: 2px !important;
            box-shadow: none !important;
            outline: none !important;
        }}

        [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {{
            font-size: 0.82rem;
        }}

        /* ===== TOOLTIP ===== */
        .stTooltipIcon svg {{
            color: {UN_BLUE};
        }}

        /* ===== DIVIDER ===== */
        hr {{
            border-color: {LIGHT};
            opacity: 0.5;
        }}

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {NEUTRAL};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {LIGHT};
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {UN_BLUE};
        }}

        /* ===== FOOTER ===== */
        footer {{
            visibility: hidden;
        }}

        /* ===== ICON TILES ===== */
        .icon-tile {{
            width: 40px;
            height: 40px;
            border-radius: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
