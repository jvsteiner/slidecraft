"""Section divider slide — HTML renderer."""
from ._helpers import escape, render_footer


def render(content, slide_num, theme, resolve_image):
    parts = ['<section style="text-align:center">']
    parts.append('<div class="sc-center-wrap">')
    if content.get('number'):
        parts.append(f'<div style="font-family:var(--font-display);font-size:72px;font-weight:700;color:var(--color-primary)">{escape(str(content["number"]))}</div>')
    parts.append(f'<h2 style="font-family:var(--font-display);font-size:44px;font-weight:700;color:var(--color-text);margin:0">{escape(content.get("title", ""))}</h2>')
    if content.get('subtitle'):
        parts.append(f'<p style="font-size:22px;color:var(--color-text-muted);margin:8px 0 0 0">{escape(content["subtitle"])}</p>')
    if content.get('body'):
        parts.append(f'<p style="font-size:20px;color:var(--color-text-secondary);margin:14px auto 0 auto;max-width:70%;line-height:1.5">{escape(content["body"])}</p>')
    parts.append('</div>')  # close sc-center-wrap
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
