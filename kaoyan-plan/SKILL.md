---
name: kaoyan-plan
description: This skill should be used when the user asks to generate study plans for 考研 (Chinese graduate entrance exam), parse course schedules, create daily/weekly study schedules, or optimize study time allocation. Supports three input modes (minimal/standard/advanced), adapts to individual chronotypes (morning person/night owl), handles task debt from missed plans, enforces Sunday review, and respects minimum block duration requirements for different subjects.
version: 2.1.0
---

# 考研规划Skill (Kaoyan Plan Generation Skill)

## 技能概述

本技能专注于考研学习计划生成，支持从课表中提取空闲时间，智能分配学习任务。采用**渐进式输入模式**（极简→标准→高级），适应不同使用场景。

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

**欠账等级**:

| 欠账时长 | 等级 | 处理策略 |
|----------|------|----------|
| < 1小时 | 轻微 | 今日碎片时间补完 |
| 1-3小时 | 中等 | 压缩今日低优先任务补课 |
| > 3小时 | 严重 | 启动"补课日"，暂停新内容 |

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

### 主规划算法（v2.1 实战版）

```python
def generate_daily_plan(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含实战补丁）

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

---

## 限制条件

- OCR识别依赖图片清晰度
- 课表格式需要一定的规范性
- 极简模式使用默认值，个性化程度较低
- 疲劳度基于主观感受，存在主观性

---

## 技能集成

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
