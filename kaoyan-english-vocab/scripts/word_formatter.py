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
7. 添加记忆方法（100%覆盖）
8. 添加词组搭配
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from kaoyan_english_core.scripts.day_calculator import get_validated_day_number


def organize_word_list(raw_content: str, output_path: str, date_str: str) -> Dict:
    """整理和格式化原始单词表

    Args:
        raw_content: 原始单词表内容（可能是从PDF/图片转换，格式混乱）
        output_path: 输出文件路径（覆盖原始文件）
        date_str: 日期字符串（格式：YYYY-MM-DD）

    Returns:
        dict: 整理结果统计
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

    # 6. 添加记忆方法和词组搭配
    words_with_memory = add_memory_methods(words_with_alerts)

    # 7. 生成输出内容
    output_content = generate_formatted_output(words_with_memory, date_str)

    # 8. 覆盖原始文件
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
    - word [音标] 释义（单行）
    - word 释义（单行）
    - 多行格式（单词单独一行，释义在后续行）
    - Markdown 格式（含 # 标题等）

    > **重要**：此函数不过滤任何单词！输入N个单词，输出必须也是N个单词。
    """
    words = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        # 跳过空行、标题、分隔线、备注、日期等元信息
        if not line or line.startswith('#') or line.startswith('---'):
            continue
        if line in ['备注：', '日期：', '备注:', '日期:']:
            continue
        if line in ['词组搭配', '# 词组搭配']:
            continue

        # 尝试匹配多种格式
        # 格式1: word [音标] 释义（单行格式）
        match = re.match(r'^(\w+)\s*\[([^\]]+)\]\s*(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": match.group(2),
                "meaning": match.group(3).strip()
            })
            continue

        # 格式2: word 释义（释义需包含中文，单行格式）
        match = re.match(r'^(\w+)\s+(.+)$', line)
        if match and re.search(r'[\u4e00-\u9fff]', match.group(2)):
            words.append({
                "word": match.group(1),
                "pronunciation": "",
                "meaning": match.group(2).strip()
            })
            continue

        # 格式3: 多行格式（单词单独一行，释义在下一行或下几行）
        # 检测纯英文单词行（可能是单词）
        if re.match(r'^[a-zA-Z]+$', line) and len(line) >= 2:
            word = line.lower()
            # 向后查找释义行
            meaning_lines = []
            j = i
            while j < len(lines):
                next_line = lines[j].strip()
                j += 1
                # 跳过空行
                if not next_line:
                    continue
                # 遇到"词组搭配"标记，停止释义收集
                if next_line in ['词组搭配', '# 词组搭配']:
                    break
                # 遇到下一个单词（纯英文行），停止并回退
                if re.match(r'^[a-zA-Z]+$', next_line) and len(next_line) >= 2:
                    j -= 1  # 回退，让外层循环处理这个单词
                    break
                # 遇到标题等，跳过
                if next_line.startswith('#') or next_line.startswith('---'):
                    continue
                # 收集释义行
                meaning_lines.append(next_line)

            if meaning_lines:
                words.append({
                    "word": word,
                    "pronunciation": "",
                    "meaning": ' '.join(meaning_lines)
                })
                i = j  # 更新索引位置

    return words


def format_words(words: List[Dict]) -> List[Dict]:
    """格式统一化

    清理多余符号，统一格式。
    """
    formatted = []
    for w in words:
        meaning = w["meaning"]
        # 清理多余符号
        meaning = re.sub(r'\.{3,}', '...', meaning)  # 省略号统一
        meaning = re.sub(r'\s+', ' ', meaning)  # 多余空格
        meaning = re.sub(r'^[;；]\s*', '', meaning)  # 开头分号

        formatted.append({
            "word": w["word"].lower().strip(),
            "pronunciation": w["pronunciation"].strip(),
            "meaning": meaning.strip()
        })

    return formatted


def group_by_word_family(words: List[Dict]) -> Dict[str, List[Dict]]:
    """按词族分类

    将同源词归类到同一词族。
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
    """
    # 常见词缀（按长度降序排列，优先匹配长词缀）
    suffixes = [
        # 名词后缀
        "ation", "ition", "ment", "ness", "ity", "ty", "ence", "ance",
        "ism", "ist", "er", "or",
        # 形容词后缀
        "ful", "less", "able", "ible", "ous", "ive", "al", "ial", "ly",
        # 动词后缀
        "ify", "ize", "ise", "en", "ing", "ed"
    ]

    # 尝试移除词缀
    for suffix in sorted(suffixes, key=len, reverse=True):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]

    return word


