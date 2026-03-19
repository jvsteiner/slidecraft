# HTML Output Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `--format html` to SlideCraft so the same YAML that produces PPTX can also produce a self-contained reveal.js HTML presentation.

**Architecture:** New `HtmlBuilder` class parallel to `DeckBuilder`. HTML layout renderers are pure functions (no class hierarchy) in `slidecraft/html_layouts/`. Theme maps to CSS custom properties. reveal.js 5.1.0 loaded from CDN.

**Tech Stack:** Python 3.10+, reveal.js 5.1.0 (CDN), built-in `html`, `base64`, `os` modules. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-03-19-html-output-design.md`

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `slidecraft/html_theme.py` | Create | Theme config → CSS custom properties, base slide styles, noscript fallback |
| `slidecraft/html_layouts/__init__.py` | Create | Registry mapping layout names → render functions |
| `slidecraft/html_layouts/_helpers.py` | Create | Shared renderers: text zones, image zones, slide headers, footers, escape |
| `slidecraft/html_layouts/title.py` | Create | Title slide renderer |
| `slidecraft/html_layouts/section.py` | Create | Section divider renderer |
| `slidecraft/html_layouts/content.py` | Create | Body content renderer |
| `slidecraft/html_layouts/closing.py` | Create | Closing slide renderer |
| `slidecraft/html_layouts/two_col.py` | Create | All 4 two-column variant renderers |
| `slidecraft/html_layouts/three_col_equal.py` | Create | All 4 three-col-equal variant renderers |
| `slidecraft/html_layouts/three_col_wide.py` | Create | All 4 three-col-wide variant renderers |
| `slidecraft/html_layouts/comparison.py` | Create | Comparison table renderer |
| `slidecraft/html_layouts/data_table.py` | Create | Data table renderer |
| `slidecraft/html_layouts/metrics.py` | Create | Metrics display renderer |
| `slidecraft/html_layouts/profile.py` | Create | Profile cards renderer |
| `slidecraft/html_layouts/quote.py` | Create | Quote/testimonial renderer |
| `slidecraft/html_builder.py` | Create | HtmlBuilder — YAML → HTML orchestrator |
| `slidecraft/__main__.py` | Modify | Add `--format` flag routing |
| `slidecraft/__init__.py` | Modify | Export HtmlBuilder |
| `tests/test_html_theme.py` | Create | Tests for CSS generation |
| `tests/test_html_helpers.py` | Create | Tests for shared HTML renderers |
| `tests/test_html_layouts.py` | Create | Tests for layout renderers |
| `tests/test_html_builder.py` | Create | Tests for HtmlBuilder orchestration |
| `tests/test_cli_format.py` | Create | Tests for --format flag |

---

### Task 1: HTML Theme — CSS Generation

**Files:**
- Create: `slidecraft/html_theme.py`
- Create: `tests/test_html_theme.py`

- [ ] **Step 1: Write failing tests for theme CSS generation**

```python
# tests/test_html_theme.py
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


class TestGenerateNoscriptCSS:
    def test_noscript_has_fallback_fonts(self):
        theme = Theme({})
        css = generate_noscript_css(theme)
        assert 'font-family' in css

    def test_noscript_is_minimal(self):
        theme = Theme({})
        css = generate_noscript_css(theme)
        # Should not reference reveal.js classes
        assert '.reveal' not in css
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_theme.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'slidecraft.html_theme'`

- [ ] **Step 3: Implement `html_theme.py`**

```python
# slidecraft/html_theme.py
"""Theme config → CSS custom properties for HTML output."""
from .theme import Theme, DEFAULT_COLORS


