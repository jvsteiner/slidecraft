"""HTML layout registry — maps layout names to render functions."""
from .title import render as _title
from .section import render as _section
from .content import render as _content
from .closing import render as _closing
from .two_col import render_text_text, render_text_image, render_image_text, render_image_image
from .three_col_equal import (
    render_text_text_text, render_text_image_text,
    render_image_text_text, render_text_text_image,
)
from .three_col_wide import (
    render_image_dtext, render_text_dimage,
    render_dimage_text, render_dtext_image,
)
from .comparison import render as _comparison
from .data_table import render as _data_table
from .quote import render as _quote
from .profile import render as _profile
from .metrics import render as _metrics

_REGISTRY = {
    'title': _title,
    'section': _section,
    'content': _content,
    'closing': _closing,
    'two_col_text_text': render_text_text,
    'two_col_text_image': render_text_image,
    'two_col_image_text': render_image_text,
    'two_col_image_image': render_image_image,
    'three_col_text_text_text': render_text_text_text,
    'three_col_text_image_text': render_text_image_text,
    'three_col_image_text_text': render_image_text_text,
    'three_col_text_text_image': render_text_text_image,
    'three_col_image_dtext': render_image_dtext,
    'three_col_text_dimage': render_text_dimage,
    'three_col_dimage_text': render_dimage_text,
    'three_col_dtext_image': render_dtext_image,
    'comparison': _comparison,
    'data_table': _data_table,
    'quote': _quote,
    'profile': _profile,
    'metrics': _metrics,
}


def get_html_layout(name: str):
    """Look up an HTML layout render function by name."""
    if name not in _REGISTRY:
        available = ', '.join(sorted(_REGISTRY.keys()))
        raise KeyError(f"Unknown HTML layout '{name}'. Available: {available}")
    return _REGISTRY[name]


def list_html_layouts() -> list[str]:
    """Return all registered HTML layout names."""
    return sorted(_REGISTRY.keys())
