"""Three-column wide layouts (1/3 + 2/3 split) — HTML renderers."""
from ._helpers import escape, render_slide_header, render_footer, render_text_zone, render_image_zone


def _render(content, slide_num, theme, resolve_image, narrow_side, narrow_type, wide_type):
    grid_cols = '1fr 2fr' if narrow_side == 'left' else '2fr 1fr'
    narrow_content = content.get('narrow', '')
    wide_content = content.get('wide', '')

    if narrow_side == 'left':
        first_content, first_type = narrow_content, narrow_type
        second_content, second_type = wide_content, wide_type
    else:
        first_content, first_type = wide_content, wide_type
        second_content, second_type = narrow_content, narrow_type

    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))
    parts.append(f'<div class="sc-grid" style="grid-template-columns:{grid_cols};margin-top:24px;align-items:start">')

    for zone_content, ztype in [(first_content, first_type), (second_content, second_type)]:
        if ztype == 'image':
            parts.append(f'<div>{render_image_zone(zone_content, resolve_image)}</div>')
        else:
            parts.append(render_text_zone(zone_content, theme))

    parts.append('</div>')
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)


def render_image_dtext(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'left', 'image', 'text')


def render_text_dimage(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'left', 'text', 'image')


def render_dimage_text(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'right', 'text', 'image')


def render_dtext_image(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'right', 'image', 'text')
