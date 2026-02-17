"""
CLI entry point: python3 -m slidecraft build content.yaml output.pptx
"""
import sys
from .builder import DeckBuilder


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 -m slidecraft build <content.yaml> [output.pptx]')
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
            print('Usage: python3 -m slidecraft build <content.yaml> [output.pptx]')
            sys.exit(1)
        content_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else 'output.pptx'

        db = DeckBuilder.from_yaml(content_path)
        db.build()
        db.save(output_path)
        return

    print(f'Unknown command: {cmd}')
    print('Commands: build, layouts')
    sys.exit(1)


if __name__ == '__main__':
    main()
