---
name: kaoyan-plan
description: This skill should be used when the user asks to generate study plans for 考研 (Chinese graduate entrance exam), parse course schedules, create daily/weekly study schedules, or optimize study time allocation. Supports three input modes (minimal/standard/advanced), adapts to individual chronotypes (morning person/night owl), handles task debt from missed plans with circuit breaker protection (>10h triggers recovery mode), enforces Sunday review, respects minimum block duration requirements for different subjects, integrates with MemOS for persistent learning progress tracking, includes context refresh mechanism (auto-prompts profile update after 30 days), mental health intervention (triggers after 3 consecutive tired days), and plan upsert logic with tagging for version control.
version: 3.2.0
---

# 考研规划Skill (Kaoyan Plan Generation Skill)

## 技能概述

本技能专注于考研学习计划生成，支持从课表中提取空闲时间，智能分配学习任务。采用**渐进式输入模式**（极简→标准→高级），适应不同使用场景。

### MemOS记忆系统集成 (v3.0新增)

本技能已集成MemOS记忆系统，实现考研学习状态的持续记录和追踪：

**核心特性**：
- **用户画像持久化**：保存考试日期、目标、作息类型等个性化配置
- **画像自动刷新**：超过30天未更新时自动触发画像确认询问（v3.1新增）
- **学习进度追踪**：记录每日计划执行情况，统计完成率和欠账时长
- **欠账熔断保护**：累计欠账超过10小时时强制暂停新内容（v3.1新增）
- **心理状态追踪**：连续3天疲惫时自动触发心理调节模式（v3.1新增）
- **计划智能更新**：同一天多次生成计划时自动归档历史版本（v3.1新增）
- **周日复盘数据**：自动汇总本周学习数据，生成完成度报告
- **优雅降级**：当MemOS不可用时，自动降级为无状态模式（v2.1.0行为）

**数据隐私**：所有学习数据通过MemOS工具管理，遵循用户配置的数据存储策略。

---

## 三层输入模式

### 1️⃣ 极简模式（默认）

**只需提供**：
- 课表（图片/PDF/口头描述）
- 今日优先任务（可选）

**适用场景**：首次使用、快速生成当日计划

**示例输入**：
```
"我周一上午没课，下午有英语课，今天想学高数第五章"
```

**输出**：基于默认考研规则生成的每日计划

**MemOS数据持久化**：首次使用后创建用户画像，后续调用会记忆用户偏好。

### 2️⃣ 标准模式

**额外需要**：
- 考试日期
- 科目权重偏好（可选，使用默认值）

**适用场景**：长期规划、需要阶段性调整

**示例输入**：
```
"我12月21日考试，数学比较薄弱，需要加强"
```

**输出**：考虑倒计时的分阶段计划

**MemOS数据持久化**：保存考试日期、科目权重配置到用户画像，用于后续个性化调整。

### 3️⃣ 高级模式

**额外需要**：
- 各科目进度
- 学习时长统计
- 疲劳度反馈

**适用场景**：精细化调整、数据分析

**示例输入**：
```
"数学进度落后10小时，这周学了18h英语12h专业课，感觉有点累"
```

**输出**：基于数据分析的个性化调整方案

**MemOS数据持久化**：从记忆中读取历史学习记录，计算进度偏差和疲劳趋势。

---

## 核心功能模块

### 功能1: 课表解析 + 空闲时间提取

**输入**: 用户课表（图片/PDF/JSON/口头描述）

**处理流程**:
1. 识别输入格式
2. 解析课表，提取课程信息
3. 识别每日空闲时段
4. 标记时段属性（上午/下午/晚上/深夜）

**输出**:
```yaml
schedule:
  free_slots:
    - day: "周一"
      time: "08:00-12:00"
      duration: 4h
    - day: "周一"
      time: "16:00-18:00"
      duration: 2h
```

### 功能2: 智能学习计划生成

**输入**: 课表数据、用户模式（极简/标准/高级）

**处理流程**:
1. 根据用户输入确定数据丰富度
2. 应用相应的规划策略
3. 考虑个体差异（chronotype）
4. 生成具体任务清单

**输出**:
- 每日计划（Markdown）
- 周计划（可选，标准模式以上）

### 功能3: 疲劳度管理（混合模型）

**输入**: 用户主观感受 + 行为数据（可选）

**处理流程**:
1. 收集用户主观反馈（精力很好/正常/有点累/很累）
2. 结合行为数据（学习时长、连续天数）
3. 计算混合疲劳度

**疲劳度公式**:
```python
fatigue = self_report * 0.6 + behavior_score * 0.4

# self_report: 用户主观感受 (0-1)
#   精力很好 → 0.0
#   正常     → 0.3
#   有点累   → 0.6
#   很累     → 0.9

# behavior_score: 行为推断 (0-1)
#   基于连续学习天数、日均时长等
```

**调整策略**:

| 主观感受 | 建议措施 |
|----------|----------|
| 精力很好 | 正常计划，可适当增加挑战 |
| 正常 | 正常计划 |
| 有点累 | 减少10-20%学习量，增加休息 |
| 很累 | 减少30%学习量，建议休息日 |

### 功能4: 任务欠账处理 (Debt Handler) ⭐实战补丁

**问题**: 计划赶不上变化是考研常态

**处理流程**:
1. 检测昨日未完成任务
2. 评估欠账严重程度
3. 生成补课建议
4. 询问用户是否采纳

**欠账等级** (v3.1更新: 增加熔断阈值):

| 欠账时长 | 等级 | 处理策略 |
|----------|------|----------|
| < 1小时 | 轻微 | 今日碎片时间补完 |
| 1-3小时 | 中等 | 压缩今日低优先任务补课 |
| 3-10小时 | 严重 | 建议补课日 |
| > 10小时 | 🔴 **熔断** | **强制暂停新内容** |

**v3.1熔断机制**: 当累计欠账超过10小时时，自动触发紧急恢复模式，暂停所有新内容学习，专注补账。

**AI自动询问**:
```
"昨天的高数任务未完成（欠账2小时）。
建议：压缩今日英语时间来补课？
选项：
1. 是，压缩英语时间补高数
2. 否，延后到周末补
3. 欠账太多，本周不补新内容，专注补账"
```

**输出**: 包含补课任务的调整后计划

### 功能5: 周日复盘模板 ⭐实战补丁

**问题**: 考研需要反复复盘，不能一直学新内容

**触发条件**: 每周日晚上自动触发

**复盘流程**:
1. 本周完成度统计
2. 错题重做（2小时强制）
3. 进度对齐检查
4. 下周计划调整

**周日复盘模板**:
```markdown
# 周日复盘 - 第{week}周 ({date})

## 本周完成度
| 科目 | 计划时长 | 实际时长 | 完成率 | 欠账 |
|------|----------|----------|--------|------|
| 数学 | {math_plan}h | {math_actual}h | {math_rate}% | {math_debt}h |
| 英语 | {eng_plan}h | {eng_actual}h | {eng_rate}% | {eng_debt}h |
| 专业课 | {major_plan}h | {major_actual}h | {major_rate}% | {major_debt}h |
| 政治 | {pol_plan}h | {pol_actual}h | {pol_rate}% | {pol_debt}h |

## 🔴 错题重做（必做，2小时）
- [ ] 数学错题本（30分钟）
- [ ] 英语阅读错题（30分钟）
- [ ] 专业课错题（30分钟）
- [ ] 政治选择题错题（30分钟）

## 进度对齐检查
- [ ] 本周目标达成检查
- [ ] 下周目标调整
- [ ] 欠账处理决策

## 下周调整
{adjustment_suggestions}
```

### 功能6: 最小块时长限制 ⭐实战补丁

**问题**: 数学需要大块时间（3小时+），单词可以碎片化

**最小块时长要求**:

