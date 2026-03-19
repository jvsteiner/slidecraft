"""Tests for shared HTML layout helpers."""
import pytest
from slidecraft.html_layouts._helpers import (
    escape, render_footer, render_slide_number,
    render_slide_header, render_text_zone, render_image_zone,
)
from slidecraft.theme import Theme


class TestEscape:
    def test_escapes_angle_brackets(self):
        assert '&lt;script&gt;' in escape('<script>')

    def test_escapes_ampersand(self):
        assert '&amp;' in escape('A & B')

    def test_passes_through_normal_text(self):
        assert escape('Hello World') == 'Hello World'


class TestRenderFooter:
    def test_contains_text(self):
        html = render_footer('Source: internal data')
        assert 'Source: internal data' in html
        assert 'sc-footer' in html

    def test_escapes_content(self):
        html = render_footer('<script>alert(1)</script>')
        assert '<script>' not in html


class TestRenderSlideNumber:
    def test_contains_number(self):
        html = render_slide_number(5)
        assert '5' in html
        assert 'sc-slide-num' in html


class TestRenderSlideHeader:
    def test_contains_title(self):
        theme = Theme({})
        html = render_slide_header(1, 'My Title', None, theme)
        assert 'My Title' in html
        assert 'sc-accent-bar' in html

    def test_contains_subtitle(self):
        theme = Theme({})
        html = render_slide_header(1, 'Title', 'Subtitle here', theme)
        assert 'Subtitle here' in html

    def test_no_subtitle_when_none(self):
        theme = Theme({})
        html = render_slide_header(1, 'Title', None, theme)
        assert 'sc-header-subtitle' not in html


class TestRenderTextZone:
    def test_string_content(self):
        theme = Theme({})
        html = render_text_zone('Simple text', theme)
        assert 'Simple text' in html

    def test_dict_with_heading_and_body(self):
        theme = Theme({})
        html = render_text_zone({'heading': 'H1', 'body': 'Body text'}, theme)
        assert 'H1' in html
        assert 'Body text' in html

    def test_dict_with_bullets(self):
        theme = Theme({})
        html = render_text_zone({'heading': 'H', 'bullets': ['A', 'B']}, theme)
        assert '<li>' in html
        assert 'A' in html
        assert 'B' in html


class TestRenderImageZone:
    def test_string_path(self):
        resolve = lambda p: f'data:image/png;base64,FAKE_{p}'
        html = render_image_zone('photo.png', resolve)
        assert 'data:image/png;base64,FAKE_photo.png' in html
        assert '<img' in html

    def test_dict_with_caption(self):
        resolve = lambda p: f'data:image/png;base64,FAKE'
        html = render_image_zone({'image': 'x.png', 'caption': 'My caption'}, resolve)
        assert 'My caption' in html
        assert 'sc-caption' in html
