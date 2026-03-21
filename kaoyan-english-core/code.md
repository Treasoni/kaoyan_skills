# kaoyan-english-core 代码模块

本文档包含 kaoyan-english-core 技能的所有代码实现。

---

## 1. MemOS集成函数

### 1.1 load_user_context_from_memory

从MemOS加载用户上下文，失败时返回None触发降级。

```python
def load_user_context_from_memory(user_input):
    """从MemOS加载用户上下文

    Returns:
        dict: 用户上下文信息，包含用户画像、词汇库等
        None: MemOS不可用时触发降级
    """
    try:
        results = search_memory(
            query=f"#user_profile #user_{user_input.get('user_id')}",
            top_k=10
        )
        return parse_memory_to_english_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable: {e}")
        return None


def parse_memory_to_english_context(memory_results):
    """将MemOS结果解析为英语学习上下文"""
    if not memory_results:
        return create_default_user_context()

    context = {
        "user_profile": extract_user_profile(memory_results),
        "vocabulary_cards": extract_word_cards(memory_results),
        "review_history": extract_review_records(memory_results),
        "mental_history": extract_mental_state(memory_results)
    }

    return context
```

### 1.2 save_word_card_to_memory

保存词汇卡片到MemOS，含降级处理。

```python
def save_word_card_to_memory(word_card, user_id):
    """保存词汇卡片到MemOS

    Args:
        word_card: 词汇卡片对象
        user_id: 用户ID
    """
    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "word_card",
                    "data": word_card.to_dict()
                },
                "tags": [
                    "#word_card",
                    f"#word_{word_card.word}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
        log_info(f"Saved word card: {word_card.word}")
    except Exception as e:
        log_warning(f"Failed to save word card {word_card.word}: {e}")
        # 降级：不影响主流程，仅不保存
```

### 1.3 record_review_session

记录复习会话到MemOS，使用upsert逻辑避免冗余。

```python
def record_review_session(user_id, session_data):
    """记录复习会话到MemOS（upsert逻辑）

    Args:
        user_id: 用户ID
        session_data: 复习会话数据
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        # 先查找今日已有记录
        today_session = search_memory(
            query=f"#review_session_current #user_{user_id} #date_{today}",
            top_k=1
        )

        if today_session:
            # 标记旧版本为历史
            add_message(
                messages=[{
                    "role": "assistant",
                    "content": {
                        "type": "review_session",
                        "version": today_session[0].get("version"),
                        "status": "superseded",
                        "data": today_session[0].get("data")
                    },
                    "tags": [
                        "#review_session_history",
                        f"#date_{today}",
                        f"#user_{user_id}"
                    ]
                }],
                user_id=user_id
            )

        # 保存新会话为当前版本
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "review_session",
                    "version": f"v{datetime.now().strftime('%H%M')}",
                    "status": "current",
                    "data": session_data
                },
                "tags": [
                    "#review_session_current",
                    f"#date_{today}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )

        log_info(f"Recorded review session for {today}")
    except Exception as e:
        log_warning(f"Failed to record session: {e}")
```

### 1.4 check_context_freshness_english

检查用户画像是否需要刷新。

```python
def check_context_freshness_english(user_context, current_date):
    """检查英语学习画像是否需要刷新

    Args:
        user_context: 用户上下文
        current_date: 当前日期

    Returns:
        dict: 包含needs_refresh, reason, questions等信息
        None: 不需要刷新
    """
    profile = user_context.get("user_profile")
    if not profile:
        return None

    updated_at = profile.get("updated_at")
    days_since_update = (current_date - updated_at).days

    # 超过30天自动触发刷新询问
    if days_since_update > 30:
        return {
            "needs_refresh": True,
            "reason": f"画像已{days_since_update}天未更新",
            "questions": [
                "你的英语水平有变化吗？(基础/中级/高级)",
                f"每日新词目标需要调整吗？(当前: {profile.get('daily_new_word_target', 50)})",
                "复习重点需要调整吗？(均衡/僻义优先/写作优先)",
                f"僻义敏感度需要调整吗？(当前: {profile.get('polysemy_sensitivity', 'medium')})"
            ]
        }

    return {"needs_refresh": False}
```

---

## 2. 欠账与疲劳检查

### 2.1 check_vocabulary_debt_with_memory

检查词汇欠账，含熔断机制。