| 科目 | 最小时长 | 原因 |
|------|----------|------|
| 数学 | 1.5小时 | 需要进入状态，碎片化效率极低 |
| 英语阅读 | 1小时 | 需要完整文章语境 |
| 专业课 | 1小时 | 需要深度思考 |
| 单词 | 15分钟 | 可碎片化 |
| 政治选择 | 20分钟 | 可碎片化 |

**自动替换逻辑**:
```python
def check_min_block_duration(slot, subject):
    """
    检查时段是否满足科目最小时长要求
    """
    min_duration = get_min_block_duration(subject)

    if slot.duration < min_duration:
        # 不满足，自动替换为可碎片化的科目
        return suggest_fragment_subject(slot.time)

    return subject

def suggest_fragment_subject(time_slot):
    """
    为碎片时段建议合适的科目
    """
    if time_slot <= 20:
        return "单词"
    elif time_slot <= 30:
        return "政治选择题"
    else:
        return "错题复习"
```

**示例**:
```
原计划：09:00-10:00 数学（1小时）
↓ 检测不满足最小1.5小时要求
替换为：09:00-10:00 单词复习（可碎片化）
```

---

## MemOS MCP工具集成 (v3.0)

### MCP工具调用策略 (v3.1更新)

本技能使用以下MemOS MCP工具实现数据持久化：

#### search_memory - 读取时机

1. **计划生成前**：获取用户画像和历史进度
2. **欠账检测**：读取昨日计划详情
3. **周日复盘**：读取本周所有学习记录
4. **画像新鲜度检查** (v3.1)：查询画像更新时间
5. **心理状态检查** (v3.1)：查询近期mental_history

#### add_message - 写入时机

1. **计划生成后**：保存计划到记忆（v3.1使用upsert逻辑）
2. **任务完成确认**：记录实际执行情况
3. **周日复盘完成**：保存复盘数据
4. **用户画像更新**：保存用户配置变更
5. **心理状态记录** (v3.1)：保存每日mental_status

#### add_feedback - 写入时机

1. **计划质量反馈**：用户对生成计划的评价
2. **技能使用体验**：整体使用满意度

#### v3.1 标签系统

本技能使用以下标签进行数据组织：

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#daily_plan_current` | 今日当前有效计划 | 每日只有1条 |
| `#daily_plan_history` | 历史计划版本归档 | 可有多条 |
| `#date_YYYY-MM-DD` | 日期索引 | 可有多条 |
| `#mental_status` | 心理状态记录 | 每日1条 |
| `#user_profile` | 用户画像 | 通常只有1条 |
| `#learning_progress` | 学习进度记录 | 每日1条 |
| `#weekly_review` | 周日复盘数据 | 每周1条 |

### 数据模型

#### 用户画像 (User Profile)
```yaml
user_profile:
  user_id: string
  conversation_id: string
  created_at: datetime
  updated_at: datetime

  profile:
    exam_date: date
    exam_target: string
    chronotype: enum (morning_person | night_person | normal)

  subject_weights:
    math: float (default 1.5)
    english: float (default 1.2)
    major: float (default 1.0)
    politics: float (default 0.6)

  preferences:
    preferred_time_slots: array
    min_block_durations: object
    fatigue_sensitivity: enum (high | medium | low)

  # v3.1 新增: 心理状态追踪
  mental_history:
    - date: date
      status: enum (energized | normal | tired | burned_out)
      stress_level: float (0.0-1.0)
      trigger: string  # 崩溃原因（可选）

  # v3.1 新增: 画像刷新配置
  refresh_config:
    last_refreshed: date
    auto_refresh_interval: int  # 天数，默认30
    pending_refresh: boolean
```

#### 学习进度记录 (Learning Progress)
```yaml
learning_progress:
  record_id: string
  user_id: string
  date: date
  created_at: datetime

  daily_plan:
    plan_id: string
    phase: string
    days_to_exam: int
    fatigue_level: float (0.0-1.0)

  tasks:
    - task_id: string
      subject: enum
      planned_duration: float
      actual_duration: float
      status: enum (completed | partial | skipped)
      time_slot: string
      priority: int

  statistics:
    total_planned_hours: float
    total_actual_hours: float
    completion_rate: float
    debt_hours: float
    continuous_study_days: int
```

#### 复盘数据 (Review Data)
```yaml
review_data:
  review_id: string
  user_id: string
  week_number: int
  week_start: date
  week_end: date
  created_at: datetime

  completion:
    math: {planned, actual, rate, debt}
    english: {planned, actual, rate, debt}
    major: {planned, actual, rate, debt}
    politics: {planned, actual, rate, debt}

  error_review:
    math_errors: int
    english_errors: int
    major_errors: int
    politics_errors: int
    time_spent: float

  adjustments:
    debt_strategy: enum
    next_week_focus: array
```

---

## 个性化适配

### Chronotype（作息类型）

**晨型人 (morning_person)**：
```
上午（08:00-12:00）：数学、高难度内容  ← 精力巅峰
下午（14:00-18:00）：英语阅读、专业课
晚上（19:00-23:00）：轻松复习、单词
深夜（23:00后）：不建议学习
```

**夜型人 (night_person)**：
```
上午（08:00-12:00）：单词、轻松内容
下午（14:00-18:00）：英语阅读、专业课
晚上（19:00-23:00）：数学、高难度内容  ← 精力巅峰
深夜（23:00后）：适度学习
```

**默认（未指定）**：使用晨型人模式（更符合考研普遍作息）

---

## 触发条件（意图优先级）

### 🔴 强触发（明确规划意图）

**必触发**：
- "生成考研计划" + 课表
- "制定学习计划" + 考研语境
- "今日学习计划"
- "考研时间表"
- "学习安排" + 考研

**原因**：用户明确要规划，直接调用技能

### 🟡 弱触发（可能需要规划）

**尝试触发，询问确认**：
- "解析课表"
- "提取空闲时间"
- 课表图片/PDF文件
- "周计划"（需要确认考研语境）

**原因**：用户可能只要课表信息，不一定需要规划

### 🔵 不触发

**不触发**：
- 非考研语境的学习计划
- 简单的时间管理建议
- 课程表查询（无规划意图）
- 纯粹的日程安排（非学习相关）

---

## 考研通用规则（默认值）

### 科目优先级

```
数学 > 英语 > 专业课 > 政治

权重：
- 数学：1.5（最重视，需要大量练习）
- 英语：1.2（单词持续，阅读稳步）
- 专业课：1.0（根据具体情况调整）
- 政治：0.6（后期突击为主）
```

### 时段适配规则（晨型人默认）

```
上午（08:00-12:00）：数学、英语单词（精力最好）
下午（14:00-18:00）：英语阅读、专业课（持续学习）
晚上（19:00-23:00）：专业课、政治复盘（总结整理）
深夜（23:00后）：仅复习，不学新内容
```

### 分阶段策略

```
基础期（>100天）：全面打基础，四科均衡
强化期（30-100天）：增加刷题量
冲刺期（7-30天）：真题模拟为主
极限冲刺期（<7天）：只复习，不学新内容
```

---

## 核心算法

### 主规划算法（v3.0 MemOS集成版）

