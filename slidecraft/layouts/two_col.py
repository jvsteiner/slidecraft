"""
Two-column layouts — 4 permutations of text and image zones.

Each supports width variants: 50_50 (default), 60_40, 40_60.

Content keys: left, right (each matches the zone type).
"""
from .base import BaseLayout
from ._helpers import render_text_zone, render_image_zone

SPLITS = {
    '50_50': (0.50, 0.50),
    '60_40': (0.60, 0.40),
    '40_60': (0.40, 0.60),
}


class _TwoColBase(BaseLayout):
    """Base for two-column layouts."""
    left_type: str = 'text'
    right_type: str = 'text'

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
        left_frac, right_frac = SPLITS.get(variant, (0.50, 0.50))

        usable = cw - gutter
        left_w = usable * left_frac
        right_w = usable * right_frac
        left_x = m
        right_x = m + left_w + gutter
        body_top = y + 0.2
        body_h = 4.5

        _render_zone(self.left_type, p, db, slide,
                     left_x, body_top, left_w, body_h,
                     content.get('left', ''))
        _render_zone(self.right_type, p, db, slide,
                     right_x, body_top, right_w, body_h,
                     content.get('right', ''))

        # Footer (optional)
        footer = content.get('footer')
        if footer:
            p.text_box(slide, m, 6.8, cw, 0.3,
                       footer, size=12, color='text_dim', align='left')


def _render_zone(zone_type, p, db, slide, x, y, w, h, content):
    if zone_type == 'image':
        render_image_zone(p, db, slide, x, y, w, h, content)
    else:
        render_text_zone(p, slide, x, y, w, h, content)


class TwoColTextText(_TwoColBase):
    name = 'two_col_text_text'
    left_type = 'text'
    right_type = 'text'


class TwoColTextImage(_TwoColBase):
    name = 'two_col_text_image'
    left_type = 'text'
    right_type = 'image'


class TwoColImageText(_TwoColBase):
    name = 'two_col_image_text'
    left_type = 'image'
    right_type = 'text'


class TwoColImageImage(_TwoColBase):
    name = 'two_col_image_image'
    left_type = 'image'
    right_type = 'image'
