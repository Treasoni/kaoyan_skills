# kaoyan-english-vocab 代码模块

本文档包含 kaoyan-english-vocab 技能的所有代码实现。

---

## 1. 真题语境检索策略

### 1.1 generate_context_article

生成语境文章，优先使用真题语境。

```python
def generate_context_article(word_list, user_preferences):
    """生成语境文章

    Args:
        word_list: 今日目标词汇
        user_preferences: 考试类型(英一/英二)、偏好主题等

    Returns:
        Article: 语境文章对象
    """
    contexts = []

    for word in word_list:
        # 1. 优先检索真题语境
        real_exam_context = search_real_exam_pool(
            word,
            exam_type=user_preferences.exam_type,
            recent_years=5  # 优先近5年
        )
        if real_exam_context:
            contexts.append(real_exam_context)
            continue

        # 2. 检索外刊同源语境
        journal_context = search_journal_pool(word)
        if journal_context:
            contexts.append(journal_context)
            continue

        # 3. 最后才用AI生成
        ai_context = generate_ai_context(
            word,
            style="The Economist",  # 明确指定外刊风格
            complexity=calculate_sentence_complexity(word)
        )
        ai_context.metadata.source = "AI生成(模拟)"
        contexts.append(ai_context)

    # 4. 将语境串联成"真题模拟材料"
    article = weave_contexts_into_article(contexts)

    return article


def search_real_exam_pool(word, exam_type, recent_years=5):
    """搜索真题语境池

    Args:
        word: 目标单词
        exam_type: 考试类型（英一/英二）
        recent_years: 优先近年真题

    Returns:
        Context: 真题语境对象，找不到返回None
    """
    # 搜索真题语境池
    pool_path = f"/考研英语/📚 真题语境池/{exam_type}/"

    # 按年份倒序搜索
    current_year = datetime.now().year
    for year in range(current_year, current_year - recent_years, -1):
        context = search_context_in_year_pool(word, pool_path, year)
        if context:
            return context

    return None


def search_journal_pool(word):
    """搜索外刊同源语境池

    Args:
        word: 目标单词

    Returns:
        Context: 外刊语境对象，找不到返回None
    """
    pool_path = "/考研英语/📰 外刊同源库/"

    # 搜索 The Economist, The Guardian 等
    for journal in ["The Economist", "The Guardian", "TIME"]:
        context = search_context_in_journal(word, pool_path, journal)
        if context:
            return context

    return None


def generate_ai_context(word, style="The Economist", complexity="medium"):
    """AI生成语境

    Args:
        word: 目标单词
        style: 文章风格
        complexity: 句式复杂度

    Returns:
        Context: AI生成的语境对象
    """
    return {
        "word": word,
        "sentence": f"[AI生成句子，风格：{style}]",
        "source": "AI生成(模拟)",
        "style": style,
        "complexity": complexity
    }


def weave_contexts_into_article(contexts):
    """将语境串联成文章

    Args:
        contexts: 语境列表

    Returns:
        Article: 完整文章
    """
    # 按主题或逻辑串联语境
    article = {
        "title": "真题模拟材料",
        "paragraphs": [],
        "word_count": 0,
        "source_stats": {
            "real_exam": 0,
            "journal": 0,
            "ai_generated": 0
        }
    }

    for ctx in contexts:
        # 统计来源
        if ctx.get("source") == "真题":
            article["source_stats"]["real_exam"] += 1
        elif "外刊" in ctx.get("source", ""):
            article["source_stats"]["journal"] += 1
        else:
            article["source_stats"]["ai_generated"] += 1

        # 构建段落
        article["paragraphs"].append(ctx.get("sentence", ""))
        article["word_count"] += len(ctx.get("sentence", "").split())

    return article
```

---

## 2. 熟词僻义检测算法

### 2.1 detect_polysemy

检测单词是否在考研中有僻义。

```python
def detect_polysemy(word):
    """检测单词是否在考研中有僻义

    Args:
        word: 目标单词

    Returns:
        PolysemyAlert: 僻义预警对象
        None: 无僻义
    """
    # 1. 检索考研大纲词表
    outline_entry = search_exam_outline(word)

    # 2. 对比大纲释义与常见释义
    common_meanings = get_common_dictionary_meanings(word)
    exam_meanings = outline_entry.meanings

    # 3. 计算语义重叠度
    overlap = calculate_semantic_overlap(common_meanings, exam_meanings)

    # 4. 判断是否存在僻义
    if overlap < 0.5:  # 重叠度低于50%，存在显著僻义
        return PolysemyAlert(
            word=word,
            alert_type="critical" if overlap < 0.3 else "warning",
            rare_meanings=[m for m in exam_meanings if m not in common_meanings],
            common_meanings=common_meanings,
            exam_frequency=calculate_exam_frequency(word)
        )

    return None


def calculate_semantic_overlap(meanings1, meanings2):
    """计算两个释义集合的语义重叠度

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


def calculate_exam_frequency(word):
    """计算单词在考研中的出现频率

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
```