```python
def generate_daily_plan_v3(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含MemOS记忆集成）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """

    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = safe_load_context(user_input)

    # 1.5 v3.1: 检查画像新鲜度 (context_refresh机制)
    profile_refresh = check_context_freshness(user_context, datetime.now())
    if profile_refresh and profile_refresh.get("needs_refresh"):
        # 返回画像刷新询问，等待用户确认后再继续
        return generate_profile_refresh_question(profile_refresh)

    # 1.6 v3.1: 检查心理状态是否需要干预
    mental_intervention = check_mental_health_intervention(user_context)
    if mental_intervention and mental_intervention.get("intervention_needed"):
        # 标记为心理调节模式，后续生成计划时应用
        user_input["mental_mode"] = mental_intervention.get("mode")

    # 2. 检查任务欠账（v3.1增强: 含熔断机制）
    debt_result = check_task_debt_with_memory(previous_plan, user_input, user_context)
    if debt_result:
        # v3.1: 检查是否触发熔断
        if debt_result.get("type") == "debt_emergency":
            return generate_emergency_recovery_plan(debt_result)
        return generate_debt_handling_plan(user_input, debt_result.get("tasks"))

    # 3. 检查周日复盘（增强: 从MemOS读取本周数据）
    if is_sunday(today):
        return generate_sunday_review_plan_with_memory(user_input, user_context)

    # 4. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input, user_context)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input, user_context)
    else:
        user_data = merge_user_input_with_memory(user_input, user_context)

    # 5. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 6. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 7. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_input.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 8. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True
    )

    # 9. MemOS: 保存计划 (可降级)
    safe_save_plan(plan, user_input, mode)

    return plan


def safe_load_context(user_input):
    """从MemOS加载用户上下文，失败时返回None触发降级"""
    try:
        results = search_memory(
            conversation_id=user_input.get("conversation_id"),
            user_id=user_input.get("user_id"),
            query=f"用户画像配置 学习进度记录",
            top_k=10
        )
        return parse_memory_results_to_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable, using defaults: {e}")
        return None


def safe_save_plan(plan, user_input, mode):
    """保存生成的计划（v3.1增强: upsert with tag逻辑）"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        user_id = user_input.get("user_id")

        # v3.1: 先尝试查找今日已有计划
        today_plan = search_memory(
            query=f"#daily_plan_current {user_id} {today}",
            top_k=1
        )

        if today_plan:
            # 更新: 标记旧版本为历史，保存新版本为当前
            old_plan = today_plan[0]
            add_message(
                messages=[{
                    "role": "assistant",
                    "content": {
                        "type": "daily_plan",
                        "version": old_plan.get("version", "v1"),
                        "status": "superseded",  # 标记为被替代
                        "data": old_plan.get("data"),
                        "superseded_at": datetime.now().isoformat()
                    },
                    "tags": ["#daily_plan_history", f"#date_{today}"]
                }],
                user_id=user_id
            )

        # 保存新计划为当前版本
        add_message(
            conversation_id=user_input.get("conversation_id"),
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "daily_plan",
                    "mode": mode,
                    "version": f"v{datetime.now().strftime('%H%M')}",
                    "status": "current",
                    "data": plan.to_dict(),
                    "timestamp": datetime.now().isoformat()
                },
                "tags": ["#daily_plan_current", f"#date_{today}"]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save plan to memory: {e}")


def check_task_debt_with_memory(previous_plan, user_input, user_context):
    """检查任务欠账（增强版：从MemOS读取昨日计划）"""
    # 如果提供了previous_plan参数，直接使用
    if previous_plan:
        return check_task_debt(previous_plan, user_input.get("completed_tasks"))

    # 否则尝试从MemOS读取昨日计划
    if user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            return check_task_debt(yesterday_plan, user_input.get("completed_tasks"))

    return []


def generate_sunday_review_plan_with_memory(user_input, user_context):
    """生成周日复盘计划（增强版：从MemOS读取本周数据）"""
    weekly_stats = None
    if user_context:
        weekly_stats = user_context.get("weekly_progress")

    return {
        "type": "sunday_review",
        "date": today,
        "weekly_stats": weekly_stats,
        "tasks": [
            {"time": "19:00-19:30", "task": "本周完成度统计", "required": True},
            {"time": "19:30-20:00", "task": "数学错题重做", "required": True},
            {"time": "20:00-20:30", "task": "英语错题重做", "required": True},
            {"time": "20:30-21:00", "task": "专业课错题重做", "required": True},
            {"time": "21:00-21:30", "task": "政治错题重做", "required": True},
            {"time": "21:30-22:00", "task": "进度对齐检查", "required": True},
            {"time": "22:00-23:00", "task": "下周计划调整", "required": True}
        ]
    }


def record_task_completion(user_id, completed_tasks, planned_tasks):
    """记录任务完成情况到MemOS"""
    try:
        stats = calculate_completion_stats(completed_tasks, planned_tasks)
        add_message(
            conversation_id=user_id,
            messages=[{
                "role": "user",
                "content": {
                    "type": "task_completion",
                    "data": stats
                }
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to record completion: {e}")


def load_weekly_data_for_review(user_id):
    """加载本周数据用于周日复盘"""
    try:
        results = search_memory(
            query=f"本周学习记录 {user_id}",
            top_k=20
        )
        return aggregate_weekly_stats(results)
    except Exception:
        return None


def parse_memory_results_to_context(memory_results):
    """解析MemOS搜索结果为用户上下文"""
    context = {
        "user_profile": None,
        "yesterday_plan": None,
        "weekly_progress": None,
        "historical_stats": None
    }

    for result in memory_results:
        content_type = result.get("content", {}).get("type")
        if content_type == "user_profile":
            context["user_profile"] = result.get("content", {}).get("data")
        elif content_type == "daily_plan" and is_yesterday(result.get("timestamp")):
            context["yesterday_plan"] = result.get("content", {}).get("data")
        elif content_type == "task_completion" and is_this_week(result.get("timestamp")):
            if not context["weekly_progress"]:
                context["weekly_progress"] = []
            context["weekly_progress"].append(result.get("content", {}).get("data"))

    return context


def calculate_completion_stats(completed_tasks, planned_tasks):
    """计算任务完成统计"""
    total_planned = sum(t.get("planned_duration", 0) for t in planned_tasks)
    total_actual = sum(t.get("actual_duration", 0) for t in completed_tasks)
    completion_rate = (total_actual / total_planned * 100) if total_planned > 0 else 0

    return {
        "total_planned_hours": total_planned,
        "total_actual_hours": total_actual,
        "completion_rate": completion_rate,
        "debt_hours": max(0, total_planned - total_actual)
    }


def aggregate_weekly_stats(weekly_records):
    """汇总本周统计数据"""
    if not weekly_records:
        return None

    aggregated = {
        "math": {"planned": 0, "actual": 0},
        "english": {"planned": 0, "actual": 0},
        "major": {"planned": 0, "actual": 0},
        "politics": {"planned": 0, "actual": 0}
    }

    for record in weekly_records:
        for subject in aggregated.keys():
            aggregated[subject]["planned"] += record.get(f"{subject}_planned", 0)
            aggregated[subject]["actual"] += record.get(f"{subject}_actual", 0)

    # 计算完成率和欠账
    for subject in aggregated.keys():
        planned = aggregated[subject]["planned"]
        actual = aggregated[subject]["actual"]
        aggregated[subject]["rate"] = (actual / planned * 100) if planned > 0 else 0
        aggregated[subject]["debt"] = max(0, planned - actual)

    return aggregated


def log_warning(message):
    """记录警告日志"""
    # 在实际实现中，这里可以连接到日志系统
    pass


def is_yesterday(timestamp_str):
    """判断时间戳是否为昨天"""
    try:
        from datetime import datetime, timedelta
        timestamp = datetime.fromisoformat(timestamp_str)
        yesterday = datetime.now() - timedelta(days=1)
        return timestamp.date() == yesterday.date()
    except:
        return False


def is_this_week(timestamp_str):
    """判断时间戳是否为本周"""
    try:
        from datetime import datetime
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start.date() <= timestamp.date() <= week_end.date()
    except:
        return False


# ============ v3.1 新增函数 ============

def check_context_freshness(user_context, current_date):
    """
    检查用户画像是否需要刷新（v3.1 context_refresh机制）

    参数:
        user_context: 用户上下文（含用户画像）
        current_date: 当前日期

    返回:
        None 或 刷新询问信息字典
    """
    if not user_context:
        return None

    profile = user_context.get("user_profile")
    if not profile:
        return None

    # 检查画像更新时间
    updated_at = profile.get("updated_at")
    if not updated_at:
        return None

    try:
        from datetime import datetime
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        days_since_update = (current_date - updated_at.date()).days

        # 超过30天自动触发刷新询问
        if days_since_update > 30:
            refresh_config = profile.get("refresh_config", {})
            auto_refresh_interval = refresh_config.get("auto_refresh_interval", 30)

            if days_since_update > auto_refresh_interval:
                return {
                    "needs_refresh": True,
                    "reason": f"画像已{days_since_update}天未更新",
                    "days_since_update": days_since_update,
                    "current_chronotype": profile.get("profile", {}).get("chronotype", "未知"),
                    "current_sensitivity": profile.get("preferences", {}).get("fatigue_sensitivity", "未知"),
                    "questions": [
                        "你的作息类型有变化吗？(晨型人/夜型人/正常)",
                        "科目优先级需要调整吗？",
                        "疲劳敏感度有变化吗？(高/中/低)"
                    ]
                }
    except Exception as e:
        log_warning(f"Failed to check context freshness: {e}")

    return {"needs_refresh": False}


def generate_profile_refresh_question(refresh_info):
    """
    生成画像刷新询问

    参数:
        refresh_info: check_context_freshness返回的刷新信息

    返回:
        画像刷新询问计划
    """
    return {
        "type": "profile_refresh",
        "reason": refresh_info.get("reason"),
        "days_since_update": refresh_info.get("days_since_update"),
        "current_settings": {
            "chronotype": refresh_info.get("current_chronotype"),
            "fatigue_sensitivity": refresh_info.get("current_sensitivity")
        },
        "questions": refresh_info.get("questions"),
        "message": f"⚠️ {refresh_info.get('reason')}，为了提供更准确的计划，请确认以下设置是否有变化："
    }


def check_task_debt_with_memory(previous_plan, user_input, user_context):
    """
    检查任务欠账（v3.1增强版：含熔断机制）

    参数:
        previous_plan: 昨日计划
        user_input: 用户输入
        user_context: 用户上下文

    返回:
        欠账任务信息 或 熔断信息
    """
    debt_tasks = []

    # 如果提供了previous_plan参数，直接使用
    if previous_plan:
        debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks"))
    # 否则尝试从MemOS读取昨日计划
    elif user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            debt_tasks = check_task_debt(yesterday_plan, user_input.get("completed_tasks"))

    if not debt_tasks:
        return None

    # v3.1: 熔断检查
    total_debt_hours = calculate_total_debt_hours(user_context, debt_tasks)
    DEBT_LIMIT = 10  # 10小时熔断阈值

    if total_debt_hours > DEBT_LIMIT:
        return {
            "type": "debt_emergency",
            "total_hours": total_debt_hours,
            "strategy": "recovery_only",
            "message": f"⚠️ 欠账已达{total_debt_hours}小时，超过安全阈值（{DEBT_LIMIT}小时）",
            "suggestion": "暂停所有新内容，专注补账",
            "tasks": generate_recovery_plan(total_debt_hours)
        }

    return {
        "type": "debt_warning",
        "tasks": debt_tasks,
        "total_hours": total_debt_hours
    }


def calculate_total_debt_hours(user_context, current_debt_tasks):
    """
    计算总欠账时长（含历史累计）

    参数:
        user_context: 用户上下文
        current_debt_tasks: 当前欠账任务

    返回:
        总欠账小时数
    """
    current_debt = sum(task.get("duration", 0) for task in current_debt_tasks)

    # 从用户上下文中获取历史累计欠账
    historical_debt = 0
    if user_context and user_context.get("weekly_progress"):
        for record in user_context.get("weekly_progress", []):
            historical_debt += record.get("debt_hours", 0)

    return current_debt + historical_debt


def generate_recovery_plan(total_debt_hours):
    """
    生成紧急恢复计划（熔断触发后使用）

    参数:
        total_debt_hours: 总欠账小时数

    返回:
        恢复计划任务列表
    """
    # 按科目优先级分配补账时间
    recovery_tasks = [
        {
            "subject": "数学",
            "duration": min(total_debt_hours * 0.4, 4),
            "task": "【补账】数学错题重做 + 未完成练习",
            "priority": 1
        },
        {
            "subject": "专业课",
            "duration": min(total_debt_hours * 0.3, 3),
            "task": "【补账】专业课复习",
            "priority": 2
        },
        {
            "subject": "英语",
            "duration": min(total_debt_hours * 0.2, 2),
            "task": "【补账】英语阅读补做",
            "priority": 3
        },
        {
            "subject": "政治",
            "duration": min(total_debt_hours * 0.1, 1),
            "task": "【补账】政治选择题补做",
            "priority": 4
        }
    ]

    return recovery_tasks


def generate_emergency_recovery_plan(debt_result):
    """
    生成紧急恢复计划（熔断模式）

    参数:
        debt_result: 欠账检测结果

    返回:
        紧急恢复计划
    """
    return {
        "type": "emergency_recovery",
        "total_debt_hours": debt_result.get("total_hours"),
        "message": debt_result.get("message"),
        "suggestion": debt_result.get("suggestion"),
        "recovery_plan": debt_result.get("tasks"),
        "notice": "⚠️ 今日暂停所有新内容学习，专注补账。欠账降至安全阈值后自动恢复正常模式。"
    }


def check_mental_health_intervention(user_context):
    """
    检查是否需要心理干预（v3.1 mental_status追踪）

    参数:
        user_context: 用户上下文

    返回:
        None 或 干预信息字典
    """
    if not user_context:
        return None

    profile = user_context.get("user_profile")
    if not profile:
        return None

    mental_history = profile.get("mental_history", [])
    if not mental_history or len(mental_history) < 3:
        return None

    # 检查最近3天的状态
    recent_days = mental_history[-3:]
    tired_count = sum(1 for d in recent_days if d.get("status") in ["tired", "burned_out"])

    if tired_count >= 3:
        # 分析压力水平
        avg_stress = sum(d.get("stress_level", 0.5) for d in recent_days) / len(recent_days)

        # 找出触发原因
        triggers = [d.get("trigger") for d in recent_days if d.get("trigger")]
        common_trigger = max(set(triggers), key=triggers.count) if triggers else "持续学习"

        return {
            "intervention_needed": True,
            "mode": "psychological_adjustment",
            "tired_days": tired_count,
            "avg_stress": avg_stress,
            "common_trigger": common_trigger,
            "actions": [
                "在计划开头添加鼓励语",
                "强制安排休息活动",
                "减少学习量30%"
            ]
        }

    return None


def record_mental_status(user_id, mental_status, stress_level, trigger=None):
    """
    记录用户心理状态到MemOS

    参数:
        user_id: 用户ID
        mental_status: 心理状态 (energized | normal | tired | burned_out)
        stress_level: 压力水平 (0.0-1.0)
        trigger: 触发原因（可选）
    """
    try:
        from datetime import datetime

        add_message(
            messages=[{
                "role": "user",
                "content": {
                    "type": "mental_status_update",
                    "data": {
                        "date": datetime.now().date().isoformat(),
                        "status": mental_status,
                        "stress_level": stress_level,
                        "trigger": trigger
                    }
                },
                "tags": ["#mental_status", f"#date_{datetime.now().strftime('%Y-%m-%d')}"]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to record mental status: {e}")
```

