# kaoyan-english-review 代码模块

本文档包含 kaoyan-english-review 技能的所有代码实现。

---

## 1. 考研适配的SM-2算法

### 1.1 calculate_next_review_kaoyan

考研适配的SM-2算法，根据考试倒计时自动调整复习间隔。

```python
def calculate_next_review_kaoyan(card, quality, exam_date):
    """考研适配的SM-2算法

    Args:
        card: 词汇卡片对象
        quality: 回忆质量评分 (0-5)
        exam_date: 考试日期

    Returns:
        Card: 更新后的卡片对象
    """
    days_to_exam = (exam_date - date.today()).days
    standard_interval = calculate_sm2_interval(card, quality)

    # 倒计时权重计算
    if days_to_exam > 100:
        # 正常阶段：标准SM-2
        current_phase = "基础期"
        phase_factor = 1.0
        adjusted_interval = standard_interval

    elif days_to_exam > 30:
        # 强化阶段（考前30-100天）：
        # - 高频词：缩短20%间隔
        # - 僻义词：缩短30%间隔
        current_phase = "强化期"
        if card.frequency >= 5 or card.polysemy_alert:
            phase_factor = 0.7 if card.polysemy_alert else 0.8
        else:
            phase_factor = 0.9
        adjusted_interval = max(1, int(standard_interval * phase_factor))

    else:
        # 冲刺阶段（考前30天内）：
        # - 所有词间隔强制缩短
        # - 高频词/僻义词：最高优先级
        current_phase = "冲刺期" if days_to_exam > 7 else "极限冲刺期"
        if card.frequency >= 5 or card.polysemy_alert:
            phase_factor = 0.5
            adjusted_interval = min(int(standard_interval * phase_factor), 3)  # 最多3天
        else:
            phase_factor = 0.7
            adjusted_interval = min(int(standard_interval * phase_factor), 7)  # 最多7天

    # 更新卡片数据
    card.current_phase = current_phase
    card.phase_factor = phase_factor
    card.adjusted_interval = adjusted_interval
    card.days_to_exam = days_to_exam
    card.next_review = date.today() + timedelta(days=adjusted_interval)

    return card


def calculate_sm2_interval(card, quality):
    """标准SM-2算法计算复习间隔

    Args:
        card: 词汇卡片对象
        quality: 回忆质量评分 (0-5)
            5: 完美记忆
            4: 正确但有犹豫
            3: 回忆困难但正确
            2: 错误但有印象
            1: 错误无印象
            0: 完全忘记

    Returns:
        int: 复习间隔（天）

    标准SM-2间隔规则：
        - 第1次复习：学习后1天
        - 第2次复习：第1次复习后3天（累计4天）
        - 第3次复习：第2次复习后7天（累计11天）
        - 后续复习：interval × ease_factor
    """
    if quality >= 3:
        # 回答正确，增加间隔
        if card.review_count == 0:
            # 第1次复习：学习后1天
            interval = 1
        elif card.review_count == 1:
            # 第2次复习：第1次复习后3天（累计4天）
            interval = 3
        elif card.review_count == 2:
            # 第3次复习：第2次复习后7天（累计11天）
            interval = 7
        else:
            # 后续复习：interval × ease_factor
            interval = int(card.interval * card.ease_factor)

        # 更新ease factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        card.ease_factor = max(1.3,
            card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )

        card.interval = interval
        card.correct_count += 1
    else:
        # 回答错误，重新开始
        card.review_count = 0
        card.interval = 1
        card.incorrect_count += 1

    card.review_count += 1
    card.forgetting_rate = card.incorrect_count / max(1, card.review_count)

    return card.interval
```

---

## 2. 每日复习清单生成

### 2.1 generate_daily_review_list

生成每日复习清单，按优先级排序。

