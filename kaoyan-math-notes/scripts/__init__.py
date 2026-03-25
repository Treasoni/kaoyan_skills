"""
考研数学笔记生成模块

本模块是 kaoyan-math-notes 技能的Python实现，包含：
- 已有笔记保护机制
- 笔记生成辅助函数
- 笔记更新函数

版本: v2.0.0 (模块化重构)
"""

from .protection import (
    check_existing_notes,
    has_content,
)

from .generation import (
    extract_knowledge_points,
    generate_note_from_template,
    generate_latex_formula,
    generate_example_block,
)

from .update import (
    update_note_with_feedback,
    analyze_understanding_barrier,
)

__all__ = [
    # 保护机制
    "check_existing_notes",
    "has_content",
    # 生成函数
    "extract_knowledge_points",
    "generate_note_from_template",
    "generate_latex_formula",
    "generate_example_block",
    # 更新函数
    "update_note_with_feedback",
    "analyze_understanding_barrier",
]

__version__ = "2.0.0"
