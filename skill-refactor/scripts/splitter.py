"""
内容拆分器

处理过长内容的模块化拆分，保持原文档结构顺序。
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ContentSection:
    """内容章节"""
    level: int
    title: str
    content: str
    start_line: int
    end_line: int
    line_count: int


class ContentSplitter:
    """内容拆分器"""

    # 保留在主文档的章节关键词
    KEEP_SECTION_KEYWORDS = {
        '概述', '功能', '触发', '使用', '验证',
        '版本', 'overview', 'usage', 'trigger',
        '简介', '说明', '目录', '索引', 'frontmatter'
    }

    # 优化的章节匹配正则 - 支持 H1-H6，兼容空格和 Windows 换行符
    SECTION_PATTERN = re.compile(r'^(#{1,6})[ \t]+(.+)$', re.MULTILINE)

    def __init__(self, content: str, filename: str = "document"):
        """
        初始化拆分器。

        参数:
            content: 文档内容
            filename: 文件名（用于生成模块名）
        """
        self.content = content
        self.filename = filename
        self.lines = content.splitlines()

    def extract_sections(self) -> List[ContentSection]:
        """提取所有章节，包括 Frontmatter"""
        sections = []
        current_section = None

        for i, line in enumerate(self.lines):
            match = self.SECTION_PATTERN.match(line)
            if match:
                # 保存上一个章节
                if current_section:
                    current_section.end_line = i - 1
                    current_section.line_count = i - current_section.start_line
                    current_section.content = '\n'.join(
                        self.lines[current_section.start_line:i]
                    )
                    sections.append(current_section)
                elif i > 0:
                    # 关键修复：捕获第一个标题之前的内容（如 YAML Frontmatter）
                    sections.append(ContentSection(
                        level=0,
                        title="Frontmatter",
                        content='\n'.join(self.lines[:i]),
                        start_line=0,
                        end_line=i - 1,
                        line_count=i
                    ))

                # 开始新章节
                current_section = ContentSection(
                    level=len(match.group(1)),
                    title=match.group(2).strip(),
                    content='',
                    start_line=i,
                    end_line=0,
                    line_count=0
                )

        # 保存最后一个章节
        if current_section:
            current_section.end_line = len(self.lines) - 1
            current_section.line_count = len(self.lines) - current_section.start_line
            current_section.content = '\n'.join(
                self.lines[current_section.start_line:]
            )
            sections.append(current_section)

        return sections

    def should_split_section(self, section: ContentSection, threshold: int = 50) -> bool:
        """
        判断章节是否应该拆分。

        参数:
            section: 章节信息
            threshold: 行数阈值

        返回:
            是否应拆分
        """
        # 强制保留 Frontmatter（level=0）
        if section.level == 0:
            return False

        # 检查是否为核心章节（保留在主文档）
        title_lower = section.title.lower()
        for keyword in self.KEEP_SECTION_KEYWORDS:
            if keyword.lower() in title_lower:
                return False

        # 检查行数是否超过阈值
        return section.line_count > threshold

    def plan_split(self, threshold: int = 50) -> Dict:
        """
        规划拆分策略。

        参数:
            threshold: 章节拆分阈值

        返回:
            {
                'all_sections': List[ContentSection],
                'split_sections': List[ContentSection],
                'total_lines': int,
                'lines_to_split': int
            }
        """
        sections = self.extract_sections()
        split_sections = []

        for section in sections:
            if self.should_split_section(section, threshold):
                split_sections.append(section)

        return {
            'all_sections': sections,
            'split_sections': split_sections,
            'total_lines': len(self.lines),
            'lines_to_split': sum(s.line_count for s in split_sections)
        }

    def execute_split(
        self,
        output_dir: Path,
        skill_name: str
    ) -> Tuple[str, List[Path]]:
        """
        执行拆分 - **保持原文档结构顺序**。

        关键改进：按照原始章节顺序遍历，在原位置插入引用链接，
        而不是把所有拆分内容追加到文档末尾。

        参数:
            output_dir: 输出目录
            skill_name: 技能名称

        返回:
            (主文档内容, 新增模块文件列表)
        """
        plan = self.plan_split()
        modules_dir = output_dir / "modules"
        modules_dir.mkdir(exist_ok=True)

        main_content_parts = []
        created_files = []

        # 按照原文档的章节顺序遍历，保证结构不乱
        for section in plan['all_sections']:
            if self.should_split_section(section):
                # 这是一个需要拆分的章节 -> 生成模块文件，在原位置插入引用
                safe_name = self._sanitize_filename(section.title)
                module_file = modules_dir / f"{safe_name}.md"

                # 生成并写入模块内容
                module_content = self._generate_module_content(section, skill_name)
                module_file.write_text(module_content, encoding='utf-8')
                created_files.append(module_file)

                # 在原位置插入章节标题 + 引用链接（保持原文结构和层级）
                heading_prefix = '#' * section.level
                main_content_parts.append(f"{heading_prefix} {section.title}\n")
                main_content_parts.append(f"> 📁 详细内容见 [{section.title}](modules/{module_file.name})\n")
            else:
                # 不需要拆分的章节，保留原内容
                main_content_parts.append(section.content)

        # 添加模块文档表（可选，放在文档末尾作为导航）
        if created_files:
            main_content_parts.append("\n---\n\n## 📁 模块文档\n")
            main_content_parts.append("| 模块 | 文件 | 内容 |\n")
            main_content_parts.append("|------|------|------|\n")
            for module_file in created_files:
                section_title = module_file.stem.replace('_', ' ').title()
                main_content_parts.append(
                    f"| {section_title} | [modules/{module_file.name}](modules/{module_file.name}) | 详细说明 |\n"
                )

        return '\n\n'.join(main_content_parts), created_files

    def _sanitize_filename(self, title: str) -> str:
        """将标题转换为有效的文件名"""
        # 移除特殊字符
        safe = re.sub(r'[^\w\s-]', '', title)
        # 空格转下划线
        safe = re.sub(r'\s+', '_', safe)
        return safe.lower()[:50]

    def _generate_module_content(self, section: ContentSection, skill_name: str) -> str:
        """生成模块文件内容"""
        return f"""# {section.title}