```python
def generate_daily_review_list(user_context, exam_date):
    """生成每日复习清单

    Args:
        user_context: 用户上下文
        exam_date: 考试日期

    Returns:
        dict: 复习清单
    """
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    today = date.today()

    # 1. 筛选今日待复习词
    due_cards = [
        card for card in vocabulary_cards
        if card.get("next_review") and card.get("next_review") <= today
    ]

    # 2. 按优先级排序
    # 优先级：僻义词 > 高频词 > 普通词
    sorted_cards = sorted(
        due_cards,
        key=lambda c: (
            -int(c.get("polysemy_alert", False)),  # 僻义词优先
            -c.get("frequency", 0),                 # 高频词次之
            c.get("next_review", today)             # 越早到期越优先
        )
    )

    # 3. 分组
    high_priority = []
    normal_priority = []

    for card in sorted_cards:
        if card.get("polysemy_alert") or card.get("frequency", 0) >= 4:
            high_priority.append(card)
        else:
            normal_priority.append(card)

    # 4. 获取阶段策略
    days_to_exam = (exam_date - today).days
    phase_target = get_phase_vocabulary_target(days_to_exam)

    return {
        "date": today.isoformat(),
        "phase": phase_target.get("focus"),
        "days_to_exam": days_to_exam,
        "high_priority": format_card_list(high_priority[:20]),  # 最多20个高优先级
        "normal_priority": format_card_list(normal_priority[:30]),  # 最多30个普通
        "stats": {
            "total_due": len(due_cards),
            "high_priority_count": len(high_priority),
            "normal_priority_count": len(normal_priority),
            "polysemy_count": sum(1 for c in due_cards if c.get("polysemy_alert"))
        }
    }


def format_card_list(cards):
    """格式化卡片列表为输出格式"""
    return [
        {
            "word": card.get("word"),
            "interval": card.get("interval"),
            "review_count": card.get("review_count"),
            "polysemy_alert": card.get("polysemy_alert"),
            "warning_level": card.get("warning_level"),
            "next_review": card.get("next_review").isoformat() if card.get("next_review") else None
        }
        for card in cards
    ]
```

---

## 3. 分阶段策略

### 3.1 get_phase_vocabulary_target

根据阶段获取词汇学习目标。

```python
def get_phase_vocabulary_target(days_to_exam):
    """根据阶段获取词汇学习目标

    Args:
        days_to_exam: 距离考试天数

    Returns:
        dict: 阶段学习目标
    """
    if days_to_exam > 300:        # 基础期
        return {
            "phase": "基础期",
            "daily_new_words": 50,
            "review_ratio": 0.3,
            "focus": "词汇积累",
            "polysemy_weight": 1.0,
            "strategy": "注重新词积累，标准SM-2间隔"
        }

    elif days_to_exam > 180:      # 强化期
        return {
            "phase": "强化期",
            "daily_new_words": 40,
            "review_ratio": 0.5,
            "focus": "僻义词+真题语境",
            "polysemy_weight": 1.2,
            "strategy": "启用熟词僻义预警，强化真题语境"
        }

    elif days_to_exam > 90:       # 十月强化期
        return {
            "phase": "十月强化期",
            "daily_new_words": 30,
            "review_ratio": 0.6,
            "focus": "僻义词强化",
            "polysemy_weight": 1.5,
            "strategy": "僻义词间隔缩短，增加真题语境"
        }

    elif days_to_exam > 30:       # 冲刺期
        return {
            "phase": "冲刺期",
            "daily_new_words": 10,
            "review_ratio": 0.9,
            "focus": "高频词+僻义词",
            "polysemy_weight": 2.0,
            "strategy": "缩短高频词间隔20%，重点复习僻义词"
        }

    else:                         # 极限冲刺
        return {
            "phase": "极限冲刺期",
            "daily_new_words": 0,
            "review_ratio": 1.0,
            "focus": "全部复习",
            "polysemy_weight": 2.0,
            "strategy": "强制缩短所有间隔，高频词最多3天一复习"
        }
```

### 3.2 阶段策略表

| 阶段 | 天数 | 每日新词 | 复习比例 | 僻义权重 |
|------|------|----------|----------|----------|
| 基础期 | >300 | 50 | 30% | 1.0x |
| 强化期 | 180-300 | 40 | 50% | 1.2x |
| 十月强化期 | 90-180 | 30 | 60% | 1.5x |
| 冲刺期 | 30-90 | 10 | 90% | 2.0x |
| 极限冲刺 | <30 | 0 | 100% | 2.0x |

---

## 4. 学习统计Dashboard

### 4.1 generate_statistics_dashboard

生成学习统计Dashboard。

