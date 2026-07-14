"""
熟词僻义检测模块

本模块处理考研英语中的熟词僻义检测，包括：
- 僻义检测算法
- 语义重叠度计算
- 考研词频计算
- 僻义词库数据

数据来源: data/polysemy-database.md
"""

from typing import List, Dict, Any, Optional


# ========================================
# 熟词僻义库数据
# ========================================

POLYSEMY_CRITICAL = [
    {"word": "address", "common_meaning": "地址", "rare_meaning": "vt. 处理，解决", "exam_frequency": "80%", "collocations": ["address the problem", "address an issue", "address concerns"]},
    {"word": "school", "common_meaning": "学校", "rare_meaning": "n. 流派，学派", "exam_frequency": "70%", "collocations": ["school of thought", "different schools", "academic school"]},
    {"word": "novel", "common_meaning": "新颖的", "rare_meaning": "n. 长篇小说", "exam_frequency": "65%", "collocations": ["historical novel", "novel writer", "write a novel"]},
    {"word": "fine", "common_meaning": "好的", "rare_meaning": "n./v. 罚款", "exam_frequency": "60%", "collocations": ["impose a fine", "fine sb for sth", "pay a fine"]},
    {"word": "reason", "common_meaning": "原因", "rare_meaning": "v. 推理，推论", "exam_frequency": "55%", "collocations": ["reason with sb", "reasoning ability", "logical reasoning"]},
    {"word": "discipline", "common_meaning": "纪律", "rare_meaning": "n. 学科", "exam_frequency": "50%", "collocations": ["academic discipline", "various disciplines", "scientific discipline"]},
    {"word": "consume", "common_meaning": "消费", "rare_meaning": "vt. 毁灭，烧毁", "exam_frequency": "40%", "collocations": ["be consumed by", "consume time", "consume energy"]},
    {"word": "draft", "common_meaning": "草稿", "rare_meaning": "n. 征兵", "exam_frequency": "35%", "collocations": ["military draft", "draft dodger", "the draft"]},
    {"word": "compound", "common_meaning": "复合的", "rare_meaning": "v. 加剧，恶化", "exam_frequency": "30%", "collocations": ["compound the problem", "compound interest", "compound error"]},
    {"word": "sustain", "common_meaning": "维持", "rare_meaning": "vt. 支撑；认可", "exam_frequency": "45%", "collocations": ["sustain economic growth", "sustain an argument", "self-sustaining"]},
    {"word": "pool", "common_meaning": "池子", "rare_meaning": "v. 共用；汇集", "exam_frequency": "40%", "collocations": ["pool resources", "pool together", "car pool"]},
    {"word": "bet", "common_meaning": "打赌", "rare_meaning": "v. 敢说；确信", "exam_frequency": "35%", "collocations": ["I bet", "you can bet", "safe bet"]},
    {"word": "swell", "common_meaning": "肿胀", "rare_meaning": "v. 增加；扩大", "exam_frequency": "30%", "collocations": ["swell up", "swell the ranks", "swelling population"]},
]

POLYSEMY_WARNING = [
    {"word": "spring", "common_meaning": "春天", "rare_meaning": "v. 突然出现，涌现", "exam_frequency": "40%", "collocations": ["spring up", "spring from", "spring into action"]},
    {"word": "table", "common_meaning": "桌子", "rare_meaning": "v. 搁置，暂缓讨论", "exam_frequency": "35%", "collocations": ["table a proposal", "table the motion", "on the table"]},
    {"word": "book", "common_meaning": "书", "rare_meaning": "v. 预订", "exam_frequency": "30%", "collocations": ["book a ticket", "book in advance", "fully booked"]},
    {"word": "weed", "common_meaning": "杂草", "rare_meaning": "v. 除草；清除", "exam_frequency": "25%", "collocations": ["weed out", "weed the garden", "weed through"]},
    {"word": "engineer", "common_meaning": "工程师", "rare_meaning": "v. 策划；设计", "exam_frequency": "25%", "collocations": ["engineer a solution", "genetically engineered", "social engineering"]},
    {"word": "remark", "common_meaning": "评论", "rare_meaning": "v. 引人注目", "exam_frequency": "20%", "collocations": ["remark on/upon", "make a remark", "remarkable achievement"]},
]


# ========================================
# 核心检测函数
# ========================================

def detect_polysemy(word: str) -> Optional[Dict[str, Any]]:
    """
    检测单词是否在考研中有僻义

    Args:
        word: 目标单词

    Returns:
        PolysemyAlert: 僻义预警对象，无僻义时返回 None

    检测逻辑：
    1. 首先查询僻义词库（POLYSEMY_CRITICAL 和 POLYSEMY_WARNING）
    2. 如果词库中存在，返回预警信息
    3. 如果词库中不存在，尝试通过语义分析检测
    """
    # 1. 首先查询词库
    library_result = get_polysemy_by_word(word)
    if library_result:
        return library_result

    # 2. 尝试语义分析检测（简化实现）
    semantic_result = detect_by_semantic_analysis(word)
    if semantic_result:
        return semantic_result

    return None


