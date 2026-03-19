"""HtmlBuilder — build an HTML presentation from YAML content."""
import os
import base64
import yaml

from .theme import Theme
from .html_theme import generate_css, generate_noscript_css
from .html_layouts import get_html_layout

REVEAL_VERSION = '5.1.0'
REVEAL_CDN = f'https://cdn.jsdelivr.net/npm/reveal.js@{REVEAL_VERSION}'

MIME_TYPES = {
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.png': 'image/png', '.gif': 'image/gif',
    '.webp': 'image/webp', '.svg': 'image/svg+xml',
}


class HtmlBuilder:
    """Build an HTML presentation from themed layouts and YAML content."""

    def __init__(self, theme_config: dict):
        self.theme = Theme(theme_config)
        self._content = None
        self._base_dir = '.'
        self._html = None

    @classmethod
    def from_yaml(cls, path: str) -> 'HtmlBuilder':
        with open(path) as f:
            content = yaml.safe_load(f)
        theme_config = content.get('theme', {})
        hb = cls(theme_config)
        hb._content = content
        hb._base_dir = os.path.dirname(os.path.abspath(path))
        return hb

    @property
    def slides_content(self) -> list:
        if self._content is None:
            return []
        slides = self._content.get('slides', [])
        return slides if isinstance(slides, list) else list(slides.items())

    def resolve_path(self, relative_path: str) -> str:
        return os.path.join(self._base_dir, relative_path)

    def resolve_image(self, relative_path: str) -> str:
        """Read an image and return a base64 data URI."""
        full_path = self.resolve_path(relative_path)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Image not found: {full_path}")
        ext = os.path.splitext(full_path)[1].lower()
        mime = MIME_TYPES.get(ext, 'application/octet-stream')
        with open(full_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('ascii')
        return f'data:{mime};base64,{encoded}'

    def build(self) -> str:
        """Build all slides and return complete HTML document."""
        css = generate_css(self.theme)
        noscript_css = generate_noscript_css(self.theme)
        sections = []

        for slide_num, slide_config in enumerate(self.slides_content, 1):
            if isinstance(slide_config, tuple):
                _, data = slide_config
            else:
                data = slide_config

            layout_name = data.get('layout')
            if not layout_name:
                raise ValueError(f"Slide missing 'layout' key: {data}")

            render_fn = get_html_layout(layout_name)
            section_html = render_fn(data, slide_num, self.theme,
                                     self.resolve_image)

            # Background image (per-slide overrides global)
            bg_image = data.get('background_image', self.theme.background_image)
            overlay_cfg = data.get('overlay', self.theme.overlay)

            if bg_image is not None:
                bg_data_uri = self.resolve_image(bg_image)
                bg_style = (f'background-image:url({bg_data_uri});'
                            f'background-size:cover;background-position:center;')
                section_html = section_html.replace(
                    '<section', f'<section style="{bg_style}"', 1)
                if overlay_cfg:
                    color = overlay_cfg.get('color', '#000000')
                    opacity = overlay_cfg.get('opacity', 0.5)
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                    overlay_div = (f'<div class="sc-overlay" style="'
                                   f'background:rgba({r},{g},{b},{opacity})"></div>')
                    idx = section_html.index('>') + 1
                    section_html = section_html[:idx] + overlay_div + section_html[idx:]

            sections.append(section_html)

        slides_html = '\n'.join(sections)

        self._html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="{REVEAL_CDN}/dist/reveal.css">
<link rel="stylesheet" href="{REVEAL_CDN}/dist/theme/white.css">
<style>
{css}
</style>
<noscript><style>
{noscript_css}
</style></noscript>
</head>
<body>
<div class="reveal"><div class="slides">
{slides_html}
</div></div>
<script src="{REVEAL_CDN}/dist/reveal.js"></script>
<script>
Reveal.initialize({{
  hash: true,
  controls: true,
  progress: true,
  center: false,
  transition: 'none',
  width: 1280,
  height: 720,
  margin: 0
}});
</script>
</body>
</html>"""
        return self._html

    def save(self, path: str):
        """Save the HTML presentation to a file."""
        if self._html is None:
            self.build()
        with open(path, 'w') as f:
            f.write(self._html)
        print(f'Saved: {path}')