def generate_css(theme: Theme) -> str:
    """Generate complete CSS for an HTML presentation."""
    # CSS custom properties from theme
    color_vars = []
    for name in DEFAULT_COLORS:
        rgb = theme.color(name)
        color_vars.append(f'  --color-{name.replace("_", "-")}: #{rgb};')

    font_vars = [
        f'  --font-display: "{theme.font_display}", sans-serif;',
        f'  --font-body: "{theme.font_body}", sans-serif;',
    ]

    root_block = ':root {\n' + '\n'.join(color_vars + font_vars) + '\n}'

    # Base slide styles
    slide_styles = """
.reveal .slides section {
  background-color: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body);
  text-align: left;
  padding: 6% 6%;
  box-sizing: border-box;
  position: relative;
  height: 100%;
}
.reveal .slides section * { box-sizing: border-box; }
.sc-accent-bar {
  width: 60px; height: 4px;
  background: var(--color-primary);
  margin-bottom: 12px;
}
.sc-footer {
  position: absolute; bottom: 3%; left: 6%; right: 6%;
  font-size: 12px; color: var(--color-text-dim);
}
.sc-slide-num {
  position: absolute; bottom: 3%; right: 6%;
  font-size: 14px; color: var(--color-text-dim);
}
.sc-header-title {
  font-family: var(--font-display);
  font-size: 2.4em; font-weight: 700;
  color: var(--color-text);
  margin: 0 0 4px 0;
}
.sc-header-subtitle {
  font-size: 1.3em;
  color: var(--color-text-secondary);
  margin: 0;
}
.sc-grid { display: grid; gap: 24px; }
.sc-text-zone p { margin: 0 0 8px 0; }
.sc-text-zone ul { margin: 0; padding-left: 0; list-style: none; }
.sc-text-zone ul li::before { content: "\\2022 "; color: var(--color-text-secondary); }
.sc-img { max-width: 100%; height: auto; display: block; }
.sc-caption { font-size: 14px; color: var(--color-text-dim); text-align: center; margin-top: 6px; }
.sc-overlay {
  position: absolute; inset: 0; z-index: 1;
}
.sc-overlay ~ * { position: relative; z-index: 2; }
"""

    return root_block + '\n' + slide_styles


def generate_noscript_css(theme: Theme) -> str:
    """Minimal fallback CSS for when reveal.js CDN is unreachable."""
    rgb = theme.color('bg')
    text_rgb = theme.color('text')
    return f"""
section {{ display: block; padding: 40px; margin: 20px auto; max-width: 960px;
  background: #{rgb}; color: #{text_rgb};
  font-family: system-ui, -apple-system, sans-serif; }}
section + section {{ border-top: 1px solid #ccc; }}
"""
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_theme.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_theme.py tests/test_html_theme.py && git commit -m "feat: add html_theme.py — theme config to CSS generation"
```

---

### Task 2: Shared HTML Helpers

**Files:**
- Create: `slidecraft/html_layouts/__init__.py` (empty initially)
- Create: `slidecraft/html_layouts/_helpers.py`
- Create: `tests/test_html_helpers.py`

- [ ] **Step 1: Create the `html_layouts` package directory**

```bash
mkdir -p /Users/jamie/Code/martin/slide-skill/slidecraft/html_layouts
touch /Users/jamie/Code/martin/slide-skill/slidecraft/html_layouts/__init__.py
```

- [ ] **Step 2: Write failing tests for helpers**

```python
# tests/test_html_helpers.py
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_helpers.py -v`
Expected: FAIL — `ImportError`

- [ ] **Step 4: Implement `_helpers.py`**

```python
# slidecraft/html_layouts/_helpers.py
"""Shared HTML renderers for layout modules."""
import html as _html
from slidecraft.theme import Theme


def escape(text: str) -> str:
    """HTML-escape user-provided text."""
    return _html.escape(str(text))


def render_footer(text: str) -> str:
    """Render a footer div at the bottom of the slide."""
    return f'<div class="sc-footer">{escape(text)}</div>'


def render_slide_number(num: int) -> str:
    """Render a slide number in the bottom-right."""
    return f'<span class="sc-slide-num">{num}</span>'


def render_slide_header(slide_num: int, title: str, subtitle: str | None,
                        theme: Theme) -> str:
    """Render accent bar + title + optional subtitle + slide number."""
    parts = ['<div class="sc-accent-bar"></div>']
    parts.append(f'<h2 class="sc-header-title">{escape(title)}</h2>')
    if subtitle:
        parts.append(f'<p class="sc-header-subtitle">{escape(subtitle)}</p>')
    parts.append(render_slide_number(slide_num))
    return '\n'.join(parts)


def render_text_zone(content, theme: Theme) -> str:
    """Render a text zone: string or {heading, body, bullets}."""
    if isinstance(content, str):
        return f'<div class="sc-text-zone"><p style="color:var(--color-text-secondary)">{escape(content)}</p></div>'

    if not isinstance(content, dict):
        return ''

    parts = ['<div class="sc-text-zone">']
    if content.get('heading'):
        parts.append(f'<h3 style="color:var(--color-primary);font-weight:700">{escape(content["heading"])}</h3>')
    if content.get('body'):
        parts.append(f'<p style="color:var(--color-text-secondary)">{escape(content["body"])}</p>')
    elif content.get('bullets'):
        parts.append('<ul>')
        for item in content['bullets']:
            if isinstance(item, str):
                parts.append(f'<li>{escape(item)}</li>')
            elif isinstance(item, dict):
                heading = escape(item.get('heading', ''))
                detail = escape(item.get('detail', ''))
                li = f'<li><strong>{heading}</strong>'
                if detail:
                    li += f'<br><span style="color:var(--color-text-muted);font-size:0.9em">{detail}</span>'
                li += '</li>'
                parts.append(li)
        parts.append('</ul>')
    parts.append('</div>')
    return '\n'.join(parts)


def render_image_zone(content, resolve_image) -> str:
    """Render an image zone: string path or {image, caption}."""
    if isinstance(content, str):
        data_uri = resolve_image(content)
        return f'<img class="sc-img" src="{data_uri}">'

    if isinstance(content, dict):
        data_uri = resolve_image(content.get('image', ''))
        caption = content.get('caption')
        html = f'<img class="sc-img" src="{data_uri}">'
        if caption:
            html += f'\n<div class="sc-caption">{escape(caption)}</div>'
        return html

    return ''
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_helpers.py -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_layouts/ tests/test_html_helpers.py && git commit -m "feat: add HTML layout helpers — text zones, image zones, headers, footers"
```

---

### Task 3: Core Layout Renderers — Title, Section, Content, Closing

**Files:**
- Create: `slidecraft/html_layouts/title.py`
- Create: `slidecraft/html_layouts/section.py`
- Create: `slidecraft/html_layouts/content.py`
- Create: `slidecraft/html_layouts/closing.py`
- Create: `tests/test_html_layouts.py`

- [ ] **Step 1: Write failing tests for the 4 core layouts**

```python
# tests/test_html_layouts.py
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
        assert '<li>' in html
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement the 4 layout renderers**

Create each file. Every renderer is a `render(content, slide_num, theme, resolve_image)` function returning an HTML `<section>` string. Use helpers from `_helpers.py` for escape, footer, slide_number, slide_header.

Reference the corresponding PPTX layout files for exact content keys:
- `title.py` keys: `title`, `tagline`, `subtitle`, `footer`, `align`
- `section.py` keys: `number`, `title`, `subtitle`, `body`, `footer`
- `content.py` keys: `title`, `subtitle`, `body` (str or list), `variant`, `footer`
- `closing.py` keys: `title`, `headline`, `bullets`, `contact`, `closing`, `footer`

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_layouts/title.py slidecraft/html_layouts/section.py slidecraft/html_layouts/content.py slidecraft/html_layouts/closing.py tests/test_html_layouts.py && git commit -m "feat: add HTML renderers for title, section, content, closing"
```

---

### Task 4: Column Layout Renderers

**Files:**
- Create: `slidecraft/html_layouts/two_col.py`
- Create: `slidecraft/html_layouts/three_col_equal.py`
- Create: `slidecraft/html_layouts/three_col_wide.py`
- Modify: `tests/test_html_layouts.py` (append tests)

- [ ] **Step 1: Write failing tests for column layouts**

Append to `tests/test_html_layouts.py`:

```python
from slidecraft.html_layouts.two_col import (
    render_text_text, render_text_image, render_image_text, render_image_image,
)
from slidecraft.html_layouts.three_col_equal import render_text_text_text
from slidecraft.html_layouts.three_col_wide import render_image_dtext


