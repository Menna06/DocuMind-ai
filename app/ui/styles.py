"""Global Streamlit styles for the DocuMind design system."""

import streamlit as st

from app.ui.theme import COLORS, RADIUS


def apply_global_styles() -> None:
    """Apply the shared DocuMind visual system."""

    st.markdown(
        f"""
        <style>

        /* =========================================================
           GLOBAL CANVAS
           ========================================================= */

        .stApp {{
            background: {COLORS["background"]};
            color: {COLORS["text_primary"]};
        }}

        .main .block-container {{
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }}


        /* =========================================================
           TYPOGRAPHY COLORS
           ========================================================= */

        h1,
        h2,
        h3 {{
            color: {COLORS["text_primary"]} !important;
        }}

        p,
        label,
        .stMarkdown {{
            color: {COLORS["text_secondary"]};
        }}


        /* =========================================================
           SIDEBAR
           ========================================================= */

        [data-testid="stSidebar"] {{
            background: {COLORS["surface"]};
            border-right: 1px solid {COLORS["border_default"]};
        }}

        [data-testid="stSidebar"] .block-container {{
            padding-top: 2rem;
        }}

        .sidebar-brand {{
            margin-bottom: 2rem;
        }}

        .sidebar-brand-title {{
            font-size: 1.35rem;
            font-weight: 700;
            color: {COLORS["text_primary"]};
            letter-spacing: -0.03em;
        }}

        .sidebar-brand-subtitle {{
            font-size: 0.72rem;
            color: {COLORS["text_muted"]};
            margin-top: 0.15rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }}

        .sidebar-section {{
            font-size: 0.68rem;
            color: {COLORS["text_muted"]};
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin: 1.5rem 0 0.5rem 0;
        }}

        [data-testid="stSidebar"] .stRadio label {{
            color: {COLORS["text_secondary"]} !important;
        }}


        /* =========================================================
           INPUTS
           ========================================================= */

        .stTextInput input,
        .stTextArea textarea {{
            background: {COLORS["surface"]} !important;
            color: {COLORS["text_primary"]} !important;
            border: 1px solid {COLORS["border_default"]} !important;
            border-radius: {RADIUS["md"]} !important;
        }}

        .stTextInput input:focus,
        .stTextArea textarea:focus {{
            border-color: {COLORS["purple"]} !important;
            box-shadow: 0 0 0 1px {COLORS["purple"]} !important;
        }}


        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button {{
            border-radius: {RADIUS["sm"]};
            border: 1px solid {COLORS["border_strong"]};
            background: {COLORS["text_primary"]};
            color: {COLORS["background"]};
            font-weight: 600;
            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                color 0.15s ease;
        }}

        .stButton > button:hover {{
            border-color: {COLORS["purple"]};
            background: {COLORS["text_primary"]};
            color: {COLORS["background"]};
        }}


        /* =========================================================
           DOCUMENT CARDS
           ========================================================= */

        .doc-card {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border_default"]};
            border-radius: {RADIUS["md"]};
            padding: 1.15rem 1.25rem;
            margin-bottom: 0.75rem;
        }}

        .doc-card-title {{
            color: {COLORS["text_primary"]};
            font-weight: 600;
            font-size: 0.98rem;
        }}

        .doc-card-meta {{
            color: {COLORS["text_muted"]};
            font-size: 0.78rem;
            margin-top: 0.35rem;
        }}

        .status-dot {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: {COLORS["success"]};
            margin-right: 6px;
        }}


        /* =========================================================
           ANSWER CARDS
           ========================================================= */

        .answer-card {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border_default"]};
            border-radius: {RADIUS["md"]};
            padding: 1.4rem 1.5rem;
            margin-top: 0.75rem;
            line-height: 1.7;
        }}

        .section-label {{
            color: {COLORS["text_muted"]};
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-weight: 700;
            margin-top: 1.8rem;
            margin-bottom: 0.65rem;
        }}


        /* =========================================================
           EVIDENCE
           ========================================================= */

        .evidence-card {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border_default"]};
            border-radius: {RADIUS["sm"]};
            padding: 0.9rem 1rem;
            margin-bottom: 0.6rem;
        }}

        .evidence-title {{
            color: {COLORS["text_primary"]};
            font-size: 0.86rem;
            font-weight: 600;
        }}

        .evidence-meta {{
            color: {COLORS["text_muted"]};
            font-size: 0.74rem;
            margin-top: 0.25rem;
        }}


        /* =========================================================
           UPLOAD AREA
           ========================================================= */

        [data-testid="stFileUploader"] {{
            background: {COLORS["surface"]};
            border: 1px dashed {COLORS["border_strong"]};
            border-radius: {RADIUS["md"]};
            padding: 0.5rem;
        }}


        /* =========================================================
           ALERTS
           ========================================================= */

        [data-testid="stAlert"] {{
            border-radius: {RADIUS["sm"]};
        }}


        /* =========================================================
           STREAMLIT CHROME
           ========================================================= */

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header {{
            background: transparent !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )