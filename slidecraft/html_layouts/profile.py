"""Profile cards layout — HTML renderer."""
from ._helpers import escape, render_slide_header, render_footer


def render(content, slide_num, theme, resolve_image):
    parts = ['<section>']
    parts.append(render_slide_header(slide_num, content.get('title', ''), content.get('subtitle'), theme))

    profiles = content.get('profiles', [])
    if not profiles:
        parts.append('</section>')
        return '\n'.join(parts)

    if len(profiles) == 1:
        _render_single(parts, profiles[0], resolve_image)
    else:
        _render_grid(parts, profiles[:4], resolve_image)

    footer = content.get('footer')
    if footer:
        parts.append(render_footer(footer))
    parts.append('</section>')
    return '\n'.join(parts)


def _render_single(parts, profile, resolve_image):
    parts.append('<div style="display:flex;gap:32px;margin-top:24px;align-items:start">')
    # Photo
    photo = profile.get('photo')
    if photo:
        data_uri = resolve_image(photo)
        parts.append(f'<img src="{data_uri}" style="width:200px;height:200px;object-fit:cover;border-radius:8px;flex-shrink:0">')
    # Info
    parts.append('<div>')
    parts.append(f'<h3 style="font-family:var(--font-display);font-size:1.6em;font-weight:700;color:var(--color-text);margin:0">{escape(profile.get("name", ""))}</h3>')
    parts.append(f'<p style="color:var(--color-primary);font-weight:700;font-size:1em;margin:4px 0 0 0">{escape(profile.get("role", ""))}</p>')
    if profile.get('company'):
        parts.append(f'<p style="color:var(--color-text-muted);font-size:0.9em;margin:4px 0 0 0">{escape(profile["company"])}</p>')
    if profile.get('bio'):
        parts.append(f'<p style="color:var(--color-text-secondary);font-size:0.9em;margin:12px 0 0 0;line-height:1.5">{escape(profile["bio"])}</p>')
    parts.append('</div>')
    parts.append('</div>')


def _render_grid(parts, profiles, resolve_image):
    count = len(profiles)
    parts.append(f'<div class="sc-grid" style="grid-template-columns:repeat({count},1fr);margin-top:24px;text-align:center">')
    for profile in profiles:
        parts.append('<div>')
        photo = profile.get('photo')
        if photo:
            data_uri = resolve_image(photo)
            parts.append(f'<img src="{data_uri}" style="width:120px;height:120px;object-fit:cover;border-radius:50%;margin:0 auto 12px auto;display:block">')
        parts.append(f'<div style="font-family:var(--font-display);font-weight:700;color:var(--color-text)">{escape(profile.get("name", ""))}</div>')
        parts.append(f'<div style="color:var(--color-primary);font-size:0.85em">{escape(profile.get("role", ""))}</div>')
        if profile.get('company'):
            parts.append(f'<div style="color:var(--color-text-muted);font-size:0.75em">{escape(profile["company"])}</div>')
        parts.append('</div>')
    parts.append('</div>')
