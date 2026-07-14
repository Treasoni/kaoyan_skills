"""
技能重构器

执行技能文件的代码提取、内容拆分等重构操作。
包含破坏性操作的防御机制。
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from .splitter import split_by_sections, ContentSplitter, analyze_split_preview


@dataclass
class CodeBlock:
    """代码块信息"""
    language: str
    code: str
    start_line: int
    end_line: int
    start_pos: int
    end_pos: int


@dataclass
class RefactorAnalysis:
    """重构分析结果"""
    skill_name: str
    skill_path: Path

    # SKILL.md 分析
    skill_exists: bool
    skill_lines: int
    has_code_blocks: bool
    code_block_count: int
    code_block_languages: List[str]

    # code.md 分析
    code_exists: bool
    code_lines: int

    # 拆分建议
    needs_code_extraction: bool
    needs_skill_split: bool
    needs_code_split: bool

    # 警告信息
    warnings: List[str] = field(default_factory=list)

    # 模块章节
    sections: List[Dict] = field(default_factory=list)

    # 总体判断
    needs_refactor: bool = False


@dataclass
class RefactorResult:
    """重构执行结果"""
    success: bool
    changes: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    lines_before: Dict[str, int] = field(default_factory=dict)
    lines_after: Dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None


# 阈值配置
SKILL_THRESHOLD = 300  # SKILL.md 行数阈值
CODE_THRESHOLD = 400   # code.md 行数阈值

# 引用模板
CODE_REFERENCE_TEMPLATE = """> 📁 详细代码实现见 [code.md](code.md)"""

MODULE_REFERENCE_TEMPLATE = """> 📁 详细内容见 [{module_name}]({module_path})"""

# 优化的代码块正则 - 兼容空格和 Windows 换行符
CODE_BLOCK_PATTERN = re.compile(
    r'```(\w*)[ \t]*\r?\n(.*?)\r?\n```',
    re.DOTALL
)


class SkillRefactor:
    """技能重构器"""

    def __init__(self, skill_path: Path):
        """
        初始化重构器。

        参数:
            skill_path: 技能目录路径
        """
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.skill_file = self.skill_path / "SKILL.md"
        self.code_file = self.skill_path / "code.md"

    def analyze(self) -> RefactorAnalysis:
        """分析技能文件，返回重构建议"""
        warnings = []

        # 检查 SKILL.md
        skill_exists = self.skill_file.exists()
        skill_lines = 0
        has_code_blocks = False
        code_block_count = 0
        code_block_languages = []

        if skill_exists:
            content = self.skill_file.read_text(encoding='utf-8')
            skill_lines = len(content.splitlines())
            blocks = self._detect_code_blocks(content)
            has_code_blocks = len(blocks) > 0
            code_block_count = len(blocks)
            code_block_languages = list(set(b.language for b in blocks))

        # 检查 code.md
        code_exists = self.code_file.exists()
        code_lines = 0

        if code_exists:
            code_lines = len(self.code_file.read_text(encoding='utf-8').splitlines())
            # 警告：code.md 已存在，提取操作可能覆盖
            if code_lines > 0:
                warnings.append(f"⚠️ code.md 已存在（{code_lines}行），代码提取将追加而非覆盖")

        # 提取章节结构
        sections = []
        if skill_exists:
            content = self.skill_file.read_text(encoding='utf-8')
            splitter = ContentSplitter(content, self.skill_name)
            sections = [
                {
                    'level': s.level,
                    'title': s.title,
                    'line_count': s.line_count
                }
                for s in splitter.extract_sections()
            ]

        # 判断是否需要重构
        needs_code_extraction = has_code_blocks and not code_exists
        needs_skill_split = skill_lines > SKILL_THRESHOLD
        needs_code_split = code_lines > CODE_THRESHOLD

        return RefactorAnalysis(
            skill_name=self.skill_name,
            skill_path=self.skill_path,
            skill_exists=skill_exists,
            skill_lines=skill_lines,
            has_code_blocks=has_code_blocks,
            code_block_count=code_block_count,
            code_block_languages=code_block_languages,
            code_exists=code_exists,
            code_lines=code_lines,
            needs_code_extraction=needs_code_extraction,
            needs_skill_split=needs_skill_split,
            needs_code_split=needs_code_split,
            warnings=warnings,
            sections=sections,
            needs_refactor=any([
                needs_code_extraction,
                needs_skill_split,
                needs_code_split
            ])
        )

    def execute(self, analysis: RefactorAnalysis) -> RefactorResult:
        """
        根据分析结果执行重构。

        参数:
            analysis: 分析结果

        返回:
            重构执行结果
        """
        result = RefactorResult(
            success=True,
            warnings=analysis.warnings.copy(),
            lines_before={
                'SKILL.md': analysis.skill_lines,
                'code.md': analysis.code_lines
            }
        )

        try:
            # 1. 代码提取（带防御机制）
            if analysis.needs_code_extraction:
                extract_result = self._extract_code_to_code_md(analysis)
                if extract_result:
                    result.changes.append(f"提取 {analysis.code_block_count} 个代码块到 code.md")
                    result.files_created.append("code.md")
                    result.files_modified.append("SKILL.md")
                elif extract_result is False and analysis.code_exists:
                    result.warnings.append("⚠️ code.md 已存在，代码提取已跳过（使用追加模式或手动合并）")

            # 2. SKILL.md 拆分（已打通）
            if analysis.needs_skill_split:
                split_files = self._split_skill_content(analysis)
                if split_files:
                    result.changes.append(f"SKILL.md 拆分为 {len(split_files) + 1} 个模块")
                    result.files_modified.append("SKILL.md")
                    result.files_created.extend(f"modules/{f.name}" for f in split_files)

            # 3. code.md 拆分（暂不实现，需要用户确认）
            if analysis.needs_code_split:
                result.warnings.append(
                    f"⚠️ code.md 超过 {CODE_THRESHOLD} 行，建议手动模块化拆分"
                )

            # 更新行数统计
            result.lines_after = {
                'SKILL.md': self._count_lines(self.skill_file),
                'code.md': self._count_lines(self.code_file)
            }

        except Exception as e:
            result.success = False
            result.error = str(e)

        return result

    def _detect_code_blocks(self, content: str) -> List[CodeBlock]:
        """检测 Markdown 内容中的所有代码块"""
        blocks = []

        for match in CODE_BLOCK_PATTERN.finditer(content):
            lang = match.group(1) or 'text'
            code = match.group(2)

            start_pos = match.start()
            end_pos = match.end()

            start_line = content[:start_pos].count('\n') + 1
            end_line = content[:end_pos].count('\n') + 1

            blocks.append(CodeBlock(
                language=lang,
                code=code,
                start_line=start_line,
                end_line=end_line,
                start_pos=start_pos,
                end_pos=end_pos
            ))

        return blocks

    def _extract_code_to_code_md(self, analysis: RefactorAnalysis) -> Optional[bool]:
        """
        提取代码到 code.md（带防御机制）。

        返回:
            True: 成功提取
            False: 跳过（已有 code.md）
            None: 无代码块可提取
        """
        if not self.skill_file.exists():
            return None

        content = self.skill_file.read_text(encoding='utf-8')
        blocks = self._detect_code_blocks(content)

        if not blocks:
            return None

        # 防御机制：检查 code.md 是否已存在
        if self.code_file.exists():
            existing_content = self.code_file.read_text(encoding='utf-8')
            if len(existing_content.strip()) > 0:
                # 已有内容，使用追加模式
                new_content = self._generate_code_md_append_content(blocks)
                self.code_file.write_text(
                    existing_content + "\n\n---\n\n" + new_content,
                    encoding='utf-8'
                )
            else:
                # 空文件，直接写入
                code_content = self._generate_code_md_content(blocks)
                self.code_file.write_text(code_content, encoding='utf-8')
        else:
            # 不存在，创建新文件
            code_content = self._generate_code_md_content(blocks)
            self.code_file.write_text(code_content, encoding='utf-8')

        # 更新 SKILL.md - 替换代码块为引用
        new_content = self._replace_code_blocks_with_reference(content, blocks)
        self.skill_file.write_text(new_content, encoding='utf-8')

        return True

    def _split_skill_content(self, analysis: RefactorAnalysis) -> List[Path]:
        """
        拆分过长的 SKILL.md 内容（已打通）。
        """
        if not self.skill_file.exists():
            return []

        content = self.skill_file.read_text(encoding='utf-8')

        # 调用 splitter.py 的拆分逻辑
        new_main_content, created_files = split_by_sections(
            content=content,
            output_dir=self.skill_path,
            skill_name=self.skill_name
        )

        # 覆写精简后的 SKILL.md
        self.skill_file.write_text(new_main_content, encoding='utf-8')

        return created_files

    def _generate_code_md_content(self, blocks: List[CodeBlock]) -> str:
        """生成 code.md ���件内容"""
        header = f"""# {self.skill_name} 代码模块

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 概述

