"""Title slide — HTML renderer."""
from ._helpers import escape, render_footer


def render(content, slide_num, theme, resolve_image):
    align = content.get('align', 'center')
    title = content.get('title', '')
    tagline = content.get('tagline')
    subtitle = content.get('subtitle')
    footer = content.get('footer')

    parts = [f'<section style="text-align:{align};display:flex;flex-direction:column;justify-content:center">']
    parts.append('<div class="sc-accent-bar" style="{}"></div>'.format(
        'margin-left:auto;margin-right:auto' if align == 'center' else ''))
    title_size = '3.6em' if len(title) <= 20 else '2.7em' if len(title) <= 40 else '2.1em'
    parts.append(f'<h1 style="font-family:var(--font-display);font-size:{title_size};font-weight:700;color:var(--color-text);margin:0">{escape(title)}</h1>')
    if tagline:
        parts.append(f'<p style="font-size:1.8em;font-weight:700;color:var(--color-primary);margin:8px 0 0 0">{escape(tagline)}</p>')
    if subtitle:
        parts.append(f'<p style="font-size:1.2em;color:var(--color-text-muted);margin:8px 0 0 0">{escape(subtitle)}</p>')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