class TestTwoColLayouts:
    def test_text_text_has_grid(self):
        content = {'title': 'T', 'left': 'Left text', 'right': 'Right text'}
        html = render_text_text(content, 1, THEME, NOOP_RESOLVE)
        assert 'Left text' in html
        assert 'Right text' in html
        assert 'grid' in html

    def test_variant_60_40(self):
        content = {'title': 'T', 'variant': '60_40', 'left': 'L', 'right': 'R'}
        html = render_text_text(content, 1, THEME, NOOP_RESOLVE)
        assert '3fr 2fr' in html

    def test_text_image(self):
        content = {'title': 'T', 'left': 'Text', 'right': 'photo.png'}
        html = render_text_image(content, 1, THEME, NOOP_RESOLVE)
        assert 'Text' in html
        assert '<img' in html

    def test_footer_in_two_col(self):
        content = {'title': 'T', 'left': 'L', 'right': 'R', 'footer': 'Src'}
        html = render_text_text(content, 1, THEME, NOOP_RESOLVE)
        assert 'Src' in html


class TestThreeColEqualLayouts:
    def test_three_text_columns(self):
        content = {'title': 'T', 'left': 'L', 'center': 'C', 'right': 'R'}
        html = render_text_text_text(content, 1, THEME, NOOP_RESOLVE)
        assert 'L' in html and 'C' in html and 'R' in html
        assert '1fr 1fr 1fr' in html


class TestThreeColWideLayouts:
    def test_image_dtext(self):
        content = {'title': 'T', 'narrow': 'photo.png', 'wide': 'Wide text'}
        html = render_image_dtext(content, 1, THEME, NOOP_RESOLVE)
        assert '<img' in html
        assert 'Wide text' in html
        assert '1fr 2fr' in html
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v -k "TwoCol or ThreeCol"`
Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement column renderers**

Each file exports named render functions (e.g., `render_text_text`, `render_text_image`). Use CSS Grid with `grid-template-columns` for column splits. Reference PPTX layouts for content keys:

- `two_col.py`: keys `left`, `right`, `variant` (50_50/60_40/40_60). Variant → grid columns mapping: `{'50_50': '1fr 1fr', '60_40': '3fr 2fr', '40_60': '2fr 3fr'}`
- `three_col_equal.py`: keys `left`, `center`, `right`. Grid: `1fr 1fr 1fr`
- `three_col_wide.py`: keys `narrow`, `wide`. Grid: `1fr 2fr` or `2fr 1fr` depending on `narrow_side`

Use `render_text_zone()` and `render_image_zone()` from `_helpers.py` for zone content.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_layouts/two_col.py slidecraft/html_layouts/three_col_equal.py slidecraft/html_layouts/three_col_wide.py tests/test_html_layouts.py && git commit -m "feat: add HTML renderers for two-col and three-col layouts"
```

---

### Task 5: Data Layout Renderers — Comparison, DataTable, Metrics

**Files:**
- Create: `slidecraft/html_layouts/comparison.py`
- Create: `slidecraft/html_layouts/data_table.py`
- Create: `slidecraft/html_layouts/metrics.py`
- Modify: `tests/test_html_layouts.py` (append tests)

- [ ] **Step 1: Write failing tests for data layouts**

Append to `tests/test_html_layouts.py`:

