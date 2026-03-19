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

    # Base slide styles
    lines.append('.reveal .slides section {')
    lines.append('  background-color: var(--color-bg);')
    lines.append('  color: var(--color-text);')
    lines.append('  font-family: var(--font-body), sans-serif;')
    lines.append('}')
    lines.append('')

    # Headings
    lines.append('.reveal .slides section h1,')
    lines.append('.reveal .slides section h2,')
    lines.append('.reveal .slides section h3 {')
    lines.append('  font-family: var(--font-display), sans-serif;')
    lines.append('  color: var(--color-text);')
    lines.append('}')
    lines.append('')

    # Utility classes
    lines.append('.sc-accent-bar {')
    lines.append('  background-color: var(--color-primary);')
    lines.append('  height: 4px;')
    lines.append('  width: 100%;')
    lines.append('}')
    lines.append('')

    lines.append('.sc-footer {')
    lines.append('  position: absolute;')
    lines.append('  bottom: 0;')
    lines.append('  left: 0;')
    lines.append('  right: 0;')
    lines.append('  font-size: 0.6em;')
    lines.append('  color: var(--color-text_muted);')
    lines.append('  padding: 0.4em 1em;')
    lines.append('}')
    lines.append('')

    lines.append('.sc-slide-num {')
    lines.append('  position: absolute;')
    lines.append('  bottom: 0.4em;')
    lines.append('  right: 1em;')
    lines.append('  font-size: 0.6em;')
    lines.append('  color: var(--color-text_dim);')
    lines.append('}')
    lines.append('')

    lines.append('.sc-header-title {')
    lines.append('  font-family: var(--font-display), sans-serif;')
    lines.append('  font-size: 2em;')
    lines.append('  font-weight: bold;')
    lines.append('  color: var(--color-text);')
    lines.append('}')
    lines.append('')

    lines.append('.sc-header-subtitle {')
    lines.append('  font-family: var(--font-display), sans-serif;')
    lines.append('  font-size: 1.2em;')
    lines.append('  color: var(--color-text_secondary);')
    lines.append('}')
    lines.append('')

    lines.append('.sc-grid {')
    lines.append('  display: grid;')
    lines.append('  gap: 1em;')
    lines.append('  width: 100%;')
    lines.append('  height: 100%;')
    lines.append('}')
    lines.append('')

    lines.append('.sc-text-zone {')
    lines.append('  padding: 1em;')
    lines.append('}')
    lines.append('')

    lines.append('.sc-img {')
    lines.append('  max-width: 100%;')
    lines.append('  height: auto;')
    lines.append('  object-fit: cover;')
    lines.append('}')
    lines.append('')

    lines.append('.sc-caption {')
    lines.append('  font-size: 0.7em;')
    lines.append('  color: var(--color-text_muted);')
    lines.append('  text-align: center;')
    lines.append('  margin-top: 0.3em;')
    lines.append('}')
    lines.append('')

    lines.append('.sc-overlay {')
    lines.append('  position: absolute;')
    lines.append('  inset: 0;')
    lines.append('  background: rgba(0, 0, 0, 0.4);')
    lines.append('}')

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
