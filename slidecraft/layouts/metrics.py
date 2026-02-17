"""
MetricsLayout — large hero metrics displayed horizontally.

Content zones:
    title, subtitle, metrics (list of {value, label, context})
"""
from .base import BaseLayout


class MetricsLayout(BaseLayout):
    name = 'metrics'

    def render(self, db, content: dict, slide_num: int):
        slide = db.new_slide()
        p = db.p
        m = db.theme.margin
        cw = self._content_width(db)

        y = p.slide_header(slide, slide_num,
                           content.get('title', ''),
                           content.get('subtitle'))

        metrics = content.get('metrics', [])
        if not metrics:
            return

        count = min(len(metrics), 4)
        gutter = db.theme.gutter

        if count == 1:
            # Single metric: centered
            col_width = cw * 0.5
            start_left = m + (cw - col_width) / 2
            self._render_metric(p, slide, metrics[0],
                                start_left, y + 0.5, col_width)
        else:
            # Multiple metrics: evenly spaced
            col_width = (cw - gutter * (count - 1)) / count
            for i, metric in enumerate(metrics[:4]):
                col_left = m + i * (col_width + gutter)
                self._render_metric(p, slide, metric,
                                    col_left, y + 0.5, col_width)

    def _render_metric(self, p, slide, metric, left, top, width):
        """Render a single metric block."""
        value = str(metric.get('value', ''))
        label = metric.get('label', '')
        context = metric.get('context', '')

        # Value — large bold primary
        p.text_box(slide, left, top, width, 0.9,
                   value, size=48, color='primary',
                   bold=True, heading=True, align='center')

        # Label
        p.text_box(slide, left, top + 1.0, width, 0.4,
                   label, size=18, color='text_secondary',
                   align='center')

        # Context
        if context:
            p.text_box(slide, left, top + 1.5, width, 0.4,
                       context, size=14, color='text_muted',
                       align='center')
