# SlideCraft

A plugin for Claude Code and Claude Cowork that builds PowerPoint presentations from natural language. Describe the deck you want, and Claude generates a YAML content file, builds it into a polished `.pptx`, and iterates with you until it's right.

No templates to fight with. No dragging boxes around. Just say what you need.

## Install

### Claude Code (CLI)

Add the plugin marketplace, then install:

```
/plugin marketplace add jvsteiner/slidecraft
/plugin install slide-builder@slidecraft
```

### Claude Cowork (Desktop)

1. Download or clone this repository
2. Open Claude Desktop and switch to the **Cowork** tab
3. Click **Plugins** in the left sidebar
4. Click **Upload plugin**
5. Select the downloaded plugin folder

The plugin handles its own Python dependency installation on first use.

## Usage

Just ask Claude to make a presentation:

> "Create a 10-slide pitch deck for a B2B SaaS product called Archway"

> "Make a quarterly board update with our key metrics"

> "Build a team intro deck with profile cards for our engineering leads"

Claude will write the YAML, pick an appropriate theme, build the `.pptx`, and hand you the file. You can then ask for changes — swap layouts, adjust colors, rewrite copy — and it rebuilds.

In Claude Code, you can also invoke the skill explicitly with `/slide-builder`.

---

## Themes

**6 built-in themes**, each with curated fonts, colors, and spacing:

| Theme | Style | Best for |
|-------|-------|----------|
| **Boardroom** | White/navy | Corporate, consulting, board decks |
| **Midnight** | Dark slate/sky-blue | Technical, dev tools, engineering |
| **Ember** | Warm white/burnt orange | Editorial, brand strategy, marketing |
| **Ink** | Pure white/red | Minimal, Apple-style, product launches |
| **Canopy** | Off-white/forest green | Sustainability, wellness, education |
| **Signal** | White/vivid purple | Consumer products, demo day, pitch |

Claude picks the theme that fits your content, or you can ask for a specific one.

### Theme configuration

Themes are defined in the `theme:` block of the YAML file:

```yaml
theme:
  font_display: "Futura"           # Headings, titles, large text
  font_body: "Avenir Next"         # Body text, bullets, captions
  background_image: "images/bg.jpg" # Optional — global background image
  overlay:                          # Optional — overlay on background images
    color: "#000000"
    opacity: 0.4
  colors:
    bg: "#0F172A"                  # Slide background
    surface: "#1E293B"             # Cards, sidebars, table headers
    primary: "#38BDF8"             # Accent color (headings, highlights)
    primary_dark: "#0EA5E9"        # Darker accent variant
    text: "#F8FAFC"               # Primary text
    text_secondary: "#CBD5E1"      # Body text, bullets
    text_muted: "#94A3B8"          # Subtitles, captions
    text_dim: "#64748B"            # Footers, slide numbers
    divider: "#334155"             # Horizontal rules
    row_alt: "#1E293B"             # Alternating table rows
    border: "#475569"              # Card/table borders
    danger: "#F87171"              # Red accent
    success: "#34D399"             # Green accent
    warning: "#FBBF24"            # Yellow accent
  spacing:
    margin: 0.8                    # Outer margin (inches)
    gutter: 0.4                    # Gap between columns (inches)
    margin_top: 0.6                # Top margin for headers
    title_height: 0.8              # Title zone height
    footer_y: 7.0                  # Footer vertical position
```

---

## Background Images

Slides can use an image as the background, configured globally or per-slide.

### Global background (all slides)

Set `background_image` in the theme block. Every slide uses this image unless overridden:

```yaml
theme:
  background_image: "images/dark-texture.jpg"
  overlay:
    color: "#000000"
    opacity: 0.5
```

### Per-slide override

Individual slides can use a different image, or disable the background entirely:

```yaml
slides:
  - layout: title
    title: "Welcome"
    background_image: "images/hero-photo.jpg"   # different image for this slide
    overlay:
      color: "#000000"
      opacity: 0.6

  - layout: content
    title: "Details"
    background_image: null                       # no background image, solid color
```

### Overlay

The optional `overlay` adds a semi-transparent color layer between the background image and slide content, improving text readability over photos. `opacity` ranges from 0.0 (fully transparent) to 1.0 (fully opaque).

Image paths are relative to the YAML file.

---

## Layouts

**21 slide layouts** covering the patterns you actually use in decks.

### Openers and closers

#### `title`

Opening slide with large title, optional tagline, subtitle, and footer.

