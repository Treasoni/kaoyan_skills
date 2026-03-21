---
name: kaoyan-english-review
description: This skill handles review planning and progress tracking for 考研英语 (Chinese graduate entrance English exam) vocabulary learning. Use it when users want to generate spaced repetition schedules based on the SM-2 algorithm, track vocabulary statistics, get daily review lists, or analyze learning progress with phase-based strategies.
version: 1.0.0
---

# 考研英语复习计划技能 (Kaoyan English Review)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能专注于考研英语词汇的复习计划和进度追踪，帮助用户：
1. **考研适配的SM-2算法**：根据考试倒计时自动调整复习间隔
2. **分阶段复习策略**：基础期/强化期/冲刺期/极限冲刺期
3. **每日复习清单**：按优先级排序（僻义词 > 高频词 > 普通词）
4. **统计dashboard**：学习进度可视化
5. **复习历史追踪**：记录每次复习的结果

**核心特色**：
- 僻义词自动加权（缩短复习间隔）
- 考试倒计时感知（考前自动调整策略）
- 与kaoyan-english-core集成，支持MemOS持久化

---

## 触发条件

### 触发此技能当：

**复习计划相关**：
- "生成考研英语复习计划"
- "间隔重复背单词"
- "考研英语词汇统计"
- "单词复习计划"
- "倒计时复习"
- "今日复习"
- "复习清单"
- "学习进度"

**统计相关**：
- "词汇统计"
- "学习dashboard"
- "进度分析"
- "掌握情况"
- "复习统计"

### 不触发此技能当：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 单词测试 → 使用 kaoyan-english-quiz
- 写作训练 → 使用 kaoyan-english-writing
- MemOS配置/欠账检查 → 使用 kaoyan-english-core

---

## 考研适配的SM-2算法

```python
# 伪代码
def calculate_next_review_kaoyan(card, quality, exam_date):
    """考研适配的SM-2算法"""

    days_to_exam = (exam_date - today).days
    standard_interval = calculate_sm2_interval(card, quality)

    # 倒计时权重计算
    if days_to_exam > 100:
        # 正常阶段：标准SM-2
        current_phase = "基础期"
        phase_factor = 1.0
        return standard_interval

    elif days_to_exam > 30:
        # 强化阶段（考前30-100天）：
        # - 高频词：缩短20%间隔
        # - 僻义词：缩短30%间隔
        current_phase = "强化期"
        if card.frequency >= 5 or card.polysemy_alert:
            phase_factor = 0.8 if card.polysemy_alert else 0.85
            return standard_interval * phase_factor
        return standard_interval

    else:
        # 冲刺阶段（考前30天内）：
        # - 所有词间隔强制缩短
        # - 高频词/僻义词：最高优先级
        current_phase = "冲刺期" if days_to_exam > 7 else "极限冲刺期"
        if card.frequency >= 5 or card.polysemy_alert:
            phase_factor = 0.5
            return min(standard_interval * phase_factor, 3)  # 最多3天
        else:
            phase_factor = 0.7
            return min(standard_interval * phase_factor, 7)  # 最多7天

    # 更新卡片数据
    card.current_phase = current_phase
    card.phase_factor = phase_factor
    card.adjusted_interval = adjusted_interval
    card.days_to_exam = days_to_exam

    return card


def calculate_sm2_interval(card, quality):
    """标准SM-2算法

    标准SM-2间隔规则：
        - 第1次复习：学习后1天
        - 第2次复习：第1次复习后3天（累计4天）
        - 第3次复习：第2次复习后7天（累计11天）
        - 后续复习：interval × ease_factor
    """
    # quality: 0-5评分
    # 5: 完美记忆
    # 4: 正确但有犹豫
    # 3: 回忆困难但正确
    # 2: 错误但有印象
    # 1: 错误无印象
    # 0: 完全忘记

    if quality >= 3:
        # 回答正确，增加间隔
        if card.review_count == 0:
            card.interval = 1  # 第1次：1天
        elif card.review_count == 1:
            card.interval = 3  # 第2次：3天（累计4天）
        elif card.review_count == 2:
            card.interval = 7  # 第3次：7天（累计11天）
        else:
            card.interval = card.interval * card.ease_factor

        # 更新ease factor
        card.ease_factor = max(1.3, card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    else:
        # 回答错误，重新开始
        card.review_count = 0
        card.interval = 1

    card.review_count += 1
    return card.interval
```

---

## 分阶段复习策略

### 阶段1: 基础期（距离考试 > 100天）

- **策略**: 标准SM-2，注重新词积累
- **每日新词**: 50个
- **复习比例**: 新词7 : 复习3
- **僻义权重**: 1.0x

### 阶段2: 强化期（距离考试 30-100天）

- **策略**: 启用熟词僻义预警，强化真题语境
- **每日新词**: 30个（减少）
- **复习比例**: 新词4 : 复习6
- **僻义权重**: 1.5x
- **特殊处理**: 僻义词自动加入每日复习

