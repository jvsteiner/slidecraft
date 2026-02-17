"""Tests for DeckBuilder — YAML parsing and end-to-end build."""
import os
import tempfile
import pytest
from slidecraft import DeckBuilder


MINIMAL_YAML = """\
theme:
  font_display: Helvetica Neue
  font_body: Helvetica Neue

slides:
  - layout: title
    title: Test Deck
  - layout: content
    title: Slide Two
    body: Some content here.
"""


class TestFromYaml:
    def test_loads_content(self, tmp_path):
        yaml_file = tmp_path / 'content.yaml'
        yaml_file.write_text(MINIMAL_YAML)
        db = DeckBuilder.from_yaml(str(yaml_file))
        assert db.content is not None
        assert len(db.slides_content) == 2

    def test_resolve_path(self, tmp_path):
        yaml_file = tmp_path / 'content.yaml'
        yaml_file.write_text(MINIMAL_YAML)
        db = DeckBuilder.from_yaml(str(yaml_file))
        resolved = db.resolve_path('images/photo.jpg')
        assert resolved == os.path.join(str(tmp_path), 'images/photo.jpg')


class TestBuild:
    def test_builds_all_slides(self, tmp_path):
        yaml_file = tmp_path / 'content.yaml'
        yaml_file.write_text(MINIMAL_YAML)
        db = DeckBuilder.from_yaml(str(yaml_file))
        db.build()
        assert len(db.prs.slides) == 2

    def test_save_creates_file(self, tmp_path):
        yaml_file = tmp_path / 'content.yaml'
        yaml_file.write_text(MINIMAL_YAML)
        output = str(tmp_path / 'output.pptx')
        db = DeckBuilder.from_yaml(str(yaml_file))
        db.build()
        db.save(output)
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0

    def test_missing_layout_key_raises(self, tmp_path):
        bad_yaml = "theme: {}\nslides:\n  - title: No Layout\n"
        yaml_file = tmp_path / 'bad.yaml'
        yaml_file.write_text(bad_yaml)
        db = DeckBuilder.from_yaml(str(yaml_file))
        with pytest.raises(ValueError, match="missing 'layout'"):
            db.build()

    def test_unknown_layout_raises(self, tmp_path):
        bad_yaml = "theme: {}\nslides:\n  - layout: fake_layout\n    title: X\n"
        yaml_file = tmp_path / 'bad.yaml'
        yaml_file.write_text(bad_yaml)
        db = DeckBuilder.from_yaml(str(yaml_file))
        with pytest.raises(KeyError, match='Unknown layout'):
            db.build()


class TestNewSlide:
    def test_adds_slide_with_bg(self):
        db = DeckBuilder({'colors': {'bg': '#000000'}})
        slide = db.new_slide()
        assert slide is not None
        assert len(db.prs.slides) == 1

    def test_custom_bg_color(self):
        db = DeckBuilder({'colors': {'bg': '#FF0000', 'surface': '#00FF00'}})
        slide = db.new_slide(bg='surface')
        assert slide is not None


class TestDictSlides:
    """Test that slides can be specified as a dict (named slides)."""

    def test_dict_slides_format(self, tmp_path):
        yaml_content = """\
theme: {}
slides:
  intro:
    layout: title
    title: Hello
  body:
    layout: content
    title: Content
    body: Text here.
"""
        yaml_file = tmp_path / 'content.yaml'
        yaml_file.write_text(yaml_content)
        db = DeckBuilder.from_yaml(str(yaml_file))
        db.build()
        assert len(db.prs.slides) == 2
