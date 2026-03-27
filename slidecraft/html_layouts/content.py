"""Content body slide — HTML renderer."""
from ._helpers import escape, render_slide_header, render_footer


def render(content, slide_num, theme, resolve_image):
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))
    body = content.get('body', '')
    variant = content.get('variant')
    font_size = content.get('font_size', 20)
    if isinstance(body, list):
        if variant == 'numbered':
            parts.append(f'<ol style="color:var(--color-text-secondary);font-size:{font_size}px;padding-left:28px;margin-top:14px">')
            for item in body:
                parts.append(f'<li style="margin-bottom:6px">{escape(item)}</li>')
            parts.append('</ol>')
        else:
            parts.append('<ul style="list-style:none;padding:0;margin-top:14px">')
            for item in body:
                parts.append(f'<li style="color:var(--color-text-secondary);font-size:{font_size}px;margin-bottom:6px">\u2022 {escape(item)}</li>')
            parts.append('</ul>')
    else:
        parts.append(f'<p style="color:var(--color-text-secondary);font-size:{font_size}px;margin-top:14px;line-height:1.5">{escape(str(body))}</p>')
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
