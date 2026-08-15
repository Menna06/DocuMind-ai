"""Layout and spacing system QA showcase for DocuMind."""

import textwrap

import streamlit as st


from app.ui.theme import (
    COLORS,
    CONTAINERS,
    DENSITY,
    LAYOUT,
    RADIUS,
    SPACING,
)


def _render_html(html: str) -> None:
    """Render raw HTML without Markdown interpretation."""
    st.html(textwrap.dedent(html).strip())


def _section_label(label: str) -> None:
    """Render a consistent showcase section label."""
    _render_html(
        f"""
        <div style="
            color: {COLORS["text_muted"]};
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin: 2.5rem 0 1rem 0;
        ">
            {label}
        </div>
        """
    )


def render_layout_showcase() -> None:
    """Render the DocuMind spacing and layout QA showcase."""

    # =========================================================
    # HERO
    # =========================================================

    _render_html(
        f"""
        <div style="
            margin-bottom: 3rem;
            font-family: 'JetBrains Mono', monospace;
        ">
            <div style="
                color: {COLORS["purple"]};
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                margin-bottom: 0.75rem;
            ">
                UI-03 · Spacing & Layout System
            </div>

            <div style="
                color: {COLORS["text_primary"]};
                font-size: 3rem;
                font-weight: 600;
                line-height: 1.1;
                letter-spacing: -0.04em;
            ">
                Space creates structure.
            </div>

            <div style="
                color: {COLORS["text_secondary"]};
                font-size: 0.95rem;
                line-height: 1.7;
                max-width: 760px;
                margin-top: 1rem;
            ">
                DocuMind uses a consistent spacing vocabulary, container
                system and density model so every page feels deliberately
                composed rather than independently assembled.
            </div>
        </div>
        """
    )

    # =========================================================
    # SPACING SCALE
    # =========================================================

    _section_label("Spacing Scale")

    spacing_items = [
        ("xs", SPACING["xs"]),
        ("sm", SPACING["sm"]),
        ("md", SPACING["md"]),
        ("lg", SPACING["lg"]),
        ("xl", SPACING["xl"]),
        ("2xl", SPACING["2xl"]),
        ("3xl", SPACING["3xl"]),
        ("4xl", SPACING["4xl"]),
        ("5xl", SPACING["5xl"]),
    ]

    for name, value in spacing_items:
        numeric_value = int(value.replace("px", ""))

        _render_html(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 0.75rem;
                font-family: 'JetBrains Mono', monospace;
            ">
                <div style="
                    width: 4rem;
                    color: {COLORS["text_muted"]};
                    font-size: 0.72rem;
                    font-weight: 700;
                ">
                    {name}
                </div>

                <div style="
                    width: {numeric_value}px;
                    min-width: 4px;
                    height: 18px;
                    background: {COLORS["purple"]};
                    border-radius: 3px;
                "></div>

                <div style="
                    color: {COLORS["text_secondary"]};
                    font-size: 0.72rem;
                ">
                    {value}
                </div>
            </div>
            """
        )

    # =========================================================
    # CONTAINER SYSTEM
    # =========================================================

    _section_label("Container System")

    container_items = [
        ("Reading", CONTAINERS["reading"]),
        ("Page", CONTAINERS["page"]),
        ("Wide", CONTAINERS["wide"]),
        ("Full", CONTAINERS["full"]),
    ]

    for name, value in container_items:
        width = value

        _render_html(
            f"""
            <div style="
                margin-bottom: 1.25rem;
                font-family: 'JetBrains Mono', monospace;
            ">
                <div style="
                    color: {COLORS["text_muted"]};
                    font-size: 0.68rem;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    margin-bottom: 0.5rem;
                ">
                    {name} · {value}
                </div>

                <div style="
                    width: {width};
                    max-width: 100%;
                    height: 52px;
                    background: {COLORS["surface"]};
                    border: 1px solid {COLORS["border_default"]};
                    border-radius: {RADIUS["md"]};
                ">
                </div>
            </div>
            """
        )

    # =========================================================
    # DENSITY
    # =========================================================

    _section_label("Density System")

    density_items = [
        ("Compact", DENSITY["compact"]),
        ("Default", DENSITY["default"]),
        ("Spacious", DENSITY["spacious"]),
    ]

    for name, settings in density_items:
        _render_html(
            f"""
            <div style="
                background: {COLORS["surface"]};
                border: 1px solid {COLORS["border_default"]};
                border-radius: 10px;
                padding: {settings["padding"]};
                margin-bottom: 1rem;
                font-family: 'JetBrains Mono', monospace;
            ">
                <div style="
                    color: {COLORS["purple"]};
                    font-size: 0.7rem;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    margin-bottom: {settings["gap"]};
                ">
                    {name}
                </div>

                <div style="
                    display: flex;
                    gap: {settings["gap"]};
                ">
                    <div style="
                        flex: 1;
                        height: 48px;
                        background: {COLORS["surface_elevated"]};
                        border: 1px solid {COLORS["border_subtle"]};
                        border-radius: 6px;
                    "></div>

                    <div style="
                        flex: 1;
                        height: 48px;
                        background: {COLORS["surface_elevated"]};
                        border: 1px solid {COLORS["border_subtle"]};
                        border-radius: 6px;
                    "></div>

                    <div style="
                        flex: 1;
                        height: 48px;
                        background: {COLORS["surface_elevated"]};
                        border: 1px solid {COLORS["border_subtle"]};
                        border-radius: 6px;
                    "></div>
                </div>
            </div>
            """
        )

    # =========================================================
    # LAYOUT CONTRACT
    # =========================================================

    _section_label("Layout Contract")

    _render_html(
        f"""
        <div style="
            border: 1px solid {COLORS["border_default"]};
            background: {COLORS["surface"]};
            border-radius: 10px;
            padding: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
        ">

            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            ">

                <div>
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 0.4rem;
                    ">
                        Sidebar
                    </div>

                    <div style="
                        color: {COLORS["text_primary"]};
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        {LAYOUT["sidebar_width"]}
                    </div>
                </div>

                <div>
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 0.4rem;
                    ">
                        Content Max Width
                    </div>

                    <div style="
                        color: {COLORS["text_primary"]};
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        {LAYOUT["content_max_width"]}
                    </div>
                </div>

                <div>
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 0.4rem;
                    ">
                        Horizontal Padding
                    </div>

                    <div style="
                        color: {COLORS["text_primary"]};
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        {LAYOUT["content_padding_x"]}
                    </div>
                </div>

                <div>
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 0.4rem;
                    ">
                        Vertical Padding
                    </div>

                    <div style="
                        color: {COLORS["text_primary"]};
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        {LAYOUT["content_padding_y"]}
                    </div>
                </div>

                <div>
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 0.4rem;
                    ">
                        Section Gap
                    </div>

                    <div style="
                        color: {COLORS["text_primary"]};
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        {LAYOUT["section_gap"]}
                    </div>
                </div>

                <div>
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.1em;
                        margin-bottom: 0.4rem;
                    ">
                        Component Gap
                    </div>

                    <div style="
                        color: {COLORS["text_primary"]};
                        font-size: 1.2rem;
                        font-weight: 600;
                    ">
                        {LAYOUT["component_gap"]}
                    </div>
                </div>

            </div>

        </div>
        """
    )