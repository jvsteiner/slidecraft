"""Tests for all layouts — verify each renders without error and produces slides."""
import pytest
from slidecraft import DeckBuilder, get_layout, list_layouts


THEME_CONFIG = {
    'font_display': 'Calibri',
    'font_body': 'Calibri',
    'colors': {
        'bg': '#FFFFFF',
        'surface': '#F5F5F5',
        'primary': '#2563EB',
    },
}


class TestLayoutRegistry:
    def test_all_12_layouts_registered(self):
        layouts = list_layouts()
        assert len(layouts) == 12

    def test_expected_layout_names(self):
        expected = {
            'title', 'section', 'content', 'two_column', 'three_column',
            'image_text', 'comparison', 'data_table', 'quote', 'profile',
            'metrics', 'closing',
        }
        assert set(list_layouts()) == expected

    def test_unknown_layout_raises(self):
        with pytest.raises(KeyError, match='Unknown layout'):
            get_layout('nonexistent')


class TestTitleLayout:
    def test_minimal(self):
        db = DeckBuilder(THEME_CONFIG)
        layout = get_layout('title')()
        layout.render(db, {'layout': 'title', 'title': 'Hello'}, 1)
        assert len(db.prs.slides) == 1

    def test_full_content(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('title')().render(db, {
            'layout': 'title',
            'title': 'Deck Title',
            'tagline': 'A great tagline',
            'subtitle': 'By Author',
            'footer': 'Confidential',
        }, 1)
        assert len(db.prs.slides) == 1


class TestSectionLayout:
    def test_minimal(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('section')().render(db, {
            'layout': 'section', 'title': 'Part One',
        }, 1)
        assert len(db.prs.slides) == 1

    def test_with_number(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('section')().render(db, {
            'layout': 'section',
            'title': 'Part One',
            'number': '01',
            'subtitle': 'Introduction',
        }, 1)
        assert len(db.prs.slides) == 1


class TestContentLayout:
    def test_text_body(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('content')().render(db, {
            'layout': 'content',
            'title': 'Overview',
            'body': 'This is a paragraph of text.',
        }, 1)
        assert len(db.prs.slides) == 1

    def test_bullet_list(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('content')().render(db, {
            'layout': 'content',
            'title': 'Key Points',
            'body': ['Point one', 'Point two', 'Point three'],
        }, 2)
        assert len(db.prs.slides) == 1

    def test_numbered_list(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('content')().render(db, {
            'layout': 'content',
            'title': 'Steps',
            'body': ['First', 'Second'],
            'variant': 'numbered',
        }, 3)
        assert len(db.prs.slides) == 1


class TestTwoColumnLayout:
    def test_string_columns(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('two_column')().render(db, {
            'layout': 'two_column',
            'title': 'Two Sides',
            'left': 'Left text',
            'right': 'Right text',
        }, 1)
        assert len(db.prs.slides) == 1

    def test_dict_columns(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('two_column')().render(db, {
            'layout': 'two_column',
            'title': 'Comparison',
            'variant': '60_40',
            'left': {
                'heading': 'Pros',
                'bullets': ['Fast', 'Simple'],
            },
            'right': {
                'heading': 'Cons',
                'body': 'Some limitations.',
            },
        }, 2)
        assert len(db.prs.slides) == 1


class TestThreeColumnLayout:
    def test_renders(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('three_column')().render(db, {
            'layout': 'three_column',
            'title': 'Three Things',
            'columns': [
                {'heading': 'One', 'body': 'First'},
                {'heading': 'Two', 'body': 'Second'},
                {'heading': 'Three', 'body': 'Third'},
            ],
        }, 1)
        assert len(db.prs.slides) == 1

    def test_with_icons(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('three_column')().render(db, {
            'layout': 'three_column',
            'title': 'Features',
            'columns': [
                {'icon': '🚀', 'heading': 'Fast', 'body': 'Very fast'},
                {'icon': '🔒', 'heading': 'Secure', 'body': 'Very secure'},
                {'icon': '💡', 'heading': 'Smart', 'body': 'Very smart'},
            ],
        }, 2)
        assert len(db.prs.slides) == 1


class TestComparisonLayout:
    def test_renders(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('comparison')().render(db, {
            'layout': 'comparison',
            'title': 'Feature Comparison',
            'headers': ['Feature', 'Us', 'Them'],
            'rows': [
                ['Speed', 'Fast', 'Slow'],
                ['Price', '$10', '$50'],
            ],
        }, 1)
        assert len(db.prs.slides) == 1

    def test_with_highlight(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('comparison')().render(db, {
            'layout': 'comparison',
            'title': 'Compare',
            'headers': ['Feature', 'Us', 'Them'],
            'rows': [['Auth', 'Yes', 'No']],
            'highlight_column': 1,
        }, 2)
        assert len(db.prs.slides) == 1


class TestDataTableLayout:
    def test_simple_table(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('data_table')().render(db, {
            'layout': 'data_table',
            'title': 'Revenue',
            'table': [
                ['Year', 'Revenue', 'Growth'],
                ['2024', '$1M', '50%'],
                ['2025', '$2M', '100%'],
            ],
        }, 1)
        assert len(db.prs.slides) == 1

    def test_with_sidebar(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('data_table')().render(db, {
            'layout': 'data_table',
            'title': 'Financials',
            'table': [
                ['Metric', 'Value'],
                ['ARR', '$1M'],
            ],
            'sidebar': {
                'title': 'Notes',
                'items': ['Growing fast', 'Profitable'],
            },
        }, 2)
        assert len(db.prs.slides) == 1


class TestQuoteLayout:
    def test_minimal(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('quote')().render(db, {
            'layout': 'quote',
            'quote': 'The best software is invisible.',
            'attribution': 'Someone Famous',
        }, 1)
        assert len(db.prs.slides) == 1

    def test_with_title_and_role(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('quote')().render(db, {
            'layout': 'quote',
            'title': 'Testimonial',
            'quote': 'Great product!',
            'attribution': 'Jane Doe',
            'role': 'CEO at Acme',
        }, 2)
        assert len(db.prs.slides) == 1


class TestProfileLayout:
    def test_single_profile(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('profile')().render(db, {
            'layout': 'profile',
            'title': 'Team',
            'profiles': [{
                'name': 'Alice',
                'role': 'CEO',
                'company': 'Acme Inc.',
                'bio': 'Founded the company in 2020.',
            }],
        }, 1)
        assert len(db.prs.slides) == 1

    def test_multiple_profiles(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('profile')().render(db, {
            'layout': 'profile',
            'title': 'Team',
            'profiles': [
                {'name': 'Alice', 'role': 'CEO'},
                {'name': 'Bob', 'role': 'CTO'},
                {'name': 'Carol', 'role': 'COO'},
            ],
        }, 2)
        assert len(db.prs.slides) == 1


class TestMetricsLayout:
    def test_single_metric(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('metrics')().render(db, {
            'layout': 'metrics',
            'title': 'Traction',
            'metrics': [
                {'value': '10K', 'label': 'Users', 'context': 'and growing'},
            ],
        }, 1)
        assert len(db.prs.slides) == 1

    def test_multiple_metrics(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('metrics')().render(db, {
            'layout': 'metrics',
            'title': 'Key Numbers',
            'metrics': [
                {'value': '$1M', 'label': 'ARR'},
                {'value': '200', 'label': 'Customers'},
                {'value': '95%', 'label': 'Retention'},
            ],
        }, 2)
        assert len(db.prs.slides) == 1


class TestClosingLayout:
    def test_minimal(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('closing')().render(db, {
            'layout': 'closing',
            'title': 'Thank You',
        }, 1)
        assert len(db.prs.slides) == 1

    def test_full(self):
        db = DeckBuilder(THEME_CONFIG)
        get_layout('closing')().render(db, {
            'layout': 'closing',
            'title': 'The Ask',
            'headline': 'Join us',
            'bullets': ['$500K raise', '200 customers'],
            'contact': {
                'email': 'hello@example.com',
                'url': 'example.com',
            },
            'closing': 'Built with care.',
        }, 10)
        assert len(db.prs.slides) == 1
