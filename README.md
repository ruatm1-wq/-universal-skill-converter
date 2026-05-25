# Universal Skill Converter 🪄

<p align="center">
  <img src="https://img.shields.io/github/license/ruatm1-wq/universal-skill-converter?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/ruatm1-wq/universal-skill-converter?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome">
</p>

**Convert any AI agent skill file to any format — instantly.**

[🇨🇳 中文版 (Chinese)](README.zh.md)

Support 10 major AI coding agents with auto-detection of source format, safe file handling, and zero config required.

## Supported Agents

| Agent | Format | Description |
|-------|--------|-------------|
| 🤖 Reasonix Code | `.reasonix/skills/<name>.md` | AI coding assistant |
| 🧠 Hermes Agent | `~/.hermes/skills/<name>/SKILL.md` | AI conversation & knowledge |
| ⚡ OpenCode | `~/.config/opencode/skills/<name>/SKILL.md` | AI coding terminal |
| 🌀 Claude Code | `.claude/plugins/<name>/SKILL.md` | Anthropic's coding agent |
| 🔵 OpenAI Codex | `.agents/plugins/<name>/SKILL.md` | OpenAI coding agent |
| 🖍️ Cursor | `.cursor/rules/<name>.mdc` | AI code editor |
| 👾 GitHub Copilot | `.github/copilot-instructions.md` | GitHub's AI assistant |
| ▶️ Continue.dev | `~/.continue/config.json` | Open-source coding agent |
| 🛠️ Aider | `CONVENTIONS.md` | Terminal AI pair programmer |
| 📦 Skills CLI | `.skills/<name>/SKILL.md` | Universal skills tool |

## Quick Start

```bash
# Install a skill from URL to multiple agents
python universal-skill-converter.py https://example.com/SKILL.md --to reasonix,hermes,opencode

# Install to ALL 10 supported agents at once
python universal-skill-converter.py skill.md --to all

# Export to a specific format without installing
python universal-skill-converter.py skill.md --export cursor

# Inspect a skill file (auto-detect format)
python universal-skill-converter.py skill.md --info

# List all supported agents
python universal-skill-converter.py --list
```

## Installation

No installation needed — just download the script and run:

```bash
curl -O https://raw.githubusercontent.com/ruatm1-wq/-universal-skill-converter/main/universal-skill-converter.py
python universal-skill-converter.py --list
```

Requires **Python 3.6+** only. Zero external dependencies.

## Features

### 🔄 Auto-Format Detection

The converter automatically detects the source format by analyzing:
- File extension (`.mdc`, `.md`, `.json`)
- YAML frontmatter fields (`runAs`, `allowed-tools`, `globs`, etc.)
- Content structure (markdown heading, JSON, etc.)

No need to tell it what format you're converting from.

### 🔒 Security First

- **Read-only** — never modifies or deletes existing files
- **No data collection** — fully offline unless you specify a URL
- **YAML validation** — rejects malformed skills before writing
- **Scope-confined** — only writes to predefined skill directories

### 🗺️ What's a "Skill"?

Skills are reusable instruction sets that teach AI agents specific workflows, guidelines, or capabilities. They typically contain:

```yaml
---
name: my-skill
description: What this skill does
---
# Follow these instructions when...
```

Different AI agents store skills in different paths and formats. This converter bridges them all.

## How It Works

```
Any skill file → Auto-detect format → Parse into unified dict
                                        ↓
                    Render to target format → Write to correct path
```

The conversion pipeline:

1. **Detect** — identifies the source format (file path, YAML fields, content structure)
2. **Parse** — extracts name, description, body, and extra fields into a universal dictionary
3. **Render** — generates the target format with correct frontmatter, template, and file structure
4. **Install** — creates subdirectories if needed, writes plugin.json for Claude/Codex, etc.

## Examples

### Convert a Cursor `.mdc` to Hermes format

```bash
python universal-skill-converter.py my-rule.mdc --to hermes
```

### Download a skill from GitHub and install everywhere

```bash
python universal-skill-converter.py \
  https://raw.githubusercontent.com/org/repo/main/skills/my-skill/SKILL.md \
  --to all
```

### Export as GitHub Copilot instructions

```bash
python universal-skill-converter.py skill.md --export github-copilot
```

### Preview what the converter detected

```bash
python universal-skill-converter.py some-skill.md --info
```

## Security Considerations

This tool only writes to specific directories under your home folder or current working directory:

| Agent | Writes To |
|-------|-----------|
| Reasonix | `~/.reasonix/skills/` |
| Hermes | `~/.hermes/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Claude/Codex | `.claude/plugins/` or `.agents/plugins/` (CWD) |
| Cursor | `.cursor/rules/` (CWD) |
| Others | CWD or home directory |

It will never access system directories, modify existing files, or exfiltrate data.

## File Format Reference

### Generic YAML Frontmatter (most common)

```yaml
---
name: skill-name
description: Brief description
---
Body content in markdown...
```

### Cursor `.mdc`

```yaml
---
description: Description
globs: **/*.ts
---
```

### Continue.dev JSON

```json
{
  "name": "skill-name",
  "description": "...",
  "systemPrompt": "..."
}
```

### Plain Markdown (Copilot, Aider)

```markdown
# Skill Name

> Description

Body content...
```

## Why This Exists

Every AI coding agent has its own skill/plugin format. If you find a great skill on GitHub written for Claude Code, you can't easily use it with Cursor or OpenCode — unless you manually reformat it.

This converter is the **universal adapter**: one skill file, any AI agent, zero manual conversion.

## Roadmap

- [ ] More agent formats (Windsurf, Kilo Code, Cline, Roo Code)
- [ ] Batch conversion (convert an entire skill library)
- [ ] GitHub marketplace integration
- [ ] Web-based converter UI

## Contributing

PRs welcome! Fork → add a new agent format to `AGENTS` dict → submit.

## License

MIT
