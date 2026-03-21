# kaoyan-electronics-core 代码实现

> 本文件包含核心协调层的详细代码实现

---

## 1. MemOS集成函数

### 1.1 加载用户上下文

```python
def load_user_context_from_memory(user_id):
    """从MemOS加载电子技术学习上下文

    Args:
        user_id: 用户ID

    Returns:
        用户上下文字典，包含画像、错误历史、知识点卡片
    """
    try:
        # 搜索用户画像
        profile_results = search_memory(
            query=f"#user_profile #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=1
        )

        # 搜索错误历史
        mistake_results = search_memory(
            query=f"#mistake_record #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=50
        )

        # 搜索知识点卡片
        knowledge_results = search_memory(
            query=f"#knowledge_card #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=100
        )

        return {
            "profile": parse_profile(profile_results),
            "mistakes": parse_mistakes(mistake_results),
            "knowledge_cards": parse_knowledge_cards(knowledge_results),
            "loaded": True
        }
    except Exception as e:
        log_warning(f"MemOS不可用，降级为无状态模式: {e}")
        return {
            "profile": get_default_profile(),
            "mistakes": [],
            "knowledge_cards": {},
            "loaded": False
        }
```

### 1.2 保存错误记录

```python
def save_mistake_to_memory(user_id, knowledge_point, mistake_type,
                           original_understanding, correction):
    """保存错误记录到MemOS

    Args:
        user_id: 用户ID
        knowledge_point: 知识点名称（如"负反馈类型判断"）
        mistake_type: 错误类型
        original_understanding: 原始理解
        correction: 正确理解
    """
    mistake_data = {
        "knowledge_point": knowledge_point,
        "mistake_type": mistake_type,
        "original_understanding": original_understanding,
        "correction": correction,
        "timestamp": get_current_time(),
        "subject": "electronics"
    }

    # 查找数学关联
    cross_refs = find_math_refs(knowledge_point)
    if cross_refs:
        mistake_data["cross_subject_refs"] = cross_refs

    try:
        add_message(
            conversation_first_message=CONVERSATION_ID,
            messages=[{
                "role": "assistant",
                "content": json.dumps(mistake_data),
                "chat_time": get_current_time()
            }]
        )
    except Exception as e:
        log_warning(f"保存错误记录失败: {e}")
```

### 1.3 生成个性化提醒

```python
def generate_personalized_reminders(user_id, knowledge_point=None):
    """基于历史错误生成个性化提醒

    Args:
        user_id: 用户ID
        knowledge_point: 可选，限定特定知识点

    Returns:
        个性化提醒列表
    """
    context = load_user_context_from_memory(user_id)
    if not context["loaded"]:
        return []

    reminders = []

    # 统计各知识点错误次数
    mistake_counts = {}
    for mistake in context["mistakes"]:
        kp = mistake.get("knowledge_point")
        if knowledge_point and kp != knowledge_point:
            continue
        mistake_counts[kp] = mistake_counts.get(kp, 0) + 1

    # 生成高频错误提醒
    for kp, count in mistake_counts.items():
        if count >= 3:
            # 获取该知识点的常见错误类型
            common_types = get_common_mistake_types(context["mistakes"], kp)
            reminders.append({
                "knowledge_point": kp,
                "mistake_count": count,
                "common_types": common_types,
                "reminder": f"⚠️ 你在「{kp}」方面已出错{count}次",
                "suggestion": generate_suggestion(kp, common_types)
            })

    return reminders
```

### 1.4 检查用户画像新鲜度

```python
def check_context_freshness_electronics(user_id):
    """检查用户画像是否需要刷新

    Returns:
        (is_fresh, days_since_update, prompt_if_stale)
    """
    try:
        results = search_memory(
            query=f"#user_profile #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=1
        )

        if not results:
            return (False, None, "请确认你的822电子技术基础学习配置")

        last_update = parse_timestamp(results[0])
        days_since = (datetime.now() - last_update).days

        if days_since > 30:
            return (
                False,
                days_since,
                f"你的学习配置已{days_since}天未更新，请确认是否需要调整"
            )

        return (True, days_since, None)
    except Exception as e:
        return (False, None, "无法检查学习配置，请手动确认")
```

---

## 2. 数学前置检查

