#!/usr/bin/env python3
"""
⭐ Universal Skill Converter — 万能 AI Agent Skill 格式转换器
让任何 AI agent 都能用市面上所有格式的 skills
"""

import os, re, json, shutil, sys
from pathlib import Path
from typing import Optional

VERSION = '1.0.0'

# ═══════════════════════════════════════════════════
# 格式注册表 — 所有支持的 AI Agent 格式
# ═══════════════════════════════════════════════════

AGENTS = {
    'reasonix': {
        'name': 'Reasonix Code',
        'desc': '编程自动化助手',
        'format': '单文件 .md',
        'path': '~/.reasonix/skills/<name>.md',
        'dir_needed': False,
        'file_name': '{name}.md',
        'fields': ['name', 'description', 'runAs', 'allowed-tools'],
        'extra': {'runAs': 'inline', 'allowed-tools': ''},
    },
    'hermes': {
        'name': 'Hermes Agent',
        'desc': 'AI 对话与知识管理',
        'format': '子目录 + SKILL.md',
        'path': '~/.hermes/skills/<name>/SKILL.md',
        'dir_needed': True,
        'file_name': 'SKILL.md',
        'fields': ['name', 'description'],
        'extra': {},
    },
    'opencode': {
        'name': 'OpenCode',
        'desc': '独立编程终端',
        'format': '子目录 + SKILL.md',
        'path': '~/.config/opencode/skills/<name>/SKILL.md',
        'dir_needed': True,
        'file_name': 'SKILL.md',
        'fields': ['name', 'description'],
        'extra': {},
    },
    'claude-code': {
        'name': 'Claude Code (Anthropic)',
        'desc': 'Anthropic 官方编程助手',
        'format': '子目录 + plugin.json + SKILL.md',
        'path': '.claude/plugins/<name>/SKILL.md',
        'dir_needed': True,
        'file_name': 'SKILL.md',
        'fields': ['name', 'description'],
        'extra': {},
        'extra_files': {
            'plugin.json': '{"name":"{name}","description":"{desc}","skills":["{name}"],"source":"./","strict":false}',
        },
    },
    'openai-codex': {
        'name': 'OpenAI Codex',
        'desc': 'OpenAI 编程代理',
        'format': '子目录 + plugin.json + SKILL.md',
        'path': '.agents/plugins/<name>/SKILL.md',
        'dir_needed': True,
        'file_name': 'SKILL.md',
        'fields': ['name', 'description'],
        'extra': {},
        'extra_files': {
            'plugin.json': '{"name":"{name}","description":"{desc}","skills":["{name}"],"source":"./","strict":false}',
        },
    },
    'cursor': {
        'name': 'Cursor',
        'desc': 'AI 代码编辑器',
        'format': '子目录 .cursor/rules/<name>.mdc',
        'path': '.cursor/rules/<name>.mdc',
        'dir_needed': False,
        'file_name': '{name}.mdc',
        'fields': ['name', 'description'],
        'extra': {},
        'template': '---\ndescription: {desc}\nglobs: **/*\n---\n\n{body}',
    },
    'github-copilot': {
        'name': 'GitHub Copilot',
        'desc': 'GitHub AI 编程助手',
        'format': '单文件 .github/copilot-instructions.md',
        'path': '.github/copilot-instructions.md',
        'dir_needed': False,
        'file_name': 'copilot-instructions.md',
        'fields': [],
        'extra': {},
        'template': '# {name}\n\n{desc}\n\n{body}',
    },
    'continue': {
        'name': 'Continue.dev',
        'desc': '开源 AI 编程助手',
        'format': 'JSON 配置 ~/.continue/config.json',
        'path': '~/.continue/config.json',
        'dir_needed': False,
        'file_name': 'config.json',
        'fields': [],
        'extra': {},
        'is_json': True,
    },
    'aider': {
        'name': 'Aider',
        'desc': '终端 AI 编程助手',
        'format': 'CONVENTIONS.md',
        'path': 'CONVENTIONS.md',
        'dir_needed': False,
        'file_name': 'CONVENTIONS.md',
        'fields': [],
        'extra': {},
        'template': '# {name}\n\n{desc}\n\n{body}',
    },
    'skills-cli': {
        'name': 'Skills CLI',
        'desc': '通用 Skills 命令行工具',
        'format': '子目录 + SKILL.md',
        'path': '.skills/<name>/SKILL.md',
        'dir_needed': True,
        'file_name': 'SKILL.md',
        'fields': ['name', 'description'],
        'extra': {},
    },
}


