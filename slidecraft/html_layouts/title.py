"""Title slide — HTML renderer."""
from ._helpers import escape, render_footer


def render(content, slide_num, theme, resolve_image):
    align = content.get('align', 'center')
    title = content.get('title', '')
    tagline = content.get('tagline')
    subtitle = content.get('subtitle')
    footer = content.get('footer')

    parts = [f'<section style="text-align:{align}">']
    parts.append('<div class="sc-center-wrap">')
    bar_style = 'margin-left:auto;margin-right:auto' if align == 'center' else ''
    parts.append(f'<div class="sc-accent-bar" style="{bar_style}"></div>')
    title_size = '64px' if len(title) <= 20 else '48px' if len(title) <= 40 else '38px'
    parts.append(f'<h1 style="font-family:var(--font-display);font-size:{title_size};font-weight:700;color:var(--color-text);margin:0">{escape(title)}</h1>')
    if tagline:
        parts.append(f'<p style="font-size:34px;font-weight:700;color:var(--color-primary);margin:8px 0 0 0">{escape(tagline)}</p>')
    if subtitle:
        parts.append(f'<p style="font-size:22px;color:var(--color-text-muted);margin:8px 0 0 0">{escape(subtitle)}</p>')
    parts.append('</div>')  # close sc-center-wrap
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
