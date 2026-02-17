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

## Available Layouts (12)

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
  # OR
  body:
    - Bullet point one
    - Bullet point two
  variant: bullets                  # "bullets" (default for lists), "numbered", "plain"
```

### two_column
Two columns with flexible width split.
```yaml
- layout: two_column
  title: "Comparison"
  subtitle: "Optional"              # optional
  variant: "50_50"                  # "50_50" (default), "60_40", "40_60"
  left: "Simple text string"
  # OR structured:
  left:
    heading: "Column Title"
    body: "Paragraph text"
    bullets:
      - Item one
      - Item two
  right:
    heading: "Other Column"
    bullets:
      - Item A
      - Item B
```

### three_column
Three equal columns with card backgrounds.
```yaml
- layout: three_column
  title: "Features"
  columns:
    - icon: "🚀"                   # optional emoji/symbol
      heading: "Fast"
      body: "Description text"
    - icon: "🔒"
      heading: "Secure"
      body: "Description text"
    - icon: "💡"
      heading: "Smart"
      body: "Description text"
```

### image_text
Image beside text (45%/50% split).
```yaml
- layout: image_text
  title: "Visual Slide"
  image: "path/to/image.jpg"       # relative to YAML file
  caption: "Photo caption"          # optional
  variant: image_left               # "image_left" (default), "image_right"
  text: "Paragraph of text"
  # OR
  text:
    - Bullet beside the image
    - Another bullet
```

### comparison
Side-by-side comparison table.
```yaml
- layout: comparison
  title: "Feature Comparison"
  headers: ["Feature", "Us", "Competitor A", "Competitor B"]
  rows:
    - ["Speed", "Fast", "Medium", "Slow"]
    - ["Price", "$10/mo", "$50/mo", "$30/mo"]
  highlight_column: 1               # optional, bolds a column (0-indexed)
```

### data_table
Data table with optional sidebar and footer.
```yaml
- layout: data_table
  title: "Financial Projections"
  table:
    - ["Year", "Revenue", "Customers"]    # first row = headers
    - ["2024", "$500K", "50"]
    - ["2025", "$2M", "200"]
  col_widths: [3, 2, 2]            # optional, relative proportions
  highlight_row: 2                  # optional, bolds a data row (1-indexed)
  sidebar:                          # optional
    title: "Key Assumptions"
    items:
      - "50% annual growth"
      - "Low churn"
  footer: "All figures projected"   # optional
```

### quote
Featured quote with attribution.
```yaml
- layout: quote
  title: "Testimonial"             # optional (if omitted, quote is vertically centered)
  quote: "This product changed everything for our team."
  attribution: "Jane Doe"
  role: "VP Engineering at Acme"   # optional
  photo: "path/to/photo.jpg"      # optional, displayed on right
```

### profile
Team member or speaker profiles (1-4 people).
```yaml
- layout: profile
  title: "The Team"
  profiles:
    - name: "Alice Smith"
      role: "CEO & Co-founder"
      company: "Acme Inc."         # optional
      bio: "10 years in SaaS."    # optional (shows for single profile)
      photo: "alice.jpg"           # optional, relative to YAML
    - name: "Bob Jones"
      role: "CTO"
      photo: "bob.jpg"
```

### metrics
Large hero metric numbers displayed horizontally (1-4).
```yaml
- layout: metrics
  title: "Key Numbers"
  subtitle: "As of Q4 2025"        # optional
  metrics:
    - value: "$1M"
      label: "ARR"
      context: "growing 100% YoY"  # optional
    - value: "200"
      label: "Customers"
    - value: "95%"
      label: "Retention"
```

### closing
Closing slide with CTA and contact info.
```yaml
- layout: closing
  title: "Thank You"
  headline: "Let's build together"  # optional, primary color
  bullets:                          # optional
    - "Schedule a demo"
    - "Visit our website"
  contact:                          # optional
    email: "hello@company.com"
    url: "company.com"
    social: "@company"
  closing: "Made with care."        # optional, bottom tagline
```

## Theme Tips

- **Dark theme**: Set `bg` to a dark color (e.g., `#0D0D0F`), `text` to white, and adjust surface/muted colors accordingly
- **Brand colors**: Override `primary` and `primary_dark` to match the brand
- **Custom fonts**: Use any font installed on the system via `font_display` and `font_body`
- All images are specified as paths relative to the YAML file location

## Build Command

```bash
cd /Users/jamie/Code/martin/slide-skill
source .venv/bin/activate
python3 -m slidecraft build /path/to/content.yaml /path/to/output.pptx
```

## Example

See the full working demo at: `/Users/jamie/Code/martin/slide-skill/examples/demo/content.yaml`