def detect_format(text: str, source_path: str = '') -> str:
    """自动检测 skill 的原始格式"""
    # 根据文件路径判断
    p = source_path.lower()
    if '.mdc' in p: return 'cursor'
    if 'copilot-instructions' in p: return 'github-copilot'
    if 'config.json' in p: return 'continue'
    if 'CONVENTIONS.md' in p or 'aider' in p: return 'aider'
    
    # 根据内容判断
    if text.startswith('---'):
        lines = text.split('\n')
        for line in lines[:20]:
            line = line.strip()
            if 'runAs:' in line: return 'reasonix'
            if 'allowed-tools:' in line: return 'reasonix'
            if 'globs:' in line: return 'cursor'
        return 'generic-yaml'  # 通用 YAML frontmatter 格式
    
    # 纯 markdown
    return 'plain-markdown'


def parse_skill(text: str, source_format: str = 'auto', source_path: str = '') -> dict:
    """解析任意格式的 skill，统一输出到中间字典"""
    if source_format == 'auto':
        source_format = detect_format(text, source_path)
    
    skill = {
        'name': '',
        'description': '',
        'body': '',
        'extra_fields': {},
    }
    
    if source_format in ('reasonix', 'hermes', 'opencode', 'claude-code', 'openai-codex', 'skills-cli', 'generic-yaml'):
        # YAML frontmatter 格式
        m = re.match(r'^---\s*\n(.*?)\n?---\s*\n(.*)', text, re.DOTALL)
        if m:
            yaml_text = m.group(1)
            body = m.group(2).strip()
            for line in yaml_text.strip().split('\n'):
                if ':' in line:
                    k, _, v = line.partition(':')
                    k, v = k.strip(), v.strip()
                    if k == 'name': skill['name'] = v
                    elif k == 'description': skill['description'] = v
                    else: skill['extra_fields'][k] = v
            skill['body'] = body
        else:
            skill['body'] = text.strip()
    
    elif source_format in ('cursor',):
        # Cursor .mdc 格式
        m = re.match(r'^---\s*\n(.*?)\n?---\s*\n(.*)', text, re.DOTALL)
        if m:
            yaml_text = m.group(1)
            body = m.group(2).strip()
            for line in yaml_text.strip().split('\n'):
                if ':' in line:
                    k, _, v = line.partition(':')
                    k, v = k.strip(), v.strip()
                    if k == 'name': skill['name'] = v
                    elif k == 'description': skill['description'] = v
                    elif k == 'globs': skill['extra_fields']['globs'] = v
                    else: skill['extra_fields'][k] = v
            skill['body'] = body
    
    elif source_format in ('github-copilot', 'aider', 'plain-markdown'):
        # 纯 Markdown: 把第一个 # 标题作为 name
        lines = text.strip().split('\n')
        body_lines = []
        for i, line in enumerate(lines):
            if line.startswith('# ') and not skill['name']:
                skill['name'] = line[2:].strip()
            elif line.startswith('> ') and not skill['description']:
                skill['description'] = line[2:].strip()
            else:
                body_lines.append(line)
        if not skill['name']:
            skill['name'] = 'unnamed-skill'
        skill['body'] = '\n'.join(body_lines).strip()
    
    elif source_format == 'continue':
        # JSON 格式
        try:
            data = json.loads(text) if isinstance(text, str) else text
            if isinstance(data, dict):
                skill['name'] = data.get('name', data.get('id', 'unnamed'))
                skill['description'] = data.get('description', '')
                skill['extra_fields'] = data
                skill['body'] = data.get('systemPrompt', data.get('prompt', ''))
        except:
            skill['body'] = str(text)
    
    # 自动填充 name
    if not skill['name']:
        skill['name'] = 'unnamed-skill'
    
    return skill


