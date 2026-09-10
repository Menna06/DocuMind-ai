"""Reusable DocuMind UI components."""

import base64
import re
from pathlib import Path
from textwrap import dedent

import streamlit as st

from app.ui.theme import (
    BUTTONS,
    COLORS,
    DOCUMENT_CARD,
    DOCUMENT_TILE,
    INPUTS,
)


def _safe_key(value: str) -> str:
    """Convert a component key into a valid Streamlit container key."""
    return re.sub(r"[^a-zA-Z0-9_-]", "-", value)


def render_button(
    label: str,
    variant: str = "primary",
    key: str | None = None,
    disabled: bool = False,
    icon: bool = False,
    full_width: bool = False,
) -> bool:
    """Render a reusable DocuMind button using the design-system tokens."""

    if variant not in BUTTONS:
        raise ValueError(
            f"Unknown button variant: {variant}. "
            f"Expected one of: {', '.join(BUTTONS.keys())}"
        )

    button = BUTTONS[variant]

    container_key = _safe_key(
        f"documind-button-{variant}-{key or label}"
    )

    width_rule = "width: 100% !important;" if full_width else "width: auto;"
    height_rule = (
        "height: 42px !important; min-height: 42px !important; max-height: 42px !important;"
        if full_width
        else "min-height: 34px;"
    )
    padding_rule = "padding: 0 18px !important;" if full_width else "padding: 0 12px;"
    justify_rule = "justify-content: center !important;" if full_width else ""
    line_height_rule = "line-height: 40px !important;" if full_width else ""
    container_width = "width: 100% !important;" if full_width else ""

    st.markdown(
        f"""
        <style>

        .st-key-{container_key} {{
            {container_width}
            margin: 0 !important;
            padding: 0 !important;
        }}

        .st-key-{container_key} [data-testid="stElementContainer"],
        .st-key-{container_key} [data-testid="stButton"] {{
            {container_width}
            margin: 0 !important;
            padding: 0 !important;
        }}

        .st-key-{container_key} button {{
            {width_rule}
            {height_rule}
            {padding_rule}
            {justify_rule}
            {line_height_rule}

            border-radius: {BUTTONS["radius"]};

            font-family: "JetBrains Mono", monospace;
            font-size: {BUTTONS["font_size"]};
            font-weight: {BUTTONS["font_weight"]};

            background: {button["background"]};
            color: {button["text"]};

            border: 1px solid {button["border"]};

            box-shadow: none;
            transition: {BUTTONS["transition"]};
            box-sizing: border-box !important;
            margin: 0 !important;
            display: inline-flex;
            align-items: center;
        }}

        .st-key-{container_key} button:hover {{
            background: {button["hover_background"]};
            color: {button["hover_text"]};
            border-color: {button["hover_border"]};
        }}

        .st-key-{container_key} button:focus {{
            box-shadow: 0 0 0 2px {button["focus_ring"]};
        }}

        .st-key-{container_key} button:disabled {{
            background: {button["disabled_background"]};
            color: {button["disabled_text"]};
            border-color: {button["disabled_border"]};
            opacity: 1;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key=container_key):

        if icon:
            st.markdown(
                f"""
                <style>

                .st-key-{container_key} button {{
                    display: inline-flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    gap: 8px !important;
                }}

                .st-key-{container_key} button::before {{
                    content: "";
                    width: 20px;
                    height: 20px;
                    display: inline-block;

                    background-color: currentColor;

                    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 3h6l1 2h4v2H4V5h4l1-2zm-3 6h12v11a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V9zm3 2v7h2v-7H9zm4 0v7h2v-7h-2z'/%3E%3C/svg%3E");

                    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 3h6l1 2h4v2H4V5h4l1-2zm-3 6h12v11a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V9zm3 2v7h2v-7H9zm4 0v7h2v-7h-2z'/%3E%3C/svg%3E");

                    -webkit-mask-repeat: no-repeat;
                    mask-repeat: no-repeat;

                    -webkit-mask-position: center;
                    mask-position: center;

                    -webkit-mask-size: contain;
                    mask-size: contain;
                }}

                </style>
                """,
                unsafe_allow_html=True,
            )

        return st.button(
            label,
            key=key,
            disabled=disabled,
            type="secondary",
        )


def render_question_input(
    label: str = "Question",
    placeholder: str = "What does the document say about...?",
    key: str = "question",
    help_text: str | None = None,
    error: str | None = None,
) -> str:
    """Render the DocuMind Question Input component."""

    input_config = INPUTS["question"]

    container_key = _safe_key(
        f"documind-question-input-{key}"
    )

    st.markdown(
        f"""
        <style>

        /* =====================================================
           QUESTION INPUT — UI-05
           ===================================================== */

        .st-key-{container_key} {{
            width: 100%;
        }}

        .st-key-{container_key} label {{
            font-family: "JetBrains Mono", monospace !important;
            color: {COLORS["text_secondary"]} !important;
        }}

        /* BaseWeb input wrapper */
        .st-key-{container_key}
        div[data-baseweb="input"] {{
            background: {input_config["background"]} !important;
            border: 1px solid {input_config["border"]} !important;
            border-radius: {INPUTS["radius"]} !important;
            box-shadow: none !important;
            transition:
                border-color 150ms ease,
                background 150ms ease;
        }}

        /* Remove Streamlit/BaseWeb focus glow */
        .st-key-{container_key}
        div[data-baseweb="input"]:focus-within {{
            background: {input_config["background"]} !important;
            border-color: {input_config["border"]} !important;
            box-shadow: none !important;
            outline: none !important;
        }}

        /* Actual input element */
        .st-key-{container_key} input {{
            background: transparent !important;
            color: {input_config["text"]} !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            font-family: "JetBrains Mono", monospace !important;
            font-size: 1rem !important;
        }}

        .st-key-{container_key} input::placeholder {{
            color: {input_config["placeholder"]} !important;
            opacity: 1 !important;
        }}

        /* Keep the input calm on hover */
        .st-key-{container_key}
        div[data-baseweb="input"]:hover {{
            border-color: {input_config["border"]} !important;
            box-shadow: none !important;
        }}

        /* Disabled state */
        .st-key-{container_key}
        div[data-baseweb="input"]:has(input:disabled) {{
            background: {input_config["disabled_background"]} !important;
            border-color: {input_config["disabled_border"]} !important;
            box-shadow: none !important;
        }}

        .st-key-{container_key} input:disabled {{
            color: {input_config["disabled_text"]} !important;
        }}

        /* Error state */
        .st-key-{container_key}.documind-input-error
        div[data-baseweb="input"] {{
            border-color: {input_config["error_border"]} !important;
        }}

        .st-key-{container_key} .documind-input-help {{
            margin-top: 6px;
            color: {COLORS["text_muted"]};
            font-family: "JetBrains Mono", monospace;
            font-size: 0.75rem;
        }}

        .st-key-{container_key} .documind-input-error-text {{
            margin-top: 6px;
            color: {input_config["error_text"]};
            font-family: "JetBrains Mono", monospace;
            font-size: 0.75rem;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key=container_key):
        value = st.text_input(
            label,
            placeholder=placeholder,
            key=key,
        )

        if error:
            st.markdown(
                f'<div class="documind-input-error-text">{error}</div>',
                unsafe_allow_html=True,
            )
        elif help_text:
            st.markdown(
                f'<div class="documind-input-help">{help_text}</div>',
                unsafe_allow_html=True,
            )

    return value


def render_answer_display(
    answer: str,
    sources: list | None = None,
) -> None:
    """Render an AI-generated answer with an animated gradient border."""

    answer_config = INPUTS["answer"]

    st.markdown(
        f"""
        <style>
        @keyframes documind-answer-gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}

        .documind-answer-wrapper {{
            position: relative;
            padding: 1px;
            border-radius: {INPUTS["radius"]};
            background: {answer_config["gradient"]};
            background-size: 300% 300%;
            animation:
                documind-answer-gradient
                {answer_config["animation_duration"]}
                ease
                infinite;
            box-shadow:
                0 0 12px rgba(137, 39, 221, 0.18),
                0 0 24px rgba(255, 45, 85, 0.08);
        }}

        .documind-answer-content {{
            background: {answer_config["background"]};
            border-radius: calc({INPUTS["radius"]} - 1px);
            padding: 24px;
            color: {COLORS["text_primary"]};
            font-family: "JetBrains Mono", monospace;
            line-height: 1.7;
        }}

        .documind-answer-label {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
            color: {COLORS["text_primary"]};
            font-family: "JetBrains Mono", monospace;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .documind-answer-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: {COLORS["purple"]};
            box-shadow: 0 0 8px {COLORS["purple"]};
        }}

        .documind-answer-text {{
            color: {COLORS["text_primary"]};
            font-family: "JetBrains Mono", monospace;
            font-size: 0.95rem;
            line-height: 1.75;
        }}
        </style>

        <div class="documind-answer-wrapper">
            <div class="documind-answer-content">
                <div class="documind-answer-label">
                    <span>Answer</span>
                    <span class="documind-answer-dot"></span>
                </div>
                <div class="documind-answer-text">
                    {answer}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if sources:
        st.markdown(
            f"""
            <div style="
                margin-top: 16px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
                color: {COLORS["text_muted"]};
            ">
                Sources
            </div>
            """,
            unsafe_allow_html=True,
        )

        for index, source in enumerate(sources, start=1):
            st.caption(f"{index}. {source}")


def render_document_dropzone(
    label: str = "Upload Documents",
    key: str = "document_upload",
):
    """Render the DocuMind dotted PDF document upload component."""

    dropzone = INPUTS["dropzone"]

    container_key = _safe_key(
        f"documind-dropzone-{key}"
    )

    st.markdown(
        f"""
        <style>

        /* =====================================================
           DOCUMENT DROPZONE — UI-05
           ===================================================== */

        .st-key-{container_key} {{
            width: 100%;
        }}

        .st-key-{container_key}
        [data-testid="stFileUploader"] {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
        }}

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzone"] {{
            background: {dropzone["background"]} !important;
            border: 1px dashed {dropzone["border"]} !important;
            border-radius: {INPUTS["radius"]} !important;
            padding: 48px 32px !important;
            box-shadow: none !important;
            transition:
                border-color 200ms ease,
                background 200ms ease;
        }}

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzone"]:hover {{
            background: {dropzone["background"]} !important;
            border-color: {dropzone["hover_border"]} !important;
            box-shadow: none !important;
        }}

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzoneInstructions"] {{
            color: {dropzone["text"]} !important;
            font-family: "JetBrains Mono", monospace !important;
        }}

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzoneInstructions"] span {{
            color: {dropzone["secondary_text"]} !important;
        }}

        .st-key-{container_key} button {{
            font-family: "JetBrains Mono", monospace !important;
            box-shadow: none !important;
        }}

        .st-key-{container_key} small {{
            color: {dropzone["muted_text"]} !important;
            font-family: "JetBrains Mono", monospace !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key=container_key):
        return st.file_uploader(
            label,
            type=["pdf"],
            key=key,
            help="Maximum file size: 50MB",
            label_visibility="collapsed",
        )


def _pdf_icon_html(icon_path: str) -> str:
    """Return the approved PDF icon as an embedded image."""

    path = Path(icon_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF icon asset not found: {icon_path}"
        )

    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")

    return (
        f'<img src="data:image/png;base64,{encoded}" '
        f'alt="PDF" '
        f'style="'
        f'width:{DOCUMENT_CARD["icon_size"]};'
        f'height:{DOCUMENT_CARD["icon_size"]};'
        f'object-fit:contain;'
        f'display:block;'
        f'">'
    )


def render_document_card(
    filename: str,
    pages: int,
    file_size: str,
    uploaded_at: str,
    status: str = "ready",
    icon_path: str = "static/icons/PDF-visual.png",
    key: str | None = None,
    pdf_bytes: bytes | None = None,
) -> dict[str, bool]:
    """
    Render the reusable DocuMind document card.

    The entire visual card, divider, menu, and action row
    remain inside one Streamlit container.
    """

    if status not in {"ready", "processing"}:
        raise ValueError(
            "Document status must be 'ready' or 'processing'."
        )

    safe_key = _safe_key(
        f"document-card-{key or filename}"
    )

    if pdf_bytes is None:
        candidate_path = Path("data/uploads") / filename
        if candidate_path.exists():
            try:
                pdf_bytes = candidate_path.read_bytes()
            except OSError:
                pdf_bytes = None

    icon_html = _pdf_icon_html(icon_path)

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    if status == "ready":
        status_html = """
            <div class="document-card-status">

                <span class="document-status-badge document-status-ready">
                    <span class="document-status-dot"></span>
                    Indexed
                </span>

                <span class="document-status-badge document-status-ready">
                    <span class="document-status-dot"></span>
                    Ready for questions
                </span>

            </div>
        """

    else:
        status_html = """
            <div class="document-card-status">

                <span class="document-status-badge document-status-processing">
                    <span class="document-processing-dot"></span>
                    Processing...
                </span>

            </div>
        """

    # ---------------------------------------------------------
    # CARD CSS
    # ---------------------------------------------------------

    card_css = f"""
    <style>

        /* =====================================================
           CARD SHELL
           ===================================================== */

        .st-key-{safe_key} {{
            width: 100%;
            box-sizing: border-box;

            background: {DOCUMENT_CARD["background"]} !important;
            border: 1px solid #28222E !important;
            border-radius: {DOCUMENT_CARD["radius"]};

            padding: 24px 24px 14px 24px;

            position: relative !important;
            overflow: visible !important;
        }}


        /* =====================================================
           MAIN DOCUMENT AREA
           ===================================================== */

        .st-key-{safe_key} .document-card-main {{
            width: 100%;

            display: flex;
            align-items: flex-start;

            gap: 20px;

            box-sizing: border-box;

            padding-right: 44px;
        }}


        /* =====================================================
           PDF ICON
           ===================================================== */

        .st-key-{safe_key} .document-card-icon {{
            flex: 0 0 {DOCUMENT_CARD["icon_size"]};

            width: {DOCUMENT_CARD["icon_size"]};
            height: {DOCUMENT_CARD["icon_size"]};
        }}

        .st-key-{safe_key} .document-card-icon img {{
            width: 100%;
            height: 100%;

            display: block;
            object-fit: contain;
        }}


        /* =====================================================
           CONTENT
           ===================================================== */

        .st-key-{safe_key} .document-card-content {{
            flex: 1;
            min-width: 0;
        }}


        /* =====================================================
           TITLE
           ===================================================== */

        .st-key-{safe_key} .document-card-title {{
            color: {COLORS["text_primary"]};

            font-family: "JetBrains Mono", monospace;
            font-size: 1rem;
            font-weight: 600;

            line-height: 1.4;

            margin: 1px 0 8px 0;

            overflow-wrap: anywhere;
        }}


        /* =====================================================
           METADATA
           ===================================================== */

        .st-key-{safe_key} .document-card-meta {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;

            gap: 8px;

            color: {DOCUMENT_CARD["metadata_color"]};

            font-family: "JetBrains Mono", monospace;
            font-size: 0.76rem;

            line-height: 1.5;
        }}

        .st-key-{safe_key} .document-meta-dot {{
            color: {COLORS["purple"]};

            font-size: 0.9rem;
            font-weight: 700;
        }}


        /* =====================================================
           STATUS BADGES
           ===================================================== */

        .st-key-{safe_key} .document-card-status {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;

            gap: 10px;

            margin-top: 12px;
        }}

        .st-key-{safe_key} .document-status-badge {{
            display: inline-flex;
            align-items: center;

            gap: 7px;

            padding: 6px 12px;

            border-radius: 999px;

            font-family: "JetBrains Mono", monospace;
            font-size: 0.72rem;
            font-weight: 500;

            line-height: 1;
        }}

        .st-key-{safe_key} .document-status-ready {{
            color: {COLORS["success"]};

            background: rgba(121, 181, 138, 0.08);

            border: 1px solid rgba(121, 181, 138, 0.28);
        }}

        .st-key-{safe_key} .document-status-dot {{
            width: 7px;
            height: 7px;

            flex: 0 0 7px;

            border-radius: 50%;

            background: {COLORS["success"]};

            box-shadow:
                0 0 6px rgba(121, 181, 138, 0.5);
        }}

        .st-key-{safe_key} .document-status-processing {{
            color: {COLORS["purple"]};

            background: rgba(124, 58, 237, 0.08);

            border: 1px solid rgba(124, 58, 237, 0.32);
        }}

        .st-key-{safe_key} .document-processing-dot {{
            width: 7px;
            height: 7px;

            flex: 0 0 7px;

            border-radius: 50%;

            border: 1px solid {COLORS["purple"]};

            background: transparent;

            animation:
                document-processing-pulse
                1.4s ease-in-out
                infinite;
        }}

        @keyframes document-processing-pulse {{

            0%, 100% {{
                opacity: 0.45;
            }}

            50% {{
                opacity: 1;
            }}

        }}


        /* =====================================================
           THREE DOT POPOVER POSITIONING & ARROW REMOVAL
           ===================================================== */

        .st-key-{safe_key}-popover,
        .st-key-{safe_key} .st-key-{safe_key}-popover {{
            position: absolute !important;
            top: 16px !important;
            right: 18px !important;
            width: 28px !important;
            height: 28px !important;
            min-width: 28px !important;
            max-width: 28px !important;
            min-height: 28px !important;
            max-height: 28px !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 25 !important;
        }}

        .st-key-{safe_key}-popover [data-testid="stPopover"],
        .st-key-{safe_key}-popover [data-testid="stPopover"] > div,
        .st-key-{safe_key}-popover [data-testid="stPopoverButton"],
        .st-key-{safe_key}-popover button {{
            position: relative !important;
            width: 28px !important;
            min-width: 28px !important;
            max-width: 28px !important;
            height: 28px !important;
            min-height: 28px !important;
            max-height: 28px !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
        }}

        /* Completely hide the arrow icon */
        .st-key-{safe_key}-popover svg,
        .st-key-{safe_key}-popover [data-testid="stIcon"],
        .st-key-{safe_key}-popover [data-testid="stPopoverButton"] svg,
        .st-key-{safe_key}-popover button svg,
        .st-key-{safe_key}-popover button span:last-child:not(:only-child) {{
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            visibility: hidden !important;
        }}

        .st-key-{safe_key}-popover button p,
        .st-key-{safe_key}-popover button span {{
            font-size: 1.35rem !important;
            line-height: 1 !important;
            color: #77717B !important;
            margin: 0 !important;
            padding: 0 !important;
            font-weight: 700 !important;
            letter-spacing: 0 !important;
        }}

        .st-key-{safe_key}-popover button:hover p,
        .st-key-{safe_key}-popover button:hover span {{
            color: #F5F2F6 !important;
            background: rgba(255, 255, 255, 0.08) !important;
            border-radius: 6px !important;
        }}


        /* =====================================================
           DIVIDER
           ===================================================== */

        .st-key-{safe_key} .document-card-divider {{
            width: 100%;
            height: 1px;

            background: {DOCUMENT_CARD["divider"]};

            margin: 16px 0 0 0 !important;
            padding: 0 !important;
        }}


        /* =====================================================
           REMOVE STREAMLIT VERTICAL GAPS
           ===================================================== */

        div.st-key-{safe_key},
        .st-key-{safe_key},
        .st-key-{safe_key} [data-testid="stVerticalBlock"],
        .st-key-{safe_key} [data-testid="stVerticalBlockBorderWrapper"] {{
            gap: 0 !important;
        }}

        .st-key-{safe_key} [data-testid="stElementContainer"] {{
            margin: 0 !important;
            padding: 0 !important;
        }}


        /* =====================================================
           ACTION ROW
           ===================================================== */

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] {{
            width: 100% !important;

            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;

            margin-top: 10px !important;
            margin-bottom: 0 !important;
            padding: 0 !important;

            gap: 0 !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div {{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div:first-child {{
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;

            width: auto !important;
            flex: 0 0 auto !important;

            padding: 0 !important;
            margin: 0 !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div:last-child {{
            display: flex !important;
            align-items: center !important;
            justify-content: flex-end !important;

            width: auto !important;
            flex: 0 0 auto !important;
            margin-left: auto !important;

            padding: 0 !important;
            margin: 0 !important;
        }}


        /* =====================================================
           COMPACT BUTTONS FOR DOCUMENT CARD
           ===================================================== */

        .st-key-{safe_key} button {{
            min-height: 28px !important;
            height: 28px !important;
            padding: 0 4px !important;
            font-size: 0.78rem !important;
            line-height: 1 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .st-key-{safe_key} button::before {{
            width: 14px !important;
            height: 14px !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div:first-child button {{
            color: {COLORS["purple"]} !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div:first-child button:hover {{
            color: {COLORS["purple_hover"]} !important;
            background: transparent !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div:last-child button {{
            color: {COLORS["coral"]} !important;
        }}

        .st-key-{safe_key} [data-testid="stHorizontalBlock"] > div:last-child button:hover {{
            color: {COLORS["coral_hover"]} !important;
            background: transparent !important;
        }}

    </style>
    """

    # ---------------------------------------------------------
    # CARD CONTENT
    # ---------------------------------------------------------

    card_html = f"""
        <div class="document-card-main">

            <div class="document-card-icon">
                {icon_html}
            </div>

            <div class="document-card-content">

                <div class="document-card-title">
                    {filename}
                </div>

                <div class="document-card-meta">

                    <span>
                        {pages} {'page' if pages == 1 else 'pages'}
                    </span>

                    <span class="document-meta-dot">
                        •
                    </span>

                    <span>
                        {file_size}
                    </span>

                    <span class="document-meta-dot">
                        •
                    </span>

                    <span>
                        Uploaded {uploaded_at}
                    </span>

                </div>

                {status_html}

            </div>

        </div>

        <div class="document-card-divider"></div>
    """

    # ---------------------------------------------------------
    # ONE CARD CONTAINER
    # ---------------------------------------------------------

    with st.container(key=safe_key):

        st.html(card_css)
        st.html(card_html)

        # 3-dots Popover Menu (positioned in top-right corner, no arrow, clean labels)
        details_clicked = False
        menu_delete_clicked = False
        with st.popover("⋮", key=f"{safe_key}-popover"):
            if pdf_bytes:
                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    key=f"{safe_key}-download",
                    use_container_width=True,
                )
            else:
                st.button(
                    "Download PDF",
                    key=f"{safe_key}-dl-disabled",
                    disabled=True,
                    use_container_width=True,
                )
            details_clicked = st.button(
                "File Details",
                key=f"{safe_key}-details",
                use_container_width=True,
            )
            menu_delete_clicked = st.button(
                "Delete Document",
                key=f"{safe_key}-menu-delete",
                use_container_width=True,
            )

        action_left, action_right = st.columns(
            [1, 1],
            gap="small",
        )

        with action_left:
            view_text_clicked = render_button(
                "View Text",
                variant="secondary",
                key=f"{safe_key}-view-text",
            )

        with action_right:
            delete_clicked = render_button(
                "Delete",
                variant="danger",
                key=f"{safe_key}-delete",
                icon=True,
            )

    return {
        "view_text": view_text_clicked,
        "delete": delete_clicked or menu_delete_clicked,
        "view_details": details_clicked,
    }

