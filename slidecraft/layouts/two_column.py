"""
TwoColumnLayout — two-column body with header.

Content zones: title, subtitle, left, right, variant
Variant: '50_50' (default), '60_40', '40_60'
Each column can be a string or dict with heading/body/bullets keys.
"""
from .base import BaseLayout

SPLIT_MAP = {
    '50_50': (0.50, 0.50),
    '60_40': (0.60, 0.40),
    '40_60': (0.40, 0.60),
}


class TwoColumnLayout(BaseLayout):
    name = 'two_column'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)
        gutter = db.theme.gutter

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        variant = content.get('variant', '50_50')
        left_frac, right_frac = SPLIT_MAP.get(variant, (0.50, 0.50))

        usable = cw - gutter
        left_w = usable * left_frac
        right_w = usable * right_frac

        left_x = m
        right_x = m + left_w + gutter

        self._render_column(p, slide, left_x, y + 0.2, left_w, content.get('left', ''))
        self._render_column(p, slide, right_x, y + 0.2, right_w, content.get('right', ''))

    @staticmethod
    def _render_column(p, slide, x, y, width, col_content):
        """Render a single column. Content can be a string or dict."""
        if isinstance(col_content, str):
            p.text_box(slide, x, y, width, 4.5,
                       col_content, size=18, color='text_secondary',
                       line_spacing=1.4)
            return

        col_y = y
        if col_content.get('heading'):
            p.text_box(slide, x, col_y, width, 0.5,
                       col_content['heading'],
                       size=22, color='primary', bold=True)
            col_y += 0.55

        if col_content.get('body'):
            p.text_box(slide, x, col_y, width, 3.5,
                       col_content['body'],
                       size=18, color='text_secondary',
                       line_spacing=1.4)
            col_y += 0.6

        if col_content.get('bullets'):
            p.bullets(slide, x, col_y, width, 3.5,
                      col_content['bullets'],
                      bullet_size=18, bullet_color='text_secondary')
