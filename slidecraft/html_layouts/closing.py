"""Closing slide — HTML renderer."""
from ._helpers import escape, render_footer, render_slide_number


def render(content, slide_num, theme, resolve_image):
    parts = ['<section style="text-align:center">']
    parts.append('<div class="sc-center-wrap">')
    parts.append(render_slide_number(slide_num))
    parts.append('<div class="sc-accent-bar" style="margin-left:auto;margin-right:auto"></div>')
    parts.append(f'<h2 style="font-family:var(--font-display);font-size:44px;font-weight:700;color:var(--color-text);margin:0">{escape(content.get("title", ""))}</h2>')
    if content.get('headline'):
        parts.append(f'<p style="font-size:28px;font-weight:700;color:var(--color-primary);margin:14px 0 0 0">{escape(content["headline"])}</p>')
    if content.get('bullets'):
        parts.append('<ul style="list-style:none;padding:0;margin:14px auto;max-width:60%;text-align:left">')
        for b in content['bullets']:
            parts.append(f'<li style="color:var(--color-text-secondary);font-size:20px;margin-bottom:5px">\u2022 {escape(b)}</li>')
        parts.append('</ul>')
    contact = content.get('contact')
    if contact:
        contact_parts = []
        for key in ('email', 'url', 'social'):
            if contact.get(key):
                contact_parts.append(escape(contact[key]))
        if contact_parts:
            parts.append(f'<p style="color:var(--color-text-muted);font-size:16px;margin-top:18px">{" | ".join(contact_parts)}</p>')
    if content.get('closing'):
        parts.append(f'<p style="color:var(--color-text-dim);font-size:16px;margin-top:12px">{escape(content["closing"])}</p>')
    parts.append('</div>')  # close sc-center-wrap
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
