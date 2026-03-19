"""Quote/testimonial layout — HTML renderer."""
from ._helpers import escape, render_slide_header, render_slide_number, render_footer


def render(content, slide_num, theme, resolve_image):
    title = content.get('title')
    quote_text = content.get('quote', '')
    attribution = content.get('attribution', '')
    role = content.get('role')
    photo = content.get('photo')
    footer_text = content.get('footer')

    has_photo = photo is not None

    parts = ['<section>']

    if title:
        parts.append(render_slide_header(slide_num, title, None, theme))
    else:
        parts.append(render_slide_number(slide_num))

    content_style = 'margin-top:32px' if title else 'display:flex;flex-direction:column;justify-content:center;min-height:60%'
    parts.append(f'<div style="{content_style}">')

    if has_photo:
        parts.append('<div style="display:flex;gap:32px;align-items:start">')
        parts.append('<div style="flex:1">')

    # Decorative quote mark
    parts.append(f'<div style="font-size:4em;color:var(--color-primary);font-weight:700;line-height:1;margin-bottom:-8px">\u201C</div>')
    # Quote text
    parts.append(f'<p style="font-size:1.4em;color:var(--color-text);line-height:1.5;margin:0 0 16px 24px">{escape(quote_text)}</p>')
    # Attribution
    attr_text = f'\u2014 {escape(attribution)}'
    if role:
        attr_text += f', {escape(role)}'
    parts.append(f'<p style="color:var(--color-text-muted);font-size:0.9em;margin:0 0 0 24px">{attr_text}</p>')

    if has_photo:
        parts.append('</div>')  # close text column
        data_uri = resolve_image(photo)
        parts.append(f'<img src="{data_uri}" style="width:200px;height:200px;object-fit:cover;border-radius:8px;flex-shrink:0">')
        parts.append('</div>')  # close flex container

    parts.append('</div>')

    if footer_text:
        parts.append(render_footer(footer_text))
    parts.append('</section>')
    return '\n'.join(parts)