```python
def check_vocabulary_debt_with_memory(user_context):
    """检查词汇欠账（含熔断机制）

    Args:
        user_context: 用户上下文

    Returns:
        dict: 欠账状态和处理策略
    """
    # 计算逾期未复习的词汇数量
    overdue_words = calculate_overdue_words(user_context)
    DEBT_LIMIT = 200  # 200个词熔断阈值

    if overdue_words > DEBT_LIMIT:
        return {
            "type": "vocabulary_emergency",
            "overdue_count": overdue_words,
            "strategy": "recovery_only",
            "message": f"⚠️ 待复习词汇已达{overdue_words}个，超过安全阈值",
            "suggestion": "暂停新词学习，专注复习",
            "recovery_plan": generate_vocabulary_recovery_plan(overdue_words)
        }

    return {"type": "normal", "overdue_count": overdue_words}


def calculate_overdue_words(user_context):
    """计算逾期未复习的词汇数量"""
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    today = date.today()

    overdue_count = 0
    for card in vocabulary_cards:
        next_review = card.get("next_review")
        if next_review and next_review < today:
            overdue_count += 1

    return overdue_count
```

### 2.2 check_vocabulary_fatigue_intervention

检查词汇学习疲劳，提供干预建议。

```python
def check_vocabulary_fatigue_intervention(user_context):
    """检查是否需要词汇疲劳干预

    Args:
        user_context: 用户上下文

    Returns:
        dict: 干预方案
        None: 无需干预
    """
    mental_history = user_context.get("mental_history", [])

    if len(mental_history) < 3:
        return None

    recent_days = mental_history[-3:]
    tired_count = sum(
        1 for d in recent_days
        if d.get("vocabulary_fatigue", 0) > 0.6
    )

    if tired_count >= 3:
        avg_fatigue = sum(
            d.get("vocabulary_fatigue", 0.5) for d in recent_days
        ) / len(recent_days)

        return {
            "intervention_needed": True,
            "mode": "vocabulary_relief",
            "avg_fatigue": avg_fatigue,
            "actions": [
                "减少新词量50%",
                "增加真题语境阅读",
                "暂停僻义词训练",
                "增加写作应用练习"
            ]
        }

    return None
```

---

## 3. 调度信号处理

### 3.1 check_dispatch_signals

检查来自kaoyan-plan的调度信号。

```python
def check_dispatch_signals(user_id):
    """检查来自kaoyan-plan的调度信号"""
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_kaoyan-english #user_{user_id}",
            top_k=5
        )

        pending = []
        for signal in signals:
            if not signal.get("processed"):
                pending.append(signal)

        return pending
    except Exception as e:
        log_warning(f"Failed to check dispatch signals: {e}")
        return []


def process_dispatch_signal(signal):
    """处理调度信号"""
    action = signal.get("action")
    context = signal.get("context", {})

    if action == "vocabulary_review_mode":
        mode = context.get("mode", "light")
        duration = context.get("duration", "30min")
        return {
            "mode": "light_review",
            "duration": duration,
            "focus": "polysemy_words",
            "instructions": f"进入轻量词汇复习模式（{duration}），仅复习僻义词"
        }

    elif action == "memory_compression_mode":
        return activate_memory_compression_mode(context)

    elif action == "polysemy_focus":
        count = context.get("count", 20)
        return {
            "mode": "polysemy_focus",
            "word_count": count,
            "instructions": f"进入僻义词专项训练模式，复习{count}个僻义词"
        }

    elif action == "weekly_error_analysis":
        return {
            "mode": "weekly_review",
            "aggregate": context.get("aggregate", True)
        }

    return None
```

---

## 4. 记忆压缩模式

### 4.1 activate_memory_compression_mode

当kaoyan-plan检测到其他科目欠账时，触发英语记忆压缩模式。

```python
def activate_memory_compression_mode(context):
    """激活记忆压缩模式

    Args:
        context: 压缩上下文，包含compress_hours, transfer_to等

    Returns:
        压缩后的学习计划
    """
    compress_hours = context.get("compress_hours", 1)
    transfer_to = context.get("transfer_to", "math")

    return {
        "mode": "memory_compression",
        "original_hours": get_planned_english_hours(),
        "compressed_hours": compress_hours,
        "transfer_to": transfer_to,
        "strategy": {
            "reduce_new_words": True,           # 减少新词量
            "focus_polysemy_only": True,        # 只复习僻义词
            "skip_context_article": True,       # 跳过语境文章生成
            "use_quick_review": True            # 使用快速复习模式
        },
        "message": f"⚠️ 英语时间压缩{compress_hours}小时，转移至{transfer_to}"
    }
```

---

## 5. 动态权重响应

### 5.1 get_phase_vocabulary_target

根据考试倒计时阶段自动调整词汇学习策略。

