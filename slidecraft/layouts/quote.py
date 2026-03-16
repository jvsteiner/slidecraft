"""
QuoteLayout — featured quote with attribution.

Content zones:
    title (optional), quote, attribution, role (optional), photo (optional),
    footer (optional)
"""
from .base import BaseLayout


class QuoteLayout(BaseLayout):
    name = 'quote'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        title = content.get('title')
        quote_text = content.get('quote', '')
        attribution = content.get('attribution', '')
        role = content.get('role')
        photo = content.get('photo')

        has_photo = photo is not None
        # Content area width shrinks if photo present
        text_width = cw * 0.65 if has_photo else cw * 0.8

        if title:
            y = p.slide_header(slide, slide_num, title)
        else:
            p.slide_number(slide, slide_num)
            # Vertically center: approximate total content height ~2.5 inches
            y = 2.2

        # Decorative opening quote mark
        p.text_box(slide, m, y - 0.2, 1.0, 1.2,
                   '\u201C', size=80, color='primary', bold=True,
                   heading=True)

        # Quote text
        quote_top = y + 0.6
        p.text_box(slide, m + 0.6, quote_top, text_width, 2.5,
                   quote_text, size=28, color='text',
                   line_spacing=1.4)

        # Attribution
        attr_y = quote_top + 2.6
        attr_text = f'\u2014 {attribution}'
        if role:
            attr_text += f', {role}'
        p.text_box(slide, m + 0.6, attr_y, text_width, 0.5,
                   attr_text, size=18, color='text_muted')

        # Optional photo on the right
        if has_photo:
            photo_path = db.resolve_path(photo)
            photo_size = 2.5
            photo_left = 13.333 - m - photo_size
            photo_top = y + 0.5
            p.image(slide, photo_path, photo_left, photo_top,
                    photo_size, photo_size)

        # Footer (optional)
        footer = content.get('footer')
        if footer:
            p.text_box(slide, m, 6.8, cw, 0.3,
                       footer, size=12, color='text_dim', align='left')
