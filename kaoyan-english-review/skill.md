---
name: kaoyan-english-review
description: This skill handles review planning and progress tracking for 考研英语 (Chinese graduate entrance English exam) vocabulary learning. Use it when users want to generate spaced repetition schedules based on the SM-2 algorithm, track vocabulary statistics, get daily review lists, or analyze learning progress with phase-based strategies.
version: 1.1.0
---

# 考研英语复习计划

> 代码实现与模板：SM-2 算法逻辑见 [code.md](code.md)，复习计划输出模板见 [templates/review-plan-template.md](templates/review-plan-template.md)

## 技能概述

基于考研适配的 SM-2 算法，按考试倒计时自动调整复习间隔，提供分阶段复习策略、每日复习清单和统计 dashboard。

核心特色：僻义词自动加权、考试倒计时感知、与 kaoyan-english-core 集成。

---

## 触发条件

**触发**：「生成考研英语复习计划」「间隔重复背单词」「今日复习」「词汇统计」「复习计划」

**不触发**：词汇整理/查词 → `kaoyan-english-vocab`；单词测试 → `kaoyan-english-quiz`；写作训练 → `kaoyan-english-writing`；配置/欠账 → `kaoyan-english-core`

---

## 考研适配 SM-2 算法

基于标准 SuperMemo SM-2 + 考试倒计时权重调整。详细实现见 [code.md](code.md)。

核心规则：
- 标准间隔：第1次1天 → 第2次3天 → 第3次7天 → 后续 `interval × ease_factor`
- quality 0-5 评分（5=完美, 0=完全忘记）
- 倒计时阶段权重：>100天标准、30-100天强化（高频词×0.85/僻义词×0.8）、≤30天冲刺（整体×0.5~0.7）

---

## 分阶段复习策略

| 阶段 | 距离考试 | 新词/天 | 新词:复习 | 僻义权重 | 重点 |
|------|----------|---------|-----------|----------|------|
| 基础期 | >100天 | 50 | 7:3 | 1.0x | 标准SM-2 |
| 强化期 | 30-100天 | 30 | 4:6 | 1.5x | 僻义词+真题语境 |
| 冲刺期 | 7-30天 | 10 | 1:9 | 2.0x | 真题语境+僻义词 |
| 极限冲刺 | <7天 | 0 | 0:10 | 2.0x | 僻义词+高频+写作词 |

---

## 输出格式

按 [templates/review-plan-template.md](templates/review-plan-template.md) 生成，包含：当前阶段、今日复习清单（按优先级排序：🔴僻义词/高频词 → 🟡普通 → 新学）、复习统计、阶段建议。

---

## 工作流程

```
加载 MemOS 画像 → 检查欠账 → 计算当前阶段 → 获取卡片列表 → 计算待复习 → 优先级排序 → 生成清单 → 保存 MemOS
```

---

## SM-2 数据字段

| 字段 | 类型 | 说明 |
|------|------|------|
| ease_factor | float | 记忆难度因子，默认2.5 |
| interval | int | 复习间隔（天） |
| review_count | int | 复习次数 |
| next_review | date | 下次复习日期 |
| forgetting_rate | float | 遗忘率 |

考研适配字段：`current_phase`（阶段）、`phase_factor`（阶段系数 0.5-1.0）、`days_to_exam`（距离考试天数）、`adjusted_interval`（调整后间隔）

---

## 技能集成

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 读取/保存用户数据，共享 Day 编号函数 |
| kaoyan-english-vocab | 获取单词信息 |
| obsidian-markdown | 创建复习计划笔记 |

---

## Day编号计算

使用 `kaoyan-english-core` 的共享函数（详见 core/code.md §8.1）：

```python
from kaoyan_english_core import get_validated_day_number, generate_day_filenames
day_number = get_validated_day_number("2026-03-16")  # 返回: 17
```

起始映射：2026-02-28 = Day 001。

---

*创建日期: 2026-03-10*
*版本: 1.1.0 (算法伪代码→code.md、模板→templates/, 2026-07-12)*