### 主规划算法（v2.1 实战版 - 降级兼容）

当MemOS不可用时，系统会降级使用v2.1.0算法：

```python
def generate_daily_plan(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含实战补丁，无MemOS降级版）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """

    # 1. 检查任务欠账（实战补丁1）
    debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks"))

    if debt_tasks:
        # 欠账处理
        return generate_debt_handling_plan(user_input, debt_tasks)

    # 2. 检查是否周日（实战补丁2）
    if is_sunday(today):
        return generate_sunday_review_plan(user_input)

    # 3. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input)
    else:
        user_data = user_input

    # 4. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 5. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 6. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_input.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 7. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True  # 实战补丁3
    )

    return plan


def check_task_debt(previous_plan, completed_tasks):
    """
    检查任务欠账（实战补丁1）

    返回:
        欠账任务列表
    """
    if not previous_plan:
        return []

    debt_tasks = []
    for task in previous_plan.tasks:
        if task not in completed_tasks:
            debt_tasks.append(task)

    return debt_tasks


def generate_debt_handling_plan(user_input, debt_tasks):
    """
    生成补课计划（实战补丁1）

    欠账处理策略：
    - 轻微（<1h）：碎片时间补
    - 中等（1-3h）：压缩低优先任务
    - 严重（>3h）：建议补课日
    """
    total_debt_hours = sum(task.duration for task in debt_tasks)

    if total_debt_hours < 1:
        strategy = "fragment"
    elif total_debt_hours < 3:
        strategy = "compress"
    else:
        strategy = "recovery_day"

    # 生成AI询问
    question = format_debt_question(debt_tasks, total_debt_hours, strategy)

    # 返回补课计划选项
    return {
        "type": "debt_handling",
        "debt_tasks": debt_tasks,
        "total_hours": total_debt_hours,
        "strategy": strategy,
        "question": question,
        "options": generate_debt_options(debt_tasks, strategy)
    }


def generate_sunday_review_plan(user_input):
    """
    生成周日复盘计划（实战补丁2）

    强制包含：
    - 本周完成度统计
    - 2小时错题重做
    - 进度对齐检查
    """
    return {
        "type": "sunday_review",
        "date": today,
        "tasks": [
            {"time": "19:00-19:30", "task": "本周完成度统计", "required": True},
            {"time": "19:30-20:00", "task": "数学错题重做", "required": True},
            {"time": "20:00-20:30", "task": "英语错题重做", "required": True},
            {"time": "20:30-21:00", "task": "专业课错题重做", "required": True},
            {"time": "21:00-21:30", "task": "政治错题重做", "required": True},
            {"time": "21:30-22:00", "task": "进度对齐检查", "required": True},
            {"time": "22:00-23:00", "task": "下周计划调整", "required": True}
        ]
    }


def check_min_block_duration(slot, subject):
    """
    检查时段是否满足科目最小时长要求（实战补丁3）

    如果不满足，自动替换为可碎片化的科目
    """
    min_duration = get_min_block_duration(subject)

    if slot.duration < min_duration:
        # 不满足，自动替换
        return suggest_fragment_subject(slot.duration)

    return subject


def get_min_block_duration(subject):
    """
    获取科目最小时长要求
    """
    requirements = {
        "数学": 1.5,      # 需要90分钟以上进入状态
        "英语阅读": 1.0,  # 需要完整文章语境
        "专业课": 1.0,    # 需要深度思考
        "单词": 0.25,     # 15分钟即可
        "政治选择": 0.33, # 20分钟即可
        "错题复习": 0.5   # 30分钟即可
    }
    return requirements.get(subject, 1.0)


def suggest_fragment_subject(duration):
    """
    为碎片时段建议合适的科目
    """
    if duration <= 0.25:  # 15分钟以内
        return "单词"
    elif duration <= 0.5:  # 30分钟以内
        return "政治选择题"
    else:  # 30-60分钟
        return "错题复习"
```

