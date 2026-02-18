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

## What it can do

**21 slide layouts** covering the patterns you actually use in decks:

| Category | Layouts |
|----------|---------|
| Openers | `title`, `section`, `closing` |
| Body | `content` (text/bullets) |
| Two-column | `text_text`, `text_image`, `image_text`, `image_image` |
| Three-column equal | `text_text_text`, `text_image_text`, `image_text_text`, `text_text_image` |
| Three-column weighted | `image_dtext`, `text_dimage`, `dimage_text`, `dtext_image` |
| Data | `comparison`, `data_table`, `metrics` |
| People | `profile`, `quote` |

**6 built-in themes:**

- **Boardroom** — White/navy. Corporate, consulting.
- **Midnight** — Dark slate/sky-blue. Technical, dev tools.
- **Ember** — Warm white/burnt orange. Editorial, brand strategy.
- **Ink** — Pure white/red. Minimal, Apple-style.
- **Canopy** — Off-white/forest green. Sustainability, wellness.
- **Signal** — White/vivid purple. Consumer, demo day.

Claude picks the theme that fits your content, or you can ask for a specific one.

## How it works under the hood

SlideCraft is a Python library (`slidecraft`) that generates PPTX files from YAML. The skill teaches Claude how to use it:

1. Claude writes a `content.yaml` with theme config and slide definitions
2. Runs `slidecraft build content.yaml output.pptx`
3. Hands you the file
4. Edits the YAML and rebuilds when you ask for changes

The YAML is the source of truth — all content, layout choices, and theming live there. Image paths are resolved relative to the YAML file.

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
templates/           # 6 pre-built themes (YAML)
plugins/             # Claude Code skill definition
examples/demo/       # 26-slide showcase deck
```