```python
from slidecraft.html_layouts.comparison import render as render_comparison
from slidecraft.html_layouts.data_table import render as render_data_table
from slidecraft.html_layouts.metrics import render as render_metrics


class TestComparisonLayout:
    def test_renders_table(self):
        content = {
            'title': 'Compare',
            'headers': ['', 'Us', 'Them'],
            'rows': [['Speed', '5ms', '200ms']],
        }
        html = render_comparison(content, 1, THEME, NOOP_RESOLVE)
        assert '<table' in html
        assert 'Us' in html
        assert '5ms' in html

    def test_highlight_column(self):
        content = {
            'title': 'T',
            'headers': ['', 'Us', 'Them'],
            'rows': [['A', 'B', 'C']],
            'highlight_column': 1,
        }
        html = render_comparison(content, 1, THEME, NOOP_RESOLVE)
        assert 'font-weight' in html  # highlighted col has bold


class TestDataTableLayout:
    def test_renders_table(self):
        content = {
            'title': 'Data',
            'table': [['Q', 'Rev'], ['Q1', '$1M']],
        }
        html = render_data_table(content, 1, THEME, NOOP_RESOLVE)
        assert '<table' in html
        assert 'Q1' in html

    def test_sidebar(self):
        content = {
            'title': 'T',
            'table': [['A'], ['B']],
            'sidebar': {'title': 'Notes', 'items': ['Note 1']},
        }
        html = render_data_table(content, 1, THEME, NOOP_RESOLVE)
        assert 'Notes' in html
        assert 'Note 1' in html


class TestMetricsLayout:
    def test_renders_metrics(self):
        content = {
            'title': 'KPIs',
            'metrics': [
                {'value': '99%', 'label': 'Uptime'},
                {'value': '42', 'label': 'Regions'},
            ],
        }
        html = render_metrics(content, 1, THEME, NOOP_RESOLVE)
        assert '99%' in html
        assert 'Uptime' in html

    def test_renders_body_and_footer(self):
        content = {
            'title': 'T',
            'metrics': [{'value': '1', 'label': 'L'}],
            'body': ['Line 1', 'Line 2'],
            'footer': 'Source note',
        }
        html = render_metrics(content, 1, THEME, NOOP_RESOLVE)
        assert 'Line 1' in html
        assert 'Source note' in html
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v -k "Comparison or DataTable or Metrics"`
Expected: FAIL

- [ ] **Step 3: Implement data layout renderers**

Reference PPTX layouts for content keys and per-cell styling logic:
- `comparison.py` keys: `headers`, `rows`, `highlight_column`, `footer`. Per-cell: bold highlight column, dim negative values (`No`, `N/A`, `None`, `-`, ``).
- `data_table.py` keys: `table`, `col_widths`, `highlight_row`, `sidebar` (`{title, items}`), `footer`. Alternating row colors.
- `metrics.py` keys: `metrics` (list of `{value, label, context}`), `body` (list of strings), `footer`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_layouts/comparison.py slidecraft/html_layouts/data_table.py slidecraft/html_layouts/metrics.py tests/test_html_layouts.py && git commit -m "feat: add HTML renderers for comparison, data_table, metrics"
```

---

### Task 6: People Layout Renderers — Profile, Quote

**Files:**
- Create: `slidecraft/html_layouts/profile.py`
- Create: `slidecraft/html_layouts/quote.py`
- Modify: `tests/test_html_layouts.py` (append tests)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_html_layouts.py`:

```python
from slidecraft.html_layouts.profile import render as render_profile
from slidecraft.html_layouts.quote import render as render_quote


class TestProfileLayout:
    def test_single_profile(self):
        content = {
            'title': 'Team',
            'profiles': [{'name': 'Alice', 'role': 'CEO', 'bio': 'Founded it.'}],
        }
        html = render_profile(content, 1, THEME, NOOP_RESOLVE)
        assert 'Alice' in html
        assert 'CEO' in html

    def test_grid_profiles(self):
        content = {
            'title': 'Team',
            'profiles': [
                {'name': 'A', 'role': 'R1'},
                {'name': 'B', 'role': 'R2'},
            ],
        }
        html = render_profile(content, 1, THEME, NOOP_RESOLVE)
        assert 'A' in html and 'B' in html


class TestQuoteLayout:
    def test_renders_quote(self):
        content = {'quote': 'Great product!', 'attribution': 'Jane Doe'}
        html = render_quote(content, 1, THEME, NOOP_RESOLVE)
        assert 'Great product!' in html
        assert 'Jane Doe' in html

    def test_renders_role(self):
        content = {'quote': 'Q', 'attribution': 'J', 'role': 'CTO'}
        html = render_quote(content, 1, THEME, NOOP_RESOLVE)
        assert 'CTO' in html
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v -k "Profile or Quote"`
Expected: FAIL

