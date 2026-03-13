# Background Image Support for SlideCraft

> Created: 2026-03-13
> Status: Approved

## Overview

Add support for background images on slides, configurable at the global theme level (applies to all slides) and per-slide (overrides the global default). Includes an optional semi-transparent color overlay for text readability.

## YAML Schema

### Global default (theme level)

```yaml
theme:
  font_display: "Fraunces 72pt"
  font_body: "Outfit"
  background_image: "images/default-bg.jpg"
  overlay:
    color: "#000000"
    opacity: 0.4
  colors:
    bg: "#0D0D0F"
    ...
```

### Per-slide override

```yaml
slides:
  - layout: title
    title: "Welcome"
    background_image: "images/hero.jpg"
    overlay:
      color: "#000000"
      opacity: 0.6

  - layout: content
    title: "Details"
    background_image: null    # explicitly disable, falls back to solid color
```

### Resolution rules

- `background_image` at theme level applies to all slides unless overridden per-slide.
- Per-slide `background_image` overrides the global.
- `background_image: null` on a slide explicitly disables it; that slide uses the solid `bg` color fill.
- `overlay` is optional at both levels. Per-slide overlay overrides global overlay.
- `overlay` without `background_image` is silently ignored.
- When no `background_image` is set anywhere, current behavior (solid color fill) is unchanged.
- Image paths are local, relative to the YAML file (same as existing image handling via `db.resolve_path()`).
- If a `background_image` path does not exist, raise a clear `FileNotFoundError` with the resolved path.

## Approach

Use a full-slide `add_picture()` shape as the background image, sized to cover the entire slide (13.333" x 7.5"). The image shape is added first so it sits behind all content in z-order.

**Why not `slide.background.fill`:** python-pptx's `FillFormat` does not expose a `picture()` method. Setting a true PPTX background image would require direct lxml XML manipulation of the `bgPr` element. Using a full-bleed image shape achieves the same visual result with standard python-pptx API.

Overlay transparency requires a small lxml touch: injecting an `<a:alpha>` element into the overlay shape's solid fill XML, since python-pptx does not expose fill transparency.

## Implementation: 3 touch points

### 1. `theme.py` — Store background config

Add two new attributes to the `Theme` class, parsed from the config dict:

- `self.background_image: str | None` — path string from `config.get('background_image')`, default `None`
- `self.overlay: dict | None` — overlay dict from `config.get('overlay')`, default `None`
  - Expected keys: `color` (hex string or theme color name, default `"#000000"`), `opacity` (float 0-1, default `0.5`)

These are raw config values. Path resolution happens in the builder at render time. Overlay `color` is resolved through `Primitives._resolve_color()` at render time, so it supports both hex strings and theme color names.

### 2. `primitives.py` — Two new methods

**`background_image(slide, image_path)`**

Adds a full-slide picture shape (13.333" x 7.5") and ensures it is the bottommost shape in z-order.

```python
def background_image(self, slide, image_path):
    """Add a full-slide background image shape."""
    pic = slide.shapes.add_picture(
        image_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    # Move to back of z-order (behind all other shapes)
    slide.shapes._spTree.remove(pic._element)
    slide.shapes._spTree.insert(2, pic._element)
```

Note: `_spTree.insert(2, ...)` places the shape after the required `<p:cSld>` children (spTree's `nvGrpSpPr` and `grpSpPr` at indices 0 and 1). This is a standard python-pptx pattern for z-order manipulation.

**`overlay(slide, color, opacity)`**

Draws a full-slide rectangle with semi-transparent fill. Added immediately after the background image so it sits between the image and content shapes.

```python
from lxml import etree

def overlay(self, slide, color='#000000', opacity=0.5):
    """Draw a semi-transparent rectangle over the full slide."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = self._resolve_color(color)
    shape.line.fill.background()
    # Set fill transparency via lxml — python-pptx doesn't expose this
    alpha_val = int(opacity * 100000)  # OOXML alpha: 0=transparent, 100000=opaque
    srgbClr = shape.fill._fill.srgbClr
    alpha_elem = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
    alpha_elem.set('val', str(alpha_val))
    # Move behind content but in front of background image
    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(3, shape._element)  # after bg image at index 2
```

### 3. `builder.py` — Update `build()` and `new_slide()`

**Passing slide data without changing layouts:** In `build()`, before calling `layout.render()`, set `self._current_slide_data` on the builder instance. `new_slide()` reads from this attribute. This way all 14 layout files remain untouched.

```python
# In build():
for i, data in enumerate(self._slides):
    self._current_slide_data = data  # set before render
    layout_cls().render(self, data, i + 1)
self._current_slide_data = None
```

**Updated `new_slide()` logic:**

1. Read `self._current_slide_data` for per-slide overrides.
2. Determine background image: check slide data for `background_image` key, fall back to `self.theme.background_image`.
3. **If background image is set and not `None`:**
   - Resolve path via `self.resolve_path(bg_image_path)`
   - Validate file exists, raise `FileNotFoundError` if not
   - Create slide with no fill (transparent background)
   - Call `self.p.background_image(slide, resolved_path)`
   - Determine overlay: check slide data for `overlay`, fall back to `self.theme.overlay`
   - If overlay config exists, call `self.p.overlay(slide, color, opacity)`
4. **If no background image (or explicitly `None`):**
   - Keep current behavior: `slide.background.fill.solid()` with themed `bg` color

## What stays the same

- All 14 layout modules are untouched — `build()` sets `_current_slide_data` before calling `render()`, so `new_slide()` has what it needs without any layout changes.
- Template YAML schema is fully backward compatible — no `background_image` key means solid fill, identical to current behavior.
- All 6 existing templates work without modification.
- Image path resolution uses the existing `db.resolve_path()` mechanism.
- The `new_slide(bg='bg')` signature and behavior is unchanged for callers.

## Shape z-order

When a background image is present, the shape stack is:

1. Background image (index 2 in spTree — first shape)
2. Overlay rectangle (index 3 — if present)
3. All content shapes (added by layouts in their normal order)

When no background image is present, behavior is unchanged (solid fill, no extra shapes).

## Backward compatibility

- No breaking changes to the YAML schema.
- No breaking changes to the Python API (`new_slide(bg='bg')` still works).
- No changes to existing template content.yaml files.
- No changes to any layout files.

## Out of scope

- Fit/letterbox sizing mode (cover only)
- True PPTX background fill via lxml bgPr manipulation
- URL-based image sources (local paths only)
- Tiled/repeated backgrounds
- Per-layout-type background defaults
