# Universal Skill Converter 🪄

**万能 AI Agent Skill 格式转换器**

一键转换 skill 文件到任意 AI 工具格式。支持 10 种主流 AI Agent。

## 支持的格式

| 工具 | 格式 | 说明 |
|------|------|------|
| 🤖 Reasonix Code | `.reasonix/skills/<name>.md` | 编程自动化助手 |
| 🧠 Hermes Agent | `~/.hermes/skills/<name>/SKILL.md` | AI 对话与知识管理 |
| ⚡ OpenCode | `~/.config/opencode/skills/<name>/SKILL.md` | 独立编程终端 |
| 🌀 Claude Code | `.claude/plugins/<name>/SKILL.md` | Anthropic 官方 |
| 🔵 OpenAI Codex | `.agents/plugins/<name>/SKILL.md` | OpenAI 编程代理 |
| 🖍️ Cursor | `.cursor/rules/<name>.mdc` | AI 代码编辑器 |
| 👾 GitHub Copilot | `.github/copilot-instructions.md` | GitHub 编程助手 |
| ▶️ Continue.dev | `~/.continue/config.json` | 开源编程助手 |
| 🛠️ Aider | `CONVENTIONS.md` | 终端编程助手 |
| 📦 Skills CLI | `.skills/<name>/SKILL.md` | 通用 CLI 工具 |

## 用法

```bash
# 从 URL 安装到指定工具
python universal-skill-converter.py https://.../SKILL.md --to reasonix,hermes,opencode

# 安装到全部 10 个工具
python universal-skill-converter.py skill.md --to all

# 导出为特定格式（不安装）
python universal-skill-converter.py skill.md --export cursor

# 查看 skill 信息
python universal-skill-converter.py skill.md --info

# 列出所有支持的 AI Agent
python universal-skill-converter.py --list
```

## 安全特性

- ✅ 自动检测源格式
- ✅ YAML frontmatter 校验
- ✅ 只读文件操作（不会删除/修改已有文件）
- ✅ 不收集任何数据
- ✅ 不联网（除非指定 URL 安装）

## 许可证

MIT
