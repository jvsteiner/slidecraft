# HTML Output Support for SlideCraft

> Created: 2026-03-19
> Status: Approved

## Overview

Add HTML output format to SlideCraft so presentations can be statically hosted and shared as web pages. Uses reveal.js for navigation/presentation controls. Same YAML input produces both PPTX and HTML output.

## CLI Interface

```bash
slidecraft build content.yaml output --format pptx   # default, current behavior
slidecraft build content.yaml output --format html
slidecraft build content.yaml output --format all     # generates both output.pptx and output.html
```

The `--format` flag defaults to `pptx` for backward compatibility. The output argument is treated as a stem — the appropriate extension is appended (`.pptx`, `.html`, or both for `--format all`).

For backward compatibility, if the output argument already ends with `.pptx` or `.html`, the extension is not doubled. E.g., `slidecraft build content.yaml output.pptx --format html` produces `output.html` (the stem `output` is extracted).

## Architecture

A new `HtmlBuilder` class sits alongside the existing `DeckBuilder`. Both read the same YAML via `from_yaml()`. The CLI routes to the correct builder based on `--format`.

```
YAML ──┬──▶ DeckBuilder ──▶ .pptx
       │
       └──▶ HtmlBuilder ──▶ .html
```

### Output format

Single self-contained `.html` file with:
- All CSS inlined in `<style>` tags
- reveal.js 5.1.0 loaded from CDN: `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/`
- Images base64-encoded as data URIs
- Minimal inline fallback CSS so content remains readable if the CDN is unreachable
- No other external dependencies

### File structure

```
slidecraft/
  html_builder.py          # HtmlBuilder — YAML → HTML orchestrator
  html_layouts/            # HTML layout renderers
    __init__.py            # Registry mapping layout names → render functions
    _helpers.py            # Shared HTML renderers for text zones, image zones,
                           #   slide headers, footers, slide numbers
    title.py
    section.py
    content.py
    two_col.py             # All 4 two-col variants
    three_col_equal.py     # All 4 three-col-equal variants
    three_col_wide.py      # All 4 three-col-wide variants
    comparison.py
    data_table.py
    metrics.py
    profile.py
    quote.py
    closing.py
  html_theme.py            # Theme config → CSS custom properties
```

## Theme → CSS Mapping

Theme colors and fonts map to CSS custom properties on `:root`:

```css
:root {
  --color-bg: #0F172A;
  --color-surface: #1E293B;
  --color-primary: #38BDF8;
  --color-primary-dark: #0EA5E9;
  --color-text: #F8FAFC;
  --color-text-secondary: #CBD5E1;
  --color-text-muted: #94A3B8;
  --color-text-dim: #64748B;
  --color-divider: #334155;
  --color-row-alt: #1E293B;
  --color-border: #475569;
  --color-danger: #F87171;
  --color-success: #34D399;
  --color-warning: #FBBF24;
  --font-display: "Futura", sans-serif;
  --font-body: "Avenir Next", sans-serif;
}
```

`html_theme.py` is responsible for:
- Converting the theme config dict to CSS custom property declarations
- Generating `@import` rules for Google Fonts when the font name matches a known Google Font; otherwise falling back to the font name + generic family (sans-serif)
- Producing the base slide styles (background color, font defaults)
- Generating a minimal fallback stylesheet (readable layout, system fonts) wrapped in a `<noscript><style>` block for when the CDN is unreachable

## Layout Mapping

Each of the 20 PPTX layout classes gets an HTML rendering function that produces a reveal.js `<section>` element. The mapping from PPTX primitives to HTML:

| PPTX primitive | HTML equivalent |
|---|---|
| `text_box()` | `<div>` with styled text |
| `paragraph()` / `run()` | `<p>` with `<span>` elements for mixed inline formatting (bold, color, font) |
| `accent_bar()` | `<div>` with colored background, fixed height |
| `bullets()` | `<ul>` with styled `<li>`. Structured bullets (heading + detail) use `<strong>` + `<span>` |
| `table()` | `<table>` with per-cell inline styles for color/alignment (mirrors callback-based PPTX styling) |
| `image()` | `<img>` with base64 `src` data URI |
| `rect()` | `<div>` with `background-color`, `border`, `border-radius` |
| `divider()` | `<hr>` or `<div>` with `border-top` |
| `slide_header()` | Shared helper: accent bar div + title + subtitle + slide number. Used by `_helpers.py` |
| `slide_number()` | `<span>` in bottom-right, absolutely positioned. Slide number passed to renderers. |
| Background image | `background-image` CSS on `<section>` (base64 data URI) |
| Overlay | `::after` pseudo-element with `rgba()` color + opacity |
| Column layouts | CSS Grid: `grid-template-columns` with variant fractions |
| Footer | Absolutely positioned `<div>` at bottom of section |

### Column variant mapping

| PPTX variant | CSS Grid columns | Notes |
|---|---|---|
| `50_50` | `1fr 1fr` | |
| `60_40` | `3fr 2fr` | |
| `40_60` | `2fr 3fr` | |
| Three-col equal | `1fr 1fr 1fr` | |
| Three-col wide (narrow left) | `1fr 2fr` | 2-column grid despite "three_col" name; the name refers to the narrow zone being ~1/3 width |
| Three-col wide (narrow right) | `2fr 1fr` | Same — 2-column grid with 1/3 + 2/3 split |

### Per-cell table styling

The PPTX `ComparisonLayout` and `DataTableLayout` use callback functions (`text_color_fn`, `cell_color_fn`, `align_fn`) for per-cell styling. In HTML, this translates to inline `style` attributes on `<td>` elements. The HTML layout renderers apply the same logic (highlight columns, negative value dimming, alternating row colors) directly when generating table HTML, rather than using callbacks.