```yaml
- layout: title
  title: "Voxel"
  tagline: "Infrastructure that disappears."
  subtitle: "Real-time edge compute for the rest of us."
  footer: "voxel.dev  |  Seed Round 2025"
  align: center          # or "left" — defaults to "center"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Main title (auto-scales font for length) |
| `tagline` | string | no | Bold accent-colored line below title |
| `subtitle` | string | no | Muted line below tagline |
| `footer` | string | no | Small text at slide bottom |
| `align` | string | no | `"center"` (default) or `"left"` |

#### `section`

Section divider with large centered text and optional section number.

```yaml
- layout: section
  number: "01"
  title: "The Problem"
  subtitle: "Why the status quo doesn't work"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `number` | string | no | Large section number displayed above title |
| `title` | string | yes | Section title |
| `subtitle` | string | no | Muted subtitle below |

#### `closing`

Closing slide with CTA, optional bullets, contact info, and tagline.

```yaml
- layout: closing
  title: "The Ask"
  headline: "Raising $4M seed to build the next compute primitive."
  bullets:
    - "Team: 3 ex-Cloudflare engineers"
    - "Prototype serving 2M req/day in private beta"
  contact:
    email: "founders@voxel.dev"
    url: "voxel.dev"
    social: "@voxel"
  closing: "Let's build the future of compute."
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Main heading |
| `headline` | string | no | Bold accent-colored subheading |
| `bullets` | list | no | Centered bullet points |
| `contact` | dict | no | Contact info: `email`, `url`, `social` |
| `closing` | string | no | Small tagline at bottom |

### Body content

#### `content`

Standard body slide with header and text or bullets.

```yaml
# Plain text
- layout: content
  title: "Our Approach"
  subtitle: "Built from first principles"
  body: "We rethought the entire stack from the ground up..."

# Bullet list
- layout: content
  title: "Key Features"
  body:
    - "Sub-50ms response times globally"
    - "Zero cold starts"
    - "Deploy in seconds"
  variant: bullets       # or "numbered"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Slide title |
| `subtitle` | string | no | Subtitle below title |
| `body` | string or list | yes | Plain text (string) or bullet items (list) |
| `variant` | string | no | `"bullets"` (default for lists), `"numbered"`, or `"plain"` |

### Two-column layouts

Four layout types with three width variants each:

| Layout | Left zone | Right zone |
|--------|-----------|------------|
| `two_col_text_text` | text | text |
| `two_col_text_image` | text | image |
| `two_col_image_text` | image | text |
| `two_col_image_image` | image | image |

**Width variants:** Set `variant` to control column proportions:

| Variant | Left | Right |
|---------|------|-------|
| `"50_50"` (default) | 50% | 50% |
| `"60_40"` | 60% | 40% |
| `"40_60"` | 40% | 60% |

```yaml
- layout: two_col_text_text
  title: "The Problem"
  variant: "50_50"
  left:
    heading: "What developers want"
    bullets:
      - "Sub-50ms response times"
      - "Zero cold starts"
  right:
    heading: "What they get today"
    bullets:
      - "Lambda cold starts: 200-800ms"
      - "Unpredictable billing"

- layout: two_col_text_image
  title: "The Product"
  variant: "60_40"
  left:
    heading: "Dashboard"
    body: "Real-time monitoring across all regions."
  right: "screenshots/dashboard.png"
```

### Three-column layouts (equal width)

Four layout types with equal-width columns:

| Layout | Left | Center | Right |
|--------|------|--------|-------|
| `three_col_text_text_text` | text | text | text |
| `three_col_text_image_text` | text | image | text |
| `three_col_image_text_text` | image | text | text |
| `three_col_text_text_image` | text | text | image |

```yaml
- layout: three_col_text_text_text
  title: "How It Works"
  left:
    heading: "1. Push"
    body: "Push a container image or point us at your repo."
  center:
    heading: "2. Warm"
    body: "Pre-warms instances in every region where your users live."
  right:
    heading: "3. Serve"
    body: "Requests route to the nearest warm instance."
```

### Three-column layouts (weighted)

Four layout types with a 1/3 + 2/3 split:

| Layout | Narrow | Wide |
|--------|--------|------|
| `three_col_image_dtext` | image (left) | text spanning 2 cols (right) |
| `three_col_text_dimage` | text (left) | image spanning 2 cols (right) |
| `three_col_dimage_text` | image spanning 2 cols (left) | text (right) |
| `three_col_dtext_image` | text spanning 2 cols (left) | image (right) |

```yaml
- layout: three_col_image_dtext
  title: "Case Study"
  left: "photos/client-logo.png"
  right:
    heading: "Results after 6 months"
    bullets:
      - "3x improvement in deploy speed"
      - "60% reduction in infrastructure costs"
```

### Data layouts

#### `comparison`

Side-by-side comparison table with optional column highlighting.

