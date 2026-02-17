---
name: slide-builder
description: Build PowerPoint presentations from YAML content using SlideCraft. Use when the user asks to create a deck, presentation, pitch deck, or slides.
---

# SlideCraft Slide Builder

You are building a PowerPoint presentation using the SlideCraft library. SlideCraft generates PPTX files from YAML content with themed layouts.

## Library Location

The SlideCraft library is at `/Users/jamie/Code/martin/slide-skill/`. It must be installed in a virtualenv before use:

```bash
cd /Users/jamie/Code/martin/slide-skill
source .venv/bin/activate
python3 -m slidecraft build <content.yaml> <output.pptx>
```

## Workflow

1. **Understand the request** — what kind of deck? How many slides? What content?
2. **Create a YAML content file** with theme configuration and slide definitions
3. **Build the PPTX** using the SlideCraft CLI
4. **Iterate** — user reviews the output and requests changes to the YAML

## YAML Structure

```yaml
theme:
  font_display: "Calibri"    # Heading font
  font_body: "Calibri"       # Body text font
  colors:
    bg: "#FFFFFF"             # Slide background
    surface: "#F5F5F5"        # Card/panel backgrounds
    primary: "#2563EB"        # Accent color (headings, highlights)
    primary_dark: "#1D4ED8"   # Darker accent variant
    text: "#111111"           # Primary text
    text_secondary: "#444444" # Body text
    text_muted: "#888888"     # Subtle text
    text_dim: "#AAAAAA"       # Very subtle text
    divider: "#E5E5E5"        # Horizontal rules
    row_alt: "#FAFAFA"        # Alternating table rows
    border: "#E0E0E0"         # Card borders
    danger: "#EF4444"         # Negative/warning
    success: "#059669"        # Positive
    warning: "#EA580C"        # Caution
  spacing:
    margin: 0.8               # Outer margin (inches)
    gutter: 0.4               # Column gap (inches)

slides:
  - layout: <layout_name>
    # ... layout-specific content keys
```

## Available Layouts (21)

### title
Opening/title slide. Center or left aligned.
```yaml
- layout: title
  title: "Deck Title"
  tagline: "A catchy tagline"       # optional, primary color
  subtitle: "By Author Name"        # optional, muted
  footer: "Confidential"            # optional, bottom
  align: center                     # or "left"
```

### section
Section break/divider. Vertically centered.
```yaml
- layout: section
  number: "01"                      # optional, large
  title: "Section Name"
  subtitle: "Optional description"  # optional
```

### content
Standard body slide with header and text or bullets.
```yaml
- layout: content
  title: "Slide Title"
  subtitle: "Optional subtitle"     # optional
  body: "Plain text paragraph"
  # OR bullet list:
  body:
    - Bullet point one
    - Bullet point two
  variant: bullets                  # "bullets" (default for lists), "numbered", "plain"
```

---

## Two-Column Layouts (4)

All two-column layouts share the same structure. Content keys: `left`, `right`.
Width variants: `50_50` (default), `60_40`, `40_60`.

**Text zones** accept a string or dict with `heading`, `body`, `bullets`.
**Image zones** accept a string (image path) or dict with `image`, `caption`.

### two_col_text_text
```yaml
- layout: two_col_text_text
  title: "Comparison"
  variant: "50_50"
  left:
    heading: "Pros"
    bullets: ["Fast", "Simple"]
  right:
    heading: "Cons"
    body: "Some limitations apply."
```

### two_col_text_image
```yaml
- layout: two_col_text_image
  title: "Feature Highlight"
  left:
    heading: "Description"
    body: "This feature enables..."
  right: "screenshots/feature.png"   # or {image: "...", caption: "..."}
```

### two_col_image_text
```yaml
- layout: two_col_image_text
  title: "Product Demo"
  left: "screenshots/demo.png"
  right:
    heading: "Key Benefits"
    bullets: ["Faster workflow", "Better results"]
```

### two_col_image_image
```yaml
- layout: two_col_image_image
  title: "Before & After"
  left: "images/before.png"
  right: "images/after.png"
```

---

## Three-Column Equal Layouts (4)

Three equal-width columns. Content keys: `left`, `center`, `right`.
Each zone is text or image depending on the layout name.

### three_col_text_text_text
```yaml
- layout: three_col_text_text_text
  title: "Core Concepts"
  left:
    heading: "Content"
    body: "YAML files define slide content."
  center:
    heading: "Theme"
    body: "Named colors and fonts."
  right:
    heading: "Layouts"
    body: "21 types handle positioning."
```

