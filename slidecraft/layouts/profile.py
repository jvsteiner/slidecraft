"""
ProfileLayout — team member or speaker profiles.

Content zones:
    title, profiles (list of {photo, name, role, bio, company}),
    footer (optional)
"""
from .base import BaseLayout


class ProfileLayout(BaseLayout):
    name = 'profile'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        profiles = content.get('profiles', [])
        if not profiles:
            return

        if len(profiles) == 1:
            self._render_single(db, slide, profiles[0], m, y, cw)
        else:
            self._render_grid(db, slide, profiles, m, y, cw)

        # Footer (optional)
        footer = content.get('footer')
        if footer:
            p.text_box(slide, m, 6.8, cw, 0.3,
                       footer, size=12, color='text_dim', align='left')

    def _render_single(self, db, slide, profile, m, y, cw):
        """Large single-profile layout: photo left, info right."""
        p = db.p
        gutter = db.theme.gutter

        photo_size = 3.0
        photo_top = y + 0.3

        # Photo on the left
        photo_path = profile.get('photo')
        if photo_path:
            resolved = db.resolve_path(photo_path)
            p.image(slide, resolved, m, photo_top, photo_size, photo_size)

        # Text on the right
        text_left = m + photo_size + gutter
        text_width = cw - photo_size - gutter
        text_top = photo_top

        # Name
        p.text_box(slide, text_left, text_top, text_width, 0.6,
                   profile.get('name', ''), size=32, color='text',
                   bold=True, heading=True)

        # Role
        role_y = text_top + 0.55
        p.text_box(slide, text_left, role_y, text_width, 0.4,
                   profile.get('role', ''), size=20, color='primary',
                   bold=True)

        # Company
        company = profile.get('company')
        info_y = role_y + 0.4
        if company:
            p.text_box(slide, text_left, info_y, text_width, 0.4,
                       company, size=18, color='text_muted')
            info_y += 0.4

        # Bio
        bio = profile.get('bio')
        if bio:
            p.text_box(slide, text_left, info_y + 0.2, text_width, 2.0,
                       bio, size=18, color='text_secondary',
                       line_spacing=1.4)

    def _render_grid(self, db, slide, profiles, m, y, cw):
        """Grid layout for 2-4 profiles."""
        p = db.p
        gutter = db.theme.gutter
        count = min(len(profiles), 4)

        col_width = (cw - gutter * (count - 1)) / count
        photo_size = min(col_width * 0.6, 1.8)

        for i, profile in enumerate(profiles[:4]):
            col_left = m + i * (col_width + gutter)
            # Center photo in column
            photo_left = col_left + (col_width - photo_size) / 2
            photo_top = y + 0.3

            # Photo
            photo_path = profile.get('photo')
            if photo_path:
                resolved = db.resolve_path(photo_path)
                p.image(slide, resolved, photo_left, photo_top,
                        photo_size, photo_size)

            # Name below photo
            name_top = photo_top + photo_size + 0.2
            p.text_box(slide, col_left, name_top, col_width, 0.4,
                       profile.get('name', ''), size=20, color='text',
                       bold=True, heading=True, align='center')

            # Role
            role_top = name_top + 0.4
            p.text_box(slide, col_left, role_top, col_width, 0.3,
                       profile.get('role', ''), size=16, color='primary',
                       align='center')

            # Company
            company = profile.get('company')
            if company:
                comp_top = role_top + 0.3
                p.text_box(slide, col_left, comp_top, col_width, 0.3,
                           company, size=14, color='text_muted',
                           align='center')
