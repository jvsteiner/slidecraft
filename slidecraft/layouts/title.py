"""
TitleLayout — opening / title slide.

Content zones: title, subtitle, tagline, footer, logo
Supports center or left alignment via content['align'].
"""
from .base import BaseLayout


class TitleLayout(BaseLayout):
    name = 'title'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)
        align = content.get('align', 'center')

        # Accent bar
        bar_x = (13.333 - 0.8) / 2 if align == 'center' else m
        p.accent_bar(slide, bar_x, 2.0)

        # Title
        p.text_box(slide, m, 2.15, cw, 1.2,
                   content.get('title', ''),
                   size=72, color='text', bold=True,
                   align=align, heading=True)

        y = 3.5

        # Tagline (optional)
        if content.get('tagline'):
            p.text_box(slide, m, y, cw, 0.7,
                       content['tagline'],
                       size=36, color='primary', bold=True,
                       align=align)
            y += 0.8

        # Subtitle (optional)
        if content.get('subtitle'):
            p.text_box(slide, m, y, cw, 0.6,
                       content['subtitle'],
                       size=24, color='text_muted',
                       align=align)

        # Footer (optional)
        if content.get('footer'):
            p.text_box(slide, m, db.theme.spacing('footer_y'), cw, 0.4,
                       content['footer'],
                       size=18, color='text_dim',
                       align=align)
