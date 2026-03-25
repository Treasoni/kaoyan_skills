"""
kaoyan-english-vocab 技能代码模块

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24

本模块提供考研英语词汇学习的核心功能，包括：
1. 真题语境检索
2. 熟词僻义检测
3. 单词查询
4. PDF词汇提取
5. 单词表整理和格式化
"""

__version__ = "2.0.0"

# 从各个子模块导出核心函数

# 真题语境检索
from .context_retrieval import (
    generate_context_article,
    search_real_exam_pool,
    search_journal_pool,
    generate_ai_context,
    weave_contexts_into_article
)

# 熟词僻义检测
from .polysemy_detector import (
    detect_polysemy,
    calculate_semantic_overlap,
    calculate_exam_frequency,
    POLYSEMY_CRITICAL,
    POLYSEMY_WARNING
)

# 单词查询
from .word_lookup import (
    lookup_word,
    format_word_card
)

# PDF词汇提取
from .pdf_extractor import (
    extract_words_from_pdf,
    parse_momo_format,
    parse_baici_format,
    parse_generic_format
)

# 单词表整理和格式化
from .word_formatter import (
    organize_word_list,
    extract_words_from_raw_content,
    format_words,
    group_by_word_family,
    extract_word_root,
    classify_by_frequency,
    add_polysemy_alerts,
    generate_formatted_output,
    calculate_next_review_date,
    count_alerts
)

__all__ = [
    # 真题语境检索
    'generate_context_article',
    'search_real_exam_pool',
    'search_journal_pool',
    'generate_ai_context',
    'weave_contexts_into_article',

    # 熟词僻义检测
    'detect_polysemy',
    'calculate_semantic_overlap',
    'calculate_exam_frequency',
    'POLYSEMY_CRITICAL',
    'POLYSEMY_WARNING',

    # 单词查询
    'lookup_word',
    'format_word_card',

    # PDF词汇提取
    'extract_words_from_pdf',
    'parse_momo_format',
    'parse_baici_format',
    'parse_generic_format',

    # 单词表整理和格式化
    'organize_word_list',
    'extract_words_from_raw_content',
    'format_words',
    'group_by_word_family',
    'extract_word_root',
    'classify_by_frequency',
    'add_polysemy_alerts',
    'generate_formatted_output',
    'calculate_next_review_date',
    'count_alerts',
]
