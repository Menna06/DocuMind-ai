"""Reusable DocuMind UI components."""

import re

import streamlit as st

from app.ui.theme import BUTTONS


def _safe_key(value: str) -> str:
    """Convert a button key into a valid Streamlit container key."""
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