# 万能 Skill 格式转换器 🪄

**任意 AI Agent skill 文件 → 一键转换到任意格式**

[🇬🇧 English](README.md)

支持 10 种主流 AI 编码助手，自动检测源格式，安全可靠，零配置。

## 支持的 AI Agent

| 工具 | 格式 | 说明 |
|------|------|------|
| 🤖 Reasonix Code | `.reasonix/skills/<name>.md` | AI 编程助手 |
| 🧠 Hermes Agent | `~/.hermes/skills/<name>/SKILL.md` | AI 对话与知识管理 |
| ⚡ OpenCode | `~/.config/opencode/skills/<name>/SKILL.md` | AI 编程终端 |
| 🌀 Claude Code | `.claude/plugins/<name>/SKILL.md` | Anthropic 官方 |
| 🔵 OpenAI Codex | `.agents/plugins/<name>/SKILL.md` | OpenAI 编程代理 |
| 🖍️ Cursor | `.cursor/rules/<name>.mdc` | AI 代码编辑器 |
| 👾 GitHub Copilot | `.github/copilot-instructions.md` | GitHub 编程助手 |
| ▶️ Continue.dev | `~/.continue/config.json` | 开源编程助手 |
| 🛠️ Aider | `CONVENTIONS.md` | 终端编程助手 |
| 📦 Skills CLI | `.skills/<name>/SKILL.md` | 通用 CLI 工具 |

## 快速开始

```bash
# 从 URL 安装 skill 到多个工具
python universal-skill-converter.py https://example.com/SKILL.md --to reasonix,hermes,opencode

# 一键安装到全部 10 个工具
python universal-skill-converter.py skill.md --to all

# 导出为特定格式（不安装）
python universal-skill-converter.py skill.md --export cursor

# 查看 skill 信息（自动检测格式）
python universal-skill-converter.py skill.md --info

# 列出所有支持的 AI Agent
python universal-skill-converter.py --list
```

## 安装

无需安装，下载即用：

```bash
curl -O https://raw.githubusercontent.com/ruatm1-wq/-universal-skill-converter/main/universal-skill-converter.py
python universal-skill-converter.py --list
```

仅需 **Python 3.6+**，零外部依赖。

## 功能特性

### 🔄 自动格式检测

转换器通过以下方式自动识别源格式：
- 文件扩展名（`.mdc`、`.md`、`.json`）
- YAML frontmatter 字段（`runAs`、`allowed-tools`、`globs` 等）
- 内容结构（markdown 标题、JSON 等）

无需告诉它你要从什么格式转换。

### 🔒 安全第一

- **只读操作** — 从不修改或删除已有文件
- **无数据收集** — 完全离线运行（除非指定 URL）
- **YAML 校验** — 格式错误自动拒绝
- **限定目录** — 只写入预定义的 skill 目录

### 🗺️ 什么是 Skill？

Skill 是可复用的指令集，用来教会 AI 代理特定的工作流程或能力：

```yaml
---
name: my-skill
description: 这个 skill 的功能说明
---
# 遇到以下情况时执行这些指令...
```

不同的 AI 工具用不同的路径和格式存储 skill。这个转换器就是连接它们的桥梁。

## 工作原理

```
任意 skill 文件 → 自动检测格式 → 解析为统一字典
                                    ↓
                    渲染为目标格式 → 写入正确路径
```

转换流程：

1. **检测** — 识别源格式（文件路径、YAML 字段、内容结构）
2. **解析** — 提取名称、描述、正文和额外字段为统一字典
3. **渲染** — 用正确的 frontmatter、模板和文件结构生成目标格式
4. **安装** — 自动创建子目录，为 Claude/Codex 生成 plugin.json 等

## 使用示例

### 将 Cursor `.mdc` 转换为 Hermes 格式

```bash
python universal-skill-converter.py my-rule.mdc --to hermes
```

### 从 GitHub 下载 skill 并安装到所有工具

```bash
python universal-skill-converter.py \
  https://raw.githubusercontent.com/org/repo/main/skills/my-skill/SKILL.md \
  --to all
```

### 导出为 GitHub Copilot 格式

```bash
python universal-skill-converter.py skill.md --export github-copilot
```

### 预览 skill 信息

```bash
python universal-skill-converter.py some-skill.md --info
```

## 安全说明

本工具只写入以下目录：

| Agent | 写入位置 |
|-------|---------|
| Reasonix | `~/.reasonix/skills/` |
| Hermes | `~/.hermes/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Claude/Codex | `.claude/plugins/` 或 `.agents/plugins/`（当前目录） |
| Cursor | `.cursor/rules/`（当前目录） |
| 其他 | 当前目录或用户目录 |

不会访问系统目录、修改已有文件、或泄露数据。

## 文件格式参考

### 通用 YAML Frontmatter（最常见）

```yaml
---
name: skill-name
description: Brief description
---
正文内容（markdown）...
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

### 纯 Markdown（Copilot、Aider）

```markdown
# Skill Name

> Description

正文内容...
```

## 为什么需要这个工具？

每个 AI 编码助手都有自己的 skill/plugin 格式。当你在 GitHub 上找到一个好 skill，如果是给 Claude Code 写的，就没法直接给 Cursor 或 OpenCode 用——除非手动改格式。

这个转换器就是**万能适配器**：一份 skill，通吃所有 AI 工具。

## 路线图

- [ ] 更多格式支持（Windsurf、Kilo Code、Cline、Roo Code）
- [ ] 批量转换（一次转换整个 skill 库）
- [ ] GitHub 市场集成
- [ ] Web 界面

## 贡献

欢迎 PR！Fork → 在 `AGENTS` 字典中添加新格式 → 提交。

## 许可证

MIT
