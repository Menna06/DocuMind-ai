"""DocuMind UI design tokens."""

COLORS = {
    # Canvas
    "background": "#100E11",

    # Surfaces
    "surface": "#151217",
    "surface_elevated": "#1C1820",
    "surface_hover": "#211B26",

    # Purple brand system
    "purple": "#8927DD",
    "purple_hover": "#9B3BE5",
    "purple_active": "#7621C1",
    "purple_subtle": "#2A1640",

    # Coral accent system
    "coral": "#F96D57",
    "coral_hover": "#FF806B",
    "coral_active": "#DE5A48",
    "coral_subtle": "#3A1C1A",

    # Typography
    "text_primary": "#F5F2F6",
    "text_secondary": "#B8B1BA",
    "text_muted": "#77717B",
    "text_disabled": "#4D4850",

    # Borders
    "border_subtle": "#211D24",
    "border_default": "#2D2830",
    "border_strong": "#403744",
    "border_accent": "#8927DD",

    # Semantic states
    "success": "#79B58A",
    "warning": "#E5B86A",
    "error": "#F96D57",
    "info": "#8E7AA8",
}

TYPOGRAPHY = {
    "font_family": "JetBrains Mono",

    # Structural hierarchy
    "display": {
        "family": "JetBrains Mono",
        "weight": 600,
    },
    "heading": {
        "family": "JetBrains Mono",
        "weight": 600,
    },

    # Default interface typography
    "body": {
        "family": "JetBrains Mono",
        "weight": 400,
    },

    # Accent / emphasis
    "accent": {
        "family": "JetBrains Mono",
        "weight": 700,
    },
}

SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px",
    "4xl": "64px",
    "5xl": "80px",
}

RADIUS = {
    "sm": "6px",
    "md": "10px",
    "lg": "14px",
}

LAYOUT = {
    "sidebar_width": "280px",
    "content_max_width": "1200px",
    "content_padding_x": "32px",
    "content_padding_y": "48px",
    "section_gap": "48px",
    "component_gap": "16px",
}

CONTAINERS = {
    "page": "1200px",
    "reading": "760px",
    "wide": "1200px",
    "full": "100%",
}

DENSITY = {
    "compact": {
        "gap": "8px",
        "padding": "8px",
    },
    "default": {
        "gap": "16px",
        "padding": "16px",
    },
    "spacious": {
        "gap": "24px",
        "padding": "24px",
    },
}

BUTTONS = {
    "primary": {
        "background": COLORS["purple"],
        "text": COLORS["text_primary"],
        "border": COLORS["purple"],
        "hover_background": COLORS["purple_hover"],
        "hover_text": COLORS["text_primary"],
        "hover_border": COLORS["purple_hover"],
        "focus_ring": COLORS["purple"],
        "disabled_background": COLORS["surface_elevated"],
        "disabled_text": COLORS["text_disabled"],
        "disabled_border": COLORS["border_subtle"],
    },

    "secondary": {
        "background": "transparent",
        "text": COLORS["purple"],
        "border": COLORS["purple"],
        "hover_background": COLORS["purple_subtle"],
        "hover_text": COLORS["text_primary"],
        "hover_border": COLORS["purple_hover"],
        "focus_ring": COLORS["purple"],
        "disabled_background": "transparent",
        "disabled_text": COLORS["text_disabled"],
        "disabled_border": COLORS["border_subtle"],
    },

    "ghost": {
        "background": "transparent",
        "text": COLORS["text_secondary"],
        "border": "transparent",
        "hover_background": COLORS["surface_hover"],
        "hover_text": COLORS["text_primary"],
        "hover_border": "transparent",
        "focus_ring": COLORS["purple"],
        "disabled_background": "transparent",
        "disabled_text": COLORS["text_disabled"],
        "disabled_border": "transparent",
    },

    "danger": {
        "background": "transparent",
        "text": COLORS["coral"],
        "border": "transparent",
        "hover_background": COLORS["coral_subtle"],
        "hover_text": COLORS["coral_hover"],
        "hover_border": "transparent",
        "focus_ring": COLORS["coral"],
        "disabled_background": "transparent",
        "disabled_text": COLORS["text_disabled"],
        "disabled_border": "transparent",
    },

    "height": "40px",
    "padding_x": "16px",
    "radius": RADIUS["md"],
    "font_size": "0.82rem",
    "font_weight": 600,
    "transition": "all 150ms ease",
}

INPUTS = {
    "question": {
        "background": COLORS["surface"],
        "border": COLORS["border_default"],
        "hover_border": COLORS["border_strong"],
        "focus_border": COLORS["purple"],
        "focus_ring": COLORS["purple_subtle"],
        "text": COLORS["text_primary"],
        "placeholder": COLORS["text_muted"],
        "disabled_background": COLORS["surface_elevated"],
        "disabled_border": COLORS["border_subtle"],
        "disabled_text": COLORS["text_disabled"],
        "error_border": "#FF4D6D",
        "error_text": "#FF4D6D",
    },

    "answer": {
        "background": COLORS["background"],

        # Animated gradient
        "gradient": (
            "linear-gradient("
            "90deg, "
            "#FF8A00 0%, "
            "#FF2D55 35%, "
            "#8927DD 65%, "
            "#FF8A00 100%"
            ")"
        ),

        "animation_duration": "6s",
    },

    "dropzone": {
        "background": COLORS["background"],
        "border": COLORS["purple"],
        "hover_border": COLORS["purple_hover"],
        "drag_border": COLORS["purple_hover"],
        "disabled_border": COLORS["border_default"],
        "error_border": "#FF4D6D",
        "text": COLORS["text_primary"],
        "secondary_text": COLORS["text_secondary"],
        "muted_text": COLORS["text_muted"],
    },

    "radius": RADIUS["lg"],
}

DOCUMENT_CARD = {
    "background": COLORS["surface"],
    "border": COLORS["border_default"],
    "border_hover": COLORS["border_strong"],
    "radius": RADIUS["md"],
    "padding": "20px",
    "icon_size": "72px",
    "divider": COLORS["border_subtle"],
    "metadata_color": COLORS["text_secondary"],
    "muted_color": COLORS["text_muted"],
    "status_success": COLORS["success"],
    "status_processing": COLORS["purple"],
    "status_background": COLORS["surface_elevated"],
}

DOCUMENT_TILE = {
    "background": COLORS["surface"],
    "border": COLORS["border_default"],
    "border_hover": COLORS["border_strong"],
    "radius": RADIUS["md"],
    "padding": "16px",
    "icon_size": "52px",
}