### 主规划算法（自适应）

```python
def generate_daily_plan(user_input, mode="minimal"):
    """
    根据用户输入模式生成计划

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")

    返回:
        每日计划
    """

    # 1. 根据模式确定数据丰富度
    if mode == "minimal":
        # 极简模式：使用默认值
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        # 标准模式：考虑考试日期
        user_data = enrich_with_exam_info(user_input)
    else:
        # 高级模式：使用完整数据
        user_data = user_input

    # 2. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 3. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 4. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_data.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0  # 默认精力良好

    # 5. 分配时段到科目
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue
    )

    return plan


def calculate_mixed_fatigue(self_report, behavior_data=None):
    """
    混合疲劳度计算

    参数:
        self_report: 用户主观感受
        behavior_data: 行为数据（可选）

    返回:
        疲劳度 (0.0-1.0)
    """
    # 主观感受权重 0.6
    self_report_map = {
        "精力很好": 0.0,
        "正常": 0.3,
        "有点累": 0.6,
        "很累": 0.9
    }
    subjective = self_report_map.get(self_report, 0.3)

    # 行为数据权重 0.4
    if behavior_data:
        behavioral = calculate_behavior_fatigue(behavior_data)
    else:
        behavioral = 0.0

    return subjective * 0.6 + behavioral * 0.4


def get_slot_preferences(chronotype):
    """
    根据作息类型返回时段偏好

    参数:
        chronotype: "morning_person" | "night_person" | "normal"

    返回:
        时段偏好字典
    """
    if chronotype == "night_person":
        return {
            "morning": ["单词", "轻松内容"],
            "afternoon": ["英语阅读", "专业课"],
            "evening": ["数学", "高难度内容"],
            "late_night": ["适度复习"]
        }
    else:  # 默认晨型人
        return {
            "morning": ["数学", "英语单词"],
            "afternoon": ["英语阅读", "专业课"],
            "evening": ["专业课", "政治", "复盘"],
            "late_night": ["仅复习"]
        }
```

---

## 模板

### 模板1: 每日计划（极简版）

```markdown
# 今日学习计划 - {date}

## 今日概览
- **空闲时间**: {free_hours}小时
- **今日重点**: {priority_task}

## 学习计划
- [ ] 08:00-10:00 | {subject1} | {task1}
- [ ] 10:00-12:00 | {subject2} | {task2}
- [ ] 14:00-16:00 | {subject3} | {task3}
- [ ] 19:00-21:00 | {subject4} | {task4}

## 备注
{notes}
```

### 模板2: 每日计划（标准版）

```markdown
# 今日学习计划 - {date}

## 今日概览
- **阶段**: {phase}
- **距离考试**: {days}天
- **今日精力**: {energy_level}
- **今日重点**: {priority_task}

## 上午计划 (08:00-12:00)
- [ ] {time1} | {subject1} | {task1}
- [ ] {time2} | {subject2} | {task2}

## 下午计划 (14:00-18:00)
- [ ] {time3} | {subject3} | {task3}
- [ ] {time4} | {subject4} | {task4}

## 晚上计划 (19:00-23:00)
- [ ] {time5} | {subject5} | {task5}
- [ ] {time6} | 复盘 | 今日总结

## 备注
{notes}
```

### 模板3: 周计划（标准/高级）

```markdown
# 本周学习计划 - 第{week}周

## 本周概览
- **日期**: {start_date} 至 {end_date}
- **阶段**: {phase}
- **距离考试**: {days}天

## 本周目标
- [ ] {goal1}
- [ ] {goal2}
- [ ] {goal3}

## 每日概要
| 日期 | 上午 | 下午 | 晚上 |
|------|------|------|------|
| 周一 | {morning1} | {afternoon1} | {evening1} |
| 周二 | {morning2} | {afternoon2} | {evening2} |
| ... | ... | ... | ... |

## 调整建议
{suggestions}
```

### 模板4: 周日复盘（强制触发）

