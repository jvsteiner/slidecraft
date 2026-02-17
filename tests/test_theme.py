"""Tests for the Theme class."""
import pytest
from pptx.dml.color import RGBColor
from slidecraft.theme import Theme, DEFAULT_COLORS, DEFAULT_SPACING


class TestThemeDefaults:
    def test_default_fonts(self):
        t = Theme({})
        assert t.font_display == 'Calibri'
        assert t.font_body == 'Calibri'

    def test_default_colors_loaded(self):
        t = Theme({})
        for name in DEFAULT_COLORS:
            assert isinstance(t.color(name), RGBColor)

    def test_default_spacing_loaded(self):
        t = Theme({})
        for key in DEFAULT_SPACING:
            assert t.spacing(key) == DEFAULT_SPACING[key]


class TestThemeCustom:
    def test_custom_fonts(self):
        t = Theme({'font_display': 'Fraunces', 'font_body': 'Outfit'})
        assert t.font_display == 'Fraunces'
        assert t.font_body == 'Outfit'

    def test_custom_colors_override_defaults(self):
        t = Theme({'colors': {'bg': '#FF0000'}})
        assert t.color('bg') == RGBColor(0xFF, 0x00, 0x00)
        # Other defaults still available
        assert isinstance(t.color('primary'), RGBColor)

    def test_custom_spacing(self):
        t = Theme({'spacing': {'margin': 1.0}})
        assert t.spacing('margin') == 1.0
        # Other defaults still available
        assert t.spacing('gutter') == DEFAULT_SPACING['gutter']


class TestColorResolution:
    def test_resolve_by_name(self):
        t = Theme({'colors': {'primary': '#2563EB'}})
        assert t.color('primary') == RGBColor(0x25, 0x63, 0xEB)

    def test_resolve_hex_string(self):
        t = Theme({})
        assert t.color('#FF8800') == RGBColor(0xFF, 0x88, 0x00)

    def test_passthrough_rgb(self):
        t = Theme({})
        c = RGBColor(0x11, 0x22, 0x33)
        assert t.color(c) is c

    def test_unknown_color_raises(self):
        t = Theme({})
        with pytest.raises(KeyError, match='Unknown theme color'):
            t.color('nonexistent')


class TestFontResolution:
    def test_heading_returns_display(self):
        t = Theme({'font_display': 'Serif', 'font_body': 'Sans'})
        assert t.font(heading=True) == 'Serif'

    def test_body_returns_body(self):
        t = Theme({'font_display': 'Serif', 'font_body': 'Sans'})
        assert t.font(heading=False) == 'Sans'


class TestProperties:
    def test_margin_property(self):
        t = Theme({'spacing': {'margin': 1.2}})
        assert t.margin == 1.2

    def test_gutter_property(self):
        t = Theme({'spacing': {'gutter': 0.5}})
        assert t.gutter == 0.5
