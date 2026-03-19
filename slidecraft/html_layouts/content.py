"""Content body slide — HTML renderer."""
from ._helpers import escape, render_slide_header, render_footer


def render(content, slide_num, theme, resolve_image):
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))
    body = content.get('body', '')
    variant = content.get('variant')
    if isinstance(body, list):
        if variant == 'numbered':
            parts.append('<ol style="color:var(--color-text-secondary);font-size:16px;padding-left:24px;margin-top:12px">')
            for item in body:
                parts.append(f'<li style="margin-bottom:5px">{escape(item)}</li>')
            parts.append('</ol>')
        else:
            parts.append('<ul style="list-style:none;padding:0;margin-top:12px">')
            for item in body:
                parts.append(f'<li style="color:var(--color-text-secondary);font-size:16px;margin-bottom:5px">\u2022 {escape(item)}</li>')
            parts.append('</ul>')
    else:
        parts.append(f'<p style="color:var(--color-text-secondary);font-size:16px;margin-top:12px;line-height:1.5">{escape(str(body))}</p>')
    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
