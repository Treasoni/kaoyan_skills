"""
考研数学核心模块

本模块是 kaoyan-math-core 技能的Python实现，包含：
- MemOS 集成（用户上下文加载、错题保存）
- 知识图谱管理
- 数学笔记生成辅助

版本: v2.0.0 (模块化重构)
"""

from .memos_client import (
    load_user_context_from_memory,
    save_mistake_to_memory,
    save_knowledge_card_to_memory,
    parse_memory_to_math_context,
    extract_user_profile,
    extract_mistake_records,
    extract_knowledge_cards,
)

from .knowledge_graph import (
    get_module_structure,
    get_knowledge_point_relationships,
    calculate_learning_path,
    get_prerequisite_map,
    get_cross_subject_connections,
)

__all__ = [
    # MemOS 集成
    "load_user_context_from_memory",
    "save_mistake_to_memory",
    "save_knowledge_card_to_memory",
    "parse_memory_to_math_context",
    "extract_user_profile",
    "extract_mistake_records",
    "extract_knowledge_cards",
    # 知识图谱
    "get_module_structure",
    "get_knowledge_point_relationships",
    "calculate_learning_path",
    "get_prerequisite_map",
    "get_cross_subject_connections",
]

__version__ = "2.0.0"