---

## 3. 熟词僻义库数据

### 3.1 Critical级别（高频陷阱）

```yaml
POLYSEMY_CRITICAL:
  - word: "address"
    common_meaning: "地址"
    rare_meaning: "vt. 处理，解决"
    exam_frequency: "80%"
    collocations: ["address the problem", "address an issue", "address concerns"]

  - word: "school"
    common_meaning: "学校"
    rare_meaning: "n. 流派，学派"
    exam_frequency: "70%"
    collocations: ["school of thought", "different schools"]

  - word: "novel"
    common_meaning: "新颖的"
    rare_meaning: "n. 长篇小说"
    exam_frequency: "65%"
    collocations: ["historical novel", "novel writer"]

  - word: "fine"
    common_meaning: "好的"
    rare_meaning: "n./v. 罚款"
    exam_frequency: "60%"
    collocations: ["impose a fine", "fine sb for sth"]

  - word: "reason"
    common_meaning: "原因"
    rare_meaning: "v. 推理，推论"
    exam_frequency: "55%"
    collocations: ["reason with sb", "reasoning ability"]

  - word: "discipline"
    common_meaning: "纪律"
    rare_meaning: "n. 学科"
    exam_frequency: "50%"
    collocations: ["academic discipline", "various disciplines"]

  - word: "consume"
    common_meaning: "消费"
    rare_meaning: "vt. 毁灭，烧毁"
    exam_frequency: "40%"
    collocations: ["be consumed by", "consume time"]

  - word: "draft"
    common_meaning: "草稿"
    rare_meaning: "n. 征兵"
    exam_frequency: "35%"
    collocations: ["military draft", "draft dodger"]

  - word: "compound"
    common_meaning: "复合的"
    rare_meaning: "v. 加剧，恶化"
    exam_frequency: "30%"
    collocations: ["compound the problem", "compound interest"]
```

### 3.2 Warning级别（中等陷阱）

```yaml
POLYSEMY_WARNING:
  - word: "spring"
    common_meaning: "春天"
    rare_meaning: "v. 突然出现，涌现"
    exam_frequency: "40%"
    collocations: ["spring up", "spring from"]

  - word: "table"
    common_meaning: "桌子"
    rare_meaning: "v. 搁置，暂缓讨论"
    exam_frequency: "35%"
    collocations: ["table a proposal", "table the motion"]

  - word: "book"
    common_meaning: "书"
    rare_meaning: "v. 预订"
    exam_frequency: "30%"
    collocations: ["book a ticket", "book in advance"]
```

---

## 4. 快速查词函数

### 4.1 lookup_word

快速查询单词信息，含僻义预警。

```python
def lookup_word(word, exam_type="english_2"):
    """快速查询单词信息

    Args:
        word: 目标单词
        exam_type: 考试类型

    Returns:
        dict: 单词信息卡片
    """
    # 1. 获取基本信息
    basic_info = get_basic_word_info(word)

    # 2. 检测僻义
    polysemy_alert = detect_polysemy(word)

    # 3. 获取真题例句
    real_exam_examples = get_real_exam_examples(word, exam_type)

    # 4. 获取搭配
    collocations = get_common_collocations(word)

    # 5. 获取词族
    word_family = get_word_family(word)

    return {
        "word": word,
        "pronunciation": basic_info.get("pronunciation"),
        "part_of_speech": basic_info.get("part_of_speech"),
        "meanings": basic_info.get("meanings"),
        "polysemy_alert": polysemy_alert,
        "real_exam_examples": real_exam_examples,
        "collocations": collocations,
        "word_family": word_family
    }


def format_word_card(word_info):
    """格式化单词卡片输出

    Args:
        word_info: 单词信息字典

    Returns:
        str: Markdown格式的单词卡片
    """
    card = f"""# {word_info['word']}

## 基本信息
**音标**: {word_info.get('pronunciation', 'N/A')}
**词性**: {word_info.get('part_of_speech', 'N/A')}
"""

    # 僻义预警
    if word_info.get('polysemy_alert'):
        alert = word_info['polysemy_alert']
        icon = "⚠️" if alert.alert_type == "critical" else "⚡"
        card += f"""
## {icon} 僻义预警 [{alert.alert_type}]

> [!danger] 陷阱提示
> 此词在考研中 **{alert.exam_frequency}** 考查僻义

**考研常考僻义**: {', '.join(alert.rare_meanings)}

### 常用搭配
"""
        for col in alert.collocations:
            card += f"- {col}\n"

    # 真题例句
    if word_info.get('real_exam_examples'):
        card += "\n### 真题例句\n"
        for example in word_info['real_exam_examples'][:3]:
            card += f"""> [!example] {example['year']}年真题 {example['section']}
> {example['sentence']}
"""

    return card
```