```markdown
# 周日复盘 - 第{week}周 ({date})

## 本周完成度
| 科目 | 计划时长 | 实际时长 | 完成率 | 欠账 |
|------|----------|----------|--------|------|
| 数学 | {math_plan}h | {math_actual}h | {math_rate}% | {math_debt}h |
| 英语 | {eng_plan}h | {eng_actual}h | {eng_rate}% | {eng_debt}h |
| 专业课 | {major_plan}h | {major_actual}h | {major_rate}% | {major_debt}h |
| 政治 | {pol_plan}h | {pol_actual}h | {pol_rate}% | {pol_debt}h |

## 🔴 错题重做（必做，2小时）
- [ ] 19:30-20:00 | 数学错题本 | 30分钟
- [ ] 20:00-20:30 | 英语阅读错题 | 30分钟
- [ ] 20:30-21:00 | 专业课错题 | 30分钟
- [ ] 21:00-21:30 | 政治选择题错题 | 30分钟

## 进度对齐检查
- [ ] 本周目标达成：{goals_status}
- [ ] 欠账处理决策：{debt_decision}
- [ ] 下周重点调整：{next_week_focus}

## 下周计划
{next_week_plan}
```

### 模板5: 补课计划（欠账处理）

```markdown
# 今日计划（含补课） - {date}

## ⚠️ 欠账提醒
昨日未完成任务：{debt_tasks}
欠账时长：{debt_hours}小时

## 补课安排
- [ ] {time1} | {subject1} | 【补课】{task1}

## 今日新内容
- [ ] {time2} | {subject2} | {task2}

## 调整说明
今日已压缩{compressed_subject}时间用于补课
```

---

## 工作流程

### v3.0工作流程（含MemOS集成）

```
[用户输入]
      ↓
[MemOS: 读取用户上下文]
  - 用户画像
  - 昨日计划
  - 本周进度
      ↓
[识别输入模式]
  ├─ 极简模式 → 使用默认值/记忆数据
  ├─ 标准模式 → 询问考试日期/偏好
  └─ 高级模式 → 分析完整数据
      ↓
[检查特殊状态]
  ├─ 任务欠账 → 生成补课方案
  └─ 周日复盘 → 生成复盘计划
      ↓
[解析课表]
      ↓
[个性化适配]
  - Chronotype (来自用户画像)
  - 疲劳度 (来自记忆/输入)
  - 科目偏好 (来自用户画像)
      ↓
[生成计划]
      ↓
[MemOS: 保存计划]
  - 保存计划到记忆
  - 更新用户画像
      ↓
[输出结果]
```

### v2.1.0工作流程（降级模式，无MemOS）

```
[用户输入]
      ↓
[识别输入模式]
  ├─ 极简模式 → 使用默认值
  ├─ 标准模式 → 询问考试日期/偏好
  └─ 高级模式 → 分析完整数据
      ↓
[解析课表]
      ↓
[个性化适配]
  - Chronotype
  - 疲劳度
  - 科目偏好
      ↓
[生成计划]
      ↓
[输出结果]
```

---

## 验证标准

### 基础功能验证
1. ✅ 极简模式下只需课表即可生成计划
2. ✅ 支持用户主观疲劳反馈
3. ✅ 支持晨型人/夜型人适配
4. ✅ 能解析图片/PDF课表
5. ✅ 能提取每日空闲时段
6. ✅ 能生成每日计划（Markdown）
7. ✅ 能生成周计划（标准模式以上）
8. ✅ 触发条件具有意图优先级
9. ✅ 默认考研规则合理
10. ✅ 能检测任务欠账并生成补课方案（实战补丁1）
11. ✅ 周日自动触发复盘模式（实战补丁2）
12. ✅ 检查时段是否满足科目最小时长要求（实战补丁3）

### MemOS集成验证 (v3.0)
13. ✅ 能从MemOS读取用户画像和历史数据
14. ✅ 计划生成后能保存到MemOS
15. ✅ 任务完成情况能记录到MemOS
16. ✅ 周日复盘能汇总本周MemOS数据
17. ✅ MemOS不可用时能优雅降级为v2.1.0模式
18. ✅ 多用户数据隔离正确（基于user_id）
19. ✅ 100天历史数据下响应时间 < 5秒

### MemOS增强验证 (v3.1)
20. ✅ 画像超过30天未更新时自动触发刷新询问
21. ✅ 累计欠账超过10小时时触发熔断模式
22. ✅ 同一天多次生成计划时使用upsert逻辑（旧版本归档为历史）
23. ✅ 连续3天疲惫反馈时触发心理调节模式
24. ✅ 生成的计划包含跨设备同步元数据
25. ✅ 心理状态记录能正确保存到MemOS
26. ✅ 用户画像更新后次日计划使用新配置

---

## 限制条件

### 基础限制
- OCR识别依赖图片清晰度
- 课表格式需要一定的规范性
- 极简模式使用默认值，个性化程度较低
- 疲劳度基于主观感受，存在主观性

### MemOS相关限制 (v3.0)
- MemOS功能依赖MCP服务器可用性
- 首次使用无历史数据，个性化效果逐步提升
- 跨设备同步需要MemOS服务支持
- 数据隐私遵循MemOS服务提供商政策

### 降级策略
当MemOS不可用时，技能会自动降级为v2.1.0无状态模式：
- search_memory失败 → 使用默认值/无状态模式
- add_message失败 → 计划正常生成，仅不保存
- MemOS完全不可用 → v2.1.0无状态模式

---

## 技能集成

### MCP工具依赖 (v3.0)

| MCP工具 | 用途 | 必需性 |
|---------|------|--------|
| search_memory | 读取用户画像、历史计划、学习进度 | 可选 |
| add_message | 保存计划、记录任务完成、保存复盘数据 | 可选 |
| add_feedback | 收集用户对计划质量的反馈 | 可选 |

**降级策略**：当MCP工具不可用时，技能会自动降级为无状态模式（v2.1.0），核心功能不受影响。

### 依赖技能

| 技能 | 用途 |
|------|------|
| obsidian-markdown | 保存学习计划和笔记 |
| docx | 导出Word/PDF格式的计划 |

---

## 使用示例

### 示例1：极简模式

**用户输入**：
```
"我周一上午没课，下午有英语，今天想学高数"
```

**AI处理**：
1. 识别为极简模式
2. 解析空闲时段：周一上午
3. 应用默认考研规则
4. 生成计划

**输出**：
```markdown
# 今日学习计划 - 2025-02-26

## 今日概览
- **空闲时间**: 4小时（上午）
- **今日重点**: 高数

## 学习计划
- [ ] 08:00-10:00 | 高数 | 第五章内容
- [ ] 10:00-12:00 | 高数 | 练习题
```

### 示例2：标准模式 + 疲劳度

**用户输入**：
```
"我12月考试，最近感觉有点累"
```

**AI处理**：
1. 识别为标准模式
2. 计算倒计时阶段
3. 记录疲劳度：有点累 → 0.6
4. 调整计划强度（减少15%）

**输出**：
```markdown
# 今日学习计划 - 2025-02-26

## 今日概览
- **阶段**: 强化期
- **距离考试**: 280天
- **今日精力**: 有点累 ⚠️
- **今日重点**: 维持性学习

## 学习计划（已调整强度）
- [ ] 08:00-10:00 | 数学 | 复习之前的错题
- [ ] 10:00-11:00 | 英语 | 单词复习（轻松）
- [ ] 11:00-12:00 | 休息 | ☕

## 建议
- 今日减少新内容学习
- 建议今晚早睡休息
```

### 示例3：高级模式 + Chronotype

**用户输入**：
```
"我是夜型人，晚上效率高。数学进度落后10h，这周学了18h英语12h专业课"
```

**AI处理**：
1. 识别为高级模式
2. 设置 chronotype = "night_person"
3. 分析进度：数学落后
4. 计算疲劳度：基于学习时长

**输出**：
```markdown
# 本周学习建议

## 进度分析
- ⚠️ 数学落后10小时，需要加强
- 英语学习充足，维持即可
- 专业课正常

## 推荐时段分配（夜型人）
- **上午（08:00-12:00）**: 单词、英语阅读
- **下午（14:00-18:00）**: 专业课
- **晚上（19:00-23:00）**: 数学 ⭐（精力巅峰期）

## 今日计划
- [ ] 08:00-10:00 | 英语 | 单词
- [ ] 14:00-16:00 | 专业课 | 第三章
- [ ] 20:00-23:00 | 数学 | 第五章 ⭐

## 调整建议
- 本周增加数学时间至15h
- 利用晚上高效时段攻克数学
```