## Shared HTML Helpers (`html_layouts/_helpers.py`)

Mirrors the PPTX `layouts/_helpers.py`. Provides:

- `render_text_zone(content, theme)` — renders a text zone (string or `{heading, body, bullets}` dict) to HTML
- `render_image_zone(content, resolve_image)` — renders an image zone (string path or `{image, caption}` dict) to HTML
- `render_slide_header(slide_num, title, subtitle, theme)` — accent bar + title + subtitle + slide number
- `render_footer(text)` — absolutely positioned footer div
- `escape(text)` — HTML-escapes user-provided text (`<`, `>`, `&`, quotes) to prevent rendering bugs

All user-provided text is HTML-escaped before insertion into the output.

## HtmlBuilder

### `HtmlBuilder.from_yaml(path)`

Same interface as `DeckBuilder.from_yaml()`:
- Parses YAML content file
- Stores theme config and slide data
- Stores `base_dir` for resolving image paths

### `build()`

1. Generate CSS from theme config via `html_theme.py`
2. For each slide in YAML (tracked with `slide_num` counter):
   - Resolve background image / overlay (per-slide overrides global, same logic as PPTX builder)
   - Look up HTML layout renderer by `layout` name
   - Call renderer with slide content dict, slide_num, theme, and resolve_image callback
   - Renderer returns an HTML `<section>` string
   - Builder wraps the section with background-image / overlay styles if applicable
3. Assemble full HTML document:
   - `<!DOCTYPE html>` + `<html>` wrapper
   - `<head>`: reveal.js 5.1.0 CDN links (CSS + JS), generated `<style>` block, `<noscript>` fallback styles
   - `<body>`: `<div class="reveal"><div class="slides">` + all sections
   - `<script>`: reveal.js initialization with config

### `save(path)`

Writes the assembled HTML string to the output file.

### Image handling

`resolve_image(relative_path)` reads the image file and returns a base64 data URI string:
```
data:image/jpeg;base64,/9j/4AAQ...
```

Supported formats determined by file extension:
- `.jpg`/`.jpeg` → `image/jpeg`
- `.png` → `image/png`
- `.gif` → `image/gif`
- `.webp` → `image/webp`
- `.svg` → `image/svg+xml`

Images that don't exist raise `FileNotFoundError`, same as the PPTX builder.

## HTML Layout Renderers

Each layout module exports a `render(content, slide_num, theme, resolve_image)` function that returns an HTML string (a `<section>` element with its contents).

Layout renderers receive:
- `content`: the slide's YAML data dict (same as PPTX layouts receive)
- `slide_num`: integer slide number for rendering slide numbers
- `theme`: the Theme instance for accessing colors/fonts
- `resolve_image`: callback to convert image paths to base64 data URIs

Layout renderers are pure functions that produce HTML strings. This keeps them testable and isolated.

### Background image and overlay

Handled at the builder level, same as PPTX. If a slide has `background_image`, the `<section>` gets an inline `background-image` style with `background-size: cover`. If `overlay` is present, a scoped `::after` pseudo-element is generated with `rgba()` color and opacity, `position: absolute`, and `inset: 0`.

### Footer

All layouts check for `content.get('footer')` and call the shared `render_footer()` helper to append an absolutely positioned `<div>` at the bottom of the section.

## Reveal.js Configuration

Pinned to reveal.js **5.1.0**. CDN URLs:
- CSS: `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css`
- JS: `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js`
- Theme: `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css` (overridden by our custom CSS)

Initialization config:

```javascript
Reveal.initialize({
  hash: true,
  controls: true,
  progress: true,
  center: false,
  transition: 'none',
  width: 1280,
  height: 720,
  margin: 0
});
```

- `center: false` — we handle our own positioning
- `transition: 'none'` — clean slide transitions matching PowerPoint behavior
- `width: 1280, height: 720` — 16:9 aspect ratio matching the PPTX canvas
- `hash: true` — URL hash navigation for deep linking to slides
- `margin: 0` — full-bleed slides, we handle margins in CSS

## Visual Parity

The HTML output will be structurally identical to the PPTX: same colors, fonts, proportions, content hierarchy, and layout structure. It will not be pixel-perfect — it will look like a native web presentation, not a screenshot of PowerPoint.

Differences users should expect:
- Text rendering differs between browsers and PowerPoint (kerning, line-breaking)
- Reveal.js adds navigation controls, keyboard shortcuts, and responsive scaling
- Column proportions are CSS Grid approximations of the PPTX inch-based positioning
- Table styling uses CSS rather than OOXML table formatting

## Dependencies

- No new Python dependencies — HTML generation is string templating
- reveal.js 5.1.0 loaded from CDN at runtime (no Python dependency)
- Base64 encoding uses Python's built-in `base64` module
- HTML escaping uses Python's built-in `html` module

## Backward Compatibility

- No breaking changes to existing CLI (`slidecraft build content.yaml output.pptx` still works)
- `--format` defaults to `pptx`
- YAML schema unchanged
- All 6 themes work for both output formats
- All per-layout features (background_image, overlay, footer, body) carry over to HTML — these are handled per-layout by each renderer, not globally

## Out of Scope

- Offline mode (vendoring reveal.js into the package)
- Speaker notes
- Slide transitions/animations beyond reveal.js defaults
- PDF export from HTML (reveal.js has this built-in via `?print-pdf` query param)
- Custom reveal.js plugins
