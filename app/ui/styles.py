import base64
from pathlib import Path
import streamlit as st

from app.ui.theme import COLORS, LAYOUT, RADIUS, TYPOGRAPHY


def _load_background_image_base64(image_path: str = "static/background.png") -> str:
    """Return the base64-encoded background image asset."""
    path = Path(image_path)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def apply_global_styles() -> None:
    """Apply the shared DocuMind visual system."""

    bg_b64 = _load_background_image_base64()

    st.markdown(
        f"""
        <style>

        /* =========================================================
           GLOBAL CANVAS
           ========================================================= */

        .stApp {{
            background-color: {COLORS["background"]};
            background-image: url("data:image/png;base64,{bg_b64}");
            background-size: cover;
            background-position: top right;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: {COLORS["text_primary"]};
        }}

        .main .block-container {{
            max-width: {LAYOUT["content_max_width"]};
            padding-top: 2.5rem;
            padding-bottom: 4rem;
            padding-left: {LAYOUT["content_padding_x"]};
            padding-right: {LAYOUT["content_padding_x"]};
            margin: 0 auto;
        }}


        /* =========================================================
           TYPOGRAPHY SYSTEM — UI-02
           ========================================================= */

        html,
        body,
        .stApp {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace;
        }}

        h1,
        h2,
        h3 {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-weight: {TYPOGRAPHY["heading"]["weight"]} !important;
            color: {COLORS["text_primary"]} !important;
        }}

        h1 {{
            font-weight: {TYPOGRAPHY["display"]["weight"]} !important;
        }}

        p,
        label,
        .stMarkdown,
        input,
        textarea,
        button {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace;
            font-weight: {TYPOGRAPHY["body"]["weight"]};
        }}

        .section-label {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace;
            font-weight: {TYPOGRAPHY["accent"]["weight"]};
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
            padding-left: 1.25rem;
            padding-right: 1.25rem;
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
            font-weight: 700;
            margin: 1.5rem 0 0.65rem 0;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {{
            gap: 4px;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label {{
            background: transparent;
            border: 1px solid transparent;
            border-radius: {RADIUS["sm"]};
            padding: 8px 12px;
            margin-bottom: 2px;
            transition: all 150ms ease;
            cursor: pointer;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover {{
            background: {COLORS["surface_hover"]};
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {{
            background: rgba(137, 39, 221, 0.12) !important;
            border-color: rgba(137, 39, 221, 0.35) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] p,
        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) p {{
            color: {COLORS["text_primary"]} !important;
            font-weight: 600 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label p {{
            color: {COLORS["text_secondary"]} !important;
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.84rem !important;
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
            box-shadow: 0 0 6px rgba(121, 181, 138, 0.5);
            margin-right: 6px;
            animation: documind-pulse-dot 2.4s infinite ease-in-out;
        }}

        @keyframes documind-pulse-dot {{
            0%, 100% {{
                opacity: 0.65;
                box-shadow: 0 0 4px rgba(121, 181, 138, 0.4);
            }}
            50% {{
                opacity: 1;
                box-shadow: 0 0 8px rgba(121, 181, 138, 0.7);
            }}
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