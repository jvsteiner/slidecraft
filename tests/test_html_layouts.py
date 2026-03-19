"""Tests for HTML layout renderers."""
import pytest
from slidecraft.theme import Theme
from slidecraft.html_layouts.title import render as render_title
from slidecraft.html_layouts.section import render as render_section
from slidecraft.html_layouts.content import render as render_content
from slidecraft.html_layouts.closing import render as render_closing

THEME = Theme({})
NOOP_RESOLVE = lambda p: f'data:image/png;base64,FAKE'


class TestTitleLayout:
    def test_contains_title(self):
        html = render_title({'title': 'Hello World'}, 1, THEME, NOOP_RESOLVE)
        assert 'Hello World' in html
        assert '<section' in html

    def test_contains_tagline(self):
        html = render_title({'title': 'T', 'tagline': 'My tagline'}, 1, THEME, NOOP_RESOLVE)
        assert 'My tagline' in html

    def test_contains_subtitle(self):
        html = render_title({'title': 'T', 'subtitle': 'Sub'}, 1, THEME, NOOP_RESOLVE)
        assert 'Sub' in html

    def test_contains_footer(self):
        html = render_title({'title': 'T', 'footer': 'Footer text'}, 1, THEME, NOOP_RESOLVE)
        assert 'Footer text' in html


class TestSectionLayout:
    def test_contains_title(self):
        html = render_section({'title': 'Part 1'}, 2, THEME, NOOP_RESOLVE)
        assert 'Part 1' in html

    def test_contains_number(self):
        html = render_section({'title': 'T', 'number': '01'}, 2, THEME, NOOP_RESOLVE)
        assert '01' in html

    def test_contains_body(self):
        html = render_section({'title': 'T', 'body': 'Intro text'}, 2, THEME, NOOP_RESOLVE)
        assert 'Intro text' in html


class TestContentLayout:
    def test_body_string(self):
        html = render_content({'title': 'T', 'body': 'Some text'}, 3, THEME, NOOP_RESOLVE)
        assert 'Some text' in html

    def test_body_list_bullets(self):
        html = render_content({'title': 'T', 'body': ['A', 'B', 'C']}, 3, THEME, NOOP_RESOLVE)
        assert '<li' in html
        assert 'A' in html

    def test_body_numbered(self):
        html = render_content({'title': 'T', 'body': ['A', 'B'], 'variant': 'numbered'}, 3, THEME, NOOP_RESOLVE)
        assert '1.' in html or '<ol' in html


class TestClosingLayout:
    def test_contains_title(self):
        html = render_closing({'title': 'Thank You'}, 10, THEME, NOOP_RESOLVE)
        assert 'Thank You' in html

    def test_contains_headline(self):
        html = render_closing({'title': 'T', 'headline': 'Big ask'}, 10, THEME, NOOP_RESOLVE)
        assert 'Big ask' in html

    def test_contains_bullets(self):
        html = render_closing({'title': 'T', 'bullets': ['X', 'Y']}, 10, THEME, NOOP_RESOLVE)
        assert 'X' in html
        assert 'Y' in html

    def test_contains_contact(self):
        html = render_closing({'title': 'T', 'contact': {'email': 'a@b.com'}}, 10, THEME, NOOP_RESOLVE)
        assert 'a@b.com' in html
