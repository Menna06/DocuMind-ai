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