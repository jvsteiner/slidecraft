"""
ThreeColumnLayout — three equal columns with card backgrounds.

Content zones: title, subtitle, columns (list of 3 dicts)
Each column dict: heading, body, icon (optional emoji/text)
"""
from .base import BaseLayout


class ThreeColumnLayout(BaseLayout):
    name = 'three_column'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        pr = db.p
        m = db.theme.margin
        cw = self._content_width(db)
        gutter = db.theme.gutter

        y = pr.slide_header(slide, slide_num,
                            content.get('title', ''),
                            content.get('subtitle'))

        columns = content.get('columns', [])
        col_w = (cw - 2 * gutter) / 3
        card_top = y + 0.2
        card_h = 4.2

        for i, col in enumerate(columns[:3]):
            col_x = m + i * (col_w + gutter)

            # Card background
            pr.rect(slide, col_x, card_top, col_w, card_h,
                    fill='surface', border='border')

            inner_x = col_x + 0.25
            inner_w = col_w - 0.5
            inner_y = card_top + 0.3

            # Icon (optional)
            if col.get('icon'):
                pr.text_box(slide, inner_x, inner_y, inner_w, 0.5,
                            col['icon'],
                            size=32, align='center')
                inner_y += 0.6

            # Heading
            if col.get('heading'):
                pr.text_box(slide, inner_x, inner_y, inner_w, 0.5,
                            col['heading'],
                            size=20, color='primary', bold=True,
                            align='center')
                inner_y += 0.55

            # Body
            if col.get('body'):
                pr.text_box(slide, inner_x, inner_y, inner_w, card_h - (inner_y - card_top) - 0.3,
                            col['body'],
                            size=16, color='text_secondary',
                            align='center', line_spacing=1.4)