> 📋 **返回主文档**: [../SKILL.md](../SKILL.md)

---

{section.content}

---

*所属技能: {skill_name}*

> 📋 **返回主文档**: [../SKILL.md](../SKILL.md)
"""


def split_by_sections(
    content: str,
    output_dir: Path,
    skill_name: str,
    threshold: int = 50
) -> Tuple[str, List[Path]]:
    """
    按章节拆分内容的便捷函数。

    参数:
        content: 文档内容
        output_dir: 输出目录
        skill_name: 技能名称
        threshold: 拆分阈值

    返回:
        (主文档内容, 新增文件列表)
    """
    splitter = ContentSplitter(content, skill_name)
    return splitter.execute_split(output_dir, skill_name)


def analyze_split_preview(content: str, threshold: int = 50) -> str:
    """
    生成拆分预览。

    参数:
        content: 文档内容
        threshold: 拆分阈值

    返回:
        预览文本
    """
    splitter = ContentSplitter(content)
    plan = splitter.plan_split(threshold)

    preview = f"""## 📊 拆分预览

**总行数**: {plan['total_lines']}
**拟拆分行数**: {plan['lines_to_split']}

### 章节结构预览（保持原顺序）

"""

    for section in plan['all_sections']:
        if splitter.should_split_section(section, threshold):
            safe_name = splitter._sanitize_filename(section.title)
            preview += f"- 📦 **{section.title}** ({section.line_count}行) → modules/{safe_name}.md\n"
        else:
            preview += f"- ✅ {section.title} ({section.line_count}行) - 保留在主文档\n"

    return preview
