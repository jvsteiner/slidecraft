"""
HTML Theme — convert a Theme instance to CSS custom properties and utility styles.

Used by the HTML preview renderer to apply slide deck theming via CSS variables.
"""
from slidecraft.theme import DEFAULT_COLORS, Theme


# All theme color names that get mapped to CSS custom properties
COLOR_NAMES = list(DEFAULT_COLORS.keys())


def generate_css(theme: Theme) -> str:
    """Generate full CSS string with custom properties and utility classes."""
    lines = []

    # :root block with CSS custom properties
    lines.append(':root {')
    for name in COLOR_NAMES:
        hex_val = str(theme.color(name))
        lines.append(f'  --color-{name}: #{hex_val};')
    lines.append(f'  --font-display: "{theme.font_display}";')
    lines.append(f'  --font-body: "{theme.font_body}";')
    lines.append('}')
    lines.append('')

    # Override reveal.js defaults
    lines.append("""
body, .reveal { background-color: var(--color-bg) !important; }
.reveal .slides section {
  background-color: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body), sans-serif;
  font-size: 24px;
  line-height: 1.4;
  text-align: left;
  padding: 40px 50px;
  box-sizing: border-box;
  overflow: hidden;
  height: 720px !important;
}
.reveal .slides section * { box-sizing: border-box; }

/* Vertical centering wrapper — use inside <section>, never flex on section itself */
.sc-center-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  width: 100%;
}

/* Reset reveal.js heading defaults */
.reveal .slides section h1,
.reveal .slides section h2,
.reveal .slides section h3,
.reveal .slides section h4 {
  font-family: var(--font-display), sans-serif;
  color: var(--color-text);
  text-transform: none;
  letter-spacing: normal;
  text-shadow: none;
  word-wrap: break-word;
  margin: 0;
}
.reveal .slides section p { margin: 0; }
.reveal .slides section ul,
.reveal .slides section ol { margin: 0; }

/* Accent bar */
.sc-accent-bar {
  background-color: var(--color-primary);
  height: 4px;
  width: 60px;
  margin-bottom: 10px;
  flex-shrink: 0;
}

/* Footer */
.sc-footer {
  position: absolute;
  bottom: 20px;
  left: 56px;
  right: 56px;
  font-size: 12px;
  color: var(--color-text_muted);
}

/* Slide number */
.sc-slide-num {
  position: absolute;
  bottom: 20px;
  right: 56px;
  font-size: 13px;
  color: var(--color-text_dim);
}

/* Slide header */
.sc-header-title {
  font-family: var(--font-display), sans-serif;
  font-size: 40px;
  font-weight: bold;
  color: var(--color-text);
  margin: 0 0 4px 0;
}
.sc-header-subtitle {
  font-size: 22px;
  color: var(--color-text_secondary);
  margin: 0 0 16px 0;
}

/* Grid */
.sc-grid {
  display: grid;
  gap: 20px;
  width: 100%;
}

/* Text zones */
.sc-text-zone { }
.sc-text-zone h3 {
  font-family: var(--font-display), sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 10px 0;
}
.sc-text-zone p {
  font-size: 20px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin: 0 0 8px 0;
}
.sc-text-zone ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sc-text-zone ul li {
  font-size: 20px;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
  line-height: 1.4;
}
.sc-text-zone ul li::before {
  content: "\\2022 ";
}

/* Images */
.sc-img {
  max-width: 100%;
  max-height: 100%;
  height: auto;
  object-fit: cover;
  display: block;
}
.sc-caption {
  font-size: 12px;
  color: var(--color-text_muted);
  text-align: center;
  margin-top: 4px;
}

/* Overlay for background images */
.sc-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
}
.sc-overlay ~ * { position: relative; z-index: 2; }

/* Tables */
.sc-table {
  border-collapse: collapse;
  width: 100%;
  font-size: 14px;
}
.sc-table th,
.sc-table td {
  padding: 8px 14px;
  text-align: left;
}
.sc-table th {
  font-weight: 700;
  color: var(--color-primary);
  background: var(--color-surface);
}
""")

    return '\n'.join(lines)


def generate_noscript_css(theme: Theme) -> str:
    """Generate minimal fallback CSS for noscript environments."""
    lines = []
    lines.append('body {')
    lines.append('  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,')
    lines.append('               "Helvetica Neue", Arial, sans-serif;')
    lines.append(f'  color: #{theme.color("text")};')
    lines.append(f'  background-color: #{theme.color("bg")};')
    lines.append('}')
    lines.append('')
    lines.append('h1, h2, h3 {')
    lines.append('  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,')
    lines.append('               "Helvetica Neue", Arial, sans-serif;')
    lines.append(f'  color: #{theme.color("text")};')
    lines.append('}')
    lines.append('')
    lines.append('img {')
    lines.append('  max-width: 100%;')
    lines.append('  height: auto;')
    lines.append('}')
    return '\n'.join(lines)
