"""
单词表整理和格式化模块

> **重要**：当用户提供单词表时，此模块必须**首先执行**！

功能：
1. 从原始内容中提取单词列表
2. 格式统一化
3. 按词族分类
4. 按考研重点分级
5. 检测僻义预警
6. 生成格式化输出
"""

import re
from typing import Dict, List
from datetime import datetime, timedelta


def organize_word_list(raw_content: str, output_path: str, date_str: str) -> Dict:
    """整理和格式化原始单词表

    Args:
        raw_content: 原始单词表内容（可能是从PDF/图片转换，格式混乱）
        output_path: 输出文件路径（覆盖原始文件）
        date_str: 日期字符串（格式：YYYY-MM-DD）

    Returns:
        dict: 整理结果统计，包含：
            - total_words: 总词数
            - high_frequency: 高频词数
            - medium_frequency: 中频词数
            - low_frequency: 低频词数
            - polysemy_alerts: 僻义预警数
            - word_families: 词族数
    """
    # 1. 提取单词列表
    words = extract_words_from_raw_content(raw_content)

    # 2. 格式统一化
    formatted_words = format_words(words)

    # 3. 按词族分类
    word_families = group_by_word_family(formatted_words)

    # 4. 按考研重点分级
    classified_words = classify_by_frequency(word_families)

    # 5. 检测僻义预警
    words_with_alerts = add_polysemy_alerts(classified_words)

    # 6. 生成输出内容
    output_content = generate_formatted_output(words_with_alerts, date_str)

    # 7. 覆盖原始文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

    return {
        "total_words": len(words),
        "high_frequency": sum(len(w) for w in classified_words["high"].values()),
        "medium_frequency": sum(len(w) for w in classified_words["medium"].values()),
        "low_frequency": sum(len(w) for w in classified_words["low"].values()),
        "polysemy_alerts": count_alerts(words_with_alerts),
        "word_families": len(word_families)
    }


def extract_words_from_raw_content(content: str) -> List[Dict]:
    """从原始内容中提取单词

    支持多种格式：
    - word [音标] 释义
    - word 释义

    Args:
        content: 原始文本内容

    Returns:
        list: 单词列表
    """
    words = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # 尝试匹配多种格式
        # 格式1: word [音标] 释义
        match = re.match(r'^(\w+)\s*\[([^\]]+)\]\s*(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": match.group(2),
                "meaning": match.group(3).strip()
            })
            continue

        # 格式2: word 释义
        match = re.match(r'^(\w+)\s+(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": "",
                "meaning": match.group(2).strip()
            })

    return words


def format_words(words: List[Dict]) -> List[Dict]:
    """格式统一化

    清理多余符号，统一格式。

    Args:
        words: 原始单词列表

    Returns:
        list: 格式化后的单词列表
    """
    formatted = []
    for w in words:
        # 清理多余符号
        meaning = w["meaning"]
        meaning = re.sub(r'\.{3,}', '...', meaning)  # 省略号统一
        meaning = re.sub(r'\s+', ' ', meaning)  # 多余空格

        formatted.append({
            "word": w["word"].lower().strip(),
            "pronunciation": w["pronunciation"].strip(),
            "meaning": meaning.strip()
        })

    return formatted


def group_by_word_family(words: List[Dict]) -> Dict[str, List[Dict]]:
    """按词族分类

    Args:
        words: 单词列表

    Returns:
        dict: 按词根分组的单词字典
    """
    families = {}

    for w in words:
        root = extract_word_root(w["word"])
        if root not in families:
            families[root] = []
        families[root].append(w)

    return families


def extract_word_root(word: str) -> str:
    """提取词根

    通过移除常见词缀来提取词根。

    Args:
        word: 目标单词

    Returns:
        str: 词根
    """
    # 常见词缀（按长度降序排列，优先匹配长词缀）
    suffixes = [
        "ation", "ition", "ment", "ness", "ly", "ful", "less",
        "able", "ible", "ous", "ive", "al", "ial", "ing", "ed",
        "er", "or", "ist", "ism", "ty", "ity", "ence", "ance",
        "ify", "ize", "ise", "en"
    ]

    # 尝试移除词缀
    for suffix in sorted(suffixes, key=len, reverse=True):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]

    return word


