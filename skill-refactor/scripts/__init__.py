"""
skill-refactor 技能的 Python 模块

提供技能文件自动化重构功能：
- 代码块检测和提取
- 内容拆分和模块化
- 变更报告生成
"""

from .detector import (
    detect_code_blocks,
    count_lines,
    analyze_skill_structure,
    needs_refactor,
    CodeBlock
)

from .splitter import (
    ContentSplitter,
    ContentSection,
    split_by_sections,
    analyze_split_preview
)

from .refactor import (
    SkillRefactor,
    RefactorAnalysis,
    RefactorResult,
    format_confirmation_prompt,
    generate_refactor_report
)

__all__ = [
    # detector
    'detect_code_blocks',
    'count_lines',
    'analyze_skill_structure',
    'needs_refactor',
    'CodeBlock',

    # splitter
    'ContentSplitter',
    'ContentSection',
    'split_by_sections',
    'analyze_split_preview',

    # refactor
    'SkillRefactor',
    'RefactorAnalysis',
    'RefactorResult',
    'format_confirmation_prompt',
    'generate_refactor_report',
]
