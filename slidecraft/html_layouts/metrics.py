"""Metrics display layout — HTML renderer."""
from ._helpers import escape, render_slide_header, render_footer


def render(content, slide_num, theme, resolve_image):
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))

    metrics = content.get('metrics', [])
    if not metrics:
        parts.append('</section>')
        return '\n'.join(parts)

    count = min(len(metrics), 4)
    parts.append(f'<div class="sc-grid" style="grid-template-columns:repeat({count},1fr);margin-top:32px;text-align:center">')

    for metric in metrics[:4]:
        value = str(metric.get('value', ''))
        label = metric.get('label', '')
        context = metric.get('context', '')

        parts.append('<div>')
        parts.append(f'<div style="font-family:var(--font-display);font-size:44px;font-weight:700;color:var(--color-primary)">{escape(value)}</div>')
        parts.append(f'<div style="font-size:20px;color:var(--color-text-secondary);margin-top:8px">{escape(label)}</div>')
        if context:
            parts.append(f'<div style="font-size:16px;color:var(--color-text-muted);margin-top:4px">{escape(context)}</div>')
        parts.append('</div>')

    parts.append('</div>')

    # Body text (optional)
    body = content.get('body', [])
    if body:
        parts.append('<div style="margin-top:32px">')
        for line in body:
            parts.append(f'<p style="color:var(--color-text-secondary);font-size:18px;margin:0 0 6px 0">{escape(line)}</p>')
        parts.append('</div>')

    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