本文件提供 {self.skill_name} 技能的代码实现逻辑。

---

"""

        sections = []
        for i, block in enumerate(blocks, 1):
            lang = block.language
            code = block.code
            sections.append(f"""### 代码块 {i}: {lang}

```{lang}
{code}
```

---

""")

        footer = f"""
## 版本信息

- **创建日期**: {datetime.now().strftime('%Y-%m-%d')}
- **版本**: 1.0.0 (自动提取)

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
"""

        return header + ''.join(sections) + footer

    def _generate_code_md_append_content(self, blocks: List[CodeBlock]) -> str:
        """生成追加到现有 code.md 的内容"""
        sections = []
        sections.append(f"""
## 新增代码块 ({datetime.now().strftime('%Y-%m-%d')})

""")

        for i, block in enumerate(blocks, 1):
            lang = block.language
            code = block.code
            sections.append(f"""### 代码块 {i}: {lang}

```{lang}
{code}
```

---

""")

        return ''.join(sections)

    def _replace_code_blocks_with_reference(self, content: str, blocks: List[CodeBlock]) -> str:
        """将代码块替换为引用链接"""
        # 从后向前替换，避免位置偏移
        result = content
        for block in reversed(blocks):
            result = result[:block.start_pos] + CODE_REFERENCE_TEMPLATE + result[block.end_pos:]

        return result

    def _count_lines(self, file_path: Path) -> int:
        """统计文件行数"""
        if not file_path.exists():
            return 0
        return len(file_path.read_text(encoding='utf-8').splitlines())


def format_confirmation_prompt(analysis: RefactorAnalysis) -> str:
    """生成用户确认提示"""

    reasons = []

    if analysis.needs_code_extraction:
        reasons.append(f"- 包含 {analysis.code_block_count} 个代码块可提取")

    if analysis.needs_skill_split:
        reasons.append(f"- 文件长度 {analysis.skill_lines} 行（超过 {SKILL_THRESHOLD} 行阈值）")

    if analysis.needs_code_split:
        reasons.append(f"- code.md 长度 {analysis.code_lines} 行（超过 {CODE_THRESHOLD} 行阈值）")

    warning_text = ""
    if analysis.warnings:
        warning_text = f"\n\n⚠️ **注意**:\n" + "\n".join(f"- {w}" for w in analysis.warnings)

    return f"""🔍 检测到 {analysis.skill_name} 需要重构：

