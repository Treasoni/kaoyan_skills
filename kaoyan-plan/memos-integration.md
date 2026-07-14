# kaoyan-plan MemOS集成规范

本文档包含 kaoyan-plan 技能的 MemOS 记忆系统集成规范。

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 目录

1. [核心原则](#核心原则)
2. [MCP工具调用策略](#mcp工具调用策略)
3. [v3.1标签系统](#v31标签系统)
4. [数据模型](#数据模型)
5. [降级策略](#降级策略)
6. [MemOS集成验证](#memos集成验证)

---

## 核心原则

- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为无状态模式
- **数据持久化**: 计划记录、用户画像、学习进度均持久化存储

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

## MCP工具调用策略

### search_memory - 读取时机

1. **计划生成前**：获取用户画像和历史进度
2. **欠账检测**：读取昨日计划详情
3. **周日复盘**：读取本周所有学习记录
4. **画像新鲜度检查** (v3.1)：查询画像更新时间
5. **心理状态检查** (v3.1)：查询近期mental_history

### add_message - 写入时机

1. **计划生成后**：保存计划到记忆（v3.1使用upsert逻辑）
2. **任务完成确认**：记录实际执行情况
3. **周日复盘完成**：保存复盘数据
4. **用户画像更新**：保存用户配置变更
5. **心理状态记录** (v3.1)：保存每日mental_status

### add_feedback - 写入时机

1. **计划质量反馈**：用户对生成计划的评价
2. **技能使用体验**：整体使用满意度

---

## v3.1标签系统

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

---

## 数据模型

### 用户画像 (User Profile)

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

### 学习进度记录 (Learning Progress)

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

### 复盘数据 (Review Data)

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

## 降级策略

当MemOS不可用时，技能会自动降级为v2.1.0无状态模式：

- search_memory失败 → 使用默认值/无状态模式
- add_message失败 → 计划正常生成，仅不保存
- MemOS完全不可用 → v2.1.0无状态模式

**降级行为**：
- ✅ 基础功能正常工作
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用智能追踪（疲劳、欠账熔断等）

---

## MemOS集成验证

### 基础验证 (v3.0)

14. ✅ 能从MemOS读取用户画像和历史数据
15. ✅ 计划生成后能保存到MemOS
16. ✅ 任务完成情况能记录到MemOS
17. ✅ 周日复盘能汇总本周MemOS数据
18. ✅ MemOS不可用时能优雅降级为v2.1.0模式
19. ✅ 多用户数据隔离正确（基于user_id）
20. ✅ 100天历史数据下响应时间 < 5秒

### 增强验证 (v3.1)

21. ✅ 画像超过30天未更新时自动触发刷新询问
22. ✅ 累计欠账超过10小时时触发熔断模式
23. ✅ 同一天多次生成计划时使用upsert逻辑（旧版本归档为历史）
24. ✅ 连续3天疲惫反馈时触发心理调节模式
25. ✅ 生成的计划包含跨设备同步元数据
26. ✅ 心理状态记录能正确保存到MemOS
27. ✅ 用户画像更新后次日计划使用新配置

---

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
