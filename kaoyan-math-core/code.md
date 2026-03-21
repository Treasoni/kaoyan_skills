# kaoyan-math-core 代码模块

本文档包含 kaoyan-math-core 技能的所有代码实现。

---

## 1. MemOS集成函数

### 1.1 load_user_context_from_memory

从MemOS加载用户上下文，失败时返回None触发降级。

```python
def load_user_context_from_memory(user_input):
    """从MemOS加载用户上下文

    Returns:
        dict: 用户上下文信息，包含用户画像、错题库等
        None: MemOS不可用时触发降级
    """
    try:
        results = search_memory(
            query=f"#user_profile {user_input.get('user_id')}",
            top_k=10
        )
        return parse_memory_to_math_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable: {e}")
        return None


def parse_memory_to_math_context(memory_results):
    """将MemOS结果解析为数学学习上下文"""
    if not memory_results:
        return create_default_user_context()

    context = {
        "user_profile": extract_user_profile(memory_results),
        "mistake_records": extract_mistake_records(memory_results),
        "knowledge_cards": extract_knowledge_cards(memory_results)
    }

    return context
```

### 1.2 save_mistake_to_memory

保存错误记录到MemOS，含降级处理。

```python
def save_mistake_to_memory(mistake_data, user_id):
    """保存错误记录到MemOS

    Args:
        mistake_data: 错误记录数据
        user_id: 用户ID
    """
    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "mistake_record",
                    "data": mistake_data
                },
                "tags": [
                    "#mistake_record",
                    f"#kp_{mistake_data['knowledge_point']}",
                    f"#mistake_type_{mistake_data['type']}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
        log_info(f"Saved mistake: {mistake_data['knowledge_point']}")
    except Exception as e:
        log_warning(f"Failed to save mistake {mistake_data['knowledge_point']}: {e}")
        # 降级：不影响主流程，仅不保存
```

### 1.3 generate_personalized_reminders

基于用户历史错误生成个性化提醒。

```python
def generate_personalized_reminders(user_id, current_kp):
    """生成个性化提醒

    Args:
        user_id: 用户ID
        current_kp: 当前知识点

    Returns:
        list: 个性化提醒列表
    """
    try:
        # 从MemOS读取该知识点的错误历史
        mistake_history = search_memory(
            query=f"#mistake_record #user_{user_id} #kp_{current_kp}",
            top_k=50
        )

        if not mistake_history:
            return []

        # 分析错误模式
        error_patterns = aggregate_error_patterns(mistake_history)

        reminders = []
        for pattern in error_patterns:
            if pattern["frequency"] >= 3:  # 重复犯错
                reminders.append(
                    f"⚠️ 你在 {pattern['type']} 方面已出错 {pattern['frequency']} 次，"
                    f"特别注意 {pattern['trigger']}"
                )

        return reminders
    except Exception as e:
        log_warning(f"Failed to generate reminders: {e}")
        return []
```

### 1.4 check_context_freshness_math

检查用户画像是否需要刷新。

```python
def check_context_freshness_math(user_context, current_date):
    """检查数学学习画像是否需要刷新

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
                "你的数学水平有变化吗？(基础/中级/高级)",
                f"考试类型需要调整吗？(当前: {profile.get('exam_type', '数一')})",
                f"考试日期需要更新吗？(当前: {profile.get('exam_date', '未设置')})",
                "重点模块需要调整吗？(高数/线代/概率)"
            ]
        }

    return {"needs_refresh": False}
```

---

## 2. 知识点联动算法

### 2.1 知识点关系图数据结构

```python
# 知识点关系图
KNOWLEDGE_GRAPH = {
    "洛必达法则": {
        "prerequisites": ["极限定义", "导数定义"],
        "combinations": ["等价无穷小", "泰勒公式"],
        "applications": ["定积分应用", "变限积分求导"],
        "cross_chapter_prompts": [
            "注意：当遇到变限积分求导时，通常会结合洛必达法则考查",
            "建议：同时复习 [[定积分应用]] 中的变限积分部分",
            "关联：洛必达法则常与泰勒公式结合考查极限问题"
        ]
    },
    "泰勒公式": {
        "prerequisites": ["导数定义", "高阶导数"],
        "combinations": ["洛必达法则", "等价无穷小"],
        "applications": ["级数展开", "近似计算"],
        "cross_chapter_prompts": [
            "注意：泰勒公式在处理复杂函数极限时比洛必达法则更简洁",
            "建议：掌握常见函数的泰勒展开式（sin x, cos x, e^x, ln(1+x)）",
            "关联：泰勒公式是级数展开的基础，参考 [[幂级数]]"
        ]
    },
    "变限积分求导": {
        "prerequisites": ["定积分定义", "导数定义"],
        "combinations": ["洛必达法则", "复合函数求导"],
        "applications": ["积分方程", "微分方程"],
        "cross_chapter_prompts": [
            "注意：变限积分求导常与洛必达法则结合考查极限",
            "建议：熟练掌握牛顿-莱布尼茨公式和链式法则",
            "关联：遇到积分方程时，常需先求导转化为微分方程"
        ]
    }
}
```

### 2.2 generate_proactive_links

生成主动关联提示。