### 示例4：任务欠账处理（实战补丁1）

**用户输入**：
```
"昨天的高数练习没做完，今天怎么办？"
```

**AI处理**：
1. 检测到欠账：高数练习（2小时）
2. 判断欠账等级：中等
3. 生成补课选项

**输出**：
```markdown
# ⚠️ 任务欠账处理

## 欠账信息
- 未完成任务：高数第五章练习
- 欠账时长：2小时
- 欠账等级：中等

## 建议处理方案

**方案1：压缩英语时间补高数**（推荐）
- 今日英语阅读时间减半
- 腾出1小时补高数
- 剩余1小时晚上补完

**方案2：延后到周末补**
- 今天按原计划进行
- 周末安排2小时补账

**方案3：今天专注补账**
- 暂停今天所有新内容
- 全天补完欠账+复习

请选择方案（1/2/3），或输入自定义方案：
```

### 示例5：周日复盘（实战补丁2）

**触发**: 自动检测到周日

**AI处理**：
1. 自动切换到周日复盘模式
2. 统计本周完成度
3. 生成错题重做任务
4. 进度对齐检查

**输出**：
```markdown
# 周日复盘 - 第5周 (2025-03-02)

## 本周完成度
| 科目 | 计划时长 | 实际时长 | 完成率 | 欠账 |
|------|----------|----------|--------|------|
| 数学 | 20h | 16h | 80% | ⚠️ 4h |
| 英语 | 12h | 14h | 117% | - |
| 专业课 | 15h | 12h | 80% | ⚠️ 3h |
| 政治 | 5h | 5h | 100% | - |

## 分析
- ✅ 英语超额完成
- ⚠️ 数学、专业课未达标，欠账7小时

## 🔴 错题重做（必做，19:30-21:30）
- [ ] 19:30-20:00 | 数学错题本 | 第五章错题
- [ ] 20:00-20:30 | 英语阅读错题 | 2018年Text1
- [ ] 20:30-21:00 | 专业课错题 | 第三章习题
- [ ] 21:00-21:30 | 政治选择题错题 | 马原错题

## 进度对齐
- [ ] 本周目标：完成高数第五章 ❌ 未完成
- [ ] 欠账决策：数学4h+专业课3h
  - 建议：下周优先补账，暂停新内容进度

## 下周调整
- 数学：减少新题量，专注补账
- 专业课：同步补账
- 英语：维持当前节奏
```

### 示例6：最小块时长限制（实战补丁3）

**场景**: 用户周三只有09:00-10:00空闲（1小时）

**AI处理**：
1. 原计划安排数学
2. 检测到时段只有1小时
3. 检查数学最小时长要求：1.5小时
4. 自动替换为单词

**输出**：
```markdown
# 今日学习计划 - 2025-02-26

## 时段调整提醒
⚠️ 09:00-10:00（1小时）不满足数学最小时长要求（1.5小时）
已自动替换为：单词复习（可碎片化）

## 学习计划
- [ ] 09:00-10:00 | 英语 | 单词复习 ✅已优化
- [ ] 14:00-16:00 | 数学 | 第五章练习 ⭐大块时间
- [ ] 19:00-21:00 | 专业课 | 第三章笔记

## 备注
- 数学需要连续90分钟以上才能进入状态
- 碎片时间用于单词等可分割的任务
```

### 示例7：画像自动刷新（v3.1新增）

**场景**：用户持续使用技能31天，画像已过期

**AI处理**：
1. 检测到画像已31天未更新
2. 触发context_refresh机制
3. 生成画像确认询问

**输出**：
```markdown
# ⚠️ 用户画像确认

你的学习画像已**31天未更新**，为了提供更准确的计划，请确认以下设置是否有变化：

## 当前设置
- **作息类型**: 晨型人
- **疲劳敏感度**: 中
- **科目权重**: 数学1.5 | 英语1.2 | 专业课1.0 | 政治0.6

## 请确认
1. **作息类型有变化吗？**
   - [ ] 保持晨型人
   - [ ] 改为夜型人
   - [ ] 改为正常

2. **科目优先级需要调整吗？**
   - [ ] 保持当前
   - [ ] 需要调整（请说明）

3. **疲劳敏感度有变化吗？**
   - [ ] 高（容易累，需要更多休息）
   - [ ] 中（保持当前）
   - [ ] 低（耐疲劳，可以高强度学习）

请回复你的选择，画像将立即更新。
```

### 示例8：欠账熔断保护（v3.1新增）

**场景**：用户累计欠账已达11小时

**AI处理**：
1. 检测到累计欠账11小时，超过10小时阈值
2. 触发debt_circuit_breaker机制
3. 生成紧急恢复计划

**输出**：
```markdown
# ⚠️ 紧急恢复模式

## 欠账警告
你的累计欠账已达 **11小时**，超过安全阈值（10小时）

**紧急措施**：
- 🔴 暂停所有新内容学习
- 🔴 今日专注补账
- 🔴 欠账降至安全阈值后自动恢复正常模式

## 今日恢复计划（补账专用）
- [ ] 08:00-12:00 | 数学 | 【紧急补账】错题重做 + 未完成练习（4小时）
- [ ] 14:00-17:00 | 专业课 | 【紧急补账】复习笔记（3小时）
- [ ] 19:00-21:00 | 英语 | 【紧急补账】阅读补做（2小时）
- [ ] 21:00-22:00 | 政治 | 【紧急补账】选择题补做（1小时）

## 预计效果
今日补账 **10小时**，剩余欠账 **1小时**（安全范围内）

## 恢复后
明日自动恢复正常学习模式，开始新内容学习
```

### 示例9：心理调节模式（v3.1新增）

**场景**：用户连续3天反馈"很累"

**AI处理**：
1. 从mental_history检测到连续3天疲惫状态
2. 触发心理干预机制
3. 生成心理调节模式计划

**输出**：
```markdown
# 今日学习计划 - 2025-02-26

## 💙 心力提醒
检测到你连续3天反馈疲惫，今日已自动调整为**心理调节模式**：

**调整措施**：
- 学习量减少30%
- 增加休息时间
- 任务以低难度复习为主
- 添加鼓励和正向反馈

## 今日计划（轻量版）

### 上午 (08:00-12:00)
- [ ] 08:00-09:30 | 数学 | 轻松复习（不做新题）
- [ ] 09:30-10:00 | 休息 | 听音乐放松 ☕
- [ ] 10:00-11:30 | 英语 | 单词复习（轻松内容）
- [ ] 11:30-12:00 | 休息 | 散步 🚶

### 下午 (14:00-18:00)
- [ ] 14:00-15:30 | 专业课 | 看笔记复习
- [ ] 15:30-16:00 | 休息 | 午休 🛏️
- [ ] 16:00-17:30 | 政治 | 看视频（轻松学习）
- [ ] 17:30-18:00 | 休息 | 冥想 🧘

### 晚上 (19:00-22:00)
- [ ] 19:00-20:00 | 自由 | 看喜欢的书 📚
- [ ] 20:00-21:00 | 复习 | 快速回顾今日内容
- [ ] 21:00-22:00 | 休息 | 早睡，恢复精力 💤

## 今日鼓励
你已经很努力了！今天给自己放个假，轻松学习，早点休息。明天精力恢复后再继续加油！🎉

## 压力记录
如果今日状态好转，请在晚上反馈："精神恢复了" 或 "还是有点累"
这将帮助系统调整后续计划。
```

### 示例10：计划版本控制（v3.1新增）

**场景**：用户一天内生成3次计划

