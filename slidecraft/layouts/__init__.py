"""
Layout registry — maps layout names to classes.
"""
from .base import BaseLayout
from .title import TitleLayout
from .section import SectionLayout
from .content import ContentLayout
from .two_col import (
    TwoColTextText, TwoColTextImage,
    TwoColImageText, TwoColImageImage,
)
from .three_col_equal import (
    ThreeColTextTextText, ThreeColTextImageText,
    ThreeColImageTextText, ThreeColTextTextImage,
)
from .three_col_wide import (
    ThreeColImageDtext, ThreeColTextDimage,
    ThreeColDimageText, ThreeColDtextImage,
)
from .comparison import ComparisonLayout
from .data_table import DataTableLayout
from .quote import QuoteLayout
from .profile import ProfileLayout
from .metrics import MetricsLayout
from .closing import ClosingLayout

_REGISTRY: dict[str, type[BaseLayout]] = {}


def _register(cls: type[BaseLayout]):
    _REGISTRY[cls.name] = cls


for _cls in [
    TitleLayout,
    SectionLayout,
    ContentLayout,
    # Two-column (4)
    TwoColTextText,
    TwoColTextImage,
    TwoColImageText,
    TwoColImageImage,
    # Three-column equal (4)
    ThreeColTextTextText,
    ThreeColTextImageText,
    ThreeColImageTextText,
    ThreeColTextTextImage,
    # Three-column wide (4)
    ThreeColImageDtext,
    ThreeColTextDimage,
    ThreeColDimageText,
    ThreeColDtextImage,
    # Other
    ComparisonLayout,
    DataTableLayout,
    QuoteLayout,
    ProfileLayout,
    MetricsLayout,
    ClosingLayout,
]:
    _register(_cls)


def get_layout(name: str) -> type[BaseLayout]:
    """Look up a layout class by name."""
    if name not in _REGISTRY:
        available = ', '.join(sorted(_REGISTRY.keys()))
        raise KeyError(f"Unknown layout '{name}'. Available: {available}")
    return _REGISTRY[name]


def list_layouts() -> list[str]:
    """Return all registered layout names."""
    return sorted(_REGISTRY.keys())