```python
def generate_proactive_links(knowledge_point, user_mistakes=None):
    """生成主动关联提示

    Args:
        knowledge_point: 当前知识点
        user_mistakes: 用户历史错误（可选）

    Returns:
        dict: 关联提示结构
    """
    graph = KNOWLEDGE_GRAPH.get(knowledge_point, {})

    links = {
        "prerequisites": graph.get("prerequisites", []),
        "combinations": graph.get("combinations", []),
        "cross_chapter_prompts": graph.get("cross_chapter_prompts", []),
        "personalized": []
    }

    # 个性化提示（基于用户历史错误）
    if user_mistakes:
        for mistake in user_mistakes:
            if mistake["type"] == "条件遗漏":
                links["personalized"].append(
                    f"💡 你经常遗漏{mistake['condition']}条件，"
                    f"复习时重点看 [[{knowledge_point}]] 的定理条件部分"
                )

    return links
```

---

## 3. 跨学科关联函数

### 3.1 跨学科知识图谱

```yaml
CROSS_SUBJECT_KNOWLEDGE_GRAPH:
  "复数运算":
    linked_electronics:
      - "频率响应分析"
      - "交流电路"
      - "滤波器设计"
      - "阻抗计算"
    link_type: prerequisite
    importance: critical
    reminder: "⚠️ 「复数运算」是「频率响应分析」的前置知识"
    key_formulas:
      - "jω表示法"
      - "复数阻抗 Z = R + jX"

  "微分方程":
    linked_electronics:
      - "暂态响应"
      - "RC/RL电路"
      - "一阶电路分析"
    link_type: application
    importance: high
    reminder: "💡 「暂态响应」本质上是「微分方程」的应用"
    key_formulas:
      - "一阶RC: τ = RC"
      - "uc(t) = U₀(1-e^(-t/τ))"

  "积分":
    linked_electronics:
      - "RC充放电"
      - "能量计算"
      - "电容储能"
    link_type: application
    reminder: "「积分」在电容能量计算中的应用"

  "拉普拉斯变换":
    linked_electronics:
      - "s域分析"
      - "传递函数"
      - "频域分析"
    link_type: prerequisite
    importance: high
    reminder: "⚠️ 「拉普拉斯变换」是「传递函数」的基础"
```

### 3.2 generate_cross_subject_reminders

生成跨学科提醒。

```python
def generate_cross_subject_reminders(knowledge_point):
    """生成跨学科提醒

    Args:
        knowledge_point: 当前数学知识点

    Returns:
        跨学科提醒列表
    """
    graph = CROSS_SUBJECT_KNOWLEDGE_GRAPH.get(knowledge_point, {})

    reminders = []
    linked = graph.get("linked_electronics", [])

    if linked:
        importance = graph.get("importance", "medium")
        icon = "⚠️" if importance == "critical" else "💡"

        reminders.append(
            f"{icon} 此知识点在电子技术中的应用：{', '.join(linked[:3])}"
        )

        if graph.get("reminder"):
            reminders.append(graph["reminder"])

    return reminders


def find_cross_subject_refs(knowledge_point):
    """查找跨学科关联"""
    graph = CROSS_SUBJECT_KNOWLEDGE_GRAPH.get(knowledge_point, {})
    return graph.get("linked_electronics", [])
```

---

## 4. 调度信号处理函数

### 4.1 check_dispatch_signals

检查来自kaoyan-plan的调度信号。

```python
def check_dispatch_signals(user_id):
    """检查来自kaoyan-plan的调度信号"""
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_kaoyan-math #user_{user_id}",
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

    if action == "high_difficulty_sop":
        return {
            "mode": "high_difficulty",
            "difficulty": context.get("difficulty", "hard"),
            "time_block": context.get("time_block", "3h"),
            "instructions": "进入高难度数学学习模式，优先攻克薄弱知识点"
        }

    elif action == "cross_subject_reminder":
        topic = context.get("topic")
        return {
            "mode": "cross_subject",
            "topic": topic,
            "related_electronics": context.get("related_electronics"),
            "reminder": f"⚠️ 学习「{topic}」时，注意与电子技术的关联"
        }

    elif action == "weekly_error_analysis":
        return {
            "mode": "weekly_review",
            "aggregate": context.get("aggregate", True)
        }

    return None
```

---

## 5. 统一错误模型函数

### 5.1 save_mistake_with_subject_tag

保存错误记录（含学科标签）。

```python
def save_mistake_with_subject_tag(mistake_data, user_id):
    """保存错误记录（含学科标签）"""
    mistake_data["subject"] = "math"
    mistake_data["cross_subject_refs"] = find_cross_subject_refs(
        mistake_data.get("knowledge_point")
    )

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
                    "#subject_math",
                    f"#kp_{mistake_data.get('knowledge_point', '')}",
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

## 6. 主流程整合

```python
def process_math_learning_v3(user_input):
    """数学学习主流程（含MemOS集成）

    Args:
        user_input: 用户输入

    Returns:
        dict: 处理结果
    """
    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = safe_load_context(user_input)

    # 1.5 检查画像新鲜度
    profile_refresh = check_context_freshness_math(
        user_context, datetime.now()
    )
    if profile_refresh and profile_refresh.get("needs_refresh"):
        return generate_profile_refresh_question(profile_refresh)

    # 2. 处理用户请求（生成笔记/更新笔记）
    result = process_math_request(user_input, user_context)

    # 3. MemOS: 保存结果 (可降级)
    if result.get("mistake_records"):
        for mistake in result["mistake_records"]:
            save_mistake_to_memory(mistake, user_input.get("user_id"))

    return result


def safe_load_context(user_input):
    """安全加载用户上下文（含降级）"""
    context = load_user_context_from_memory(user_input)
    if context is None:
        log_info("MemOS unavailable, using default context")
        return create_default_user_context()
    return context
```