{chr(10).join(reasons)}
{warning_text}

是否执行重构？
[✅ 立即执行] [⏭️ 跳过] [📋 查看详情]
"""


def generate_refactor_report(
    skill_name: str,
    analysis: RefactorAnalysis,
    result: RefactorResult
) -> str:
    """生成重构变更报告"""

    report = f"""# 🔧 技能重构报告: {skill_name}

## 📊 变更统计

| 项目 | 原始 | 重构后 |
|------|------|--------|
| SKILL.md 行数 | {analysis.skill_lines} | {result.lines_after.get('SKILL.md', 'N/A')} |
| code.md 行数 | {analysis.code_lines} | {result.lines_after.get('code.md', 'N/A')} |
| 新增模块文件 | 0 | {len(result.files_created)} |

## ✅ 执行操作

"""

    for i, change in enumerate(result.changes, 1):
        report += f"{i}. {change}\n"

    if result.warnings:
        report += "\n## ⚠️ 警告信息\n\n"
        for w in result.warnings:
            report += f"- {w}\n"

    report += f"""
## 📁 文件变更

### 修改的文件
"""
    for f in result.files_modified:
        report += f"- 修改: {f}\n"

    report += "\n### 新增的文件\n"
    for f in result.files_created:
        report += f"- 新增: {f}\n"

    if not result.success:
        report += f"""
## ❌ 错误信息

{result.error}
"""

    return report