```python
def get_phase_vocabulary_target(days_to_exam):
    """根据阶段获取词汇学习目标"""

    if days_to_exam > 300:        # 基础期
        return {
            "daily_new_words": 50,
            "review_ratio": 0.3,
            "focus": "词汇积累",
            "polysemy_weight": 1.0
        }

    elif days_to_exam > 180:      # 强化期
        return {
            "daily_new_words": 40,
            "review_ratio": 0.5,
            "focus": "僻义词+真题语境",
            "polysemy_weight": 1.2
        }

    elif days_to_exam > 90:       # 十月强化期
        return {
            "daily_new_words": 30,
            "review_ratio": 0.6,
            "focus": "僻义词强化",
            "polysemy_weight": 1.5
        }

    elif days_to_exam > 30:       # 冲刺期
        return {
            "daily_new_words": 10,
            "review_ratio": 0.9,
            "focus": "高频词+僻义词",
            "polysemy_weight": 2.0
        }

    else:                         # 极限冲刺
        return {
            "daily_new_words": 0,
            "review_ratio": 1.0,
            "focus": "全部复习",
            "polysemy_weight": 2.0
        }
```

---

## 6. 统一错误模型

### 6.1 save_unified_english_mistake

保存英语错误记录（统一格式）。

```python
def save_unified_english_mistake(mistake_data, user_id):
    """保存英语错误记录（统一格式）"""
    mistake_data["subject"] = "english"

    # 英语专用错误类型
    if mistake_data.get("type") == "polysemy_error":
        mistake_data["tags"].append("#polysemy_critical")

    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "unified_mistake_record",
                    "data": mistake_data
                },
                "tags": [
                    "#mistake_record",
                    "#subject_english",
                    f"#word_{mistake_data.get('word', '')}",
                    f"#mistake_type_{mistake_data.get('type', 'unknown')}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save mistake: {e}")
```

---

## 7. 数据模型

### 7.1 用户画像 (User Profile)

```yaml
user_profile:
  user_id: string
  conversation_id: string
  created_at: datetime
  updated_at: datetime

  profile:
    exam_date: date
    exam_type: enum (english_1 | english_2)
    target_score: int
    current_level: enum (basic | intermediate | advanced)

  vocabulary_base:
    total_words: int
    mastered_count: int
    reviewing_count: int
    new_count: int

  preferences:
    daily_new_word_target: int (default 50)
    review_focus: enum (balanced | polysemy_priority | writing_priority)
    learning_style: enum (context_first | rote_first)
    polysemy_sensitivity: enum (high | medium | low)

  mental_history:
    - date: date
      status: enum (energized | normal | tired | burned_out)
      vocabulary_fatigue: float (0.0-1.0)
      trigger: string

  refresh_config:
    last_refreshed: date
    auto_refresh_interval: int
    pending_refresh: boolean
```

### 7.2 词汇卡片 (Word Card)

```yaml
word_card:
  word: string
  user_id: string
  created_at: datetime
  updated_at: datetime

  # SM-2基础字段
  ease_factor: float (default 2.5)
  interval: int
  review_count: int
  next_review: date
  correct_count: int
  incorrect_count: int
  forgetting_rate: float

  # 考研适配字段
  exam_date: date
  current_phase: string
  phase_factor: float
  days_to_exam: int
  adjusted_interval: int

  # 僻义预警字段
  polysemy_alert: bool
  warning_level: string (critical | warning | attention)
  exam_frequency: string
  rare_meanings: array
  common_meanings: array
```

### 7.3 复习记录 (Review Record)

```yaml
review_record:
  record_id: string
  user_id: string
  date: date
  created_at: datetime

  session_info:
    words_reviewed: int
    new_words: int
    duration_minutes: int

  results:
    correct_count: int
    incorrect_count: int
    polysemy_errors: int

  phase_context:
    current_phase: string
    days_to_exam: int
```

---

## 8. Day编号计算（共享功能）

### 8.1 calculate_day_number

基于日期计算Day编号，所有英语子技能共享此函数。