def render_skill(skill: dict, target_format: str, install_path: Optional[Path] = None) -> str:
    """将中间字典渲染为目标格式的文本"""
    name = skill['name']
    desc = skill['description']
    body = skill['body']
    extra = skill['extra_fields']
    
    agent = AGENTS.get(target_format)
    if not agent:
        raise ValueError(f'不支持的格式: {target_format}')
    
    # ── 带 YAML frontmatter 的格式 ──
    if target_format in ('reasonix', 'hermes', 'opencode', 'skills-cli'):
        fields = {}
        for f in agent['fields']:
            if f == 'name': fields['name'] = name
            elif f == 'description': fields['description'] = desc
            elif f in extra: fields[f] = extra[f]
            elif f in agent.get('extra', {}): fields[f] = agent['extra'][f]
        
        # 传递 extra_fields 中匹配的字段
        for k, v in extra.items():
            if k in agent['fields'] and k not in fields:
                fields[k] = v
        
        yaml_lines = ['---']
        for k, v in fields.items():
            if v: yaml_lines.append(f'{k}: {v}')
        yaml_lines.append('---')
        
        return '\n'.join(yaml_lines) + '\n\n' + body
    
    # ── Claude Code / OpenAI Codex（需要 plugin.json） ──
    elif target_format in ('claude-code', 'openai-codex'):
        fields = {'name': name, 'description': desc}
        yaml_lines = ['---']
        for k, v in fields.items():
            if v: yaml_lines.append(f'{k}: {v}')
        yaml_lines.append('---')
        
        content = '\n'.join(yaml_lines) + '\n\n' + body
        
        # 同时生成 plugin.json
        if install_path and 'extra_files' in agent:
            plugin_content = agent['extra_files']['plugin.json'].format(name=name, desc=desc)
            (install_path.parent / 'plugin.json').write_text(plugin_content, encoding='utf-8')
        
        return content
    
    # ── Cursor .mdc ──
    elif target_format == 'cursor':
        template = agent.get('template', '---\ndescription: {desc}\nglobs: **/*\n---\n\n{body}')
        globs = extra.get('globs', '**/*')
        return template.format(name=name, desc=desc, body=body, globs=globs)
    
    # ── GitHub Copilot / Aider ──
    elif target_format in ('github-copilot', 'aider'):
        template = agent.get('template', '# {name}\n\n{desc}\n\n{body}')
        return template.format(name=name, desc=desc, body=body)
    
    # ── Continue.dev JSON ──
    elif target_format == 'continue':
        data = {
            'name': name,
            'description': desc,
            'systemPrompt': body,
        }
        # 合并 extra_fields
        if isinstance(extra, dict):
            for k, v in extra.items():
                if k not in data:
                    data[k] = v
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    return body


def install_skill(skill_text: str, target_agents: list, source_format: str = 'auto', source_path: str = '') -> dict:
    """解析并安装 skill 到指定工具"""
    skill = parse_skill(skill_text, source_format, source_path)
    name = skill['name']
    
    results = {}
    for agent_id in target_agents:
        agent = AGENTS.get(agent_id)
        if not agent:
            results[agent_id] = f'❌ 不支持的格式: {agent_id}'
            continue
        
        # 计算路径
        home = Path.home()
        if agent_id == 'reasonix':
            base = home / '.reasonix' / 'skills'
        elif agent_id == 'hermes':
            base = home / '.hermes' / 'skills'
        elif agent_id == 'opencode':
            base = home / '.config' / 'opencode' / 'skills'
        elif agent_id in ('claude-code',):
            base = Path.cwd() / '.claude' / 'plugins'
        elif agent_id in ('openai-codex',):
            base = Path.cwd() / '.agents' / 'plugins'
        elif agent_id == 'cursor':
            base = Path.cwd() / '.cursor' / 'rules'
        elif agent_id == 'github-copilot':
            base = Path.cwd() / '.github'
        elif agent_id == 'continue':
            base = home / '.continue'
        elif agent_id == 'aider':
            base = Path.cwd()
        elif agent_id == 'skills-cli':
            base = Path.cwd() / '.skills'
        else:
            base = Path.cwd()
        
        file_name = agent['file_name'].format(name=name)
        
        if agent['dir_needed']:
            target_dir = base / name
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / file_name
        else:
            base.mkdir(parents=True, exist_ok=True)
            target_path = base / file_name
        
        try:
            content = render_skill(skill, agent_id, target_path)
            target_path.write_text(content, encoding='utf-8')
            results[agent_id] = f'✅ {agent["name"]} → {target_path}'
        except Exception as e:
            results[agent_id] = f'❌ {agent["name"]}: {e}'
    
    return {
        'name': name,
        'description': skill['description'],
        'body_length': len(skill['body']),
        'results': results,
    }