```python
MATH_PREREQUISITES = {
    "频率响应分析": {
        "required_math": [
            {
                "topic": "复数运算",
                "level": "basic",
                "check": "能正确进行复数加减乘除运算",
                "refresher": "复数运算回顾：j²=-1, Z=R+jX"
            },
            {
                "topic": "对数运算",
                "level": "basic",
                "check": "能理解对数坐标（波特图）",
                "refresher": "对数坐标：20log|H(jω)|"
            }
        ],
        "warning": "⚠️ 开始「频率响应」前，建议先确认数学基础是否扎实"
    },
    "暂态响应": {
        "required_math": [
            {
                "topic": "微分方程",
                "level": "intermediate",
                "check": "能求解一阶线性微分方程",
                "refresher": "一阶RC方程：τ·du/dt + u = U"
            },
            {
                "topic": "指数函数",
                "level": "basic",
                "check": "理解指数函数的图像和性质",
                "refresher": "指数衰减：e^(-t/τ)"
            }
        ],
        "warning": "⚠️ 「暂态响应」需要微分方程基础"
    },
    "滤波器设计": {
        "required_math": [
            {
                "topic": "拉普拉斯变换",
                "level": "intermediate",
                "check": "理解s域分析",
                "refresher": "传递函数：H(s)=Uo(s)/Ui(s)"
            }
        ],
        "warning": "⚠️ 「滤波器设计」需要拉普拉斯变换基础"
    }
}


def check_math_prerequisites(topic, user_context):
    """检查数学前置知识

    Args:
        topic: 要学习的电子技术主题
        user_context: 用户上下文（含数学学习记录）

    Returns:
        前置检查结果和建议
    """
    prereqs = MATH_PREREQUISITES.get(topic)

    if not prereqs:
        return {"needed": False}

    results = []
    for req in prereqs["required_math"]:
        math_topic = req["topic"]
        # 检查用户数学掌握程度
        mastery = get_math_mastery_level(user_context, math_topic)

        results.append({
            "topic": math_topic,
            "required_level": req["level"],
            "current_level": mastery,
            "passed": mastery >= req["level"],
            "refresher": req["refresher"]
        })

    all_passed = all(r["passed"] for r in results)

    return {
        "needed": True,
        "topic": topic,
        "warning": prereqs["warning"] if not all_passed else None,
        "results": results,
        "all_passed": all_passed
    }


def get_math_mastery_level(user_context, math_topic):
    """获取用户对某数学知识点的掌握程度

    Args:
        user_context: 用户上下文
        math_topic: 数学知识点名称

    Returns:
        掌握程度 (0-100)
    """
    # 尝试从MemOS获取数学学习记录
    try:
        results = search_memory(
            query=f"#knowledge_card #subject_math #kp_{math_topic}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=1
        )
        if results:
            return parse_mastery_level(results[0])
    except:
        pass

    # 默认返回基础水平
    return 30
```

---

## 3. 跨学科知识关联

```python
# 数学→电子技术知识图谱
MATH_TO_ELECTRONICS_MAP = {
    "复数运算": ["频率响应分析", "交流电路", "滤波器设计", "阻抗计算"],
    "微分方程": ["暂态响应", "RC/RL电路", "一阶电路分析"],
    "积分": ["RC充放电", "能量计算", "电容储能"],
    "拉普拉斯变换": ["s域分析", "传递函数", "频域分析"]
}

# 电子技术→数学反向映射
ELECTRONICS_TO_MATH_MAP = {
    "频率响应分析": ["复数运算", "对数运算"],
    "暂态响应": ["微分方程", "指数函数"],
    "滤波器设计": ["拉普拉斯变换", "复数运算"],
    "RC电路": ["积分", "微分方程"],
    "RL电路": ["微分方程", "指数函数"]
}


def generate_cross_subject_reminders(electronics_topic):
    """生成跨学科提醒（数学→电子技术）

    Args:
        electronics_topic: 当前学习的电子技术主题

    Returns:
        跨学科提醒
    """
    math_topics = ELECTRONICS_TO_MATH_MAP.get(electronics_topic, [])
    if not math_topics:
        return None

    return {
        "electronics_topic": electronics_topic,
        "required_math": math_topics,
        "reminder": f"⚠️ 「{electronics_topic}」需要以下数学基础：{', '.join(math_topics)}",
        "suggestion": f"💡 建议先复习数学「{math_topics[0]}」再深入学习{electronics_topic}"
    }


def find_math_refs(electronics_topic):
    """查找与电子技术知识点相关的数学知识点

    Args:
        electronics_topic: 电子技术知识点

    Returns:
        相关数学知识点列表
    """
    return ELECTRONICS_TO_MATH_MAP.get(electronics_topic, [])
```

---

## 4. 调度信号处理

