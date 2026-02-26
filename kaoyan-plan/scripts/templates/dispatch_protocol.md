# 跨技能调度协议文档

> kaoyan-plan × kaoyan-math × kaoyan-english × kaoyan-electronics
> Version: 1.0.0

---

## 概述

本文档定义了四个考研技能之间的调度协议，实现中央调度、跨学科协调和动态权重分配。

---

## 1. 调度信号格式

### 1.1 信号结构

```yaml
dispatch_signal:
  type: "dispatch_signal"
  signal_id: "sig_{timestamp}_{random}"
  target_skill: "kaoyan-math" | "kaoyan-english" | "kaoyan-electronics"
  action: string  # 要执行的动作
  context: object  # 上下文参数
  source: "kaoyan-plan"
  priority: "high" | "medium" | "low"
  timestamp: "ISO8601"
  expires_at: "ISO8601"  # 可选：信号过期时间
```

### 1.2 MemOS标签

每个调度信号使用以下标签：
- `#dispatch_signal` - 调度信号标记
- `#target_{skill_name}` - 目标技能
- `#user_{user_id}` - 用户标识
- `#action_{action_name}` - 动作类型

---

## 2. 调度动作定义

### 2.1 kaoyan-math 动作

| 动作名 | 触发条件 | 上下文参数 | 说明 |
|--------|----------|------------|------|
| `high_difficulty_sop` | 晨型人+高精力 | `{difficulty: "hard", time_block: "3h"}` | 高难度数学SOP |
| `cross_subject_reminder` | 学习相关电子技术内容 | `{topic: "复数运算", related_electronics: "频率响应"}` | 跨学科提醒 |
| `weekly_error_analysis` | 周日复盘 | `{aggregate: true}` | 错误分析汇总 |

### 2.2 kaoyan-english 动作

| 动作名 | 触发条件 | 上下文参数 | 说明 |
|--------|----------|------------|------|
| `vocabulary_review_mode` | 疲劳检测 | `{mode: "light", duration: "30min"}` | 轻量词汇复习 |
| `memory_compression_mode` | 其他科目欠账 | `{compress_hours: 1, transfer_to: "math"}` | 记忆压缩模式 |
| `polysemy_focus` | 僻义错误率高 | `{focus: "polysemy", count: 20}` | 僻义词专项 |
| `weekly_error_analysis` | 周日复盘 | `{aggregate: true}` | 错误分析汇总 |

### 2.3 kaoyan-electronics 动作

| 动作名 | 触发条件 | 上下文参数 | 说明 |
|--------|----------|------------|------|
| `check_math_prerequisites` | 学习需要数学基础的内容 | `{topic: "频率响应", required_math: ["复数运算"]}` | 数学前置检查 |
| `circuit_analysis_sop` | 电路图分析 | `{circuit_type: "共射放大"}` | 电路分析SOP |
| `weekly_error_analysis` | 周日复盘 | `{aggregate: true}` | 错误分析汇总 |

---

## 3. 调度规则

### 3.1 精力状态调度

```yaml
精力调度规则:
  高精力 (fatigue < 0.4):
    晨型人_上午: kaoyan-math → high_difficulty_sop
    夜型人_晚上: kaoyan-math → high_difficulty_sop
    时间块: 3小时

  中等精力 (0.4 <= fatigue < 0.6):
    推荐科目: kaoyan-electronics, kaoyan-english(阅读)
    时间块: 2小时

  低精力 (fatigue >= 0.6):
    推荐科目: kaoyan-english → vocabulary_review_mode
    时间块: 30分钟
```

### 3.2 欠账调度

```yaml
欠账调度规则:
  数学欠账 > 3h 且 英语有余量:
    触发: kaoyan-english → memory_compression_mode
    效果: 英语时间压缩1h，转移至数学

  专业课欠账 > 2h:
    优先级提升: electronics_weight *= 1.3

  累计欠账 > 10h:
    触发: 熔断机制
    效果: 暂停新内容，专注补账
```

### 3.3 跨学科调度

```yaml
跨学科调度规则:
  学习"频率响应":
    触发: cross_subject_reminder
    提醒: "⚠️ 需要数学「复数运算」基础"

  学习"暂态响应":
    触发: check_math_prerequisites
    检查: 微分方程基础

  学习"滤波器设计":
    触发: cross_subject_reminder
    提醒: "💡 关联数学「拉普拉斯变换」"
```

---

## 4. 信号处理流程

### 4.1 信号发送（kaoyan-plan）

```python
def send_dispatch_signal(target_skill, action, context, user_id):
    """发送调度信号到目标技能"""
    signal = {
        "type": "dispatch_signal",
        "signal_id": f"sig_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random_id()}",
        "target_skill": target_skill,
        "action": action,
        "context": context,
        "source": "kaoyan-plan",
        "priority": calculate_priority(action),
        "timestamp": datetime.now().isoformat()
    }

    # 保存到MemOS
    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": signal
            }],
            tags=[
                "#dispatch_signal",
                f"#target_{target_skill}",
                f"#user_{user_id}",
                f"#action_{action}"
            ],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to send dispatch signal: {e}")

    return signal
```

### 4.2 信号接收（目标技能）

```python
def check_dispatch_signals(user_id, skill_name):
    """检查是否有待处理的调度信号"""
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_{skill_name} #user_{user_id}",
            top_k=10
        )

        pending_signals = []
        for signal in signals:
            # 检查是否过期
            if signal.get("expires_at"):
                if datetime.fromisoformat(signal["expires_at"]) < datetime.now():
                    continue

            # 检查是否已处理
            if signal.get("processed"):
                continue

            pending_signals.append(signal)

        return pending_signals
    except Exception as e:
        log_warning(f"Failed to check dispatch signals: {e}")
        return []


def process_dispatch_signal(signal):
    """处理调度信号"""
    action = signal.get("action")
    context = signal.get("context", {})

    if action == "high_difficulty_sop":
        return execute_high_difficulty_sop(context)
    elif action == "vocabulary_review_mode":
        return execute_vocabulary_review_mode(context)
    elif action == "memory_compression_mode":
        return execute_memory_compression_mode(context)
    elif action == "cross_subject_reminder":
        return execute_cross_subject_reminder(context)
    elif action == "weekly_error_analysis":
        return execute_weekly_error_analysis(context)
    else:
        log_warning(f"Unknown action: {action}")
        return None
```

---

## 5. 全局权重计算

### 5.1 动态权重算法

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

### 5.2 阶段权重表

| 阶段 | 天数范围 | 数学 | 英语 | 专业课 | 政治 |
|------|----------|------|------|--------|------|
| 基础期 | >300 | 1.2 | 1.44 | 0.8 | 0.48 |
| 强化期 | 180-300 | 1.5 | 1.2 | 1.0 | 0.6 |
| 十月强化期 | 90-180 | 1.95 | 0.96 | 1.5 | 1.2 |
| 冲刺期 | 30-90 | 2.25 | 0.72 | 1.8 | 1.2 |
| 极限冲刺 | <30 | 3.0 | 0.48 | 2.0 | 1.2 |

---

## 6. 优雅降级

当MemOS不可用时：

1. **调度信号**: 使用会话内临时存储
2. **权重计算**: 使用当前阶段默认值
3. **跨学科提醒**: 在生成计划时内联提示
4. **错误记录**: 保存到本地笔记文件

---

## 7. 版本历史

- **v1.0.0** (2025-02-26): 初始版本
  - 定义调度信号格式
  - 实现跨技能调度规则
  - 全局权重计算算法
  - 跨学科知识关联触发
