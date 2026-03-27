"""Three-column equal-width layouts — HTML renderers."""
from ._helpers import escape, render_slide_header, render_footer, render_text_zone, render_image_zone


def _render(content, slide_num, theme, resolve_image, zone_types):
    keys = ('left', 'center', 'right')
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))
    parts.append('<div class="sc-grid" style="grid-template-columns:1fr 1fr 1fr;margin-top:24px;align-items:start">')
    font_size = content.get('font_size')
    for key, ztype in zip(keys, zone_types):
        zone_content = content.get(key, '')
        if ztype == 'image':
            parts.append(f'<div>{render_image_zone(zone_content, resolve_image)}</div>')
        else:
            parts.append(render_text_zone(zone_content, theme, font_size=font_size))
    parts.append('</div>')
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)


def render_text_text_text(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, ('text', 'text', 'text'))


def render_text_image_text(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, ('text', 'image', 'text'))


def render_image_text_text(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, ('image', 'text', 'text'))


def render_text_text_image(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, ('text', 'text', 'image'))