### 阶段3: 冲刺期（距离考试 7-30天）

- **策略**: 缩短高频词间隔20%
- **每日新词**: 10个（极少）
- **复习比例**: 新词1 : 复习9
- **僻义权重**: 2.0x
- **重点**: 真题语境文章 + 僻义词

### 阶段4: 极限冲刺期（距离考试 < 7天）

- **策略**: 强制缩短所有间隔，高频词最多3天一复习
- **每日新词**: 0个（停止）
- **复习比例**: 100%复习
- **僻义权重**: 2.0x
- **重点**: 僻义词 + 高频词 + 写作词汇

---

## 模板

### 复习计划模板

```markdown
# 考研英语复习计划

## 复习算法
基于 SuperMemo SM-2 间隔重复算法 + 考研倒计时权重

## 当前阶段
**阶段**: {强化期}
**距离考试**: {90}天
**策略**: 僻义词间隔缩短20%，高频词缩短15%

## 今日复习 (2025-02-25)

### 🔴 高优先级（僻义词+高频词）
- [ ] address - 间隔3天 [僻义词critical]
- [ ] school - 间隔5天 [僻义词warning]
- [ ] exemplify - 间隔7天 [高频]

### 🟡 普通复习
- [ ] ubiquitous - 间隔7天
- [ ] mitigate - 间隔10天

### 新学单词 ({new_count}个)
- [ ] resilience
- [ ] paradigm

## 复习统计
- 总词汇量: 2500
- 已掌握: 1800 (72%)
- 复习中: 500 (20%)
- 新学: 200 (8%)
- 僻义词待加强: 45

## 阶段建议
当前距离考试90天，进入强化期：
- 每日新词量：30个（减少）
- 重点关注：僻义词 + 真题语境
- 写作训练：每周2次写作替换练习
```

---

## 工作流程

```
[从MemOS加载用户上下文]
      ↓
[检查画像新鲜度]
      ↓
[检查词汇欠账]
      ↓
[计算当前阶段]
      ↓
[获取所有词汇卡片]
      ↓
[计算今日待复习词]
      ↓
[按优先级排序]
      ↓
[生成复习清单]
      ↓
[保存到MemOS]
```

---

## 数据字段说明

### SM-2基础字段

| 字段 | 类型 | 说明 |
|------|------|------|
| ease_factor | float | 记忆难度因子，默认2.5 |
| interval | int | 复习间隔（天） |
| review_count | int | 复习次数 |
| next_review | date | 下次复习日期 |
| correct_count | int | 正确次数 |
| incorrect_count | int | 错误次数 |
| forgetting_rate | float | 遗忘率 = incorrect_count / review_count |

### 考研适配字段

| 字段 | 类型 | 说明 |
|------|------|------|
| exam_date | date | 考试日期 |
| current_phase | string | 当前阶段（基础期/强化期/冲刺期/极限冲刺期） |
| phase_factor | float | 阶段系数（0.5-1.0） |
| days_to_exam | int | 距离考试天数 |
| adjusted_interval | int | 调整后的复习间隔 |

---

## 验证标准

1. ✅ 能够基于SM-2算法生成复习计划
2. ✅ 能够根据考试倒计时调整复习间隔
3. ✅ 能够识别并优先处理僻义词
4. ✅ 能够生成每日复习清单（按优先级排序）
5. ✅ 能够统计学习进度
6. ✅ 能够记录复习结果到MemOS
7. ✅ 分阶段策略正确执行

---

## 限制条件

- 需要已建立的词汇库
- 需要用户提供考试日期
- MemOS不可用时降级为本地模式

---

## 技能集成

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 读取/保存用户数据 |
| kaoyan-english-vocab | 获取单词信息 |
| obsidian-markdown | 创建复习计划笔记 |

---

## Day编号计算规则 ⚠️

本技能使用 `kaoyan-english-core` 提供的共享Day编号计算函数。

### 推荐做法

```python
# 使用共享函数获取验证后的Day编号
from kaoyan_english_core import get_validated_day_number, generate_day_filenames

# 获取Day编号（双重验证）
day_number = get_validated_day_number("2026-03-16")  # 返回：17

# 生成文件名
filenames = generate_day_filenames("2026-03-16", day_number)
```

### 函数说明

| 函数 | 说明 | 位置 |
|------|------|------|
| `get_validated_day_number()` | 双重验证获取Day编号 | core/code.md §8.1 |
| `generate_day_filenames()` | 生成四类文件名 | core/code.md §8.1 |

### Day编号对应关系

| 日期 | Day编号 |
|------|---------|
| 2026-02-28 | Day 001 |
| 2026-03-01 | Day 002 |
| 2026-03-15 | Day 016 |
| 2026-03-16 | Day 017 |
| 2026-03-17 | Day 018 |

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
*最后更新: 2026-03-16（添加Day编号计算规则）*
