"""
考研数学知识点结构模块

本模块是 kaoyan-math-structure 技能的Python实现，包含：
- 知识点关系图数据
- 目录结构模板
- 高等数学/线性代数/概率论知识点树
- 知识点查询函数

版本: v2.0.0 (模块化重构)
"""

from .data import (
    KNOWLEDGE_GRAPH,
    MODULE_STRUCTURE,
    HIGHER_MATH_KNOWLEDGE_TREE,
    LINEAR_ALGEBRA_KNOWLEDGE_TREE,
    PROBABILITY_KNOWLEDGE_TREE,
)

from .queries import (
    get_knowledge_structure,
    find_submodule,
    get_knowledge_relations,
    generate_directory_structure,
    get_all_keywords,
    search_knowledge_point,
)

__all__ = [
    # 数据结构
    "KNOWLEDGE_GRAPH",
    "MODULE_STRUCTURE",
    "HIGHER_MATH_KNOWLEDGE_TREE",
    "LINEAR_ALGEBRA_KNOWLEDGE_TREE",
    "PROBABILITY_KNOWLEDGE_TREE",
    # 查询函数
    "get_knowledge_structure",
    "find_submodule",
    "get_knowledge_relations",
    "generate_directory_structure",
    "get_all_keywords",
    "search_knowledge_point",
]

__version__ = "2.0.0"
