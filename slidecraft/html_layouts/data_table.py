"""Data table layout — HTML renderer."""
from ._helpers import escape, render_slide_header, render_footer


def render(content, slide_num, theme, resolve_image):
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))

    table_data = content.get('table', [])
    sidebar = content.get('sidebar')
    highlight_row = content.get('highlight_row')
    footer_text = content.get('footer')

    if not table_data:
        parts.append('</section>')
        return '\n'.join(parts)

    if sidebar:
        parts.append('<div class="sc-grid" style="grid-template-columns:3fr 2fr;margin-top:16px;align-items:start">')

    # Table
    parts.append('<table style="border-collapse:collapse;width:100%">')
    for row_idx, row in enumerate(table_data):
        parts.append('<tr>')
        for col_idx, val in enumerate(row):
            tag = 'th' if row_idx == 0 else 'td'
            styles = ['padding:10px 16px']

            if row_idx == 0:
                styles.append('font-weight:700')
                styles.append('color:var(--color-primary)')
                styles.append('background:var(--color-surface)')
            else:
                bg = 'var(--color-row-alt)' if row_idx % 2 == 0 else 'var(--color-bg)'
                styles.append(f'background:{bg}')

                if highlight_row is not None and row_idx == highlight_row:
                    styles.append('font-weight:700')
                    styles.append('font-size:1.1em')
                    styles.append('color:var(--color-primary)')
                else:
                    styles.append('color:var(--color-text-secondary)')

            align = 'left' if col_idx == 0 else 'center'
            styles.append(f'text-align:{align}')

            parts.append(f'<{tag} style="{";".join(styles)}">{escape(str(val))}</{tag}>')
        parts.append('</tr>')
    parts.append('</table>')

    # Sidebar
    if sidebar:
        parts.append('<div style="background:var(--color-surface);border:1px solid var(--color-border);border-radius:8px;padding:16px">')
        if sidebar.get('title'):
            parts.append(f'<h4 style="color:var(--color-primary);font-weight:700;margin:0 0 12px 0">{escape(sidebar["title"])}</h4>')
        if sidebar.get('items'):
            parts.append('<ul style="list-style:none;padding:0;margin:0">')
            for item in sidebar['items']:
                parts.append(f'<li style="color:var(--color-text-secondary);margin-bottom:6px">\u2022 {escape(item)}</li>')
            parts.append('</ul>')
        parts.append('</div>')
        parts.append('</div>')  # close grid

    if footer_text:
        parts.append(render_footer(footer_text))
    parts.append('</section>')
    return '\n'.join(parts)
