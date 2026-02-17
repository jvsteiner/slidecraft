"""
ContentLayout — standard body slide with header and text/bullets.

Content zones: title, subtitle, body (str or list), variant
Variant: 'bullets' (default for lists), 'numbered', 'plain' (default for strings)
"""
from .base import BaseLayout


class ContentLayout(BaseLayout):
    name = 'content'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        body = content.get('body', '')
        variant = content.get('variant')

        if isinstance(body, list):
            if variant is None:
                variant = 'bullets'
            if variant == 'numbered':
                items = [f'{i+1}. {item}' for i, item in enumerate(body)]
                # Render as plain paragraphs (numbered prefix already added)
                tf = p.text_box(slide, m, y + 0.1, cw, 5.0 - y,
                                '', size=20, color='text_secondary')
                tf.paragraphs[0].text = ''
                for item in items:
                    p.paragraph(tf, item, size=20, color='text_secondary',
                                space_before=8)
            else:
                # Default bullets
                p.bullets(slide, m, y + 0.1, cw, 5.0 - y, body,
                          bullet_size=20, bullet_color='text_secondary')
        else:
            # Plain text paragraph
            p.text_box(slide, m, y + 0.1, cw, 5.0 - y,
                       str(body), size=20, color='text_secondary',
                       line_spacing=1.4)
