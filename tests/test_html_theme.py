"""Tests for HTML theme CSS generation."""
import pytest
from slidecraft.theme import Theme
from slidecraft.html_theme import generate_css, generate_noscript_css


class TestGenerateCSS:
    def test_contains_color_variables(self):
        theme = Theme({'colors': {'bg': '#0F172A', 'primary': '#38BDF8'}})
        css = generate_css(theme)
        assert '--color-bg: #0F172A' in css
        assert '--color-primary: #38BDF8' in css

    def test_contains_font_variables(self):
        theme = Theme({'font_display': 'Futura', 'font_body': 'Avenir Next'})
        css = generate_css(theme)
        assert '--font-display: "Futura"' in css
        assert '--font-body: "Avenir Next"' in css

    def test_contains_slide_base_styles(self):
        theme = Theme({'colors': {'bg': '#0F172A'}})
        css = generate_css(theme)
        assert '.reveal .slides section' in css
        assert 'background-color' in css

    def test_default_theme_generates_valid_css(self):
        theme = Theme({})
        css = generate_css(theme)
        assert ':root' in css
        assert '--color-bg' in css

    def test_all_default_colors_present(self):
        theme = Theme({})
        css = generate_css(theme)
        for name in [
            'bg', 'surface', 'primary', 'primary_dark', 'danger',
            'success', 'warning', 'text', 'text_secondary', 'text_muted',
            'text_dim', 'divider', 'row_alt', 'border',
        ]:
            assert f'--color-{name}:' in css

    def test_utility_classes_present(self):
        theme = Theme({})
        css = generate_css(theme)
        for cls in [
            '.sc-accent-bar', '.sc-footer', '.sc-slide-num',
            '.sc-header-title', '.sc-header-subtitle',
            '.sc-grid', '.sc-text-zone', '.sc-img',
            '.sc-caption', '.sc-overlay',
        ]:
            assert cls in css


class TestGenerateNoscriptCSS:
    def test_noscript_has_fallback_fonts(self):
        theme = Theme({})
        css = generate_noscript_css(theme)
        assert 'font-family' in css

    def test_noscript_is_minimal(self):
        theme = Theme({})
        css = generate_noscript_css(theme)
        assert '.reveal' not in css