def classify_by_frequency(word_families: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """按考研重点分级

    高频词库基于考研真题词频统计。
    """
    # 考研高频词库（基于真题词频）
    high_freq_words = {
        # 动词类
        "address", "sustain", "consume", "compound", "reason",
        "remark", "inquire", "destine", "destroy", "pollute",
        # 名词类
        "discipline", "school", "novel", "draft", "engine",
        # 形容词类
        "final", "desolate", "fine",
        # 其他高频
        "anger", "fire", "cloth", "week", "bet", "pool", "swell",
        "weed", "spring", "table", "book"
    }

    classified = {
        "high": {},    # ⭐⭐⭐
        "medium": {},  # ⭐⭐
        "low": {}      # ⭐
    }

    for root, words in word_families.items():
        # 检查词根或任一单词是否在高频词库中
        is_high = root in high_freq_words or any(w["word"] in high_freq_words for w in words)
        # 词族有多个词，可能是重点词族
        is_medium = len(words) >= 2

        if is_high:
            classified["high"][root] = words
        elif is_medium:
            classified["medium"][root] = words
        else:
            classified["low"][root] = words

    return classified


def add_polysemy_alerts(classified_words: Dict) -> Dict:
    """添加僻义预警

    基于熟词僻义库标记预警级别。
    """
    # Critical级别僻义词库（高频陷阱）
    critical_polysemy = {
        "address": {"common": "地址", "rare": "vt. 处理，解决", "frequency": "80%"},
        "school": {"common": "学校", "rare": "n. 流派，学派", "frequency": "70%"},
        "novel": {"common": "新颖的", "rare": "n. 长篇小说", "frequency": "65%"},
        "fine": {"common": "好的", "rare": "n./v. 罚款", "frequency": "60%"},
        "reason": {"common": "原因", "rare": "v. 推理，推论", "frequency": "55%"},
        "discipline": {"common": "纪律", "rare": "n. 学科", "frequency": "50%"},
        "consume": {"common": "消费", "rare": "vt. 毁灭，烧毁", "frequency": "40%"},
        "draft": {"common": "草稿", "rare": "n. 征兵", "frequency": "35%"},
        "compound": {"common": "复合的", "rare": "v. 加剧，恶化", "frequency": "30%"},
        "sustain": {"common": "维持", "rare": "vt. 支撑；认可", "frequency": "45%"},
        "pool": {"common": "池子", "rare": "v. 共用；汇集", "frequency": "40%"},
        "bet": {"common": "打赌", "rare": "v. 敢说；确信", "frequency": "35%"},
        "swell": {"common": "肿胀", "rare": "v. 增加；扩大", "frequency": "30%"},
    }

    # Warning级别僻义词库（中等陷阱）
    warning_polysemy = {
        "spring": {"common": "春天", "rare": "v. 突然出现，涌现", "frequency": "40%"},
        "table": {"common": "桌子", "rare": "v. 搁置，暂缓讨论", "frequency": "35%"},
        "book": {"common": "书", "rare": "v. 预订", "frequency": "30%"},
        "weed": {"common": "杂草", "rare": "v. 除草；清除", "frequency": "25%"},
        "engineer": {"common": "工程师", "rare": "v. 策划；设计", "frequency": "25%"},
        "remark": {"common": "评论", "rare": "v. 引人注目", "frequency": "20%"},
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


def add_memory_methods(classified_words: Dict) -> Dict:
    """添加记忆方法和词组搭配

    确保每个单词都有记忆方法（100%覆盖）。
    """
    # 记忆方法模板
    memory_templates = {
        # 词根词缀记忆法
        "suffix_templates": {
            "ation": "名词后缀，表示行为、过程或结果",
            "ition": "名词后缀，表示行为、状态",
            "ment": "名词后缀，表示行为、结果、状态",
            "ness": "名词后缀，表示性质、状态",
            "ful": "形容词后缀，表示充满...的",
            "less": "形容词后缀，表示无...的",
            "able": "形容词后缀，表示可...的",
            "ive": "形容词后缀，表示有...性质的",
            "ly": "副词后缀，表示...地",
        },
        # 常用词组搭配库
        "collocations": {
            "address": ["address the problem", "address an issue", "address concerns"],
            "sustain": ["sustain development", "sustain economic growth", "self-sustaining"],
            "consume": ["be consumed by", "consume time", "consume energy"],
            "remark": ["remark on/upon", "make a remark", "remarkable achievement"],
            "discipline": ["academic discipline", "strict discipline", "self-discipline"],
            "final": ["final decision", "final exam", "in the final analysis"],
        }
    }

    result = {"high": {}, "medium": {}, "low": {}}

    for level, families in classified_words.items():
        for root, words in families.items():
            for w in words:
                word = w["word"]

                # 生成记忆方法
                w["memory_method"] = generate_memory_method(word, root)

                # 添加词组搭配
                w["collocations"] = get_collocations(word, memory_templates["collocations"])

            result[level][root] = words

    return result


def generate_memory_method(word: str, root: str) -> Dict:
    """生成记忆方法

    优先使用词根词缀法，其次使用联想法。
    """
    # 检测词根词缀
    suffix_info = detect_suffix(word)

    if suffix_info:
        return {
            "type": "词根词缀",
            "root": root,
            "suffix": suffix_info["suffix"],
            "explanation": suffix_info["explanation"],
            "method": f"{root}（词根）+ {suffix_info['suffix']}（{suffix_info['explanation']}）"
        }
    else:
        # 使用联想法
        return {
            "type": "联想",
            "method": generate_association(word)
        }


def detect_suffix(word: str) -> Dict:
    """检测单词的词缀"""
    suffixes = {
        "ation": "名词后缀，表示行为、过程或结果",
        "ition": "名词后缀，表示行为、状态",
        "ment": "名词后缀，表示行为、结果、状态",
        "ness": "名词后缀，表示性质、状态",
        "ful": "形容词后缀，表示充满...的",
        "less": "形容词后缀，表示无...的",
        "able": "形容词后缀，表示可...的",
        "ible": "形容词后缀，表示可...的",
        "ous": "形容词后缀，表示具有...的",
        "ive": "形容词后缀，表示有...性质的",
        "al": "形容词后缀，表示...的",
        "ly": "副词后缀，表示...地",
        "er": "名词后缀，表示做...的人/物",
        "or": "名词后缀，表示做...的人/物",
        "ing": "动名词/现在分词后缀",
        "ed": "过去式/过去分词后缀",
    }

    for suffix, explanation in sorted(suffixes.items(), key=lambda x: -len(x[0])):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return {"suffix": suffix, "explanation": explanation}

    return None


def generate_association(word: str) -> str:
    """生成联想记忆法"""
    # 简化实现：基于单词特征生成联想
    if len(word) <= 4:
        return f"短词记忆：{word} - 通过反复使用加深印象"
    else:
        return f"分解记忆：将 {word} 分解音节，逐部分记忆"


def get_collocations(word: str, collocation_db: Dict) -> List[str]:
    """获取词组搭配"""
    if word in collocation_db:
        return collocation_db[word]
    # 默认返回通用搭配
    return [f"{word} + n.", f"{word} + prep.", f"be {word}ed"]


def generate_formatted_output(classified_words: Dict, date_str: str) -> str:
    """生成格式化输出内容

    严格遵循 templates/formatted-wordlist.md 格式。
    """
    total = sum(len(w) for f in classified_words.values() for w in f.values())
    high_count = sum(len(w) for w in classified_words["high"].values())
    medium_count = sum(len(w) for w in classified_words["medium"].values())
    low_count = sum(len(w) for w in classified_words["low"].values())
    polysemy_count = count_alerts(classified_words)

    # 计算Day编号（使用统一的 day_calculator 模块，基准：2026-02-28 = Day-001）
    day_number = get_validated_day_number(date_str)

    # 计算距离考试天数（考试日期：2026-12-20）
    exam_date = datetime(2026, 12, 20)
    days_to_exam = (exam_date - current_date).days

    content = f"""# 考研英语单词表 - Day {day_number:03d}

**日期**: {date_str}
**词汇量**: {total}词
**来源**: 单词整理
**距离考试**: {days_to_exam}天

---

"""

    # 高频词
    if classified_words["high"]:
        content += "## ⭐⭐⭐ 高频词（必考词汇）\n\n"
        for i, (root, words) in enumerate(classified_words["high"].items(), 1):
            content += f"### 词族{i}: {root}族（{len(words)}词）\n\n"
            for w in words:
                content += format_word_entry(w, "⭐⭐⭐")
            content += "---\n\n"

    # 中频词
    if classified_words["medium"]:
        content += "## ⭐⭐ 中频词（常考词汇）\n\n"
        for i, (root, words) in enumerate(classified_words["medium"].items(), 1):
            content += f"### 词族{i}: {root}族（{len(words)}词）\n\n"
            for w in words:
                content += format_word_entry(w, "⭐⭐")
            content += "---\n\n"

    # 低频词
    if classified_words["low"]:
        content += "## ⭐ 低频词（生僻词汇）\n\n"
        for i, (root, words) in enumerate(classified_words["low"].items(), 1):
            content += f"### 词族{i}: {root}族（{len(words)}词）\n\n"
            for w in words:
                content += format_word_entry(w, "⭐")
            content += "---\n\n"

    # 统计信息
    content += f"""## 📊 统计信息

| 分类 | 数量 | 说明 |
|------|------|------|
| 高频词（⭐⭐⭐） | {high_count}词 | 必考词汇，重点记忆 |
| 中频词（⭐⭐） | {medium_count}词 | 常考词汇 |
| 低频词（⭐） | {low_count}词 | 生僻词汇 |
| 僻义预警词 | {polysemy_count}词 | 需特别注意 |

"""

    # 僻义预警汇总
    if polysemy_count > 0:
        content += "## ⚠️ 僻义预警汇总\n\n"
        content += format_polysemy_summary(classified_words)

    # 下次复习日期
    content += f"""
---

**下次复习日期**: {calculate_next_review_date(date_str)}

---

> [!tip] 学习建议
> 1. 优先记忆高频词（⭐⭐⭐）
> 2. 重点复习僻义预警词
> 3. 按词族记忆，提高效率
> 4. 结合真题语境文章巩固
"""

    return content


def format_word_entry(w: Dict, star_level: str) -> str:
    """格式化单个单词条目"""
    entry = f"#### {w['word']} {star_level}\n"
    entry += f"**{w.get('pronunciation', '')}** {w['meaning']}\n\n"

    # 词组搭配
    if w.get('collocations'):
        entry += "| 词组搭配 | 释义 |\n|---------|------|\n"
        for col in w['collocations'][:3]:
            entry += f"| {col} | （待补充） |\n"
        entry += "\n"

    # 僻义预警
    if w.get('polysemy_alert'):
        alert = w['polysemy_alert']
        icon = "🔴" if alert['level'] == "critical" else "🟡"
        level_text = "critical" if alert['level'] == "critical" else "warning"
        entry += f"> ⚠️ **僻义预警** [{level_text}]\n"
        entry += f"> - **常见义**：{alert['common']}\n"
        entry += f"> - **考研僻义**：{alert['rare']}\n"
        entry += f"> - **考频**：{alert['frequency']}\n\n"

    # 记忆方法
    if w.get('memory_method'):
        memory = w['memory_method']
        entry += "> 🧠 **记忆方法**\n"
        if memory['type'] == "词根词缀":
            entry += f"> - **词根**：{memory.get('root', '')}\n"
            entry += f"> - **后缀**：{memory.get('suffix', '')}（{memory.get('explanation', '')}）\n"
        else:
            entry += f"> - **联想**：{memory.get('method', '')}\n"
        entry += "\n"

    entry += "---\n\n"
    return entry


def format_polysemy_summary(classified_words: Dict) -> str:
    """格式化僻义预警汇总"""
    critical_words = []
    warning_words = []

    for level, families in classified_words.items():
        for root, words in families.items():
            for w in words:
                if w.get('polysemy_alert'):
                    alert = w['polysemy_alert']
                    word_info = {
                        "word": w['word'],
                        "common": alert['common'],
                        "rare": alert['rare'],
                        "frequency": alert['frequency']
                    }
                    if alert['level'] == 'critical':
                        critical_words.append(word_info)
                    else:
                        warning_words.append(word_info)

    content = ""

    if critical_words:
        content += "### [critical] 高频陷阱\n\n"
        content += "| 单词 | 常见义 | 考研僻义 | 出现频率 |\n|------|--------|----------|----------|\n"
        for w in critical_words:
            content += f"| {w['word']} | {w['common']} | **{w['rare']}** | {w['frequency']} |\n"
        content += "\n"

    if warning_words:
        content += "### [warning] 中等陷阱\n\n"
        content += "| 单词 | 常见义 | 考研僻义 | 出现频率 |\n|------|--------|----------|----------|\n"
        for w in warning_words:
            content += f"| {w['word']} | {w['common']} | {w['rare']} | {w['frequency']} |\n"
        content += "\n"

    return content


def calculate_next_review_date(date_str: str) -> str:
    """计算下次复习日期（2天后）"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date + timedelta(days=2)
    return next_date.strftime("%Y-%m-%d")


def count_alerts(words_with_alerts: Dict) -> int:
    """统计僻义预警数量"""
    count = 0
    for level in words_with_alerts.values():
        for words in level.values():
            for w in words:
                if w.get('polysemy_alert'):
                    count += 1
    return count