def get_polysemy_by_word(word: str) -> Optional[Dict[str, Any]]:
    """
    根据单词从僻义词库获取僻义信息

    Args:
        word: 目标单词

    Returns:
        dict: 僻义信息，找不到返回None
    """
    word_lower = word.lower()

    # 先查找 Critical 级别
    for item in POLYSEMY_CRITICAL:
        if item["word"].lower() == word_lower:
            return {
                "word": word,
                "alert_type": "critical",
                "common_meanings": [item["common_meaning"]],
                "rare_meanings": [item["rare_meaning"]],
                "exam_frequency": item["exam_frequency"],
                "collocations": item["collocations"]
            }

    # 再查找 Warning 级别
    for item in POLYSEMY_WARNING:
        if item["word"].lower() == word_lower:
            return {
                "word": word,
                "alert_type": "warning",
                "common_meanings": [item["common_meaning"]],
                "rare_meanings": [item["rare_meaning"]],
                "exam_frequency": item["exam_frequency"],
                "collocations": item["collocations"]
            }

    return None


def detect_by_semantic_analysis(word: str) -> Optional[Dict[str, Any]]:
    """
    通过语义分析检测僻义（简化实现）

    实际应用中，这里可以：
    1. 调用词典API获取常见释义
    2. 对比考研大纲释义
    3. 计算语义重叠度
    """
    # 简化实现：返回 None，表示需要人工判断
    return None


# ========================================
# 辅助计算函数
# ========================================

def calculate_semantic_overlap(meanings1: List[str], meanings2: List[str]) -> float:
    """
    计算两个释义集合的语义重叠度

    Args:
        meanings1: 释义集合1（常见释义）
        meanings2: 释义集合2（考研大纲释义）

    Returns:
        float: 重叠度 (0.0-1.0)

    计算方法：
    - 使用 Jaccard 相似度
    - 重叠度 < 0.3 → Critical 级别
    - 重叠度 0.3-0.5 → Warning 级别
    - 重叠度 > 0.5 → 无预警
    """
    if not meanings1 or not meanings2:
        return 0.0

    # 提取释义中的关键词
    words1 = set()
    for m in meanings1:
        words1.update(extract_keywords(m))

    words2 = set()
    for m in meanings2:
        words2.update(extract_keywords(m))

    if not words1 or not words2:
        return 0.0

    # 计算 Jaccard 相似度
    intersection = words1 & words2
    union = words1 | words2

    return len(intersection) / len(union)


def extract_keywords(text: str) -> set:
    """
    从释义文本中提取关键词

    Args:
        text: 释义文本

    Returns:
        set: 关键词集合
    """
    # 停用词列表
    stopwords = {
        "the", "a", "an", "of", "to", "in", "for", "and", "or",
        "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did",
        "this", "that", "these", "those", "it", "its"
    }

    # 分词并过滤
    words = text.lower().split()
    keywords = set()

    for word in words:
        # 移除标点
        word = ''.join(c for c in word if c.isalnum())
        if word and word not in stopwords and len(word) > 1:
            keywords.add(word)

    return keywords


def calculate_exam_frequency(word: str) -> str:
    """
    计算单词在考研中的出现频率

    Args:
        word: 目标单词

    Returns:
        str: 频率等级 (high/medium/low)
    """
    _ = word  # 参数保留用于未来扩展（如调用词频API）
    # 首先检查僻义词库中的频率
    polysemy_info = get_polysemy_by_word(word)
    if polysemy_info:
        freq_str = polysemy_info.get("exam_frequency", "0%")
        # 解析频率字符串
        try:
            freq_value = int(freq_str.replace("%", ""))
            if freq_value >= 50:
                return "high"
            elif freq_value >= 30:
                return "medium"
            else:
                return "low"
        except ValueError:
            pass

    # 默认返回 low
    return "low"


def is_polysemy_word(word: str) -> bool:
    """
    快速判断单词是否为僻义词

    Args:
        word: 目标单词

    Returns:
        bool: 是否为僻义词
    """
    return get_polysemy_by_word(word) is not None


def get_polysemy_level(word: str) -> Optional[str]:
    """
    获取僻义预警级别

    Args:
        word: 目标单词

    Returns:
        str: "critical" / "warning" / None
    """
    result = get_polysemy_by_word(word)
    if result:
        return result.get("alert_type")
    return None


# ========================================
# 批量检测函数
# ========================================

def detect_polysemy_batch(words: List[str]) -> Dict[str, Dict]:
    """
    批量检测单词僻义

    Args:
        words: 单词列表

    Returns:
        dict: 检测结果，key为单词，value为检测结果（None表示无僻义）
    """
    results = {}
    for word in words:
        results[word] = detect_polysemy(word)
    return results


def filter_polysemy_words(words: List[str], level: str = "all") -> List[str]:
    """
    筛选僻义词

    Args:
        words: 单词列表
        level: 筛选级别 ("critical" / "warning" / "all")

    Returns:
        list: 符合条件的僻义词列表
    """
    result = []
    for word in words:
        polysemy_info = get_polysemy_by_word(word)
        if polysemy_info:
            if level == "all":
                result.append(word)
            elif polysemy_info.get("alert_type") == level:
                result.append(word)
    return result


# ========================================
# 格式化输出函数
# ========================================

def format_polysemy_alert(word: str) -> str:
    """
    格式化输出僻义预警

    Args:
        word: 目标单词

    Returns:
        str: Markdown格式的预警信息
    """
    info = get_polysemy_by_word(word)
    if not info:
        return ""

    level = info.get("alert_type", "warning")

    content = f"> ⚠️ **僻义预警** [{level}]\n"
    content += f"> - **常见义**：{info['common_meanings'][0]}\n"
    content += f"> - **考研僻义**：**{info['rare_meanings'][0]}**\n"
    content += f"> - **考频**：{info['exam_frequency']}\n"

    if info.get('collocations'):
        content += "> - **常用搭配**：" + "、".join(info['collocations'][:3]) + "\n"

    return content
