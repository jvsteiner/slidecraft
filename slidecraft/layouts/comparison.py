"""
ComparisonLayout — side-by-side comparison table.

Content zones:
    title, subtitle, headers (list), rows (list of lists),
    highlight_column (optional int), footer (optional)
"""
from .base import BaseLayout


class ComparisonLayout(BaseLayout):
    name = 'comparison'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        headers = content.get('headers', [])
        rows = content.get('rows', [])
        highlight_col = content.get('highlight_column')

        # Build table data: header row + data rows
        table_data = [headers] + rows
        if not table_data or not table_data[0]:
            return

        num_cols = len(headers)
        col_widths = [cw / num_cols] * num_cols

        negative_values = {'No', 'N/A', 'None', '-', ''}

        def text_color_fn(row_idx, col_idx, val):
            if row_idx == 0:
                return 'primary'
            if highlight_col is not None and col_idx == highlight_col:
                return 'text'
            if str(val).strip() in negative_values:
                return 'text_dim'
            return 'text_secondary'

        def cell_color_fn(row_idx, col_idx, val):
            # Default table styling handles this
            return None

        def align_fn(row_idx, col_idx):
            if col_idx == 0:
                return 'left'
            return 'center'

        table_height = min(0.4 * len(table_data), 7.5 - y - 0.5)

        tbl_shape = p.table(slide, m, y + 0.2, cw, table_height,
                            table_data, col_widths=col_widths,
                            header_color='primary',
                            text_color_fn=text_color_fn,
                            align_fn=align_fn,
                            font_size=16)

        # Bold the highlight column values
        if highlight_col is not None:
            tbl = tbl_shape.table
            for row_idx in range(1, len(table_data)):
                cell = tbl.cell(row_idx, highlight_col)
                for para in cell.text_frame.paragraphs:
                    para.font.bold = True

        # Footer (optional)
        footer = content.get('footer')
        if footer:
            p.text_box(slide, m, 6.8, cw, 0.3,
                       footer, size=12, color='text_dim', align='left')