def classify_by_frequency(word_families: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """按考研重点分级

    Args:
        word_families: 按词族分组的单词

    Returns:
        dict: 分级后的单词字典，包含high/medium/low三个级别
    """
    # 考研高频词库（部分示例）
    high_freq_words = {
        "remark", "pollute", "final", "week", "anger", "engine",
        "fire", "cloth", "destiny", "destroy", "inquire", "desolate"
    }

    classified = {
        "high": {},    # ⭐⭐⭐
        "medium": {},  # ⭐⭐
        "low": {}      # ⭐
    }

    for root, words in word_families.items():
        if root in high_freq_words or any(w["word"] in high_freq_words for w in words):
            classified["high"][root] = words
        elif len(words) >= 2:  # 词族有多个词，可能是重点
            classified["medium"][root] = words
        else:
            classified["low"][root] = words

    return classified


def add_polysemy_alerts(classified_words: Dict) -> Dict:
    """添加僻义预警

    Args:
        classified_words: 分级后的单词字典

    Returns:
        dict: 添加了僻义预警的单词字典
    """
    # Critical级别僻义词库
    critical_polysemy = {
        "fine": {"common": "好的", "rare": "n./v. 罚款", "frequency": "60%"},
        "sustain": {"common": "维持", "rare": "vt. 支撑；认可", "frequency": "45%"},
        "pool": {"common": "池子", "rare": "v. 共用；汇集", "frequency": "40%"},
        "bet": {"common": "打赌", "rare": "v. 敢说；确信", "frequency": "35%"},
        "swell": {"common": "肿胀", "rare": "v. 增加；扩大", "frequency": "30%"}
    }

    # Warning级别僻义词库
    warning_polysemy = {
        "weed": {"common": "杂草", "rare": "v. 除草；清除", "frequency": "25%"},
        "engineer": {"common": "工程师", "rare": "v. 策划；设计", "frequency": "25%"},
        "remark": {"common": "评论", "rare": "v. 引人注目", "frequency": "20%"}
    }

    result = {"high": {}, "medium": {}, "low": {}}

    for level, families in classified_words.items():
        for root, words in families.items():
            for w in words:
                word = w["word"]
                if word in critical_polysemy:
                    w["polysemy_alert"] = {
                        "level": "critical",
                        **critical_polysemy[word]
                    }
                elif word in warning_polysemy:
                    w["polysemy_alert"] = {
                        "level": "warning",
                        **warning_polysemy[word]
                    }

            result[level][root] = words

    return result


def generate_formatted_output(classified_words: Dict, date_str: str) -> str:
    """生成格式化输出内容

    Args:
        classified_words: 分级后的单词字典
        date_str: 日期字符串

    Returns:
        str: 格式化的Markdown内容
    """
    total = sum(len(w) for f in classified_words.values() for w in f.values())
    high_count = sum(len(w) for w in classified_words["high"].values())
    medium_count = sum(len(w) for w in classified_words["medium"].values())
    low_count = sum(len(w) for w in classified_words["low"].values())

    content = f"""# 单词表 - Day {{N}}

**日期**：{date_str}
**词汇量**：{total}词
**来源**：墨墨导出

---

"""

    # 高频词
    if classified_words["high"]:
        content += "## ⭐⭐⭐ 高频词（必考词汇）\n\n"
        for i, (root, words) in enumerate(classified_words["high"].items(), 1):
            content += f"### 词族{i}: {root}（{len(words)}词）\n"
            for w in words:
                content += f"#### {w['word']}\n"
                content += f"{w['pronunciation']} {w['meaning']}\n"
                if w.get('polysemy_alert'):
                    alert = w['polysemy_alert']
                    icon = "🔴" if alert['level'] == "critical" else "🟡"
                    content += f"- {icon} 僻义预警：{alert['rare']}（考研{alert['frequency']}考此义）\n"
                content += "\n"
            content += "---\n\n"

    # 中频词
    if classified_words["medium"]:
        content += "## ⭐⭐ 中频词（常考词汇）\n\n"
        for i, (root, words) in enumerate(classified_words["medium"].items(), 1):
            content += f"### 词族{i}: {root}（{len(words)}词）\n"
            for w in words:
                content += f"#### {w['word']}\n"
                content += f"{w['pronunciation']} {w['meaning']}\n\n"
            content += "---\n\n"

    # 低频词
    if classified_words["low"]:
        content += "## ⭐ 低频词（生僻词汇）\n\n"
        for i, (root, words) in enumerate(classified_words["low"].items(), 1):
            content += f"### 词族{i}: {root}（{len(words)}词）\n"
            for w in words:
                content += f"#### {w['word']}\n"
                content += f"{w['pronunciation']} {w['meaning']}\n\n"
            content += "---\n\n"

    # 统计信息
    content += f"""## 📊 统计信息

| 分类 | 数量 |
|------|------|
| 高频词 | {high_count} |
| 中频词 | {medium_count} |
| 低频词 | {low_count} |

**下次复习日期**：{calculate_next_review_date(date_str)}
"""

    return content


def calculate_next_review_date(date_str: str) -> str:
    """计算下次复习日期（2天后）

    Args:
        date_str: 当前日期字符串（格式：YYYY-MM-DD）

    Returns:
        str: 下次复习日期字符串
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date + timedelta(days=2)
    return next_date.strftime("%Y-%m-%d")


def count_alerts(words_with_alerts: Dict) -> int:
    """统计僻义预警数量

    Args:
        words_with_alerts: 包含预警的单词字典

    Returns:
        int: 预警总数
    """
    count = 0
    for level in words_with_alerts.values():
        for words in level.values():
            for w in words:
                if w.get('polysemy_alert'):
                    count += 1
    return count
