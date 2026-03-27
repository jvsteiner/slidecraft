"""Two-column layouts — HTML renderers."""
from ._helpers import escape, render_slide_header, render_footer, render_text_zone, render_image_zone

SPLITS = {
    '50_50': '1fr 1fr',
    '60_40': '3fr 2fr',
    '40_60': '2fr 3fr',
}


def _render(content, slide_num, theme, resolve_image, left_type, right_type):
    variant = content.get('variant', '50_50')
    grid_cols = SPLITS.get(variant, '1fr 1fr')

    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))
    parts.append(f'<div class="sc-grid" style="grid-template-columns:{grid_cols};margin-top:24px;align-items:start">')

    font_size = content.get('font_size')
    left_content = content.get('left', '')
    right_content = content.get('right', '')

    if left_type == 'image':
        parts.append(f'<div>{render_image_zone(left_content, resolve_image)}</div>')
    else:
        parts.append(render_text_zone(left_content, theme, font_size=font_size))

    if right_type == 'image':
        parts.append(f'<div>{render_image_zone(right_content, resolve_image)}</div>')
    else:
        parts.append(render_text_zone(right_content, theme, font_size=font_size))

    parts.append('</div>')
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)


def render_text_text(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'text', 'text')


def render_text_image(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'text', 'image')


def render_image_text(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'image', 'text')


def render_image_image(content, slide_num, theme, resolve_image):
    return _render(content, slide_num, theme, resolve_image, 'image', 'image')