### three_col_text_image_text
```yaml
- layout: three_col_text_image_text
  title: "Architecture"
  left:
    heading: "Input"
    body: "YAML content files"
  center: "diagrams/flow.png"
  right:
    heading: "Output"
    body: "PPTX presentation"
```

### three_col_image_text_text
```yaml
- layout: three_col_image_text_text
  title: "Product Overview"
  left: "images/screenshot.png"
  center:
    heading: "Features"
    bullets: ["Fast", "Reliable"]
  right:
    heading: "Benefits"
    body: "Save hours per week."
```

### three_col_text_text_image
```yaml
- layout: three_col_text_text_image
  title: "Results"
  left:
    heading: "Before"
    body: "Manual slide creation"
  center:
    heading: "After"
    body: "Automated from YAML"
  right: "images/result.png"
```

---

## Three-Column Double-Width Layouts (4)

One narrow zone (1/3) and one wide zone (2/3). Content keys: `narrow`, `wide`.
The layout name tells you which side is narrow and what content type each zone holds.

### three_col_image_dtext
Narrow image left, double-width text right.
```yaml
- layout: three_col_image_dtext
  title: "Feature Detail"
  narrow: "images/icon.png"
  wide:
    heading: "How It Works"
    body: "Detailed explanation of the feature."
```

### three_col_text_dimage
Narrow text left, double-width image right.
```yaml
- layout: three_col_text_dimage
  title: "Visual Showcase"
  narrow:
    heading: "Caption"
    body: "Description of the image."
  wide: "images/hero.png"
```

### three_col_dimage_text
Double-width image left, narrow text right.
```yaml
- layout: three_col_dimage_text
  title: "Dashboard View"
  wide: "images/dashboard.png"
  narrow:
    heading: "Highlights"
    bullets: ["Real-time data", "Custom filters"]
```

### three_col_dtext_image
Double-width text left, narrow image right.
```yaml
- layout: three_col_dtext_image
  title: "Deep Dive"
  wide:
    heading: "Analysis"
    body: "Extended text content with full analysis."
  narrow: "images/chart.png"
```

---

## Other Layouts

### comparison
Side-by-side comparison table.
```yaml
- layout: comparison
  title: "Feature Comparison"
  headers: ["Feature", "Us", "Competitor A"]
  rows:
    - ["Speed", "Fast", "Slow"]
    - ["Price", "$10/mo", "$50/mo"]
  highlight_column: 1               # optional, bolds a column (0-indexed)
```

### data_table
Data table with optional sidebar and footer.
```yaml
- layout: data_table
  title: "Financial Projections"
  table:
    - ["Year", "Revenue", "Customers"]
    - ["2024", "$500K", "50"]
    - ["2025", "$2M", "200"]
  col_widths: [3, 2, 2]            # optional, relative proportions
  highlight_row: 2                  # optional (1-indexed)
  sidebar:                          # optional
    title: "Assumptions"
    items: ["50% growth", "Low churn"]
  footer: "All figures projected"   # optional
```

### quote
Featured quote with attribution.
```yaml
- layout: quote
  title: "Testimonial"             # optional
  quote: "This product changed everything."
  attribution: "Jane Doe"
  role: "VP Engineering"           # optional
  photo: "photos/jane.jpg"        # optional
```

### profile
Team member profiles (1-4 people).
```yaml
- layout: profile
  title: "The Team"
  profiles:
    - name: "Alice Smith"
      role: "CEO"
      company: "Acme Inc."        # optional
      bio: "10 years in SaaS."   # optional
      photo: "photos/alice.jpg"   # optional
```

### metrics
Large hero numbers (1-4).
```yaml
- layout: metrics
  title: "Key Numbers"
  metrics:
    - value: "$1M"
      label: "ARR"
      context: "growing 100% YoY" # optional
    - value: "200"
      label: "Customers"
```

### closing
Closing slide with CTA.
```yaml
- layout: closing
  title: "Thank You"
  headline: "Let's build together"  # optional
  bullets:                          # optional
    - "Schedule a demo"
    - "Visit our website"
  contact:                          # optional
    email: "hello@company.com"
    url: "company.com"
    social: "@company"
  closing: "Made with care."        # optional
```

## Theme Tips

- **Dark theme**: Set `bg` to a dark color, `text` to white, adjust surface/muted accordingly
- **Brand colors**: Override `primary` and `primary_dark`
- **Custom fonts**: Use any installed system font via `font_display` and `font_body`
- All image paths are relative to the YAML file location

## Build Command

```bash
cd /Users/jamie/Code/martin/slide-skill
source .venv/bin/activate
python3 -m slidecraft build /path/to/content.yaml /path/to/output.pptx
```

## Example

Full working demo at: `/Users/jamie/Code/martin/slide-skill/examples/demo/content.yaml`
