"""
SlideCraft — build PowerPoint decks from YAML content with themed layouts.

Quick start:
    python3 -m slidecraft build content.yaml output.pptx

Programmatic usage:
    from slidecraft import DeckBuilder
    db = DeckBuilder.from_yaml('content.yaml')
    db.build()
    db.save('output.pptx')
"""
from .builder import DeckBuilder
from .theme import Theme
from .layouts import get_layout, list_layouts

__all__ = ['DeckBuilder', 'Theme', 'get_layout', 'list_layouts']
