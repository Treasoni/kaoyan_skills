# kaoyan-plan 跨技能调度协议

本文档包含 kaoyan-plan 技能的跨技能协调协议（v3.2新增）。

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 目录

1. [调度规则表](#调度规则表)
2. [调度信号格式](#调度信号格式)
3. [发送调度信号函数](#发送调度信号函数)
4. [全局权重计算](#全局权重计算)
5. [阶段权重表](#阶段权重表)
6. [跨学科协调](#跨学科协调)
7. [周日全科复盘](#周日全科复盘)
8. [统一用户画像](#统一用户画像)
9. [统一错误模型](#统一错误模型)
10. [跨技能集成验证](#跨技能集成验证)

---

## 调度规则表

本技能作为"中央大脑"，负责协调 kaoyan-math、kaoyan-english、kaoyan-electronics 三个技能的联合调度。

| 条件 | 目标技能 | 动作 | 上下文 |
|------|----------|------|--------|
| 晨型人 + 高精力 (08:00-12:00) | kaoyan-math, kaoyan-electronics | `high_difficulty_sop` | `{difficulty: "hard", time_block: "3h"}` |
| 疲劳检测 (fatigue > 0.6) | kaoyan-english | `vocabulary_review_mode` | `{mode: "light", duration: "30min"}` |
| 数学欠账 > 3h + 英语有余量 | kaoyan-english | `memory_compression_mode` | `{compress_hours: 1, transfer_to: "math"}` |
| 学习"频率响应" | kaoyan-math | `cross_subject_reminder` | `{topic: "复数运算"}` |
| 周日复盘 | 全部技能 | `weekly_error_analysis` | `{aggregate: true}` |

---

## 调度信号格式

```python
# 通过MemOS传递调度信号
dispatch_signal = {
    "type": "dispatch_signal",
    "target_skill": "kaoyan-math",
    "action": "high_difficulty_sop",
    "context": {"difficulty": "hard", "time_block": "3h"},
    "source": "kaoyan-plan",
    "timestamp": "2025-02-26T08:00:00"
}
# MemOS标签: #dispatch_signal #target_kaoyan-math #user_{user_id}
```

---

## 发送调度信号函数

```python
def send_dispatch_signal(target_skill, action, context, user_id):
    """发送调度信号到目标技能"""
    signal = {
        "type": "dispatch_signal",
        "signal_id": f"sig_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "target_skill": target_skill,
        "action": action,
        "context": context,
        "source": "kaoyan-plan",
        "priority": calculate_priority(action),
        "timestamp": datetime.now().isoformat()
    }

    try:
        add_message(
            messages=[{"role": "assistant", "content": signal}],
            tags=[
                "#dispatch_signal",
                f"#target_{target_skill}",
                f"#user_{user_id}"
            ],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to send dispatch signal: {e}")

    return signal


def calculate_priority(action):
    """根据动作类型计算优先级"""
    priority_map = {
        "high_difficulty_sop": 1,      # 最高优先
        "memory_compression_mode": 2,
        "vocabulary_review_mode": 3,
        "cross_subject_reminder": 4,
        "weekly_error_analysis": 5     # 最低优先
    }
    return priority_map.get(action, 3)
```

---

## 全局权重计算

```python
def calculate_global_weights(days_to_exam: int) -> dict:
    """根据距离考试天数计算动态权重"""

    if days_to_exam > 300:        # 基础期
        exam_urgency_factor = 0.8
        english_factor = 1.2      # 英语词汇积累
        major_factor = 0.8

    elif days_to_exam > 180:      # 强化期
        exam_urgency_factor = 1.0
        english_factor = 1.0
        major_factor = 1.0

    elif days_to_exam > 90:       # 十月强化期
        exam_urgency_factor = 1.3
        english_factor = 0.8      # 压缩英语
        major_factor = 1.5        # 提升专业课

    elif days_to_exam > 30:       # 冲刺期
        exam_urgency_factor = 1.5
        english_factor = 0.6      # 进一步压缩
        major_factor = 1.8

    else:                         # 极限冲刺
        exam_urgency_factor = 2.0
        english_factor = 0.4      # 最小化英语
        major_factor = 2.0

    return {
        "math": 1.5 * exam_urgency_factor,
        "english": 1.2 * english_factor,
        "electronics": 1.0 * major_factor,
        "politics": 0.6 * exam_urgency_factor,
        "phase": get_phase_name(days_to_exam),
        "days_to_exam": days_to_exam
    }


def get_phase_name(days_to_exam: int) -> str:
    """获取阶段名称"""
    if days_to_exam > 300:
        return "基础期"
    elif days_to_exam > 180:
        return "强化期"
    elif days_to_exam > 90:
        return "十月强化期"
    elif days_to_exam > 30:
        return "冲刺期"
    else:
        return "极限冲刺期"
```

---

## 阶段权重表

| 阶段 | 天数 | 数学 | 英语 | 专业课 | 政治 |
|------|------|------|------|--------|------|
| 基础期 | >300 | 1.2 | 1.44 | 0.8 | 0.48 |
| 强化期 | 180-300 | 1.5 | 1.2 | 1.0 | 0.6 |
| 十月强化期 | 90-180 | 1.95 | 0.96 | 1.5 | 1.2 |
| 冲刺期 | 30-90 | 2.25 | 0.72 | 1.8 | 1.2 |
| 极限冲刺 | <30 | 3.0 | 0.48 | 2.0 | 1.2 |

---

## 跨学科协调

### 数学↔专业课知识关联

从 `scripts/data/cross_subject_graph.yaml` 读取跨学科知识关联：

```yaml
# 数学 → 电子技术
"复数运算":
  linked_electronics: ["频率响应分析", "交流电路", "滤波器设计"]
  reminder: "⚠️ 学习「频率响应」时，复习数学「复数运算」会更清晰"

"微分方程":
  linked_electronics: ["暂态响应", "RC/RL电路", "一阶电路分析"]
  reminder: "💡 「暂态响应」本质上是「微分方程」的应用"
```

### 跨学科提醒生成

```python
def generate_cross_subject_reminder(current_topic, user_context):
    """生成跨学科提醒

    Args:
        current_topic: 当前学习主题
        user_context: 用户上下文

    Returns:
        跨学科提醒信息
    """
    try:
        # 加载跨学科知识图谱
        graph = load_cross_subject_graph()

        # 查找关联
        for math_topic, links in graph.get("math_to_electronics", {}).items():
            if current_topic in links.get("linked_electronics", []):
                return {
                    "type": "cross_subject_reminder",
                    "math_topic": math_topic,
                    "electronics_topic": current_topic,
                    "reminder": links.get("reminder", "").format(electronics=current_topic),
                    "importance": links.get("importance", "medium")
                }

        return None
    except Exception as e:
        log_warning(f"Failed to generate cross-subject reminder: {e}")
        return None
```

---

## 周日全科复盘

周日自动触发全科复盘，生成跨学科错题报告：

```python
def generate_weekly_cross_subject_report(user_context):
    """生成周日全科复盘报告

    Args:
        user_context: 用户上下文（含各技能学习数据）

    Returns:
        全科复盘报告
    """
    report = {
        "type": "weekly_cross_subject_report",
        "week_number": get_current_week_number(),
        "subjects": {
            "math": aggregate_math_errors(user_context),
            "english": aggregate_english_errors(user_context),
            "electronics": aggregate_electronics_errors(user_context),
            "politics": aggregate_politics_errors(user_context)
        },
        "cross_subject_analysis": analyze_cross_subject_errors(user_context),
        "adjustments": generate_adjustments(user_context)
    }

    return report
```

---

## 统一用户画像

### 全局用户画像格式

```yaml
global_user_profile:
  user_id: string
  exam_config:
    exam_date: date                    # 单一真实来源
    target_school: "湖南大学"
    days_to_exam: int

  energy_profile:
    chronotype: morning_person | night_person | normal
    peak_hours: [8, 12]                # 高效时段
    fatigue_sensitivity: high | medium | low

  subject_weights:
    math:
      base_weight: 1.5
      current_weight: 1.5              # 动态调整
      debt_hours: float
    english:
      base_weight: 1.2
      current_weight: 1.2
      vocabulary_debt: int
    electronics:
      base_weight: 1.0
      current_weight: 1.0
      debt_hours: float

  mental_history:                      # 统一心理状态追踪
    - date: date
      status: energized | normal | tired | burned_out
      affected_skills: [math, english]
```

---

## 统一错误模型

### 错误类型定义

```yaml
unified_mistake_record:
  record_id: string
  user_id: string
  subject: math | english | electronics | politics  # 学科标签
  knowledge_point: string

  mistake_type: enum
    - condition_omission               # 通用：条件遗漏
    - calculation_error                # 数学/电子：计算错误
    - concept_confusion                # 通用：概念混淆
    - circuit_misread                  # 电子专用：电路误读
    - polysemy_error                   # 英语专用：多义词错误

  cross_subject_refs: [string]         # 跨学科关联

  tags:
    - "#mistake_record"
    - "#subject_{subject}"
```

### 保存统一错误记录

```python
def save_unified_mistake(mistake_data, user_id):
    """保存统一错误记录到MemOS"""
    try:
        subject = mistake_data.get("subject", "unknown")

        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "unified_mistake_record",
                    "data": mistake_data
                },
                "tags": [
                    "#mistake_record",
                    f"#subject_{subject}",
                    f"#kp_{mistake_data.get('knowledge_point', '')}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save unified mistake: {e}")
```

---

## 跨技能集成验证

30. ✅ 晨型人高精力时段触发数学高难度SOP
31. ✅ 疲劳检测触发英语轻量复习模式
32. ✅ 数学欠账触发英语记忆压缩
33. ✅ 全局权重计算各阶段正确
34. ✅ 跨学科提醒生成（数学→电子）
35. ✅ 周日复盘生成全科错题报告
36. ✅ MemOS不可用时各技能独立运行（优雅降级）

---

## 新增数据文件

| 文件 | 路径 | 说明 |
|------|------|------|
| cross_subject_graph.yaml | `scripts/data/cross_subject_graph.yaml` | 跨学科知识关联数据 |
| dispatch_protocol.md | `scripts/templates/dispatch_protocol.md` | 调度协议文档 |
| weekly_cross_subject_report.md | `scripts/templates/weekly_cross_subject_report.md` | 周报模板 |

---

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
