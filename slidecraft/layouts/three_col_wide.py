"""
Three-column double-width layouts — 4 permutations.

One narrow zone (1/3 width) and one wide zone (2/3 width).
Content keys: narrow, wide.
"""
from .base import BaseLayout
from ._helpers import render_text_zone, render_image_zone


class _ThreeColWideBase(BaseLayout):
    """Base for 1/3 + 2/3 layouts."""
    narrow_side: str = 'left'   # 'left' or 'right'
    narrow_type: str = 'text'   # 'text' or 'image'
    wide_type: str = 'text'     # 'text' or 'image'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)
        gutter = db.theme.gutter

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        narrow_w = (cw - gutter) / 3
        wide_w = (cw - gutter) * 2 / 3
        body_top = y + 0.2
        body_h = 4.5

        if self.narrow_side == 'left':
            narrow_x = m
            wide_x = m + narrow_w + gutter
        else:
            wide_x = m
            narrow_x = m + wide_w + gutter

        narrow_content = content.get('narrow', '')
        wide_content = content.get('wide', '')

        if self.narrow_type == 'image':
            render_image_zone(p, db, slide, narrow_x, body_top,
                              narrow_w, body_h, narrow_content)
        else:
            render_text_zone(p, slide, narrow_x, body_top,
                             narrow_w, body_h, narrow_content)

        if self.wide_type == 'image':
            render_image_zone(p, db, slide, wide_x, body_top,
                              wide_w, body_h, wide_content)
        else:
            render_text_zone(p, slide, wide_x, body_top,
                             wide_w, body_h, wide_content)

        # Footer (optional)
        footer = content.get('footer')
        if footer:
            p.text_box(slide, m, 6.8, cw, 0.3,
                       footer, size=12, color='text_dim', align='left')


class ThreeColImageDtext(_ThreeColWideBase):
    name = 'three_col_image_dtext'
    narrow_side = 'left'
    narrow_type = 'image'
    wide_type = 'text'


class ThreeColTextDimage(_ThreeColWideBase):
    name = 'three_col_text_dimage'
    narrow_side = 'left'
    narrow_type = 'text'
    wide_type = 'image'


class ThreeColDimageText(_ThreeColWideBase):
    name = 'three_col_dimage_text'
    narrow_side = 'right'
    narrow_type = 'text'
    wide_type = 'image'


class ThreeColDtextImage(_ThreeColWideBase):
    name = 'three_col_dtext_image'
    narrow_side = 'right'
    narrow_type = 'image'
    wide_type = 'text'