```python
def generate_statistics_dashboard(user_context):
    """生成学习统计Dashboard

    Args:
        user_context: 用户上下文

    Returns:
        dict: 统计数据
    """
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    review_history = user_context.get("review_history", [])

    # 基础统计
    total_words = len(vocabulary_cards)
    mastered_count = sum(
        1 for c in vocabulary_cards
        if c.get("review_count", 0) >= 5 and c.get("forgetting_rate", 1) < 0.2
    )
    reviewing_count = sum(
        1 for c in vocabulary_cards
        if c.get("review_count", 0) > 0 and c.get("forgetting_rate", 1) >= 0.2
    )
    new_count = sum(
        1 for c in vocabulary_cards
        if c.get("review_count", 0) == 0
    )

    # 僻义统计
    polysemy_words = [c for c in vocabulary_cards if c.get("polysemy_alert")]
    polysemy_mastered = sum(
        1 for c in polysemy_words
        if c.get("review_count", 0) >= 5 and c.get("forgetting_rate", 1) < 0.2
    )
    polysemy_need_review = len(polysemy_words) - polysemy_mastered

    # 近7天复习统计
    recent_reviews = [
        r for r in review_history
        if (date.today() - r.get("date", date.today())).days <= 7
    ]
    total_reviewed = sum(r.get("words_reviewed", 0) for r in recent_reviews)
    avg_accuracy = (
        sum(r.get("results", {}).get("correct_count", 0) for r in recent_reviews) /
        max(1, sum(r.get("results", {}).get("correct_count", 0) + r.get("results", {}).get("incorrect_count", 0) for r in recent_reviews))
    )

    return {
        "summary": {
            "total_words": total_words,
            "mastered_count": mastered_count,
            "mastered_percentage": f"{mastered_count / max(1, total_words) * 100:.1f}%",
            "reviewing_count": reviewing_count,
            "new_count": new_count
        },
        "polysemy": {
            "total": len(polysemy_words),
            "mastered": polysemy_mastered,
            "need_review": polysemy_need_review
        },
        "recent_7_days": {
            "total_reviewed": total_reviewed,
            "avg_accuracy": f"{avg_accuracy * 100:.1f}%",
            "daily_avg": total_reviewed / 7
        },
        "progress_chart": generate_progress_chart_data(review_history)
    }


def generate_progress_chart_data(review_history):
    """生成进度图表数据"""
    # 按日期聚合
    daily_data = {}
    for record in review_history:
        record_date = record.get("date")
        if record_date:
            date_str = record_date.isoformat()
            if date_str not in daily_data:
                daily_data[date_str] = {
                    "reviewed": 0,
                    "correct": 0,
                    "incorrect": 0
                }
            daily_data[date_str]["reviewed"] += record.get("session_info", {}).get("words_reviewed", 0)
            daily_data[date_str]["correct"] += record.get("results", {}).get("correct_count", 0)
            daily_data[date_str]["incorrect"] += record.get("results", {}).get("incorrect_count", 0)

    return daily_data
```

---

## 5. 复习记录保存

### 5.1 save_review_result

保存复习结果。

```python
def save_review_result(user_id, word, quality, review_time=None):
    """保存复习结果

    Args:
        user_id: 用户ID
        word: 复习的单词
        quality: 回忆质量评分 (0-5)
        review_time: 复习时间（可选）
    """
    review_time = review_time or datetime.now()

    try:
        # 获取当前卡片
        card = get_word_card(user_id, word)

        # 计算下次复习时间
        exam_date = get_exam_date(user_id)
        updated_card = calculate_next_review_kaoyan(card, quality, exam_date)

        # 更新卡片
        update_word_card(user_id, updated_card)

        # 记录复习历史
        add_review_history(user_id, {
            "word": word,
            "quality": quality,
            "review_time": review_time,
            "interval": updated_card.interval,
            "phase": updated_card.current_phase
        })

        log_info(f"Saved review result for {word}: quality={quality}")
    except Exception as e:
        log_warning(f"Failed to save review result: {e}")
```

---

## 6. 数据字段说明

### 6.1 SM-2基础字段

| 字段 | 类型 | 说明 |
|------|------|------|
| ease_factor | float | 记忆难度因子，默认2.5 |
| interval | int | 复习间隔（天） |
| review_count | int | 复习次数 |
| next_review | date | 下次复习日期 |
| correct_count | int | 正确次数 |
| incorrect_count | int | 错误次数 |
| forgetting_rate | float | 遗忘率 = incorrect_count / review_count |

### 6.2 考研适配字段

| 字段 | 类型 | 说明 |
|------|------|------|
| exam_date | date | 考试日期 |
| current_phase | string | 当前阶段（基础期/强化期/冲刺期/极限冲刺期） |
| phase_factor | float | 阶段系数（0.5-1.0） |
| days_to_exam | int | 距离考试天数 |
| adjusted_interval | int | 调整后的复习间隔 |

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