- [ ] **Step 3: Implement profile and quote renderers**

Reference PPTX layouts:
- `profile.py` keys: `profiles` (list of `{name, role, company, bio, photo}`), `footer`. Single profile = large card. 2-4 = grid (CSS Grid columns).
- `quote.py` keys: `title`, `quote`, `attribution`, `role`, `photo`, `footer`. Decorative open-quote character `\u201C`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_layouts/profile.py slidecraft/html_layouts/quote.py tests/test_html_layouts.py && git commit -m "feat: add HTML renderers for profile and quote layouts"
```

---

### Task 7: HTML Layout Registry

**Files:**
- Modify: `slidecraft/html_layouts/__init__.py`

- [ ] **Step 1: Write failing test**

Append to `tests/test_html_layouts.py`:

```python
from slidecraft.html_layouts import get_html_layout, list_html_layouts


class TestHtmlLayoutRegistry:
    def test_all_20_layouts_registered(self):
        assert len(list_html_layouts()) == 20

    def test_get_title(self):
        fn = get_html_layout('title')
        assert callable(fn)

    def test_get_two_col_text_text(self):
        fn = get_html_layout('two_col_text_text')
        assert callable(fn)

    def test_unknown_raises(self):
        with pytest.raises(KeyError):
            get_html_layout('nonexistent')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py::TestHtmlLayoutRegistry -v`
Expected: FAIL

- [ ] **Step 3: Implement the registry**

```python
# slidecraft/html_layouts/__init__.py
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_layouts.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_layouts/__init__.py tests/test_html_layouts.py && git commit -m "feat: add HTML layout registry — 20 layouts registered"
```

---

### Task 8: HtmlBuilder — YAML → HTML Orchestrator

**Files:**
- Create: `slidecraft/html_builder.py`
- Create: `tests/test_html_builder.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_html_builder.py
"""Tests for HtmlBuilder — YAML to HTML orchestration."""
import os
import pytest
import tempfile
import yaml
from slidecraft.html_builder import HtmlBuilder


MINIMAL_YAML = {
    'theme': {'colors': {'bg': '#000000', 'text': '#FFFFFF'}},
    'slides': [
        {'layout': 'title', 'title': 'Test Deck'},
        {'layout': 'content', 'title': 'Slide 2', 'body': 'Hello'},
    ],
}


@pytest.fixture
def yaml_path(tmp_path):
    p = tmp_path / 'content.yaml'
    p.write_text(yaml.dump(MINIMAL_YAML))
    return str(p)


class TestHtmlBuilderFromYaml:
    def test_loads_yaml(self, yaml_path):
        hb = HtmlBuilder.from_yaml(yaml_path)
        assert hb.slides_content is not None
        assert len(hb.slides_content) == 2


class TestHtmlBuilderBuild:
    def test_build_produces_html(self, yaml_path):
        hb = HtmlBuilder.from_yaml(yaml_path)
        html = hb.build()
        assert '<!DOCTYPE html>' in html
        assert 'reveal' in html
        assert 'Test Deck' in html
        assert 'Hello' in html

    def test_build_contains_css_variables(self, yaml_path):
        hb = HtmlBuilder.from_yaml(yaml_path)
        html = hb.build()
        assert '--color-bg' in html

    def test_build_contains_revealjs_init(self, yaml_path):
        hb = HtmlBuilder.from_yaml(yaml_path)
        html = hb.build()
        assert 'Reveal.initialize' in html


