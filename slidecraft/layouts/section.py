"""
SectionLayout — section break / divider slide.

Content zones: title, subtitle, number
Vertically centered content with optional large section number.
"""
from .base import BaseLayout


class SectionLayout(BaseLayout):
    name = 'section'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        y = 2.5

        # Section number (optional)
        if content.get('number'):
            p.text_box(slide, m, y, cw, 1.2,
                       str(content['number']),
                       size=80, color='primary', bold=True,
                       align='center', heading=True)
            y += 1.3

        # Section title
        p.text_box(slide, m, y, cw, 1.0,
                   content.get('title', ''),
                   size=48, color='text', bold=True,
                   align='center', heading=True)
        y += 1.1

        # Subtitle (optional)
        if content.get('subtitle'):
            p.text_box(slide, m, y, cw, 0.6,
                       content['subtitle'],
                       size=24, color='text_muted',
                       align='center')
