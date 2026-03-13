"""
Theme — resolve named colors, fonts, and spacing from a config dict.

Theme config (from YAML):
    theme:
      font_display: "Fraunces 72pt"
      font_body: "Outfit"
      colors:
        bg: "#0D0D0F"
        primary: "#2563EB"
        text: "#FFFFFF"
        ...
      spacing:
        margin: 0.8        # inches, outer margin
        gutter: 0.4        # inches, between columns
        title_height: 0.8  # inches, title zone height
"""
from pptx.dml.color import RGBColor


DEFAULT_COLORS = {
    'bg': '#FFFFFF',
    'surface': '#F5F5F5',
    'primary': '#2563EB',
    'primary_dark': '#1D4ED8',
    'danger': '#EF4444',
    'success': '#059669',
    'warning': '#EA580C',
    'text': '#111111',
    'text_secondary': '#444444',
    'text_muted': '#888888',
    'text_dim': '#AAAAAA',
    'divider': '#E5E5E5',
    'row_alt': '#FAFAFA',
    'border': '#E0E0E0',
}

DEFAULT_SPACING = {
    'margin': 0.8,
    'margin_top': 0.6,
    'gutter': 0.4,
    'title_height': 0.8,
    'footer_y': 7.0,
}


class Theme:
    """Resolve named colors, fonts, and spacing from config."""

    def __init__(self, config: dict):
        self.font_display = config.get('font_display', 'Helvetica Neue')
        self.font_body = config.get('font_body', 'Helvetica Neue')
        self.background_image = config.get('background_image')
        self.overlay = config.get('overlay')

        self._colors = {}
        merged = {**DEFAULT_COLORS, **config.get('colors', {})}
        for key, val in merged.items():
            self._colors[key] = self._parse_hex(val) if isinstance(val, str) else val

        self._spacing = {**DEFAULT_SPACING, **config.get('spacing', {})}

    @staticmethod
    def _parse_hex(hex_str: str) -> RGBColor:
        h = hex_str.lstrip('#')
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def color(self, name_or_rgb) -> RGBColor:
        """Resolve a color by theme name, hex string, or pass through RGBColor."""
        if isinstance(name_or_rgb, RGBColor):
            return name_or_rgb
        if name_or_rgb in self._colors:
            return self._colors[name_or_rgb]
        if isinstance(name_or_rgb, str) and name_or_rgb.startswith('#'):
            return self._parse_hex(name_or_rgb)
        raise KeyError(
            f"Unknown theme color: '{name_or_rgb}'. "
            f"Available: {sorted(self._colors.keys())}"
        )

    def font(self, heading: bool = False) -> str:
        """Return display font for headings, body font otherwise."""
        return self.font_display if heading else self.font_body

    def spacing(self, key: str) -> float:
        """Return spacing value in inches."""
        return self._spacing[key]

    @property
    def margin(self) -> float:
        return self._spacing['margin']

    @property
    def gutter(self) -> float:
        return self._spacing['gutter']