class TestHtmlBuilderSave:
    def test_save_writes_file(self, yaml_path, tmp_path):
        hb = HtmlBuilder.from_yaml(yaml_path)
        hb.build()
        out = str(tmp_path / 'output.html')
        hb.save(out)
        assert os.path.isfile(out)
        with open(out) as f:
            assert '<!DOCTYPE html>' in f.read()


class TestResolveImage:
    def test_resolves_png(self, tmp_path):
        # Create a tiny 1x1 PNG
        import base64
        png_bytes = base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
        )
        img_path = tmp_path / 'test.png'
        img_path.write_bytes(png_bytes)

        yaml_content = {
            'theme': {},
            'slides': [{'layout': 'title', 'title': 'T'}],
        }
        yp = tmp_path / 'content.yaml'
        yp.write_text(yaml.dump(yaml_content))

        hb = HtmlBuilder.from_yaml(str(yp))
        data_uri = hb.resolve_image('test.png')
        assert data_uri.startswith('data:image/png;base64,')

    def test_missing_image_raises(self, yaml_path):
        hb = HtmlBuilder.from_yaml(yaml_path)
        with pytest.raises(FileNotFoundError):
            hb.resolve_image('nonexistent.jpg')
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_builder.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `html_builder.py`**

```python
# slidecraft/html_builder.py
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
                    # Convert hex to rgba
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                    overlay_div = (f'<div class="sc-overlay" style="'
                                   f'background:rgba({r},{g},{b},{opacity})"></div>')
                    section_html = section_html.replace(
                        '<section', f'<section', 1)
                    # Insert overlay after opening tag
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_builder.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/html_builder.py tests/test_html_builder.py && git commit -m "feat: add HtmlBuilder — YAML to HTML orchestrator with reveal.js"
```

---

### Task 9: CLI — Add `--format` Flag

**Files:**
- Modify: `slidecraft/__main__.py`
- Modify: `slidecraft/__init__.py`
- Create: `tests/test_cli_format.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_cli_format.py
"""Tests for CLI --format flag."""
import os
import pytest
import yaml
import tempfile
import subprocess
import sys


MINIMAL_YAML = {
    'theme': {},
    'slides': [{'layout': 'title', 'title': 'CLI Test'}],
}


@pytest.fixture
def yaml_file(tmp_path):
    p = tmp_path / 'content.yaml'
    p.write_text(yaml.dump(MINIMAL_YAML))
    return str(p)


class TestOutputStemExtraction:
    """Test that output path stem is correctly extracted."""
    from slidecraft.__main__ import _extract_stem

    def test_plain_stem(self):
        assert self._extract_stem('output') == 'output'

    def test_strips_pptx(self):
        assert self._extract_stem('output.pptx') == 'output'

    def test_strips_html(self):
        assert self._extract_stem('output.html') == 'output'

    def test_preserves_path(self):
        assert self._extract_stem('/tmp/my/output.pptx') == '/tmp/my/output'

    def test_preserves_other_ext(self):
        assert self._extract_stem('report.final') == 'report.final'


class TestFormatFlag:
    def test_default_produces_pptx(self, yaml_file, tmp_path):
        out = str(tmp_path / 'out')
        subprocess.run([sys.executable, '-m', 'slidecraft', 'build',
                        yaml_file, out], check=True)
        assert os.path.isfile(out + '.pptx')

    def test_format_html(self, yaml_file, tmp_path):
        out = str(tmp_path / 'out')
        subprocess.run([sys.executable, '-m', 'slidecraft', 'build',
                        yaml_file, out, '--format', 'html'], check=True)
        assert os.path.isfile(out + '.html')

    def test_format_all(self, yaml_file, tmp_path):
        out = str(tmp_path / 'out')
        subprocess.run([sys.executable, '-m', 'slidecraft', 'build',
                        yaml_file, out, '--format', 'all'], check=True)
        assert os.path.isfile(out + '.pptx')
        assert os.path.isfile(out + '.html')
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_cli_format.py -v`
Expected: FAIL

