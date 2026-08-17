"""Reusable DocuMind UI components."""

import re

import streamlit as st

from app.ui.theme import BUTTONS, COLORS, INPUTS


def _safe_key(value: str) -> str:
    """Convert a component key into a valid Streamlit container key."""
    return re.sub(r"[^a-zA-Z0-9_-]", "-", value)


def render_button(
    label: str,
    variant: str = "primary",
    key: str | None = None,
    disabled: bool = False,
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

    st.markdown(
        f"""
        <style>
        .st-key-{container_key} button {{
            width: auto;
            min-height: {BUTTONS["height"]};
            padding: 0 {BUTTONS["padding_x"]};
            border-radius: {BUTTONS["radius"]};

            font-family: "JetBrains Mono", monospace;
            font-size: {BUTTONS["font_size"]};
            font-weight: {BUTTONS["font_weight"]};

            background: {button["background"]};
            color: {button["text"]};
            border: 1px solid {button["border"]};

            box-shadow: none;
            transition: {BUTTONS["transition"]};
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
            cursor: not-allowed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key=container_key):
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

            box-shadow:
                0 0 8px {COLORS["purple"]};
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

        /*
         * Streamlit creates an outer file-uploader container
         * around the actual dropzone.
         *
         * The outer container must NOT have its own border.
         */

        .st-key-{container_key}
        [data-testid="stFileUploader"] {{
            background: transparent !important;

            border: none !important;

            padding: 0 !important;

            box-shadow: none !important;
        }}

        /*
         * This is the ONLY border in the component.
         */

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

        /*
         * Calm hover state.
         * Still only ONE purple dotted border.
         */

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzone"]:hover {{
            background: {dropzone["background"]} !important;

            border-color: {dropzone["hover_border"]} !important;

            box-shadow: none !important;
        }}

        /*
         * Upload instructions
         */

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzoneInstructions"] {{
            color: {dropzone["text"]} !important;

            font-family: "JetBrains Mono", monospace !important;
        }}

        .st-key-{container_key}
        [data-testid="stFileUploaderDropzoneInstructions"] span {{
            color: {dropzone["secondary_text"]} !important;
        }}

        /*
         * Native Streamlit upload button.
         * Keep its functionality while preventing it from
         * introducing another visual border treatment.
         */

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