"""
BaseLayout — abstract base class for all slide layouts.

Every layout must:
1. Declare a `name` (used in YAML: layout: <name>)
2. Implement `render(db, content, slide_num)`
"""
from abc import ABC, abstractmethod


class BaseLayout(ABC):
    """Abstract base for slide layouts."""

    name: str = ''  # Override in subclass

    @abstractmethod
    def render(self, db, content: dict, slide_num: int):
        """Render this layout onto a new slide.

        Args:
            db: DeckBuilder instance (provides .new_slide(), .p (primitives), .theme)
            content: Dict of content for this slide (from YAML)
            slide_num: Slide number for footer
        """
        ...

    def _content_width(self, db) -> float:
        """Usable content width (slide width minus margins)."""
        return 13.333 - 2 * db.theme.margin