---

## 5. PDF词汇提取函数

### 5.1 extract_words_from_pdf

从PDF中提取单词列表。

```python
def extract_words_from_pdf(pdf_path, app_type="momo"):
    """从PDF中提取单词列表

    Args:
        pdf_path: PDF文件路径
        app_type: APP类型（momo/baici）

    Returns:
        list: 单词列表
    """
    # 读取PDF内容
    content = read_pdf(pdf_path)

    # 根据APP类型选择解析器
    if app_type == "momo":
        words = parse_momo_format(content)
    elif app_type == "baici":
        words = parse_baici_format(content)
    else:
        words = parse_generic_format(content)

    return words


def parse_momo_format(content):
    """解析墨墨背单词导出格式"""
    words = []
    lines = content.split('\n')

    for line in lines:
        # 墨墨格式: 单词 [音标] 释义
        match = re.match(r'^(\w+)\s*\[([^\]]+)\]\s*(.+)$', line.strip())
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": match.group(2),
                "meaning": match.group(3).strip()
            })

    return words


def parse_baici_format(content):
    """解析百词斩导出格式"""
    words = []
    lines = content.split('\n')

    for line in lines:
        # 百词斩格式可能不同
        match = re.match(r'^(\w+)\s+(.+)$', line.strip())
        if match:
            words.append({
                "word": match.group(1),
                "meaning": match.group(2).strip()
            })

    return words
```

---

## 6. 单词表整理和格式化函数（必须步骤）⚠️

> **重要**：当用户提供单词表时，此函数必须**首先执行**！

### 6.1 organize_word_list

整理和格式化原始单词表。

```python
def organize_word_list(raw_content, output_path, date_str):
    """整理和格式化原始单词表

    Args:
        raw_content: 原始单词表内容（可能是从PDF/图片转换，格式混乱）
        output_path: 输出文件路径（覆盖原始文件）
        date_str: 日期字符串

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

    # 6. 生成输出内容
    output_content = generate_formatted_output(words_with_alerts, date_str)

    # 7. 覆盖原始文件
    write_file(output_path, output_content)

    return {
        "total_words": len(words),
        "high_frequency": len(classified_words["high"]),
        "medium_frequency": len(classified_words["medium"]),
        "low_frequency": len(classified_words["low"]),
        "polysemy_alerts": count_alerts(words_with_alerts),
        "word_families": len(word_families)
    }


def extract_words_from_raw_content(content):
    """从原始内容中提取单词"""
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


def format_words(words):
    """格式统一化"""
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


def group_by_word_family(words):
    """按词族分类"""
    families = {}

    for w in words:
        root = extract_word_root(w["word"])
        if root not in families:
            families[root] = []
        families[root].append(w)

    return families


def extract_word_root(word):
    """提取词根"""
    # 常见词缀
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


def classify_by_frequency(word_families):
    """按考研重点分级"""
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


def add_polysemy_alerts(classified_words):
    """添加僻义预警"""
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


def generate_formatted_output(classified_words, date_str):
    """生成格式化输出内容"""
    content = f"""# 单词表 - Day {{N}}

**日期**：{date_str}
**词汇量**：{{count}}词
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
    total = sum(len(w) for f in classified_words.values() for w in f.values())
    high_count = sum(len(w) for w in classified_words["high"].values())
    medium_count = sum(len(w) for w in classified_words["medium"].values())
    low_count = sum(len(w) for w in classified_words["low"].values())

    content += f"""## 📊 统计信息

| 分类 | 数量 |
|------|------|
| 高频词 | {high_count} |
| 中频词 | {medium_count} |
| 低频词 | {low_count} |

**下次复习日期**：{calculate_next_review_date(date_str)}
"""

    return content


def calculate_next_review_date(date_str):
    """计算下次复习日期（2天后）"""
    from datetime import datetime, timedelta
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_date = date + timedelta(days=2)
    return next_date.strftime("%Y-%m-%d")
```

### 6.2 执行流程

```
[用户提供单词表]
      ↓
[步骤0: organize_word_list] ← 必须首先执行！
      ↓
[覆盖原始单词表文件]
      ↓
[步骤1: detect_polysemy]
      ↓
[步骤2: generate_context_article + 生成四类笔记]
```

### 6.3 验证标准

1. ✅ 必须在生成四类笔记**之前**执行单词表整理
2. ✅ 整理后的单词表必须覆盖原始文件
3. ✅ 必须按词族分类
4. ✅ 必须按考研重点分级（⭐⭐⭐ / ⭐⭐ / ⭐）
5. ✅ 必须检测并标记僻义预警（🔴 Critical / 🟡 Warning）

---

*创建日期: 2026-03-10*
*版本: 1.1.0*
*最后更新: 2026-03-18（添加单词表整理函数）*