- [ ] **Step 3: Update `__main__.py`**

```python
# slidecraft/__main__.py
"""CLI entry point: python3 -m slidecraft build <content.yaml> [output] [--format pptx|html|all]"""
import os
import sys
from .builder import DeckBuilder
from .html_builder import HtmlBuilder


def _extract_stem(path: str) -> str:
    """Extract output stem, stripping .pptx or .html extension if present."""
    for ext in ('.pptx', '.html'):
        if path.endswith(ext):
            return path[:-len(ext)]
    return path


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 -m slidecraft build <content.yaml> [output] [--format pptx|html|all]')
        print('       python3 -m slidecraft layouts')
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'layouts':
        from .layouts import list_layouts
        print('Available layouts:')
        for name in list_layouts():
            print(f'  - {name}')
        return

    if cmd == 'build':
        if len(sys.argv) < 3:
            print('Usage: python3 -m slidecraft build <content.yaml> [output] [--format pptx|html|all]')
            sys.exit(1)

        content_path = sys.argv[2]
        output_raw = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 'output'

        # Parse --format flag
        fmt = 'pptx'
        for i, arg in enumerate(sys.argv):
            if arg == '--format' and i + 1 < len(sys.argv):
                fmt = sys.argv[i + 1]

        stem = _extract_stem(output_raw)

        if fmt in ('pptx', 'all'):
            db = DeckBuilder.from_yaml(content_path)
            db.build()
            db.save(stem + '.pptx')

        if fmt in ('html', 'all'):
            hb = HtmlBuilder.from_yaml(content_path)
            hb.build()
            hb.save(stem + '.html')

        return

    print(f'Unknown command: {cmd}')
    print('Commands: build, layouts')
    sys.exit(1)


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Update `__init__.py` to export HtmlBuilder**

Add `HtmlBuilder` to the public API:

```python
# Add to slidecraft/__init__.py
from .html_builder import HtmlBuilder
# Update __all__ to include HtmlBuilder
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_cli_format.py -v`
Expected: All PASS

- [ ] **Step 6: Run full test suite**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest -v`
Expected: All tests pass (existing + new)

- [ ] **Step 7: Commit**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add slidecraft/__main__.py slidecraft/__init__.py tests/test_cli_format.py && git commit -m "feat: add --format flag to CLI — supports pptx, html, all"
```

---

### Task 10: Integration Test — Full YAML → HTML

**Files:**
- Modify: `tests/test_html_builder.py` (append integration test)

- [ ] **Step 1: Write integration test using a real template YAML**

Append to `tests/test_html_builder.py`:

```python
class TestIntegrationWithTemplate:
    def test_midnight_template_builds_html(self):
        """Build the midnight template as HTML — exercises all layout types."""
        template_path = os.path.join(
            os.path.dirname(__file__), '..', 'templates', 'midnight', 'content.yaml')
        if not os.path.isfile(template_path):
            pytest.skip('Template not found')
        hb = HtmlBuilder.from_yaml(template_path)
        html = hb.build()
        assert '<!DOCTYPE html>' in html
        assert 'Voxel' in html  # title from midnight template
        assert '<section' in html
```

- [ ] **Step 2: Run integration test**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest tests/test_html_builder.py::TestIntegrationWithTemplate -v`
Expected: PASS

- [ ] **Step 3: Manual visual check**

```bash
cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && python -m slidecraft build templates/midnight/content.yaml /tmp/midnight --format html && echo "Open /tmp/midnight.html in browser to check"
```

- [ ] **Step 4: Run full test suite one final time**

Run: `cd /Users/jamie/Code/martin/slide-skill && source .venv/bin/activate && pytest -v`
Expected: All PASS

- [ ] **Step 5: Commit and push**

```bash
cd /Users/jamie/Code/martin/slide-skill && git add tests/test_html_builder.py && git commit -m "test: add integration test — full YAML to HTML pipeline" && git push origin main
```