```yaml
- layout: comparison
  title: "How We Compare"
  headers: ["", "Us", "Competitor A", "Competitor B"]
  rows:
    - ["Speed", "<5ms", "200ms", "50ms"]
    - ["Pricing", "$0.01/req", "$0.05/req", "$0.03/req"]
  highlight_column: 1
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Slide title |
| `subtitle` | string | no | Subtitle |
| `headers` | list | yes | Column headers |
| `rows` | list of lists | yes | Table rows |
| `highlight_column` | int | no | Column index to bold (0-based) |

#### `data_table`

Data table with optional sidebar and footer.

```yaml
- layout: data_table
  title: "Financial Summary"
  table:
    - ["Quarter", "Revenue", "Growth"]
    - ["Q1", "$2.1M", "+12%"]
    - ["Q2", "$2.8M", "+33%"]
  col_widths: [2, 1, 1]
  highlight_row: 2
  sidebar:
    title: "Key Takeaways"
    items:
      - "Revenue up 33% QoQ"
      - "Strongest quarter to date"
  footer: "Source: internal financial data, 2025"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Slide title |
| `subtitle` | string | no | Subtitle |
| `table` | list of lists | yes | First row = headers, rest = data |
| `col_widths` | list of numbers | no | Relative column widths |
| `highlight_row` | int | no | Row index to bold (1-based, 0 = header) |
| `sidebar` | dict | no | Side panel: `title` and `items` list |
| `footer` | string | no | Small text at bottom |

#### `metrics`

Large hero numbers displayed horizontally (1-4 metrics).

```yaml
- layout: metrics
  title: "Traction"
  metrics:
    - value: "2M"
      label: "Requests / day"
      context: "Up from 500K in Q1"
    - value: "42"
      label: "Edge regions"
    - value: "<5ms"
      label: "p99 latency"
      context: "Global average"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Slide title |
| `subtitle` | string | no | Subtitle |
| `metrics` | list of dicts | yes | Each: `value`, `label`, `context` (optional) |

### People layouts

#### `profile`

Team member or speaker profiles. Renders as a single large card (1 profile) or grid (2-4 profiles).

```yaml
- layout: profile
  title: "Leadership Team"
  profiles:
    - name: "Alex Chen"
      role: "CEO & Co-founder"
      company: "Previously: Cloudflare"
      bio: "Built Workers KV from scratch. 10 years in distributed systems."
      photo: "photos/alex.jpg"
    - name: "Sam Rivera"
      role: "CTO & Co-founder"
      photo: "photos/sam.jpg"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | yes | Slide title |
| `profiles` | list of dicts | yes | Each: `name`, `role`, `company`, `bio`, `photo` (all optional except `name`) |

#### `quote`

Featured testimonial with optional photo.

```yaml
- layout: quote
  title: "What Users Say"
  quote: "Voxel cut our deploy times from minutes to seconds. It just works."
  attribution: "Alex Chen"
  role: "CTO, Acme Corp"
  photo: "photos/alex.jpg"
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `title` | string | no | Optional slide title (centers quote if omitted) |
| `quote` | string | yes | The quote text |
| `attribution` | string | yes | Who said it |
| `role` | string | no | Title/company of the person |
| `photo` | string | no | Portrait image path |

---

## Zone content formats

Column layouts use **zones** for content. Each zone is either text or image.

### Text zones

Text zones accept a plain string or a structured dict:

```yaml
# Simple — renders as a paragraph
left: "This is plain body text."

# Structured — heading + body or bullets
left:
  heading: "Section Title"
  body: "Paragraph text below the heading."

left:
  heading: "Key Points"
  bullets:
    - "First point"
    - "Second point"
    - "Third point"
```

### Image zones

Image zones accept a path string or a dict with caption:

```yaml
# Simple — just the image
right: "screenshots/dashboard.png"

# With caption
right:
  image: "screenshots/dashboard.png"
  caption: "Real-time monitoring dashboard"
```

All image paths are relative to the YAML file.

---

## How it works under the hood

SlideCraft is a Python library (`slidecraft`) that generates PPTX files from YAML. The skill teaches Claude how to use it:

1. Claude writes a `content.yaml` with theme config and slide definitions
2. Runs `slidecraft build content.yaml output.pptx`
3. Hands you the file
4. Edits the YAML and rebuilds when you ask for changes

The YAML is the source of truth — all content, layout choices, and theming live there.

## CLI

```bash
# Build a presentation
slidecraft build content.yaml output.pptx

# List all available layouts
slidecraft layouts
```

## Development

If you're working on the skill itself:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Key paths:

```
slidecraft/          # Python library
  builder.py         # YAML → PPTX orchestrator
  theme.py           # Color/font/spacing system
  primitives.py      # Low-level PPTX drawing
  layouts/           # 21 layout implementations
templates/           # 6 pre-built themes (YAML + reference PPTX)
plugins/             # Claude Code skill definition
examples/demo/       # 26-slide showcase deck
```