**AI处理**：
1. 第1次生成：保存为`#daily_plan_current`
2. 第2次生成：将第1版标记为`#daily_plan_history`，保存新版本为`#daily_plan_current`
3. 第3次生成：将第2版标记为`#daily_plan_history`，保存新版本为`#daily_plan_current`

**MemOS存储结果**：
```
#daily_plan_current (1条):
- 2025-02-26 | v1430 | 状态: current

#daily_plan_history (2条):
- 2025-02-26 | v0930 | 状态: superseded | 被替代时间: 14:30
- 2025-02-26 | v1200 | 状态: superseded | 被替代时间: 14:30

#date_2025-02-26 (3条):
- 包含所有版本
```

**好处**：
- search_memory查询今日计划时只返回1条当前版本
- 历史版本归档保存，可追溯修改记录
- 避免一天多次沟通导致记忆过载

### 示例11：MemOS集成学习进度追踪（v3.0新增）

**场景**：用户持续使用技能一周后

**AI处理**：
1. 从MemOS读取用户画像：考试日期12月21日，晨型人
2. 读取本周学习记录：数学16h/20h，英语14h/12h
3. 分析进度：数学欠账4h，英语超额完成
4. 生成本日计划时考虑欠账情况

**输出**：
```markdown
# 今日学习计划 - 2025-02-26

## 学习状态（基于记忆数据）
- **连续学习天数**：7天 🎉
- **本周进度**：数学80% | 英语117% | 专业课85%
- **欠账提醒**：数学欠4小时，今日优先补账

## 今日概览
- **阶段**: 强化期
- **距离考试**: 280天
- **今日重点**: 补高数第五章 + 新内容

## 补课安排（来自记忆分析）
- [ ] 08:00-10:00 | 数学 | 【补课】第五章未完成练习 ⭐
- [ ] 10:00-12:00 | 数学 | 【补课】错题重做

## 今日新内容
- [ ] 14:00-16:00 | 英语 | 阅读理解（维持进度）
- [ ] 19:00-21:00 | 专业课 | 第三章

## 记录说明
今日执行情况将自动保存到学习进度记录中
```

---

## 跨技能调度协议 (v3.2新增)

本技能作为"中央大脑"，负责协调 kaoyan-math、kaoyan-english、kaoyan-electronics 三个技能的联合调度。

### 调度规则表

| 条件 | 目标技能 | 动作 | 上下文 |
|------|----------|------|--------|
| 晨型人 + 高精力 (08:00-12:00) | kaoyan-math, kaoyan-electronics | `high_difficulty_sop` | `{difficulty: "hard", time_block: "3h"}` |
| 疲劳检测 (fatigue > 0.6) | kaoyan-english | `vocabulary_review_mode` | `{mode: "light", duration: "30min"}` |
| 数学欠账 > 3h + 英语有余量 | kaoyan-english | `memory_compression_mode` | `{compress_hours: 1, transfer_to: "math"}` |
| 学习"频率响应" | kaoyan-math | `cross_subject_reminder` | `{topic: "复数运算"}` |
| 周日复盘 | 全部技能 | `weekly_error_analysis` | `{aggregate: true}` |

### 调度信号格式

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

### 发送调度信号函数

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
```

---

## 全局权重计算 (v3.2新增)

### 动态权重算法

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

### 阶段权重表

| 阶段 | 天数 | 数学 | 英语 | 专业课 | 政治 |
|------|------|------|------|--------|------|
| 基础期 | >300 | 1.2 | 1.44 | 0.8 | 0.48 |
| 强化期 | 180-300 | 1.5 | 1.2 | 1.0 | 0.6 |
| 十月强化期 | 90-180 | 1.95 | 0.96 | 1.5 | 1.2 |
| 冲刺期 | 30-90 | 2.25 | 0.72 | 1.8 | 1.2 |
| 极限冲刺 | <30 | 3.0 | 0.48 | 2.0 | 1.2 |

---

## 跨学科协调 (v3.2新增)

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

### 周日全科复盘

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

## 统一用户画像 (v3.2新增)

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

## 统一错误模型 (v3.2新增)

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

## 新增数据文件

| 文件 | 路径 | 说明 |
|------|------|------|
| cross_subject_graph.yaml | `scripts/data/cross_subject_graph.yaml` | 跨学科知识关联数据 |
| dispatch_protocol.md | `scripts/templates/dispatch_protocol.md` | 调度协议文档 |
| weekly_cross_subject_report.md | `scripts/templates/weekly_cross_subject_report.md` | 周报模板 |

---

## 跨技能集成验证 (v3.2新增)

30. ✅ 晨型人高精力时段触发数学高难度SOP
31. ✅ 疲劳检测触发英语轻量复习模式
32. ✅ 数学欠账触发英语记忆压缩
33. ✅ 全局权重计算各阶段正确
34. ✅ 跨学科提醒生成（数学→电子）
35. ✅ 周日复盘生成全科错题报告
36. ✅ MemOS不可用时各技能独立运行（优雅降级）

---

## 版本历史

### v3.2.0 (2025-02-26)
**跨技能联合架构**：
- **跨技能调度协议**：作为"中央大脑"协调math/english/electronics技能
- **全局权重计算**：根据考试倒计时动态调整各科权重
- **跨学科知识关联**：数学↔专业课知识关联提醒
- **统一错误模型**：全科错题记录统一格式
- **周日全科复盘**：跨学科错题分析报告
- **统一用户画像**：全局用户画像格式定义

**新增文件**：
- `scripts/data/cross_subject_graph.yaml`
- `scripts/templates/dispatch_protocol.md`
- `scripts/templates/weekly_cross_subject_report.md`

**向后兼容**：完全保留v3.1.0所有功能，新增功能均为可选增强

### v3.1.0 (2025-02-26)
**鲁棒性增强**：
- **context_refresh机制**：用户画像超过30天未更新时自动触发刷新询问，避免"认知偏差"
- **debt_circuit_breaker熔断**：累计欠账超过10小时时强制暂停新内容，防止"死循环"崩溃
- **upsert with tag**：同一天多次生成计划时自动归档历史版本，解决"并发冗余"问题
- **mental_status追踪**：连续3天疲惫时自动触发心理调节模式，记录崩溃点和压力水平
- **跨设备同步元数据**：在所有模板中添加MemOS同步元数据，支持未来反向同步功能

**新增数据模型字段**：
- user_profile.mental_history：心理状态历史记录
- user_profile.refresh_config：画像刷新配置

**新增函数**：
- check_context_freshness()：检查画像新鲜度
- check_mental_health_intervention()：心理干预检查
- calculate_total_debt_hours()：累计欠账计算
- generate_recovery_plan()：紧急恢复计划生成
- record_mental_status()：心理状态记录

**模板更新**：
- daily_plan.md：添加心力提醒、同步元数据
- weekly_plan.md：添加同步元数据
- report.md：添加用户画像确认部分、同步元数据

**向后兼容**：完全保留v3.0.0所有功能，新增功能均为可选增强

### v3.0.0 (2025-02-26)
**新增功能**：
- 集成MemOS记忆系统，支持用户画像持久化
- 实现学习进度追踪和历史数据读取
- 增强周日复盘功能，自动汇总本周数据
- 添加任务完成情况记录功能
- 支持多用户数据隔离（基于user_id）

**改进**：
- 欠账检测可从MemOS读取昨日计划
- 用户偏好（chronotype、科目权重）可持久化
- 新增降级策略，确保MemOS不可用时核心功能正常

**向后兼容**：完全保留v2.1.0所有功能，新增功能均为可选增强

### v2.1.0
**新增功能**：
- 任务欠账处理（实战补丁1）
- 周日复盘模板（实战补丁2）
- 最小块时长限制（实战补丁3）

### v2.0.0
**新增功能**：
- 三层输入模式（极简/标准/高级）
- 疲劳度混合模型
- Chronotype适配

### v1.0.0
**初始版本**：
- 课表解析
- 空闲时间提取
- 基础计划生成

