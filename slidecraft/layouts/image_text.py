"""
ImageTextLayout — image beside text body.

Content zones: title, image, text (str or list), caption, variant
Variant: 'image_left' (default), 'image_right'
Image takes ~45% width, text ~50%, with gutter between.
"""
from .base import BaseLayout


class ImageTextLayout(BaseLayout):
    name = 'image_text'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)
        gutter = db.theme.gutter

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        variant = content.get('variant', 'image_left')
        img_w = cw * 0.45
        txt_w = cw * 0.50

        if variant == 'image_right':
            txt_x = m
            img_x = m + txt_w + gutter
        else:
            img_x = m
            txt_x = m + img_w + gutter

        body_top = y + 0.2
        img_h = 4.0

        # Image
        if content.get('image'):
            img_path = db.resolve_path(content['image'])
            p.image(slide, img_path, img_x, body_top, img_w, img_h)

        # Caption (optional, below image)
        if content.get('caption'):
            p.text_box(slide, img_x, body_top + img_h + 0.1, img_w, 0.4,
                       content['caption'],
                       size=14, color='text_dim', align='center')

        # Text body
        text = content.get('text', '')
        if isinstance(text, list):
            p.bullets(slide, txt_x, body_top, txt_w, 4.5,
                      text, bullet_size=18, bullet_color='text_secondary')
        else:
            p.text_box(slide, txt_x, body_top, txt_w, 4.5,
                       str(text), size=18, color='text_secondary',
                       line_spacing=1.4)
