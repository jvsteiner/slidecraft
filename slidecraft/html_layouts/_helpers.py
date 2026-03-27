"""Shared HTML renderers for layout modules."""
import html as _html
from slidecraft.theme import Theme


def escape(text: str) -> str:
    """HTML-escape user-provided text."""
    return _html.escape(str(text))


def render_footer(text: str) -> str:
    """Render a footer div at the bottom of the slide."""
    return f'<div class="sc-footer">{escape(text)}</div>'


def render_slide_number(num: int) -> str:
    """Render a slide number in the bottom-right."""
    return f'<span class="sc-slide-num">{num}</span>'


def render_slide_header(slide_num: int, title: str, subtitle: str | None,
                        theme: Theme) -> str:
    """Render accent bar + title + optional subtitle + slide number."""
    parts = ['<div class="sc-accent-bar"></div>']
    parts.append(f'<h2 class="sc-header-title">{escape(title)}</h2>')
    if subtitle:
        parts.append(f'<p class="sc-header-subtitle">{escape(subtitle)}</p>')
    parts.append(render_slide_number(slide_num))
    return '\n'.join(parts)


def render_text_zone(content, theme: Theme, font_size=None) -> str:
    """Render a text zone: string or {heading, body, bullets}."""
    fs_attr = f' style="font-size:{font_size}px"' if font_size else ''
    if isinstance(content, str):
        return (
            f'<div class="sc-text-zone"{fs_attr}>'
            f'<p>{escape(content)}</p></div>'
        )

    if not isinstance(content, dict):
        return ''

    parts = [f'<div class="sc-text-zone"{fs_attr}>']
    if content.get('heading'):
        parts.append(f'<h3>{escape(content["heading"])}</h3>')
    if content.get('body'):
        parts.append(f'<p>{escape(content["body"])}</p>')
    elif content.get('bullets'):
        parts.append('<ul>')
        for item in content['bullets']:
            if isinstance(item, str):
                parts.append(f'<li>{escape(item)}</li>')
            elif isinstance(item, dict):
                heading = escape(item.get('heading', ''))
                detail = escape(item.get('detail', ''))
                li = f'<li><strong>{heading}</strong>'
                if detail:
                    li += (
                        f'<br><span style="color:var(--color-text-muted);'
                        f'font-size:14px">{detail}</span>'
                    )
                li += '</li>'
                parts.append(li)
        parts.append('</ul>')
    parts.append('</div>')
    return '\n'.join(parts)


def render_image_zone(content, resolve_image) -> str:
    """Render an image zone: string path or {image, caption}."""
    if isinstance(content, str):
        data_uri = resolve_image(content)
        return f'<img class="sc-img" src="{data_uri}">'

    if isinstance(content, dict):
        data_uri = resolve_image(content.get('image', ''))
        caption = content.get('caption')
        html = f'<img class="sc-img" src="{data_uri}">'
        if caption:
            html += f'\n<div class="sc-caption">{escape(caption)}</div>'
        return html

    return ''
