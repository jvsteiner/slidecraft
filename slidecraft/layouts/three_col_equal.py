"""
Three-column equal-width layouts — 4 permutations.

Three equal-width columns, each either text or image.
Content keys: left, center, right.
"""
from .base import BaseLayout
from ._helpers import render_text_zone, render_image_zone


class _ThreeColEqualBase(BaseLayout):
    """Base for equal-width three-column layouts."""
    zone_types: tuple = ('text', 'text', 'text')

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)
        gutter = db.theme.gutter

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        col_w = (cw - 2 * gutter) / 3
        body_top = y + 0.2
        body_h = 4.5

        keys = ('left', 'center', 'right')
        for i, (key, zone_type) in enumerate(zip(keys, self.zone_types)):
            col_x = m + i * (col_w + gutter)
            col_content = content.get(key, '')
            if zone_type == 'image':
                render_image_zone(p, db, slide, col_x, body_top,
                                  col_w, body_h, col_content)
            else:
                render_text_zone(p, slide, col_x, body_top,
                                 col_w, body_h, col_content)


class ThreeColTextTextText(_ThreeColEqualBase):
    name = 'three_col_text_text_text'
    zone_types = ('text', 'text', 'text')


class ThreeColTextImageText(_ThreeColEqualBase):
    name = 'three_col_text_image_text'
    zone_types = ('text', 'image', 'text')


class ThreeColImageTextText(_ThreeColEqualBase):
    name = 'three_col_image_text_text'
    zone_types = ('image', 'text', 'text')


class ThreeColTextTextImage(_ThreeColEqualBase):
    name = 'three_col_text_text_image'
    zone_types = ('text', 'text', 'image')