```python
from datetime import datetime

def calculate_day_number(target_date=None):
    """基于日期计算Day编号

    起始日期：2026-02-28 = Day 001
    计算公式：Day编号 = 1 + (目标日期 - 起始日期)的天数

    Args:
        target_date: 目标日期（YYYY-MM-DD格式字符串或datetime对象）
                     默认为None，使用当前日期

    Returns:
        int: Day编号（例如：17表示Day 017）

    Examples:
        >>> calculate_day_number("2026-02-28")
        1
        >>> calculate_day_number("2026-03-01")
        2
        >>> calculate_day_number("2026-03-16")
        17
        >>> calculate_day_number("2026-03-17")
        18
    """
    # 考研英语学习起始日期
    START_DATE = "2026-02-28"
    START_DAY = 1

    # 处理输入参数
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d")

    # 解析起始日期
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")

    # 计算天数差
    days_diff = (target_date - start_date).days

    # 计算Day编号
    day_number = START_DAY + days_diff

    # 确保Day编号不小于1
    return max(day_number, START_DAY)


def get_max_day_number_from_files(directory="考研英语/📰 真题语境文章"):
    """从现有文件中提取最大Day编号

    扫描指定目录中的所有.md文件，从文件名格式
    'Day-XXX-YYYY-MM-DD.md' 中提取Day编号。

    Args:
        directory: 要扫描的目录路径

    Returns:
        int: 找到的最大Day编号，如果没有文件则返回0
    """
    import os
    import re

    max_day = 0

    try:
        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                # 匹配文件名格式：Day-XXX-YYYY-MM-DD.md
                match = re.match(r"Day-(\d+)-\d{4}-\d{2}-\d{2}\.md", filename)
                if match:
                    day_num = int(match.group(1))
                    max_day = max(max_day, day_num)
    except FileNotFoundError:
        # 目录不存在，返回0
        pass
    except Exception as e:
        # 其他错误，记录警告并返回0
        log_warning(f"Failed to scan directory {directory}: {e}")

    return max_day


def get_validated_day_number(target_date=None,
                             directory="考研英语/📰 真题语境文章"):
    """获取验证后的Day编号（双重验证机制）

    同时使用两种方法计算Day编号：
    1. 基于现有文件的最大Day编号 + 1
    2. 基于日期计算的Day编号

    取两者中的较大值，确保：
    - 不覆盖现有文件（使用较大的编号）
    - Day编号与日期基本一致（差异过大时警告）

    Args:
        target_date: 目标日期（YYYY-MM-DD格式），默认为今天
        directory: 用于文件检查的目录

    Returns:
        int: 验证后的Day编号

    Warning:
        如果两种方法计算的Day编号差异 > 2，
        会发出警告（可能存在学习中断或文件缺失）
    """
    from_files = get_max_day_number_from_files(directory) + 1
    from_date = calculate_day_number(target_date)

    # 检查差异
    diff = abs(from_files - from_date)
    if diff > 2:
        log_warning(
            f"Day编号差异较大：文件检查显示Day {from_files}，"
            f"但日期计算显示Day {from_date}（差异{diff}天）"
        )
        log_info("将使用较大的Day编号以避免覆盖现有文件")

    # 返回较大的值（防止覆盖）
    return max(from_files, from_date)


def format_day_number(day_number, padding=3):
    """格式化Day编号为字符串

    Args:
        day_number: Day编号（整数）
        padding: 填充宽度，默认为3（例如：17 → "017"）

    Returns:
        str: 格式化后的Day编号字符串

    Examples:
        >>> format_day_number(1)
        '001'
        >>> format_day_number(17)
        '017'
        >>> format_day_number(100)
        '100'
    """
    return f"{day_number:0{padding}d}"


def generate_day_filenames(target_date=None, day_number=None):
    """生成四类学习笔记的文件名

    Args:
        target_date: 目标日期（YYYY-MM-DD格式）
        day_number: Day编号（整数），如果为None则自动计算

    Returns:
        dict: 包含四类文件名的字典

    Examples:
        >>> generate_day_filenames("2026-03-16", 17)
        {
            "context_article": "Day-017-2026-03-16.md",
            "quiz": "Quiz-Day-017-2026-03-16.md",
            "statistics": "Statistics-Day-017-2026-03-16.md",
            "writing": "Day-017-2026-03-16.md"
        }
    """
    if day_number is None:
        day_number = get_validated_day_number(target_date)

    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")

    day_str = format_day_number(day_number)

    return {
        "context_article": f"Day-{day_str}-{target_date}.md",
        "quiz": f"Quiz-Day-{day_str}-{target_date}.md",
        "statistics": f"Statistics-Day-{day_str}-{target_date}.md",
        "writing": f"Day-{day_str}-{target_date}.md"
    }
```

### 8.2 使用示例

```python
# 示例1：计算今天的Day编号
today_day = calculate_day_number()
print(f"Today is Day {format_day_number(today_day)}")

# 示例2：计算指定日期的Day编号
day_17 = calculate_day_number("2026-03-16")
print(f"2026-03-16 is Day {format_day_number(day_17)}")

# 示例3：获取验证后的Day编号（推荐）
validated_day = get_validated_day_number("2026-03-16")
print(f"Validated Day number: {validated_day}")

# 示例4：生成所有文件名
filenames = generate_day_filenames("2026-03-16", 17)
print(filenames)
# {
#     "context_article": "Day-017-2026-03-16.md",
#     "quiz": "Quiz-Day-017-2026-03-16.md",
#     "statistics": "Statistics-Day-017-2026-03-16.md",
#     "writing": "Day-017-2026-03-16.md"
# }
```

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
*最后更新: 2026-03-16（添加Day编号计算模块）*