def list_all_agents():
    """列出所有支持的 AI Agent"""
    print(f'\n{"="*60}')
    print(f'  万能 Skill 格式转换器 v{VERSION}')
    print(f'  支持 {len(AGENTS)} 种 AI Agent 格式')
    print(f'{"="*60}\n')
    
    for aid, agent in AGENTS.items():
        print(f'  [{aid:15s}] {agent["name"]:<30s} {agent["format"]}')
    print()


def show_help():
    print(f'''
⭐ 万能 Skill 格式转换器 v{VERSION}

用法:
  # 查看支持的 AI Agent
  python ua.py --list

  # 自动检测并显示 skill 信息
  python ua.py skill.md --info

  # 安装到指定工具
  python ua.py skill.md --to reasonix,hermes,opencode

  # 从 URL 安装
  python ua.py https://.../SKILL.md --to all

  # 从 URL 安装到指定工具
  python ua.py https://.../SKILL.md --to cursor,claude-code

  # 指定源格式（自动检测失败时）
  python ua.py skill.mdc --source cursor --to reasonix,opencode

支持的 AI Agent（--to 参数）:
  all       - 安装到全部支持的 agent
''')
    for aid, agent in AGENTS.items():
        print(f'  {aid:15s} - {agent["name"]}')


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f'万能 Skill 格式转换器 v{VERSION}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('source', nargs='?', help='Skill 文件路径或 URL')
    parser.add_argument('--to', default='', help='目标 agent 列表 (逗号分隔) 或 all')
    parser.add_argument('--source-format', default='auto', choices=['auto'] + list(AGENTS.keys()) + ['plain-markdown', 'generic-yaml'],
                        help='源格式（默认自动检测）')
    parser.add_argument('--list', action='store_true', help='列出所有支持的 AI Agent')
    parser.add_argument('--info', action='store_true', help='显示 skill 信息')
    parser.add_argument('--export', help='导出为指定格式到 stdout')
    
    args = parser.parse_args()
    
    if args.list:
        list_all_agents()
        return
    
    if not args.source:
        show_help()
        return
    
    # ── 读取 ──
    source = args.source
    if source.startswith(('http://', 'https://')):
        import urllib.request
        try:
            print(f'📥 下载中...')
            req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=15)
            text = resp.read().decode('utf-8')
        except Exception as e:
            print(f'❌ 下载失败: {e}')
            return
        src_path = source
    else:
        p = Path(source)
        if not p.exists():
            print(f'❌ 文件不存在: {source}')
            return
        text = p.read_text(encoding='utf-8')
        src_path = str(p)
    
    # ── 解析 ──
    fmt = detect_format(text, src_path) if args.source_format == 'auto' else args.source_format
    skill = parse_skill(text, fmt, src_path)
    name = skill['name'] or '(未命名)'
    desc = skill['description'] or '(无描述)'
    body_len = len(skill['body'])
    extra_fields = skill['extra_fields']
    
    print(f'\n📋 Skill 信息:')
    print(f'  名称: {name}')
    print(f'  描述: {desc[:80]}')
    print(f'  检测格式: {fmt}')
    print(f'  正文: {body_len} 字符')
    if extra_fields:
        print(f'  额外字段: {json.dumps(extra_fields, ensure_ascii=False)}')
    
    if args.info:
        return
    
    # ── 导出 ──
    if args.export:
        try:
            content = render_skill(skill, args.export)
            print(content)
        except Exception as e:
            print(f'❌ 导出失败: {e}')
        return
    
    # ── 安装 ──
    if not args.to:
        print('\n❌ 请指定 --to 目标 (或 --list 查看支持的格式)')
        return
    
    targets = list(AGENTS.keys()) if args.to == 'all' else [t.strip() for t in args.to.split(',')]
    
    print(f'\n📦 安装目标 ({len(targets)}): {", ".join(targets)}')
    result = install_skill(text, targets, fmt, src_path)
    
    print(f'\n📦 安装结果:')
    for agent_id, msg in result['results'].items():
        print(f'  {msg}')
    print(f'\n✅ 完成!')


if __name__ == '__main__':
    main()
