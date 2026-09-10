import base64
from pathlib import Path

import streamlit as st

from app.ui.theme import COLORS, LAYOUT, RADIUS, TYPOGRAPHY


def load_image_base64(image_name: str) -> str:
    """Return base64-encoded image string for an asset in static/ or given path."""
    path = Path(image_name)
    if not path.exists():
        static_dir = Path(__file__).resolve().parent.parent.parent / "static"
        path = static_dir / image_name
    if not path.exists():
        path = Path("static") / image_name
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _load_background_image_base64(
    image_path: str = "static/background.png",
) -> str:
    """Return the base64-encoded background image asset."""
    return load_image_base64(image_path)


def apply_global_styles() -> None:
    """Apply the shared DocuMind visual system."""

    bg_b64 = _load_background_image_base64()

    sidebar_bg_b64 = (
        load_image_base64("SidebarVisual.PNG")
        or load_image_base64("SidebarVisual.png")
    )

    st.markdown(
        f"""
        <style>

        /* =========================================================
           GLOBAL CANVAS
           ========================================================= */

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

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {COLORS["background"]} !important;
            border-color: #28222E !important;
        }}

        div[data-testid="stAlert"] {{
            background-color: {COLORS["background"]} !important;
            border: 1px solid #28222E !important;
        }}

        .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container,
        .stAppViewContainer .main .block-container {{
            max-width: {LAYOUT["content_max_width"]} !important;
            padding-top: 0.75rem !important;
            padding-bottom: 4rem !important;
            padding-left: {LAYOUT["content_padding_x"]} !important;
            padding-right: {LAYOUT["content_padding_x"]} !important;
            margin: 0 auto !important;
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
   SIDEBAR — UI-08
   ========================================================= */



/* App View Container & Header transparent fallbacks to prevent any white flash */
[data-testid="stAppViewContainer"],
.stAppViewContainer,
[data-testid="stToolbar"],
.stAppHeader {{
    background-color: transparent !important;
    background: transparent !important;
}}

header[data-testid="stHeader"],
[data-testid="stHeader"] {{
    background-color: transparent !important;
    background: transparent !important;
    height: 2.2rem !important;
    min-height: 2.2rem !important;
}}

/* Sidebar container - default dark background (active across all states and transitions) */
section[data-testid="stSidebar"],
section.stSidebar,
[data-testid="stSidebar"] {{
    background-color: {COLORS["background"]} !important;
    background-image: url("data:image/png;base64,{sidebar_bg_b64}") !important;
    background-size: 100% 100% !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
}}

/* Force Streamlit sidebar container width & background when EXPANDED */
section[data-testid="stSidebar"][aria-expanded="true"],
section.stSidebar[aria-expanded="true"],
[data-testid="stSidebar"][aria-expanded="true"] {{
    width: {LAYOUT["sidebar_width"]} !important;
    min-width: {LAYOUT["sidebar_width"]} !important;
    max-width: {LAYOUT["sidebar_width"]} !important;
    flex-basis: {LAYOUT["sidebar_width"]} !important;
    flex-shrink: 0 !important;
    margin-left: 0 !important;
    transform: translateX(0) !important;

    background-color: {COLORS["background"]} !important;
    background-image: url("data:image/png;base64,{sidebar_bg_b64}") !important;

    background-size: 100% 100% !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;

    border-right: 1px solid {COLORS["border_subtle"]} !important;
    transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1),
                margin-left 300ms cubic-bezier(0.4, 0, 0.2, 1),
                width 300ms cubic-bezier(0.4, 0, 0.2, 1),
                min-width 300ms cubic-bezier(0.4, 0, 0.2, 1),
                max-width 300ms cubic-bezier(0.4, 0, 0.2, 1),
                flex-basis 300ms cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

/* Sidebar when COLLAPSED */
section[data-testid="stSidebar"][aria-expanded="false"],
section.stSidebar[aria-expanded="false"],
[data-testid="stSidebar"][aria-expanded="false"] {{
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    flex-basis: 0 !important;
    margin-left: 0 !important;
    padding: 0 !important;
    transform: translateX(-100%) !important;
    border-right: none !important;
    overflow: hidden !important;
    pointer-events: none !important;
    background-color: {COLORS["background"]} !important;
    background-image: url("data:image/png;base64,{sidebar_bg_b64}") !important;
    background-size: 100% 100% !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1),
                width 300ms cubic-bezier(0.4, 0, 0.2, 1),
                min-width 300ms cubic-bezier(0.4, 0, 0.2, 1),
                max-width 300ms cubic-bezier(0.4, 0, 0.2, 1),
                flex-basis 300ms cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

/* Smooth transition for main content area when sidebar opens/closes */
.main,
section.main {{
    margin-left: 0 !important;
    transition: margin-left 300ms cubic-bezier(0.4, 0, 0.2, 1),
                padding-left 300ms cubic-bezier(0.4, 0, 0.2, 1),
                width 300ms cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

/* =========================================================
   SIDEBAR TOGGLE BUTTONS (COLLAPSE & EXPAND)
   ========================================================= */

/* Sidebar Collapse Button (Inside open sidebar header, next to DOCUMIND) */
[data-testid="stSidebarCollapseButton"] {{
    position: absolute !important;
    top: 35px !important;
    right: 10px !important;
    z-index: 9999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

[data-testid="stSidebarCollapseButton"] button,
button[data-testid="stSidebarCollapseButton"] {{
    width: 28px !important;
    height: 28px !important;
    min-width: 28px !important;
    min-height: 28px !important;
    padding: 0 !important;
    border-radius: 6px !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #B8B1BA !important;
    font-size: 0 !important;
    line-height: 0 !important;
    text-indent: -9999px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    position: relative !important;
    transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease !important;
}}

[data-testid="stSidebarCollapseButton"] button:hover,
button[data-testid="stSidebarCollapseButton"]:hover {{
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
    color: #FFFFFF !important;
}}

[data-testid="stSidebarCollapseButton"] button *,
button[data-testid="stSidebarCollapseButton"] * {{
    display: none !important;
    visibility: hidden !important;
    font-size: 0 !important;
    line-height: 0 !important;
    color: transparent !important;
    opacity: 0 !important;
}}

/* Custom SVG icon with inward arrow */
[data-testid="stSidebarCollapseButton"] button::before,
button[data-testid="stSidebarCollapseButton"]::before {{
    content: "" !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    text-indent: 0 !important;
    width: 17px !important;
    height: 17px !important;
    background-color: currentColor !important;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='18' height='18' rx='4'/%3E%3Cline x1='9' y1='3' x2='9' y2='21'/%3E%3Cpath d='M16 9l-3 3 3 3'/%3E%3C/svg%3E") !important;
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='18' height='18' rx='4'/%3E%3Cline x1='9' y1='3' x2='9' y2='21'/%3E%3Cpath d='M16 9l-3 3 3 3'/%3E%3C/svg%3E") !important;
    -webkit-mask-size: contain !important;
    mask-size: contain !important;
    -webkit-mask-repeat: no-repeat !important;
    mask-repeat: no-repeat !important;
    -webkit-mask-position: center !important;
    mask-position: center !important;
}}

/* Tooltip: "Close sidebar" */
[data-testid="stSidebarCollapseButton"] button::after,
button[data-testid="stSidebarCollapseButton"]::after {{
    content: "Close sidebar" !important;
    position: absolute !important;
    top: calc(100% + 8px) !important;
    right: 0 !important;
    background: #1C1A20 !important;
    color: #FFFFFF !important;
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    line-height: 1.35 !important;
    text-indent: 0 !important;
    padding: 6px 13px !important;
    border-radius: 9999px !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6) !important;
    white-space: nowrap !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transition: opacity 150ms ease, visibility 150ms ease !important;
    z-index: 10000 !important;
}}

[data-testid="stSidebarCollapseButton"] button:hover::after,
button[data-testid="stSidebarCollapseButton"]:hover::after {{
    opacity: 1 !important;
    visibility: visible !important;
}}

/* Sidebar Expand Button (When sidebar is collapsed, on the main web page) */
[data-testid="stExpandSidebarButton"],
button[data-testid="stExpandSidebarButton"] {{
    position: fixed !important;
    top: 35px !important;
    left: 18px !important;
    z-index: 99999 !important;
    width: 28px !important;
    height: 28px !important;
    min-width: 28px !important;
    min-height: 28px !important;
    padding: 0 !important;
    border-radius: 6px !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #B8B1BA !important;
    font-size: 0 !important;
    line-height: 0 !important;
    text-indent: -9999px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease !important;
}}

[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stExpandSidebarButton"]:hover {{
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
    color: #FFFFFF !important;
}}

[data-testid="stExpandSidebarButton"] *,
button[data-testid="stExpandSidebarButton"] * {{
    display: none !important;
    visibility: hidden !important;
    font-size: 0 !important;
    line-height: 0 !important;
    color: transparent !important;
    opacity: 0 !important;
}}

/* Custom SVG icon with outward arrow */
[data-testid="stExpandSidebarButton"]::before,
button[data-testid="stExpandSidebarButton"]::before {{
    content: "" !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    text-indent: 0 !important;
    width: 17px !important;
    height: 17px !important;
    background-color: currentColor !important;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='18' height='18' rx='4'/%3E%3Cline x1='9' y1='3' x2='9' y2='21'/%3E%3Cpath d='M14 9l3 3-3 3'/%3E%3C/svg%3E") !important;
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='18' height='18' rx='4'/%3E%3Cline x1='9' y1='3' x2='9' y2='21'/%3E%3Cpath d='M14 9l3 3-3 3'/%3E%3C/svg%3E") !important;
    -webkit-mask-size: contain !important;
    mask-size: contain !important;
    -webkit-mask-repeat: no-repeat !important;
    mask-repeat: no-repeat !important;
    -webkit-mask-position: center !important;
    mask-position: center !important;
}}

/* Tooltip: "Open sidebar" */
[data-testid="stExpandSidebarButton"]::after,
button[data-testid="stExpandSidebarButton"]::after {{
    content: "Open sidebar" !important;
    position: absolute !important;
    top: calc(100% + 8px) !important;
    left: 0 !important;
    background: #1C1A20 !important;
    color: #FFFFFF !important;
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    line-height: 1.35 !important;
    text-indent: 0 !important;
    padding: 6px 13px !important;
    border-radius: 9999px !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6) !important;
    white-space: nowrap !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transition: opacity 150ms ease, visibility 150ms ease !important;
    z-index: 100000 !important;
}}

[data-testid="stExpandSidebarButton"]:hover::after,
button[data-testid="stExpandSidebarButton"]:hover::after {{
    opacity: 1 !important;
    visibility: visible !important;
}}

div[data-testid="stSidebarContent"],
div[data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] > div:first-child {{
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    background: transparent !important;
}}

/* Sidebar content positioning */
[data-testid="stSidebar"] .block-container,
[data-testid="stSidebarContent"] .block-container {{
    padding-top: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 0.5rem !important;

    display: flex !important;
    flex-direction: column !important;

    min-height: calc(100vh - 2rem) !important;
    box-sizing: border-box !important;

    position: relative !important;
}}

.sidebar-footer-brand {{
    position: fixed !important;
    left: 1rem !important;
   bottom: 10.5rem !important;
    z-index: 9999 !important;
    width: {LAYOUT["sidebar_width"]} !important;
    pointer-events: none !important;
}}

.sidebar-footer-title {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: {COLORS["text_primary"]} !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
}}

.sidebar-footer-subtitle {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 0.62rem !important;
    font-weight: 400 !important;
    color: {COLORS["text_muted"]} !important;
    margin-top: 0.3rem !important;
    line-height: 1.2 !important;
}}

/* =========================================================
   SIDEBAR CONTENT POSITIONING
   ========================================================= */

[data-testid="stSidebarContent"] {{
    padding-top: 0 !important;
}}

[data-testid="stSidebarUserContent"] {{
    padding-top: 0 !important;
}}

[data-testid="stSidebar"] .sidebar-brand {{
    margin-top: -3.0rem !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 8px !important;
}}

.sidebar-brand-logo {{
    width: 29px !important;
    height: 29px !important;
    min-width: 29px !important;
    object-fit: contain !important;
    display: block !important;
    flex-shrink: 0 !important;
}}

.sidebar-brand-title {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: {COLORS["text_primary"]} !important;
    letter-spacing: -0.03em !important;
    line-height: 1 !important;
    white-space: nowrap !important;
}}

.sidebar-brand-subtitle {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 0.72rem;
    color: {COLORS["text_muted"]};
    margin-top: 0.15rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}}

       .sidebar-section {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    font-size: 0.68rem;
    color: {COLORS["text_muted"]};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    margin: 2.5rem 0 0.65rem 0;
}}

.sidebar-system-status {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
    color: #77717B;
    font-size: 0.78rem;
    line-height: 1.8;
}}

.sidebar-system-status div {{
    font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
}}








        /* ============================================================
           WORKSPACE NAVIGATION — UI-08
           ============================================================ */

        /* Workspace container */
        [data-testid="stSidebar"] .st-key-workspace_nav {{
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        [data-testid="stSidebar"] .st-key-workspace_nav > div {{
            gap: 6px !important;
        }}

        /* Button wrappers */
        [data-testid="stSidebar"] .st-key-workspace_documents,
        [data-testid="stSidebar"] .st-key-workspace_ask,
        [data-testid="stSidebar"] .st-key-workspace_upload {{
            width: 100% !important;
            max-width: 100% !important;
            min-width: 100% !important;

            margin: 0 !important;
            padding: 0 !important;

            box-sizing: border-box !important;
        }}

        /* Base button */
        [data-testid="stSidebar"] .st-key-workspace_documents button,
        [data-testid="stSidebar"] .st-key-workspace_ask button,
        [data-testid="stSidebar"] .st-key-workspace_upload button {{
            position: relative !important;

            width: 100% !important;
            max-width: 100% !important;
            min-width: 100% !important;

            height: 36px !important;
            min-height: 36px !important;
            max-height: 36px !important;

            box-sizing: border-box !important;

            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;

            padding: 0 32px 0 44px !important;
            margin: 0 !important;

            background: rgba(16, 14, 17, 0.35) !important;

            border: 1px solid {COLORS["border_default"]} !important;
            border-radius: {RADIUS["md"]} !important;

            color: {COLORS["text_secondary"]} !important;

            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.76rem !important;
            font-weight: 400 !important;
            line-height: 1 !important;

            text-align: left !important;

            box-shadow: none !important;

            transition:
                background 150ms ease,
                border-color 150ms ease,
                color 150ms ease !important;

            cursor: pointer !important;
        }}

        /* Force Streamlit's inner content left */
        [data-testid="stSidebar"] .st-key-workspace_documents button > div,
        [data-testid="stSidebar"] .st-key-workspace_ask button > div,
        [data-testid="stSidebar"] .st-key-workspace_upload button > div {{
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;

            width: 100% !important;
            flex: 1 1 auto !important;

            margin: 0 !important;
            padding: 0 !important;

            text-align: left !important;
        }}

        /* Button text */
        [data-testid="stSidebar"] .st-key-workspace_documents button p,
        [data-testid="stSidebar"] .st-key-workspace_ask button p,
        [data-testid="stSidebar"] .st-key-workspace_upload button p {{
            display: block !important;

            width: auto !important;

            margin: 0 !important;
            padding: 0 !important;

            color: inherit !important;

            font-family: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            line-height: 1 !important;

            white-space: nowrap !important;
            text-align: left !important;
        }}

        /* Remove Streamlit's own icon */
        [data-testid="stSidebar"] .st-key-workspace_documents button svg,
        [data-testid="stSidebar"] .st-key-workspace_ask button svg,
        [data-testid="stSidebar"] .st-key-workspace_upload button svg {{
            display: none !important;
        }}


        /* ============================================================
           DOCUMENTS ICON
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_documents button::before {{
            content: "" !important;

            position: absolute !important;
            left: 14px !important;
            top: 50% !important;

            width: 17px !important;
            height: 17px !important;

            transform: translateY(-50%) !important;

            background-color: {COLORS["text_secondary"]} !important;

            -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='8' y1='13' x2='16' y2='13'/%3E%3Cline x1='8' y1='17' x2='16' y2='17'/%3E%3C/svg%3E") center / contain no-repeat !important;

            mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='8' y1='13' x2='16' y2='13'/%3E%3Cline x1='8' y1='17' x2='16' y2='17'/%3E%3C/svg%3E") center / contain no-repeat !important;

            pointer-events: none !important;
        }}


        /* ============================================================
           ASK DOCUMIND ICON
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_ask button::before {{
            content: "" !important;

            position: absolute !important;
            left: 14px !important;
            top: 50% !important;

            width: 17px !important;
            height: 17px !important;

            transform: translateY(-50%) !important;

            background-color: {COLORS["text_secondary"]} !important;

            -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 15a3 3 0 0 1-3 3H9l-5 3v-3a3 3 0 0 1-2-3V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3z'/%3E%3Cline x1='7' y1='9' x2='17' y2='9'/%3E%3Cline x1='7' y1='13' x2='13' y2='13'/%3E%3C/svg%3E") center / contain no-repeat !important;

            mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 15a3 3 0 0 1-3 3H9l-5 3v-3a3 3 0 0 1-2-3V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3z'/%3E%3Cline x1='7' y1='9' x2='17' y2='9'/%3E%3Cline x1='7' y1='13' x2='13' y2='13'/%3E%3C/svg%3E") center / contain no-repeat !important;

            pointer-events: none !important;
        }}


        /* ============================================================
           UPLOAD ICON
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_upload button::before {{
            content: "+" !important;

            position: absolute !important;
            left: 14px !important;
            top: 50% !important;

            width: 17px !important;
            height: 17px !important;

            transform: translateY(-53%) !important;

            color: {COLORS["text_secondary"]} !important;

            font-family: Arial, sans-serif !important;
            font-size: 22px !important;
            font-weight: 300 !important;
            line-height: 17px !important;

            text-align: center !important;

            pointer-events: none !important;
        }}


        /* ============================================================
           HOVER
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_documents button:hover,
        [data-testid="stSidebar"] .st-key-workspace_ask button:hover,
        [data-testid="stSidebar"] .st-key-workspace_upload button:hover {{
            background: rgba(28, 24, 32, 0.42) !important;
            border-color: {COLORS["border_strong"]} !important;
            color: {COLORS["text_primary"]} !important;

            box-shadow: none !important;
        }}

        /* ============================================================
           ACTIVE PAGE
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_documents button[data-testid="stBaseButton-primary"],
        [data-testid="stSidebar"] .st-key-workspace_ask button[data-testid="stBaseButton-primary"] {{
            background: rgba(21, 18, 23, 0.55) !important;

            border-color: {COLORS["border_strong"]} !important;

            color: {COLORS["text_primary"]} !important;

            box-shadow:
                inset 2px 0 0 {COLORS["coral"]} !important;
        }}

        /* Active Documents / Ask DocuMind icons */

        [data-testid="stSidebar"] .st-key-workspace_documents button[data-testid="stBaseButton-primary"]::before,
        [data-testid="stSidebar"] .st-key-workspace_ask button[data-testid="stBaseButton-primary"]::before {{
            background-color: {COLORS["coral"]} !important;
        }}

        /* Active Documents / Ask DocuMind text */

        [data-testid="stSidebar"] .st-key-workspace_documents button[data-testid="stBaseButton-primary"] p,
        [data-testid="stSidebar"] .st-key-workspace_ask button[data-testid="stBaseButton-primary"] p {{
            color: {COLORS["text_primary"]} !important;
        }}

        /* Active Documents / Ask DocuMind indicator */

        [data-testid="stSidebar"] .st-key-workspace_documents button[data-testid="stBaseButton-primary"]::after,
        [data-testid="stSidebar"] .st-key-workspace_ask button[data-testid="stBaseButton-primary"]::after {{
            content: "" !important;

            position: absolute !important;
            right: 14px !important;
            top: 50% !important;

            width: 5px !important;
            height: 5px !important;

            transform: translateY(-50%) !important;

            border-radius: 50% !important;

            background: {COLORS["coral"]} !important;

            pointer-events: none !important;
        }}

                /* ============================================================
           UPLOAD ACTIVE STATE
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_upload button[data-testid="stBaseButton-primary"] {{
            background: rgba(16, 14, 17, 0.35) !important;

            border-color: {COLORS["border_default"]} !important;

            color: {COLORS["text_secondary"]} !important;

            box-shadow:
                inset 2px 0 0 {COLORS["coral"]} !important;
        }}

        /* Upload active icon */

        [data-testid="stSidebar"] .st-key-workspace_upload button[data-testid="stBaseButton-primary"]::before {{
            color: {COLORS["coral"]} !important;

            background-color: transparent !important;
        }}

        /* Upload active indicator */

        [data-testid="stSidebar"] .st-key-workspace_upload button[data-testid="stBaseButton-primary"]::after {{
            content: "" !important;

            position: absolute !important;
            right: 14px !important;
            top: 50% !important;

            width: 5px !important;
            height: 5px !important;

            transform: translateY(-50%) !important;

            border-radius: 50% !important;

            background: {COLORS["coral"]} !important;

            pointer-events: none !important;
        }}

        /* ============================================================
           ACTIVE BUTTON FOCUS / CLICK STATE
           ============================================================ */

        [data-testid="stSidebar"] .st-key-workspace_documents button[data-testid="stBaseButton-primary"]:focus,
        [data-testid="stSidebar"] .st-key-workspace_documents button[data-testid="stBaseButton-primary"]:active,
        [data-testid="stSidebar"] .st-key-workspace_ask button[data-testid="stBaseButton-primary"]:focus,
        [data-testid="stSidebar"] .st-key-workspace_ask button[data-testid="stBaseButton-primary"]:active {{
            background: rgba(21, 18, 23, 0.55) !important;

            border-color: {COLORS["border_strong"]} !important;

            color: {COLORS["text_primary"]} !important;

            box-shadow:
                inset 2px 0 0 {COLORS["coral"]} !important;
        }}

        [data-testid="stSidebar"] .st-key-workspace_upload button[data-testid="stBaseButton-primary"]:focus,
        [data-testid="stSidebar"] .st-key-workspace_upload button[data-testid="stBaseButton-primary"]:active {{
            background: rgba(16, 14, 17, 0.35) !important;

            border-color: {COLORS["border_default"]} !important;

            color: {COLORS["text_secondary"]} !important;

            box-shadow: none !important;
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
    background: #B026FF;
    box-shadow:
        0 0 4px #B026FF,
        0 0 8px rgba(176, 38, 255, 0.8),
        0 0 14px rgba(176, 38, 255, 0.45);
    margin-right: 6px;
    animation: documind-pulse-dot 2.4s infinite ease-in-out;
}}

       @keyframes documind-pulse-dot {{
    0%, 100% {{
        opacity: 0.7;
        box-shadow:
            0 0 4px #B026FF,
            0 0 8px rgba(176, 38, 255, 0.7),
            0 0 12px rgba(176, 38, 255, 0.35);
    }}
    50% {{
        opacity: 1;
        box-shadow:
            0 0 5px #B026FF,
            0 0 10px rgba(176, 38, 255, 0.9),
            0 0 18px rgba(176, 38, 255, 0.55);
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
           DOCUMENTS WEBPAGE — UI-09
           ========================================================= */

        /* Header typography */
        .documents-header {{
            margin-top: -1.5rem !important;
            margin-bottom: 2.35rem !important;
            padding-top: 0 !important;
        }}

        .documents-title {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: {COLORS["text_primary"]} !important;
            letter-spacing: -0.03em !important;
            margin: 0 0 0.35rem 0 !important;
            line-height: 1.2 !important;
        }}

        .documents-subtitle {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.85rem !important;
            color: {COLORS["text_muted"]} !important;
            margin: 0 !important;
            line-height: 1.5 !important;
        }}

        /* Action Bar Container & Row Alignment */
        .st-key-documents_action_bar,
        .st-key-documents_action_bar > div {{
            width: 100% !important;
            margin: 0 0 0.35rem 0 !important;
            padding: 0 !important;
        }}

        .st-key-documents_action_bar [data-testid="stHorizontalBlock"] {{
            display: flex !important;
            align-items: stretch !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            gap: 16px !important;
        }}

        .st-key-documents_action_bar [data-testid="stColumn"] {{
            display: flex !important;
            align-items: stretch !important;
            margin: 0 !important;
            padding: 0 !important;
            min-height: 42px !important;
            height: 42px !important;
        }}

        .st-key-documents_action_bar [data-testid="stColumn"] > div,
        .st-key-documents_action_bar [data-testid="stVerticalBlockBorderWrapper"],
        .st-key-documents_action_bar [data-testid="stVerticalBlock"] {{
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            margin: 0 !important;
            padding: 0 !important;
            gap: 0 !important;
            display: flex !important;
            align-items: stretch !important;
        }}

        .st-key-documents_search_box,
        .st-key-documents_upload_col {{
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: stretch !important;
        }}

        .st-key-documents_search_box [data-testid="stElementContainer"],
        .st-key-documents_upload_col [data-testid="stElementContainer"] {{
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: stretch !important;
        }}

        /* Search input reset */
        .st-key-documents_search_box [data-testid="stTextInput"] {{
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: stretch !important;
        }}

        .st-key-documents_search_box label {{
            display: none !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
            width: 0 !important;
        }}

        /* Strip intermediate wrappers */
        .st-key-documents_search_box [data-testid="stTextInput"] > div,
        .st-key-documents_search_box .react-aria-TextField,
        .st-key-documents_search_box [data-baseweb="base-input"],
        .st-key-documents_search_box [data-baseweb="input"] {{
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            display: flex !important;
            align-items: center !important;
        }}

        .st-key-documents_search_box [data-baseweb="base-input"]::before,
        .st-key-documents_search_box [data-baseweb="base-input"]::after,
        .st-key-documents_search_box [data-baseweb="input"]::before,
        .st-key-documents_search_box [data-baseweb="input"]::after,
        .st-key-documents_search_box [data-testid="stTextInputIcon"] {{
            content: none !important;
            display: none !important;
        }}

        /* Completely eliminate "Press Enter to apply" overlay and instructions */
        .st-key-documents_search_box [data-testid="InputInstructions"],
        .st-key-documents_search_box [data-testid="stTextInputInstructions"],
        .st-key-documents_search_box .stTextInputInstructions,
        .st-key-documents_search_box [data-testid="stTextInputRootElement"] [data-testid="InputInstructions"],
        [data-testid="InputInstructions"],
        [data-testid="stTextInputInstructions"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            pointer-events: none !important;
        }}

        /* EXACT SHELL: Applied strictly to the root container */
        .st-key-documents_search_box [data-testid="stTextInputRootElement"] {{
            background: {COLORS["background"]} !important;
            border: 1px solid #28222E !important;
            border-radius: 10px !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            box-sizing: border-box !important;
            display: flex !important;
            align-items: center !important;
            padding: 0 14px 0 14px !important;
            margin: 0 !important;
            width: 100% !important;
            position: relative !important;
            transition: border-color 150ms ease, box-shadow 150ms ease !important;
        }}

        .st-key-documents_search_box [data-testid="stTextInputRootElement"]:hover {{
            border-color: #403744 !important;
        }}

        .st-key-documents_search_box [data-testid="stTextInputRootElement"]:focus-within {{
            border-color: {COLORS["purple"]} !important;
            box-shadow: 0 0 0 1px {COLORS["purple"]} !important;
            outline: none !important;
        }}

        /* Reset inner BaseWeb input container */
        .st-key-documents_search_box [data-baseweb="input"],
        .st-key-documents_search_box [data-baseweb="base-input"] {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
        }}

        /* Exactly one magnifying glass on the root container */
        .st-key-documents_search_box [data-testid="stTextInputRootElement"]::before {{
            content: "" !important;
            display: inline-block !important;
            width: 16px !important;
            height: 16px !important;
            margin-right: 10px !important;
            flex-shrink: 0 !important;
            background-color: {COLORS["text_muted"]} !important;
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E") !important;
            -webkit-mask-size: contain !important;
            mask-size: contain !important;
            -webkit-mask-repeat: no-repeat !important;
            mask-repeat: no-repeat !important;
            -webkit-mask-position: center !important;
            mask-position: center !important;
            transition: background-color 150ms ease !important;
        }}

        .st-key-documents_search_box [data-testid="stTextInputRootElement"]:focus-within::before {{
            background-color: {COLORS["purple"]} !important;
        }}

        .st-key-documents_search_box input,
        .st-key-documents_search_box input:focus {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.84rem !important;
            color: {COLORS["text_primary"]} !important;
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            height: 40px !important;
            line-height: 40px !important;
            width: 100% !important;
        }}

        .st-key-documents_search_box input::placeholder {{
            color: {COLORS["text_muted"]} !important;
            opacity: 1 !important;
        }}

        .st-key-documents_search_box input::-webkit-calendar-picker-indicator,
        .st-key-documents_search_box input::-webkit-list-button {{
            display: none !important;
            -webkit-appearance: none !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            pointer-events: none !important;
        }}

        /* Upload button column & button */
        .st-key-documents_upload_col [data-testid="stButton"] {{
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: stretch !important;
        }}

        .st-key-documents_upload_col button {{
            width: 100% !important;
            height: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            box-sizing: border-box !important;
            border-radius: 10px !important;
            background: {COLORS["background"]} !important;
            color: {COLORS["purple"]} !important;
            border: 1px solid {COLORS["purple"]} !important;
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.84rem !important;
            font-weight: 600 !important;
            line-height: 40px !important;
            padding: 0 18px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 !important;
            box-shadow: none !important;
            transition: all 150ms ease !important;
            cursor: pointer !important;
        }}

        .st-key-documents_upload_col button:hover {{
            background: rgba(137, 39, 221, 0.12) !important;
            color: {COLORS["text_primary"]} !important;
            border-color: {COLORS["purple_hover"]} !important;
        }}

        .st-key-documents_upload_col button:focus {{
            box-shadow: 0 0 0 2px {COLORS["purple"]} !important;
            outline: none !important;
        }}

        /* Section Header */
        .documents-section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 0.5rem !important;
            margin-bottom: 0.4rem !important;
            width: 100%;
        }}

        .documents-section-label {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            color: {COLORS["text_muted"]} !important;
        }}

        .documents-section-count {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.76rem !important;
            color: {COLORS["text_muted"]} !important;
            font-weight: 500 !important;
        }}

        .documents-search-tag {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.68rem !important;
            font-weight: 500 !important;
            color: {COLORS["purple"]} !important;
            background: rgba(137, 39, 221, 0.12) !important;
            border: 1px solid rgba(137, 39, 221, 0.28) !important;
            border-radius: 999px !important;
            padding: 2px 8px !important;
            display: inline-flex !important;
            align-items: center !important;
            line-height: 1 !important;
        }}

        /* Empty Filter State */
        .documents-empty-filter-state {{
            background: {COLORS["background"]} !important;
            border: 1px solid #28222E !important;
            border-radius: 10px !important;
            padding: 24px 28px !important;
            margin-bottom: 16px !important;
            text-align: center !important;
        }}

        .documents-empty-filter-title {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            color: {COLORS["text_primary"]} !important;
            margin-bottom: 6px !important;
        }}

        .documents-empty-filter-sub {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.76rem !important;
            color: {COLORS["text_muted"]} !important;
        }}

        /* Card 'View Text' icon */
        [class*="view-text"] button::before {{
            content: "";
            display: inline-block;
            width: 14px;
            height: 14px;
            margin-right: 6px;
            background-color: currentColor;
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='16' y1='13' x2='8' y2='13'/%3E%3Cline x1='16' y1='17' x2='8' y2='17'/%3E%3Cline x1='10' y1='9' x2='8' y2='9'/%3E%3C/svg%3E");
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='16' y1='13' x2='8' y2='13'/%3E%3Cline x1='16' y1='17' x2='8' y2='17'/%3E%3Cline x1='10' y1='9' x2='8' y2='9'/%3E%3C/svg%3E");
            -webkit-mask-size: contain;
            mask-size: contain;
            -webkit-mask-repeat: no-repeat;
            mask-repeat: no-repeat;
            -webkit-mask-position: center;
            mask-position: center;
        }}

        /* Extracted Text Drawer */
        .documents-text-drawer {{
            background: {COLORS["background"]} !important;
            border: 1px solid #28222E !important;
            border-radius: {RADIUS["md"]};
            padding: 18px 22px;
            margin-top: 10px;
            margin-bottom: 20px;
        }}

        .documents-drawer-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid {COLORS["border_subtle"]};
        }}

        .documents-drawer-title {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: {COLORS["text_primary"]} !important;
        }}

        .documents-drawer-meta {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.72rem !important;
            color: {COLORS["text_muted"]} !important;
        }}

        /* Document Details Drawer */
        .documents-info-drawer {{
            background: {COLORS["background"]} !important;
            border: 1px solid #28222E !important;
            border-radius: {RADIUS["md"]} !important;
            padding: 18px 22px !important;
            margin-top: 10px !important;
            margin-bottom: 20px !important;
        }}

        .documents-info-grid {{
            display: grid !important;
            grid-template-columns: 1.8fr 0.72fr 0.88fr 0.88fr 0.95fr 2.55fr !important;
            gap: 16px 20px !important;
            align-items: start !important;
            margin-top: 14px !important;
            margin-bottom: 14px !important;
        }}

        .documents-info-item {{
            display: flex !important;
            flex-direction: column !important;
            gap: 4px !important;
            min-width: 0 !important;
        }}

        .documents-info-label {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.68rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            color: {COLORS["text_muted"]} !important;
            font-weight: 600 !important;
            white-space: nowrap !important;
        }}

        .documents-info-value {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.75rem !important;
            color: {COLORS["text_primary"]} !important;
            white-space: nowrap !important;
            text-overflow: ellipsis !important;
            overflow: hidden !important;
        }}

        @media (max-width: 1080px) {{
            .documents-info-grid {{
                grid-template-columns: repeat(3, 1fr) !important;
                gap: 16px 24px !important;
            }}
            .documents-info-value {{
                white-space: normal !important;
                word-break: break-word !important;
            }}
        }}

        @media (max-width: 640px) {{
            .documents-info-grid {{
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 14px 16px !important;
            }}
        }}

        /* Document Card 3-Dots Popover Body Dropdown */
        div[data-testid="stPopoverBody"] {{
            background: #131016 !important;
            border: 1px solid #28222E !important;
            border-radius: 8px !important;
            padding: 6px !important;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.85) !important;
            min-width: 160px !important;
        }}

        div[data-testid="stPopoverBody"] button,
        div[data-testid="stPopoverBody"] [data-testid="stDownloadButton"] button {{
            background: transparent !important;
            border: none !important;
            border-radius: 6px !important;
            color: #D4CED9 !important;
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 8px 12px !important;
            min-height: 32px !important;
            height: 32px !important;
            margin: 2px 0 !important;
            width: 100% !important;
            box-shadow: none !important;
            transition: background 150ms ease, color 150ms ease !important;
        }}

        div[data-testid="stPopoverBody"] button:hover,
        div[data-testid="stPopoverBody"] [data-testid="stDownloadButton"] button:hover {{
            background: rgba(255, 255, 255, 0.06) !important;
            color: #FFFFFF !important;
        }}

        div[data-testid="stPopoverBody"] [data-testid="stElementContainer"]:has([class*="menu-delete"]) button,
        div[data-testid="stPopoverBody"] button[key*="menu-delete"],
        div[data-testid="stPopoverBody"] [class*="menu-delete"] button {{
            color: #F96D57 !important;
        }}

        div[data-testid="stPopoverBody"] [data-testid="stElementContainer"]:has([class*="menu-delete"]) button:hover,
        div[data-testid="stPopoverBody"] button[key*="menu-delete"]:hover,
        div[data-testid="stPopoverBody"] [class*="menu-delete"] button:hover {{
            background: rgba(249, 109, 87, 0.12) !important;
            color: #FF806B !important;
        }}

        /* Delete confirmation modal / banner */
        .documents-delete-banner {{
            background: rgba(249, 109, 87, 0.08) !important;
            border: 1px solid rgba(249, 109, 87, 0.28) !important;
            border-radius: {RADIUS["md"]} !important;
            padding: 16px 20px !important;
            margin-top: 10px !important;
            margin-bottom: 20px !important;
        }}

        .documents-delete-text {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.84rem !important;
            color: {COLORS["text_primary"]} !important;
            margin-bottom: 12px !important;
        }}

        /* Document Intelligence Banner */
        .document-intelligence-banner {{
            background: {COLORS["background"]} !important;
            border: 1px solid #28222E !important;
            border-radius: 14px !important;
            padding: 32px !important;
            margin-top: 1.15rem !important;
            margin-bottom: 1.25rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 32px !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
        }}

        .document-intelligence-content {{
            flex: 1 1 50% !important;
            min-width: 280px !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 12px !important;
        }}

        .document-intelligence-tag {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.14em !important;
            text-transform: uppercase !important;
            color: {COLORS["purple"]} !important;
        }}

        .document-intelligence-headline {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 1.45rem !important;
            font-weight: 600 !important;
            color: {COLORS["text_primary"]} !important;
            line-height: 1.35 !important;
            margin: 0 !important;
            letter-spacing: -0.02em !important;
        }}

        .document-intelligence-headline a,
        .document-intelligence-banner a[data-testid="stHeaderActionElements"] {{
            display: none !important;
        }}

        .document-intelligence-desc {{
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.8rem !important;
            color: #9A93A0 !important;
            line-height: 1.6 !important;
            margin: 0 !important;
        }}

        .document-intelligence-badge {{
            display: inline-flex !important;
            align-items: center !important;
            gap: 12px !important;
            margin-top: 14px !important;
            color: {COLORS["text_primary"]} !important;
            font-family: "{TYPOGRAPHY["font_family"]}", monospace !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            box-shadow: none !important;
            width: fit-content !important;
        }}

        .document-intelligence-icon-box {{
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            max-width: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            flex-shrink: 0 !important;
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid #28222E !important;
            border-radius: 8px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        .document-intelligence-icon-box::before {{
            content: "" !important;
            display: block !important;
            width: 17px !important;
            height: 17px !important;
            flex-shrink: 0 !important;
            background-color: {COLORS["coral"]} !important;
            -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3Ccircle cx='12' cy='11' r='1.5' fill='black'/%3E%3C/svg%3E") center / contain no-repeat !important;
            mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3Ccircle cx='12' cy='11' r='1.5' fill='black'/%3E%3C/svg%3E") center / contain no-repeat !important;
        }}

        .document-intelligence-visual {{
            flex: 1 1 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            max-width: 520px !important;
        }}

        .document-intelligence-visual img {{
            width: 100% !important;
            height: auto !important;
            max-height: 220px !important;
            object-fit: contain !important;
            display: block !important;
            mix-blend-mode: screen !important;
        }}

        @media (max-width: 768px) {{
            .document-intelligence-banner {{
                flex-direction: column !important;
                align-items: stretch !important;
                padding: 24px !important;
            }}
            .document-intelligence-visual {{
                max-width: 100% !important;
            }}
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

        .stDeployButton,
        [data-testid="stDeployButton"] {{
            display: none !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )