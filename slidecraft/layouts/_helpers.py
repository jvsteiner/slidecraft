"""
Shared zone renderers for column layouts.

Two zone types:
  - text: heading + body text or bullet list
  - image: image file with optional caption
"""


def render_text_zone(p, slide, x, y, width, height, content):
    """Render a text zone: optional heading + body/bullets.

    Content can be:
      - str: plain paragraph
      - dict: {heading, body, bullets}
    """
    if isinstance(content, str):
        p.text_box(slide, x, y, width, height, content,
                   size=18, color='text_secondary', line_spacing=1.4)
        return
    if not isinstance(content, dict):
        return

    zone_y = y
    if content.get('heading'):
        p.text_box(slide, x, zone_y, width, 0.5,
                   content['heading'], size=22, color='primary', bold=True)
        zone_y += 0.55

    remaining = height - (zone_y - y)

    if content.get('body'):
        p.text_box(slide, x, zone_y, width, remaining,
                   content['body'], size=18, color='text_secondary',
                   line_spacing=1.4)
    elif content.get('bullets'):
        p.bullets(slide, x, zone_y, width, remaining,
                  content['bullets'], bullet_size=18,
                  bullet_color='text_secondary')


def render_image_zone(p, db, slide, x, y, width, height, content):
    """Render an image zone: image with optional caption.

    Content can be:
      - str: image path (relative to YAML file)
      - dict: {image, caption}
    """
    if isinstance(content, str):
        img_path = db.resolve_path(content)
        caption = None
    elif isinstance(content, dict):
        img_path = db.resolve_path(content.get('image', ''))
        caption = content.get('caption')
    else:
        return

    img_h = height - (0.5 if caption else 0)
    p.image(slide, img_path, x, y, width, img_h)

    if caption:
        p.text_box(slide, x, y + img_h + 0.1, width, 0.4,
                   caption, size=14, color='text_dim', align='center')