```python
def check_dispatch_signals(user_id):
    """检查来自kaoyan-plan的调度信号

    Args:
        user_id: 用户ID

    Returns:
        待处理的调度信号列表
    """
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_kaoyan-electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=5
        )

        pending = []
        for signal in signals:
            if not signal.get("processed"):
                pending.append(signal)

        return pending
    except Exception as e:
        log_warning(f"检查调度信号失败: {e}")
        return []


def process_dispatch_signal(signal):
    """处理调度信号

    Args:
        signal: 调度信号字典

    Returns:
        处理结果
    """
    action = signal.get("action")
    context = signal.get("context", {})

    if action == "check_math_prerequisites":
        topic = context.get("topic")
        return {
            "mode": "prerequisite_check",
            "topic": topic,
            "required_math": context.get("required_math", []),
            "instructions": f"检查学习「{topic}」所需的数学基础"
        }

    elif action == "circuit_analysis_sop":
        circuit_type = context.get("circuit_type")
        return {
            "mode": "circuit_analysis",
            "circuit_type": circuit_type,
            "instructions": f"使用标准SOP分析{circuit_type}"
        }

    elif action == "weekly_error_analysis":
        return {
            "mode": "weekly_review",
            "aggregate": context.get("aggregate", True)
        }

    return None


def mark_signal_processed(signal_id, user_id):
    """标记调度信号为已处理

    Args:
        signal_id: 信号ID
        user_id: 用户ID
    """
    try:
        add_feedback(
            conversation_first_message=CONVERSATION_ID,
            feedback_content=f"调度信号 {signal_id} 已处理"
        )
    except Exception as e:
        log_warning(f"标记信号失败: {e}")
```

---

## 5. 统一错误模型

```python
def save_mistake_with_subject_tag(mistake_data, user_id):
    """保存错误记录（含学科标签）

    Args:
        mistake_data: 错误数据字典
        user_id: 用户ID
    """
    mistake_data["subject"] = "electronics"

    # 添加学科标签
    tags = mistake_data.get("tags", [])
    tags.append("#mistake_record")
    tags.append("#subject_electronics")

    # 添加知识点标签
    kp = mistake_data.get("knowledge_point", "")
    if kp:
        tags.append(f"#kp_{kp}")

    # 添加错误类型标签
    mistake_type = mistake_data.get("type", "unknown")
    tags.append(f"#mistake_type_{mistake_type}")

    mistake_data["tags"] = tags

    try:
        add_message(
            conversation_first_message=CONVERSATION_ID,
            messages=[{
                "role": "assistant",
                "content": json.dumps(mistake_data),
                "chat_time": get_current_time()
            }]
        )
    except Exception as e:
        log_warning(f"保存错误记录失败: {e}")
```

---

## 6. 考点权重计算

```python
def calculate_priority_score(exam_frequency, exam_importance, mastery_level, days_to_exam):
    """计算知识点优先级分数

    Args:
        exam_frequency: 考试频率 (1-10)
        exam_importance: 考试重要性 (1-10)
        mastery_level: 掌握程度 (0-100)
        days_to_exam: 距离考试天数

    Returns:
        优先级分数
    """
    # 时间衰减因子
    if days_to_exam > 180:
        alpha = 0.8  # 基础阶段
    elif days_to_exam > 90:
        alpha = 1.0  # 强化阶段
    elif days_to_exam > 30:
        alpha = 1.5  # 冲刺阶段
    else:
        alpha = 2.0  # 押题阶段

    # 优先级公式
    priority = (exam_frequency * exam_importance) / (mastery_level + 1) * alpha

    return int(priority * 10)  # 放大10倍便于比较


def get_study_time_recommendation(priority_score):
    """根据优先级分数推荐学习时间

    Args:
        priority_score: 优先级分数

    Returns:
        (建议时间, 策略描述)
    """
    if priority_score > 50:
        return ("60-90分钟", "重点突破，每天必练")
    elif priority_score > 20:
        return ("30-45分钟", "强化训练，隔天练习")
    elif priority_score > 10:
        return ("15-20分钟", "保持手感，每周复习")
    else:
        return ("0-10分钟", "考前突击，考前一周")
```

---

## 7. 辅助函数

```python
def log_warning(message):
    """记录警告日志"""
    print(f"[WARNING] {message}")


def get_current_time():
    """获取当前时间字符串"""
    from datetime import datetime
    return datetime.now().isoformat()


def parse_timestamp(memory_item):
    """从MemOS记录解析时间戳"""
    # 实现细节...
    pass


def get_default_profile():
    """获取默认用户画像"""
    return {
        "exam_type": "822电子技术基础",
        "target_school": "湖南大学",
        "focus_modules": ["模电", "数电"]
    }


def get_common_mistake_types(mistakes, knowledge_point):
    """获取某知识点的常见错误类型"""
    types = []
    for m in mistakes:
        if m.get("knowledge_point") == knowledge_point:
            types.append(m.get("mistake_type"))
    return list(set(types))


def generate_suggestion(knowledge_point, common_types):
    """根据错误类型生成建议"""
    suggestions = {
        "circuit_misread": "建议先识别电路拓扑，再进行分析",
        "calculation_error": "注意单位统一，检查公式是否正确",
        "concept_confusion": "建议画对比表格，区分易混淆概念",
        "forgot_condition": "使用检查清单，确保不遗漏条件"
    }
    return [suggestions.get(t, "多练习相关题目") for t in common_types]
```

---

*创建日期: 2026-03-12*
*版本: 1.0.0*
