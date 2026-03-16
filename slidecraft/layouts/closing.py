"""
ClosingLayout — closing slide with CTA and contact info.

Content zones:
    title, headline, bullets (optional), contact (optional),
    closing (optional), footer (optional)
"""
from .base import BaseLayout


class ClosingLayout(BaseLayout):
    name = 'closing'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        p.slide_number(slide, slide_num)

        title = content.get('title', '')
        headline = content.get('headline', '')
        bullets = content.get('bullets')
        contact = content.get('contact')
        closing_text = content.get('closing')

        center_x = 13.333 / 2

        # Accent bar centered above title
        bar_width = 0.8
        bar_left = center_x - bar_width / 2
        y = 1.8
        p.accent_bar(slide, bar_left, y, width=bar_width)

        # Title
        y += 0.25
        p.text_box(slide, m, y, cw, 0.9,
                   title, size=48, color='text',
                   bold=True, heading=True, align='center')

        # Headline
        y += 1.0
        if headline:
            p.text_box(slide, m, y, cw, 0.7,
                       headline, size=30, color='primary',
                       bold=True, align='center')
            y += 0.8

        # Bullets (left-aligned within centered content area)
        if bullets:
            bullet_width = cw * 0.6
            bullet_left = m + (cw - bullet_width) / 2
            y += 0.2
            p.bullets(slide, bullet_left, y, bullet_width, 2.0,
                      items=bullets,
                      bullet_size=18, bullet_color='text_secondary')
            y += 0.4 * len(bullets) + 0.3

        # Contact info
        if contact:
            contact_y = max(y + 0.3, 5.5)
            parts = []
            if contact.get('email'):
                parts.append(contact['email'])
            if contact.get('url'):
                parts.append(contact['url'])
            if contact.get('social'):
                parts.append(contact['social'])
            if parts:
                p.text_box(slide, m, contact_y, cw, 0.4,
                           '  |  '.join(parts),
                           size=16, color='text_muted', align='center')

        # Closing tagline
        if closing_text:
            p.text_box(slide, m, 6.5, cw, 0.4,
                       closing_text, size=16, color='text_dim',
                       align='center')

        # Footer (optional)
        footer = content.get('footer')
        if footer:
            p.text_box(slide, m, 6.8, cw, 0.3,
                       footer, size=12, color='text_dim', align='center')