def render_document_tile(
    icon_path: str = "static/icons/PDF-visual.png",
    key: str | None = None,
) -> None:
    """
    Render the reusable empty document visual tile.

    The tile intentionally contains no text or actions.
    The consuming page provides its own content around the
    reusable visual treatment.
    """

    safe_key = _safe_key(
        f"document-tile-{key or 'default'}"
    )

    icon_html = _pdf_icon_html(icon_path)

    tile_css = dedent(
        f"""
        <style>

        .st-key-{safe_key} {{
            width: 100%;
        }}

        .st-key-{safe_key} .document-tile {{
            width: 100%;
            min-height: 150px;
            box-sizing: border-box;

            display: flex;
            align-items: center;

            background: {DOCUMENT_CARD["background"]};
            border: 1px solid {DOCUMENT_CARD["border"]};
            border-radius: {DOCUMENT_CARD["radius"]};

            padding: 24px;
            position: relative;
        }}

        .st-key-{safe_key} .document-tile-icon {{
            width: {DOCUMENT_CARD["icon_size"]};
            height: {DOCUMENT_CARD["icon_size"]};

            flex: 0 0 {DOCUMENT_CARD["icon_size"]};
        }}

        .st-key-{safe_key} .document-tile-menu {{
            position: absolute;
            top: 14px;
            right: 16px;

            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;

            user-select: none;
            pointer-events: none;
        }}

        .st-key-{safe_key} .document-tile-menu-dot {{
            display: block;
            width: 3.5px;
            height: 3.5px;
            border-radius: 50%;
            background: {COLORS["text_secondary"]};
        }}

        </style>
        """
    )

    tile_html = dedent(
        f"""
        <div class="document-tile">
            <div class="document-tile-icon">
                {icon_html}
            </div>

            <div class="document-tile-menu">
                <span class="document-tile-menu-dot"></span>
                <span class="document-tile-menu-dot"></span>
                <span class="document-tile-menu-dot"></span>
            </div>
        </div>
        """
    )

    with st.container(key=safe_key):
        st.html(tile_css + tile_html)


def render_canvas_background(
    image_path: str = "static/background.png",
    key: str = "global-canvas",
) -> None:
    """
    Render the reusable DocuMind canvas background using the provided
    background image asset.
    """
    safe_key = _safe_key(f"documind-canvas-{key}")
    path = Path(image_path)
    if not path.exists():
        return

    bg_b64 = base64.b64encode(path.read_bytes()).decode("utf-8")

    canvas_css = f"""
    <style>
    .stApp {{
        background-color: {COLORS["background"]};
        color: {COLORS["text_primary"]};
    }}
    [data-testid="stMain"],
    .stMain,
    section.main {{
        background-color: {COLORS["background"]} !important;
        background-image: url("data:image/png;base64,{bg_b64}") !important;
        background-size: 100% auto !important;
        background-position: top right !important;
        background-repeat: no-repeat !important;
        background-attachment: local !important;
    }}
    </style>
    """
    st.html(canvas_css)