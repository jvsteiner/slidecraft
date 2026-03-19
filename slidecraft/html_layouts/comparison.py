"""Comparison table layout — HTML renderer."""
from ._helpers import escape, render_slide_header, render_footer

NEGATIVE_VALUES = {'No', 'N/A', 'None', '-', ''}


def render(content, slide_num, theme, resolve_image):
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))

    headers = content.get('headers', [])
    rows = content.get('rows', [])
    highlight_col = content.get('highlight_column')
    table_data = [headers] + rows

    if not table_data or not table_data[0]:
        parts.append('</section>')
        return '\n'.join(parts)

    parts.append('<table style="border-collapse:collapse;width:100%;margin-top:16px">')

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

                if highlight_col is not None and col_idx == highlight_col:
                    styles.append('font-weight:700')
                    styles.append('color:var(--color-text)')
                elif str(val).strip() in NEGATIVE_VALUES:
                    styles.append('color:var(--color-text-dim)')
                else:
                    styles.append('color:var(--color-text-secondary)')

            align = 'left' if col_idx == 0 else 'center'
            styles.append(f'text-align:{align}')

            parts.append(f'<{tag} style="{";".join(styles)}">{escape(str(val))}</{tag}>')
        parts.append('</tr>')

    parts.append('</table>')

    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)
