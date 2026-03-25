"""
熟词僻义检测模块

本模块处理考研英语中的熟词僻义检测，包括：
- 僻义检测算法
- 语义重叠度计算
- 考研词频计算
- 僻义词库数据

来源: code.md 第161-342行
"""

from typing import List, Dict, Any, Optional


# 熟词僻义库数据
POLYSEMY_CRITICAL = [
    {"word": "address", "common_meaning": "地址", "rare_meaning": "vt. 处理，解决", "exam_frequency": "80%", "collocations": ["address the problem", "address an issue", "address concerns"]},
    {"word": "school", "common_meaning": "学校", "rare_meaning": "n. 流派，学派", "exam_frequency": "70%", "collocations": ["school of thought", "different schools"]},
    {"word": "novel", "common_meaning": "新颖的", "rare_meaning": "n. 长篇小说", "exam_frequency": "65%", "collocations": ["historical novel", "novel writer"]},
    {"word": "fine", "common_meaning": "好的", "rare_meaning": "n./v. 罚款", "exam_frequency": "60%", "collocations": ["impose a fine", "fine sb for sth"]},
    {"word": "reason", "common_meaning": "原因", "rare_meaning": "v. 推理，推论", "exam_frequency": "55%", "collocations": ["reason with sb", "reasoning ability"]},
    {"word": "discipline", "common_meaning": "纪律", "rare_meaning": "n. 学科", "exam_frequency": "50%", "collocations": ["academic discipline", "various disciplines"]},
    {"word": "consume", "common_meaning": "消费", "rare_meaning": "vt. 毁灭，烧毁", "exam_frequency": "40%", "collocations": ["be consumed by", "consume time"]},
    {"word": "draft", "common_meaning": "草稿", "rare_meaning": "n. 征兵", "exam_frequency": "35%", "collocations": ["military draft", "draft dodger"]},
    {"word": "compound", "common_meaning": "复合的", "rare_meaning": "v. 加剧，恶化", "exam_frequency": "30%", "collocations": ["compound the problem", "compound interest"]},
]

POLYSEMY_WARNING = [
    {"word": "spring", "common_meaning": "春天", "rare_meaning": "v. 突然出现，涌现", "exam_frequency": "40%", "collocations": ["spring up", "spring from"]},
    {"word": "table", "common_meaning": "桌子", "rare_meaning": "v. 搁置，暂缓讨论", "exam_frequency": "35%", "collocations": ["table a proposal", "table the motion"]},
    {"word": "book", "common_meaning": "书", "rare_meaning": "v. 预订", "exam_frequency": "30%", "collocations": ["book a ticket", "book in advance"]},
]


def detect_polysemy(word: str) -> Optional[Dict[str, Any]]:
    """
    检测单词是否在考研中有僻义

    Args:
        word: 目标单词

    Returns:
        PolysemyAlert: 僻义预警对象，无僻义时返回 None
    """
    # 1. 检索考研大纲词表
    outline_entry = search_exam_outline(word)

    # 2. 对比大纲释义与常见释义
    common_meanings = get_common_dictionary_meanings(word)
    exam_meanings = outline_entry.get("meanings", []) if outline_entry else []

    # 3. 计算语义重叠度
    overlap = calculate_semantic_overlap(common_meanings, exam_meanings)

    # 4. 判断是否存在僻义
    if overlap < 0.5:  # 重叠度低于50%，存在显著僻义
        return {
            "word": word,
            "alert_type": "critical" if overlap < 0.3 else "warning",
            "rare_meanings": [m for m in exam_meanings if m not in common_meanings],
            "common_meanings": common_meanings,
            "exam_frequency": calculate_exam_frequency(word)
        }

    return None


def calculate_semantic_overlap(meanings1: List[str], meanings2: List[str]) -> float:
    """
    计算两个释义集合的语义重叠度

    Args:
        meanings1: 释义集合1
        meanings2: 释义集合2

    Returns:
        float: 重叠度 (0.0-1.0)
    """
    if not meanings1 or not meanings2:
        return 0.0

    # 简化实现：计算释义关键词交集比例
    words1 = set()
    for m in meanings1:
        words1.update(m.lower().split())

    words2 = set()
    for m in meanings2:
        words2.update(m.lower().split())

    # 移除停用词
    stopwords = {"the", "a", "an", "of", "to", "in", "for", "and", "or"}
    words1 -= stopwords
    words2 -= stopwords

    if not words1 or not words2:
        return 0.0

    intersection = words1 & words2
    union = words1 | words2

    return len(intersection) / len(union)


def calculate_exam_frequency(word: str) -> str:
    """
    计算单词在考研中的出现频率

    Args:
        word: 目标单词

    Returns:
        str: 频率等级 (high/medium/low)
    """
    # 查询历年真题词频
    frequency_data = query_exam_frequency_database(word)

    if frequency_data >= 5:
        return "high"
    elif frequency_data >= 2:
        return "medium"
    else:
        return "low"


def search_exam_outline(word: str) -> Optional[Dict[str, Any]]:
    """
    搜索考研大纲词表

    Args:
        word: 目标单词

    Returns:
        dict: 大纲词条，找不到返回None
    """
    # 简化实现：实际应从大纲文件中检索
    return None


def get_common_dictionary_meanings(word: str) -> List[str]:
    """
    获取常见词典释义

    Args:
        word: 目标单词

    Returns:
        list: 常见释义列表
    """
    # 简化实现：实际应从词典API获取
    return []


def query_exam_frequency_database(word: str) -> int:
    """
    查询真题词频数据库

    Args:
        word: 目标单词

    Returns:
        int: 出现次数
    """
    # 简化实现：实际应从词频数据库查询
    return 0


def get_polysemy_by_word(word: str) -> Optional[Dict[str, Any]]:
    """
    根据单词获取僻义信息（从库中查找）

    Args:
        word: 目标单词

    Returns:
        dict: 僻义信息，找不到返回None
    """
    # 先查找 Critical 级别
    for item in POLYSEMY_CRITICAL:
        if item["word"].lower() == word.lower():
            return {
                "level": "critical",
                **item
            }

    # 再查找 Warning 级别
    for item in POLYSEMY_WARNING:
        if item["word"].lower() == word.lower():
            return {
                "level": "warning",
                **item
            }

    return None


def is_polysemy_word(word: str) -> bool:
    """
    快速判断单词是否为僻义词

    Args:
        word: 目标单词

    Returns:
        bool: 是否为僻义词
    """
    return get_polysemy_by_word(word) is not None
