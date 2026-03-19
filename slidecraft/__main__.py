"""CLI entry point: python3 -m slidecraft build <content.yaml> [output] [--format pptx|html|all]"""
import os
import sys
from .builder import DeckBuilder
from .html_builder import HtmlBuilder


def _extract_stem(path: str) -> str:
    """Extract output stem, stripping .pptx or .html extension if present."""
    for ext in ('.pptx', '.html'):
        if path.endswith(ext):
            return path[:-len(ext)]
    return path


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 -m slidecraft build <content.yaml> [output] [--format pptx|html|all]')
        print('       python3 -m slidecraft layouts')
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'layouts':
        from .layouts import list_layouts
        print('Available layouts:')
        for name in list_layouts():
            print(f'  - {name}')
        return

    if cmd == 'build':
        if len(sys.argv) < 3:
            print('Usage: python3 -m slidecraft build <content.yaml> [output] [--format pptx|html|all]')
            sys.exit(1)

        content_path = sys.argv[2]
        output_raw = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 'output'

        # Parse --format flag
        fmt = 'pptx'
        for i, arg in enumerate(sys.argv):
            if arg == '--format' and i + 1 < len(sys.argv):
                fmt = sys.argv[i + 1]

        stem = _extract_stem(output_raw)

        if fmt in ('pptx', 'all'):
            db = DeckBuilder.from_yaml(content_path)
            db.build()
            db.save(stem + '.pptx')

        if fmt in ('html', 'all'):
            hb = HtmlBuilder.from_yaml(content_path)
            hb.build()
            hb.save(stem + '.html')

        return

    print(f'Unknown command: {cmd}')
    print('Commands: build, layouts')
    sys.exit(1)


if __name__ == '__main__':
    main()
