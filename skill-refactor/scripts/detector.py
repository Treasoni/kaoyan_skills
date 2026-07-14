"""
代码块检测器

用于检测 Markdown 文件中的代码块、统计行数、分析文件结构。
复用 splitter.py 的章节提取逻辑（DRY 原则）。
"""

import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

# 复用 splitter.py 的章节提取逻辑
from .splitter import ContentSplitter, ContentSection


@dataclass
class CodeBlock:
    """代码块信息"""
    language: str
    code: str
    start_line: int
    end_line: int
    start_pos: int
    end_pos: int


# 优化的代码块正则 - 兼容空格和 Windows 换行符
CODE_BLOCK_PATTERN = re.compile(
    r'```(\w*)[ \t]*\r?\n(.*?)\r?\n```',
    re.DOTALL
)

# 可提取的代码语言
EXTRACTABLE_LANGUAGES = {
    'python', 'py', 'yaml', 'yml',
    'javascript', 'js', 'typescript', 'ts',
    'json', 'bash', 'sh', 'shell', 'mermaid'
}


def detect_code_blocks(content: str) -> List[CodeBlock]:
    """
    检测 Markdown 内容中的所有代码块。

    参数:
        content: Markdown 文本内容

    返回:
        代码块列表
    """
    blocks = []

    for match in CODE_BLOCK_PATTERN.finditer(content):
        lang = match.group(1) or 'text'
        code = match.group(2)

        # 计算行号
        start_pos = match.start()
        end_pos = match.end()

        start_line = content[:start_pos].count('\n') + 1
        end_line = content[:end_pos].count('\n') + 1

        if lang.lower() in EXTRACTABLE_LANGUAGES:
            blocks.append(CodeBlock(
                language=lang,
                code=code,
                start_line=start_line,
                end_line=end_line,
                start_pos=start_pos,
                end_pos=end_pos
            ))

    return blocks


def count_lines(file_path: Path) -> int:
    """
    统计文件行数。

    参数:
        file_path: 文件路径

    返回:
        行数（文件不存在返回 0）
    """
    if not file_path.exists():
        return 0

    try:
        content = file_path.read_text(encoding='utf-8')
        return len(content.splitlines())
    except Exception:
        return 0


def extract_sections(content: str) -> List[Dict]:
    """
    提取 Markdown 文档的章节结构。

    复用 splitter.py 的 ContentSplitter 逻辑（DRY 原则）。

    参数:
        content: Markdown 文本内容

    返回:
        章节列表
    """
    splitter = ContentSplitter(content)
    sections = splitter.extract_sections()

    return [
        {
            'level': s.level,
            'title': s.title,
            'start_line': s.start_line,
            'end_line': s.end_line,
            'line_count': s.line_count
        }
        for s in sections
    ]


def analyze_skill_structure(skill_path: Path) -> Dict:
    """
    分析技能目录结构。

    参数:
        skill_path: 技能目录路径

    返回:
        结构分析结果
    """
    skill_file = skill_path / "SKILL.md"
    code_file = skill_path / "code.md"

    result = {
        "skill_name": skill_path.name,
        "skill_exists": skill_file.exists(),
        "code_exists": code_file.exists(),
        "skill_lines": 0,
        "code_lines": 0,
        "has_code_blocks": False,
        "code_block_count": 0,
        "code_block_languages": [],
        "sections": [],
        "has_modules": (skill_path / "modules").exists(),
        "has_scripts": (skill_path / "scripts").exists()
    }

    if skill_file.exists():
        content = skill_file.read_text(encoding='utf-8')
        result["skill_lines"] = len(content.splitlines())

        blocks = detect_code_blocks(content)
        result["has_code_blocks"] = len(blocks) > 0
        result["code_block_count"] = len(blocks)
        result["code_block_languages"] = list(set(b.language for b in blocks))

        # 复用 splitter.py 的章节提取逻辑
        result["sections"] = extract_sections(content)

    if code_file.exists():
        result["code_lines"] = count_lines(code_file)

    return result


def needs_refactor(
    skill_path: Path,
    skill_threshold: int = 300,
    code_threshold: int = 400
) -> Dict:
    """
    判断技能是否需要重构。

    参数:
        skill_path: 技能目录路径
        skill_threshold: SKILL.md 行数阈值
        code_threshold: code.md 行数阈值

    返回:
        {
            'needs_refactor': bool,
            'reasons': List[str],
            'analysis': Dict
        }
    """
    analysis = analyze_skill_structure(skill_path)
    reasons = []

    # 检查是否需要代码提取
    if analysis['has_code_blocks'] and not analysis['code_exists']:
        reasons.append(f"包含 {analysis['code_block_count']} 个代码块可提取")

    # 检查 SKILL.md 长度
    if analysis['skill_lines'] > skill_threshold:
        reasons.append(f"文件长度 {analysis['skill_lines']} 行（超过 {skill_threshold} 行阈值）")

    # 检查 code.md 长度
    if analysis['code_lines'] > code_threshold:
        reasons.append(f"code.md 长度 {analysis['code_lines']} 行（超过 {code_threshold} 行阈值）")

    return {
        'needs_refactor': len(reasons) > 0,
        'reasons': reasons,
        'analysis': analysis
    }
