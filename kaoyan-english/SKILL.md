---
name: kaoyan-english
description: This skill should be used when the user asks to organize English vocabulary for 考研英语 (Chinese graduate entrance English exam), generate review plans from PDF exports, create spaced repetition schedules, take vocabulary quizzes, handle polysemy (rare word meanings), look up word information, or practice writing output in the context of 考研英语 exam preparation. Now integrated with MemOS for persistent vocabulary tracking and cross-device synchronization.
version: 3.2.0
---

# 考研英语复习技能 (Kaoyan English Review Skill)

## 技能概述

本技能专注于考研英语词汇复习，帮助用户从单词APP（墨墨/百词斩等）导出的PDF中提取词汇，生成基于真题语境的复习材料，提供熟词僻义预警、考研适配的间隔重复复习计划、快速查词、测试功能和写作输出训练。

**v3.1.0新增**: 集成MemOS记忆系统，实现词汇学习状态的持久化存储、跨设备同步和智能追踪。当MemOS不可用时，技能自动降级为v2.0.0无状态模式。

## MemOS集成说明 (v3.1.0)

### 核心原则
- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为无状态模式
- **数据持久化**: 词汇学习记录、用户画像、复习历史均持久化存储
- **跨设备同步**: 支持多设备间词汇学习进度同步

### MemOS功能特性
1. **用户画像追踪**: 记录英语水平、考试信息、学习偏好
2. **词汇卡片持久化**: SM-2算法状态永久保存
3. **复习历史记录**: 完整的复习会话历史
4. **测试结果追踪**: 测试成绩和错误分析
5. **词汇疲劳追踪**: 防止学习倦怠的智能提醒
6. **欠账熔断机制**: 超过200个待复习词时自动触发复习模式
7. **画像刷新机制**: 30天未更新时提示确认学习配置

### 降级行为
当MemOS不可用时：
- ✅ 所有v2.0.0功能正常工作
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用智能追踪（疲劳、欠账熔断等）

---

## 核心功能模块

### 功能1: 词汇整理 + 真题语境文章

**输入**: 用户从单词APP（墨墨/百词斩等）导出的PDF

**处理流程**:
1. 读取PDF内容，提取单词列表
2. 为每个单词获取：音标、词性、释义、词频
3. **检测熟词僻义**：识别考研中的僻义陷阱
4. **优先检索真题语境**：真题语境池 → 外刊同源 → AI生成
5. 将单词串联成真题风格的语境文章
6. 在文章中高亮目标词汇

**输出**:
- Obsidian笔记：每日词汇记录（含僻义预警）
- 真题语境文章：包含目标词汇的连贯文章
- PDF导出：可打印的词汇表（通过docx技能）

### 功能2: 考研适配的复习计划 + 统计追踪

**输入**: 学习天数、考试日期、词汇库、复习历史

**处理流程**:
1. 使用**考研适配的SM-2算法**计算下次复习时间
2. **考虑考试倒计时**：基础期/强化期/冲刺期/极限冲刺期
3. **僻义词自动加权**：缩短复习间隔
4. 根据正确率调整复习间隔
5. 生成每日复习清单
6. 统计每个单词的复习次数、正确率、遗忘率

**输出**:
- 复习计划表：每日待复习单词（按优先级排序）
- 统计dashboard：学习进度可视化
- 阶段提醒：当前复习阶段建议

### 功能3: 快速查词 + 僻义预警

**输入**: 单个单词或短语

**处理流程**:
1. 查询单词基本信息（音标、词性、释义）
2. **检测熟词僻义**：显示僻义预警级别
3. 提供真题例句（含僻义用法）
4. 显示常用搭配
5. 展示同义词/反义词/词族

**输出**: 紧凑的单词卡片（含⚠️僻义预警）

### 功能4: 单词测试功能

**输入**: 测试类型（词义/搭配/拼写）、测试范围

**处理流程**:
1. 根据复习计划选取待测试单词
2. **优先测试僻义词**
3. 生成多种题型（选择题、填空题、拼写题）
4. 执行测试
5. 记录结果并更新统计数据

**输出**:
- 测试题（支持打印或交互式）
- 答案与解析
- 成绩统计
- 僻义词专项报告

### 功能5: 写作输出转化（新增）

**输入**: 目标词汇、写作类型（议论文/图表描述/信件）

**处理流程**:
1. 选择今日复习词汇中的写作必备词
2. 生成**写作替换升级题**
3. 生成**汉译英练习**
4. 生成**词义辨析题**
5. 提供高级词汇替换建议

**输出**:
- 写作替换练习题
- 汉译英翻译题
- 词义辨析选择题
- 写作词汇库

---

## 触发条件

### 触发此技能当：

**词汇整理相关**:
- "整理考研英语单词" + 提供PDF
- "生成考研英语复习文章"
- "从PDF提取单词"
- "墨墨背单词导出"
- "百词斩导出"
- "真题语境文章"
- "外刊风格"

**复习计划相关**:
- "生成考研英语复习计划"
- "间隔重复背单词"
- "考研英语词汇统计"
- "单词复习计划"
- "倒计时复习"

**查词测试相关**:
- "查单词"（在考研语境下）
- "考研英语单词测试"
- "单词quiz"
- "测试词汇量"
- "词义测试"

**僻义预警相关**:
- "熟词僻义"
- "僻义"
- "陷阱词"
- "考研陷阱"
- "一词多义"

**写作输出相关**:
- "写作替换"
- "汉译英"
- "写作词汇"
- "高级词汇替换"
- "作文用词"

**导出相关**:
- "导出单词PDF"
- "打印单词表"

### 不触发此技能当：

- 普通英语学习（无考研语境）
- 简单翻译请求
- 写作批改（非词汇相关）
- 语法讲解
- 英语听力练习

---

## 数据结构

### 单词卡片格式（完整版 v3.1.0）

```yaml
---
# 基础信息
word: "address"
pronunciation: "/əˈdres/"
part_of_speech: "verb/noun"
difficulty: "important"
frequency: 5
first_seen: "2025-01-15"

# MemOS元数据 (v3.1新增)
word_id: "addr_20250115_001"
user_id: "user_12345"
created_at: "2025-01-15T10:30:00Z"
updated_at: "2025-02-20T15:45:00Z"
memos_word_id: "memos_addr_001"
memos_last_sync: "2025-02-20T15:45:00Z"

# 僻义预警
polysemy_alert: true
warning_level: "critical"
exam_frequency: "80%"
rare_meanings:
  - meaning: "处理；解决；着手处理"
    part_of_speech: "vt."
    common_collocations: ["address the problem", "address an issue", "address concerns"]
common_meanings:
  - meaning: "地址；称呼"
    part_of_speech: "n./vt."

# 真题语境
real_exam_contexts:
  - year: 2022
    paper: "英语一"
    section: "完形填空"
    sentence: "The committee failed to **address** the concerns raised by the public."
    sentence_translation: "委员会未能处理公众提出的关切。"
    other_core_words: ["committee", "concern", "raise"]
  - year: 2020
    paper: "英语二"
    section: "阅读理解"
    sentence: "We must **address** the root causes of inequality."
    sentence_translation: "我们必须解决不平等的根本原因。"

# SM-2 + 考研适配
ease_factor: 2.5
interval: 7
review_count: 3
last_review: "2025-02-20"
next_review: "2025-02-25"
exam_date: "2025-12-21"
days_to_exam: 300
current_phase: "基础期"
phase_factor: 1.0
adjusted_interval: 7

# 复习统计
correct_count: 2
incorrect_count: 1
forgetting_rate: 0.33

# 写作应用
writing_usages:
  - pattern: "address the problem/issue"
    formality: "high"
    alternative_for: "solve/deal with"
    example: "The government must address the problem of inequality."

# 标签与分类
tags: ["动词", "高频", "僻义critical", "写作必备"]
exam_years: [2018, 2020, 2022]
---

# address

## 基本信息
**音标**: /əˈdres/
**词性**: vt./n.
**难度**: ⭐⭐⭐⭐⭐

## ⚠️ 僻义预警 [critical]

> [!danger] 陷阱提示
> 此词在考研中 **80%** 考查僻义"处理"，而非常见义"地址"

**考研常考僻义**: vt. 处理；解决；着手处理

### 真题例句
> [!example] 2022年真题 完形填空
> The committee failed to **address** the concerns raised by the public.

> [!example] 2020年真题 阅读理解
> We must **address** the root causes of inequality.

### 常用搭配
- address the problem - 解决问题
- address an issue - 处理议题
- address concerns - 处理关切

## 常见义（对比）
n. 地址； vt. 称呼

⚠️ 易错点：在阅读中遇到此词时，首先考虑"处理"义

## 写作应用

### 高级替换
- **初级**: solve/deal with the problem
- **高级**: **address** the problem

### 写作例句
> The government must **address** the problem of inequality.
> (政府必须处理不平等问题。)

## 词族
- addressee (n.) - 收件人
- addresser (n.) - 发言人

## 学习记录
| 日期 | 结果 | 间隔 | 阶段 |
|------|------|------|------|
| 2025-01-15 | 新学 | - | 基础期 |
| 2025-01-18 | 正确 | 3 | 基础期 |
| 2025-01-25 | 错误（误为"地址"） | 7 | 基础期 |
| 2025-02-20 | 正确 | 7 | 基础期 |

## 我的僻义错误记录 📌

### 陷阱记忆
- [x] 我误以为address只有"地址"的意思
- [x] ❌ 为什么会这样想：这是最常见的日常用法
- [x] ✅ 正确的理解应该是：考研中80%考查"处理"义
- [ ] 📌 提醒：看到address → 第一反应"处理"

### 错误实例
- [ ] 2025-01-25 阅读：把"address the issue"理解为"给问题发地址"
- [x] ✅ 正确翻译：处理这个问题
```

### 真题语境卡片格式（新增）

```markdown
---
context_source: "真题"
source_year: 2023
source_paper: "英语一"
source_type: "阅读理解"
source_section: "Text 3"
source_topic: "社会政策"
difficulty_level: "hard"
cefr_level: "C1"
word_count: 22
core_word_density: "5/22 (23%)"
---

## 真题语境: exemplify

> [!quote] 2023年英语一 阅读理解 Text 3
> The case of California's energy policy **exemplifies** how well-intentioned regulations can have unintended consequences when market dynamics are overlooked.

### 句式分析
- **结构**: 让步状语从句 + how引导宾语从句
- **外刊风格**: 经济学人式论证逻辑（例子→观点→深层分析）
- **词汇密度**: 5个考研核心词 / 22词 (23%)

### 同句其他核心词
- well-intentioned: 善意的
- regulation: 规章制度
- unintended: 意外的
- consequence: 后果
- overlook: 忽视

> ⚠️ **时效提醒**：此语境来自2023年真题，保证时效性和权威性
```

### 文件组织结构（更新后）

```
考研英语/
├── 📑 索引.md                    # MOC
├── 📊 学习统计.md                # 统计dashboard
├── 📅 复习计划.md                # 复习计划
│
├── 📚 重点词汇库/                # 单独文件
│   ├── exemplify.md
│   ├── address.md               # 带僻义预警
│   └── ...
│
├── 📖 一般词汇库/                # 汇总存储
│   ├── A组词汇.md
│   └── ...
│
├── 📝 每日词汇/
│   ├── Day-001-2025-01-15.md
│   └── ...
│
├── 📚 真题语境池/                # 新增
│   ├── 英语一/
│   │   ├── 阅读理解/
│   │   │   ├── 按年份汇总/
│   │   │   └── 按主题分类/
│   │   ├── 完形填空/
│   │   └── 翻译/
│   └── 英语二/
│       └── ...
│
├── 📰 外刊同源库/                # 新增
│   ├── The Economist/
│   └── The Guardian/
│
├── ⚠️ 熟词僻义库/                # 新增
│   ├── critical级别.md
│   ├── warning级别.md
│   └── 完整列表.md
│
├── ✍️ 写作词汇库/                # 新增
│   ├── 议论文必备.md
│   ├── 图表描述.md
│   └── 信件写作.md
│
└── 🧪 测试记录/
    ├── Quiz-Day-005.md
    └── Writing-Output-Day-005.md  # 新增
```

---

## 工作流程

```
[用户提供PDF]
      ↓
[提取单词列表]
      ↓
[检测熟词僻义]
      ↓
[识别重点词汇]
      ↓
┌─────┴─────┐
│           │
[检索真题语境] [生成词汇卡片]
│           │
└─────┬─────┘
      ↓
[生成语境文章]
      ↓
[保存到Obsidian]
      ↓
[生成复习计划]
      ↓
[导出PDF（可选）]
```

---

## 模板

### 模板1: 每日词汇

```markdown
# 每日词汇 - Day {day_number}

**日期**: {date}
**来源**: 墨墨背单词导出
**当前阶段**: {基础期/强化期/冲刺期/极限冲刺期}
**距离考试**: {days}天

---

## 重点词汇

| 单词 | 音标 | 释义 | ⚠️僻义 |
|------|------|------|--------|
| exemplify | /ɪɡˈzemplɪfaɪ/ | 举例说明 | |
| address | /əˈdres/ | 地址/处理 | [critical] |

---

## ⚠️ 僻义预警

### address [critical]
- 常见义：地址
- **考研僻义（80%）**: 处理、解决
- 搭配：address the problem, address an issue

---

## 真题语境文章

{article_with_real_exam_contexts}

---

## 今日复习

### 待复习单词 ({due_count}个)
- [ ] exemplify - 间隔7天
- [ ] address - 间隔3天 [僻义词优先]

### 新学单词 ({new_count}个)
- [ ] resilience
- [ ] paradigm
```

### 模板2: 测试题

```markdown
# 单词测试 - Day {day_number}

## 词义选择
1. exemplify
   - [ ] A. 忽略
   - [ ] B. 举例说明

## ⚠️ 僻义测试
2. address (在考研中最常见的意义是)
   - [ ] A. 地址
   - [ ] B. 处理、解决

## 搭配填空
3. The report _____ the need for reform.
   - [ ] A. exemplifies
   - [ ] B. exemplify

## 答案与统计
- 得分：___ / 100
- 需加强：{weak_words}
- 僻义词错误：{polysemy_errors}
```

### 模板3: 写作输出测试（新增）

```markdown
# 写作输出测试 - Day {day_number}

## 题型1: 写作替换升级

> 原句: Many people think that technology is important.
>
> 任务: 使用今日复习词汇 exemplify 或 contention 改写此句

> [!example] 参考答案
> **分析**：原句使用了基础词汇 many people, think, important。在考研写作中应替换为更正式的表达。
>
> **答案1**: Many scholars **contend** that technology plays a crucial role in modern society.
> **答案2**: The rapid development of AI **exemplifies** the profound impact of technology on our lives.
>
> **评注**：
> - contend 比 think 更正式，常用于学术观点表达
> - exemplify 将"think"转化为"例证"，句式更有深度

---

## 题型2: 观点表达（使用目标词汇）

> 题目: 表达"环境保护重要"这一观点
> 必用词汇: imperative, mitigate, consequence

> [!example] 参考答案
> **分析**：使用三个目标词汇构建复合句。
>
> **答案**: It is **imperative** that we take immediate action to **mitigate** the negative **consequences** of climate change.
>
> **评注**：
> - imperative: 虚拟语气句型，写作加分项
> - mitigate: 替代 reduce/solve，更精准
> - consequence: 替代 result，更正式

---

## 题型3: 词义辨析（为写作选词）

> 题目: 想表达"这个问题很严重"，应选择：
> - [ ] A. This problem is serious.
> - [ ] B. This issue is **critical**.
> - [ ] C. This matter is **grave**.

> [!example] 解析
> **分析**：三个选项语法都正确，但写作水平不同。
>
> **答案**: 选 B 或 C
>
> **评注**：
> - serious (基础词): 中学词汇，写作中避免过度使用 ⚠️
> - critical (考研高级词): 表示"关键的，危急的"，高频考点 ⭐⭐⭐
> - grave (正式词汇): 更正式，表示"严重的，严峻的" ⭐⭐

⚠️ 写作提醒：在议论文中，优先使用 critical 替代 serious
```

### 模板4: 复习计划（更新版）

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

## 核心算法

### 考研适配的SM-2算法

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
    """标准SM-2算法"""
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
            card.interval = 1
        elif card.review_count == 1:
            card.interval = 6
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

### 熟词僻义检测算法（新增）

```python
# 伪代码
def detect_polysemy(word):
    """检测单词是否在考研中有僻义"""

    # 1. 检索考研大纲词表
    outline_entry = search_exam_outline(word)

    # 2. 对比大纲释义与常见释义
    common_meanings = get_common_dictionary_meanings(word)
    exam_meanings = outline_entry.meanings

    # 3. 计算语义重叠度
    overlap = calculate_semantic_overlap(common_meanings, exam_meanings)

    # 4. 判断是否存在僻义
    if overlap < 0.5:  # 重叠度低于50%，存在显著僻义
        return PolysemyAlert(
            word=word,
            alert_type="critical" if overlap < 0.3 else "warning",
            rare_meanings=[m for m in exam_meanings if m not in common_meanings],
            common_meanings=common_meanings,
            exam_frequency=calculate_exam_frequency(word)
        )

    return None
```

### 真题语境检索策略（新增）

```python
# 伪代码
def generate_context_article(word_list, user_preferences):
    """生成语境文章"""
    # word_list: 今日目标词汇
    # user_preferences: 考试类型(英一/英二)、偏好主题等

    contexts = []

    for word in word_list:
        # 1. 优先检索真题语境
        real_exam_context = search_real_exam_pool(
            word,
            exam_type=user_preferences.exam_type,
            recent_years=5  # 优先近5年
        )
        if real_exam_context:
            contexts.append(real_exam_context)
            continue

        # 2. 检索外刊同源语境
        journal_context = search_journal_pool(word)
        if journal_context:
            contexts.append(journal_context)
            continue

        # 3. 最后才用AI生成
        ai_context = generate_ai_context(
            word,
            style="The Economist",  # 明确指定外刊风格
            complexity=calculate_sentence_complexity(word)
        )
        ai_context.metadata.source = "AI生成(模拟)"
        contexts.append(ai_context)

    # 4. 将语境串联成"真题模拟材料"
    article = weave_contexts_into_article(contexts)

    return article
```

---

## MemOS集成核心函数 (v3.1.0新增)

### 函数1: load_user_context_from_memory

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
            query=f"#user_profile {user_input.get('user_id')}",
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

### 函数2: save_word_card_to_memory

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

### 函数3: record_review_session

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

### 函数4: calculate_next_review_with_memory

计算下次复习时间，从MemOS读取历史数据。

```python
def calculate_next_review_with_memory(word, quality, user_context):
    """计算下次复习时间（从MemOS读取历史数据）

    Args:
        word: 目标单词
        quality: 复习质量评分 (0-5)
        user_context: 用户上下文

    Returns:
        dict: 包含interval, next_review, updated_card等信息
    """
    try:
        # 从MemOS读取该词的历史记录
        word_history = search_memory(
            query=f"#word_card_{word} #user_{user_context.get('user_id')}",
            top_k=1
        )

        if word_history:
            card = word_history[0]
            # 使用历史数据计算新的复习间隔
            return calculate_sm2_next_review(card, quality, user_context)
        else:
            # 新词，使用初始参数
            return initialize_new_word_card(word, quality, user_context)
    except Exception as e:
        log_warning(f"Failed to load word history for {word}: {e}")
        return {"interval": 1, "next_review": tomorrow()}
```

### 函数5: check_context_freshness_english (v3.1鲁棒性增强)

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

### 函数6: check_vocabulary_debt_with_memory (v3.1鲁棒性增强)

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

### 函数7: check_vocabulary_fatigue_intervention (v3.1鲁棒性增强)

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

### 主流程整合

```python
def process_vocabulary_learning_v3(user_input, mode="minimal"):
    """词汇学习主流程（含MemOS集成）

    Args:
        user_input: 用户输入
        mode: 处理模式

    Returns:
        dict: 处理结果
    """
    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = safe_load_context(user_input)

    # 1.5 v3.1: 检查画像新鲜度
    profile_refresh = check_context_freshness_english(
        user_context, datetime.now()
    )
    if profile_refresh and profile_refresh.get("needs_refresh"):
        return generate_profile_refresh_question(profile_refresh)

    # 1.6 v3.1: 检查词汇欠账
    debt_check = check_vocabulary_debt_with_memory(user_context)
    if debt_check.get("type") == "vocabulary_emergency":
        return generate_vocabulary_emergency_plan(debt_check)

    # 1.7 v3.1: 检查词汇疲劳
    fatigue_check = check_vocabulary_fatigue_intervention(user_context)
    if fatigue_check and fatigue_check.get("intervention_needed"):
        user_input["relief_mode"] = fatigue_check.get("mode")

    # 2. 处理用户请求（提取单词/查词/生成复习计划）
    result = process_vocabulary_request(user_input, user_context)

    # 3. MemOS: 保存结果 (可降级)
    safe_save_vocabulary_result(result, user_input)

    return result


def safe_load_context(user_input):
    """安全加载用户上下文（含降级）"""
    context = load_user_context_from_memory(user_input)
    if context is None:
        log_info("MemOS unavailable, using default context")
        return create_default_user_context()
    return context


def safe_save_vocabulary_result(result, user_input):
    """安全保存结果（含降级）"""
    if result.get("word_cards"):
        for card in result["word_cards"]:
            save_word_card_to_memory(card, user_input.get("user_id"))

    if result.get("review_session"):
        record_review_session(user_input.get("user_id"), result["review_session"])
```

---

## MemOS数据模型 (v3.1.0新增)

### 用户画像 (User Profile)

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

### 复习记录 (Review Record)

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

### 测试记录 (Test Record)

```yaml
test_record:
  test_id: string
  user_id: string
  test_type: enum (meaning_quiz | collocation_quiz | writing_output)
  date: date
  created_at: datetime

  test_data:
    word_count: int
    questions: array

  results:
    score: float
    polysemy_errors: array
    weak_words: array

  memos_test_id: string
```

---

## MemOS标签系统 (v3.1.0新增)

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#user_profile` | 用户画像 | 每用户1条 |
| `#word_card` | 词汇卡片 | 每词每用户1条 |
| `#word_{word}` | 单词索引 | 可多条（不同用户） |
| `#review_session_current` | 今日当前复习会话 | 每用户每日1条 |
| `#review_session_history` | 历史复习会话归档 | 多条 |
| `#date_{YYYY-MM-DD}` | 日期索引 | 多条 |
| `#test_result` | 测试记录 | 多条 |

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

### 考研适配字段（新增）

| 字段 | 类型 | 说明 |
|------|------|------|
| exam_date | date | 考试日期 |
| current_phase | string | 当前阶段（基础期/强化期/冲刺期/极限冲刺期） |
| phase_factor | float | 阶段系数（0.5-1.0） |
| days_to_exam | int | 距离考试天数 |
| adjusted_interval | int | 调整后的复习间隔 |

### 僻义预警字段（新增）

| 字段 | 类型 | 说明 |
|------|------|------|
| polysemy_alert | bool | 是否存在僻义 |
| warning_level | string | 预警级别（critical/warning/attention） |
| exam_frequency | string | 僻义出现频率 |
| rare_meanings | array | 僻义列表 |
| common_meanings | array | 常见义列表 |

### 真题语境字段（新增）

| 字段 | 类型 | 说明 |
|------|------|------|
| real_exam_contexts | array | 真题例句列表 |
| year | int | 真题年份 |
| paper | string | 英语一/英语二 |
| section | string | 题型（阅读/完形/翻译） |
| sentence | string | 例句 |
| sentence_translation | string | 例句翻译 |

### 写作应用字段（新增）

| 字段 | 类型 | 说明 |
|------|------|------|
| writing_usages | array | 写作用法列表 |
| pattern | string | 搭配模式 |
| formality | string | 正式程度 |
| alternative_for | string | 可替换的初级词汇 |
| example | string | 例句 |

---

## 技能集成

### 依赖技能

| 技能 | 用途 |
|------|------|
| obsidian-markdown | 创建笔记、管理词汇库 |
| docx | 导出Word文档、PDF打印 |

### 调用示例

```markdown
<!-- 使用obsidian-markdown创建单词卡片 -->
使用obsidian-markdown技能创建单词卡片文件

<!-- 使用docx导出词汇表 -->
使用docx技能生成可打印的Word文档
```

---

## 功能详解

### 1. PDF词汇提取

当用户提供PDF文件时：

1. **识别PDF来源**：判断是墨墨、百词斩或其他APP
2. **提取单词列表**：解析PDF文本，提取单词和释义
3. **检测熟词僻义**：对每个单词进行僻义检测
4. **分类词汇**：
   - 重点词汇：考研高频词、真题常考词
   - **僻义词**：标记warning级别
   - 一般词汇：基础词、低频词
5. **生成词汇卡片**：为每个单词创建结构化卡片

### 2. 真题语境文章生成（更新）

将目标词汇串联成文章：

1. **分析词汇主题**：识别词汇的常见领域（科技、社会、经济等）
2. **优先检索真题语境**：
   - 真题语境池（近20年）
   - 外刊同源（经济学人、卫报等）
   - AI生成（仅作为补充）
3. **构建文章框架**：确定文章主题和结构
4. **嵌入目标词汇**：在文章中自然地使用目标词汇
5. **高亮标记**：使用粗体或颜色高亮目标词汇

**文章模板**：
```markdown
# {主题}真题语境文章

## 原文
{article_content_with_real_exam_contexts}

## 语境来源
- 真题来源：{year}年{paper} {section}
- 外刊来源：{journal_name}
- 句式分析：{sentence_structure}

## 高亮词汇
- {word1}: {context} {polysemy_warning}
- {word2}: {context}
```

### 3. 考研适配的复习计划（更新）

基于考研适配的SM-2算法：

1. **初始化**：新单词设置初始参数
2. **计算阶段**：根据考试日期确定当前阶段
3. **应用权重**：根据阶段和单词类型调整间隔
4. **每日计算**：检查哪些单词需要复习
5. **生成清单**：按优先级排序（僻义词 > 高频词 > 普通词）
6. **更新统计**：记录复习结果，更新参数

**分阶段策略**：

```markdown
## 阶段1: 基础期（距离考试 > 100天）
- 策略: 标准SM-2，注重新词积累
- 每日新词: 50个
- 复习比例: 新词7 : 复习3

## 阶段2: 强化期（距离考试 30-100天）
- 策略: 启用熟词僻义预警，强化真题语境
- 每日新词: 30个（减少）
- 复习比例: 新词4 : 复习6
- 特殊处理: 僻义词自动加入每日复习

## 阶段3: 冲刺期（距离考试 7-30天）
- 策略: 缩短高频词间隔20%
- 每日新词: 10个（极少）
- 复习比例: 新词1 : 复习9
- 重点: 真题语境文章 + 僻义词

## 阶段4: 极限冲刺期（距离考试 < 7天）
- 策略: 强制缩短所有间隔，高频词最多3天一复习
- 每日新词: 0个（停止）
- 复习比例: 100%复习
- 重点: 僻义词 + 高频词 + 写作词汇
```

### 4. 快速查词（更新）

查询单个单词：

1. **搜索本地词汇库**：检查是否已记录该单词
2. **检测熟词僻义**：显示僻义预警
3. **获取单词信息**：音标、词性、释义、例句
4. **显示关联信息**：同义词、反义词、词族、搭配
5. **生成紧凑卡片**：适合快速浏览

### 5. 单词测试（更新）

生成测试题：

1. **选择测试范围**：今日复习词、僻义词、特定难度词、随机词
2. **优先测试僻义词**
3. **生成题型**：
   - 词义选择（四选一，含僻义选项）
   - 搭配填空
   - 拼写测试
4. **执行测试**：交互式或打印
5. **统计结果**：得分、错词、僻义词错误、薄弱项

### 6. 写作输出转化（新增）

生成写作训练题：

1. **选择目标词汇**：从今日复习词中选择写作必备词
2. **生成题型**：
   - 写作替换升级：用高级词替换简单表达
   - 汉译英练习：给定中文，用目标词翻译
   - 词义辨析：在写作语境中选择最合适的词
3. **提供替换建议**：初级词汇 → 高级词汇对照表
4. **执行测试**：交互式或打印
5. **统计结果**：得分、薄弱词汇、提升建议

---

## 熟词僻义库（新增）

### Critical级别（高频陷阱）

| 单词 | 常见义 | **考研僻义** | 出现频率 |
|------|--------|-------------|----------|
| address | 地址 | **vt. 处理，解决** | 80% |
| school | 学校 | **n. 流派，学派** | 70% |
| novel | 新颖的 | **n. 长篇小说** | 65% |
| fine | 好的 | **n./v. 罚款** | 60% |
| reason | 原因 | **v. 推理，推论** | 55% |
| discipline | 纪律 | **n. 学科** | 50% |
| consume | 消费 | **vt. 毁灭，烧毁** | 40% |
| draft | 草稿 | **n. 征兵** | 35% |
| compound | 复合的 | **v. 加剧，恶化** | 30% |

### Warning级别（中等陷阱）

| 单词 | 常见义 | 考研僻义 | 出现频率 |
|------|--------|----------|----------|
| spring | 春天 | **v. 突然出现，涌现** | 40% |
| table | 桌子 | **v. 搁置，暂缓讨论** | 35% |
| book | 书 | **v. 预订** | 30% |

---

## 写作词汇库（新增）

### 议论文必备

#### 表达观点
- contend (v. 声称，主张) - Many scholars contend that...
- assert (v. 断言) - Critics assert that...
- exemplify (v. 例证) - This case exemplifies...

#### 表示程度
- imperative (adj. 必要的) - It is imperative that...
- profound (adj. 深远的) - have profound impact on...
- negligible (adj. 可忽略的) - be negligible compared to...

#### 表示因果关系
- consequence (n. 结果) - as a consequence of...
- correlation (n. 相关性) - there is a correlation between...
- attributable (adj. 可归因的) - be attributable to...

#### 表示转折
- conversely (adv. 相反地) - Conversely, some argue that...
- notwithstanding (prep. 尽管) - Notwithstanding these challenges...

### 图表描述

#### 数据变化
- **上升**: soar, surge, climb, ascend
- **下降**: plummet, plunge, decline, descend
- **波动**: fluctuate, oscillate, vary
- **稳定**: stabilize, level off, remain constant

#### 程度描述
- substantial, significant, considerable, moderate, marginal

### 信件写作

#### 开头
- I am writing to inquire about...
- I was dismayed to learn that...
- I would like to express my appreciation for...

#### 结尾
- I look forward to your prompt response.
- Your assistance in this matter is greatly appreciated.
- Please let me know if you require any further information.

---

## 记忆压缩模式 (v3.2.0新增)

当kaoyan-plan检测到其他科目欠账时，可触发英语记忆压缩模式，将英语学习时间压缩转移给其他科目。

### 压缩策略

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

### 压缩模式下的调整

| 功能 | 正常模式 | 压缩模式 |
|------|----------|----------|
| 每日新词 | 50个 | 20个 |
| 复习重点 | 均衡 | 仅僻义词+高频词 |
| 语境文章 | 生成 | 跳过 |
| 测试 | 完整 | 仅快速测试 |
| 写作训练 | 包含 | 跳过 |

---

## 调度信号处理 (v3.2.0新增)

### 检查调度信号

从kaoyan-plan接收调度信号并执行相应动作。

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

### 支持的调度动作

| 动作名 | 说明 | 上下文参数 |
|--------|------|------------|
| `vocabulary_review_mode` | 轻量词汇复习 | `{mode, duration}` |
| `memory_compression_mode` | 记忆压缩模式 | `{compress_hours, transfer_to}` |
| `polysemy_focus` | 僻义词专项 | `{focus, count}` |
| `weekly_error_analysis` | 周日错误分析 | `{aggregate}` |

---

## 动态权重响应 (v3.2.0新增)

根据考试倒计时阶段自动调整词汇学习策略。

### 阶段词汇目标

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

### 阶段策略表

| 阶段 | 天数 | 每日新词 | 复习比例 | 僻义权重 |
|------|------|----------|----------|----------|
| 基础期 | >300 | 50 | 30% | 1.0x |
| 强化期 | 180-300 | 40 | 50% | 1.2x |
| 十月强化期 | 90-180 | 30 | 60% | 1.5x |
| 冲刺期 | 30-90 | 10 | 90% | 2.0x |
| 极限冲刺 | <30 | 0 | 100% | 2.0x |

---

## 统一错误模型集成 (v3.2.0新增)

### 学科标签

所有错误记录添加学科标签以支持跨技能聚合。

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

### 英语专用错误类型

| 错误类型 | 说明 | 标签 |
|----------|------|------|
| `polysemy_error` | 多义词错误 | `#polysemy_critical` |
| `collocation_error` | 搭配错误 | `#collocation` |
| `condition_omission` | 条件遗漏 | `#condition` |
| `concept_confusion` | 概念混淆 | `#concept` |

---

## 验证标准

1. 能够从用户提供的PDF中提取单词列表
2. 能够识别并分类重点词汇、僻义词和一般词汇
3. **能够优先使用真题语境而非AI生成文章**
4. **能够正确检测和预警熟词僻义**
5. **能够根据考试倒计时调整复习间隔**
6. **能够生成写作输出测试题**
7. 能够基于SM-2算法生成复习计划
8. 能够统计学习进度并生成dashboard
9. 能够快速查询单词信息（含僻义预警）
10. 能够生成并执行单词测试
11. **能够生成高级词汇替换建议**
12. 触发条件准确无误
13. **警告格式与kaoyan-math保持一致（⚠️图标）**
14. **例题格式与kaoyan-math保持一致（[!example] callout）**

### 跨技能集成验证 (v3.2.0新增)
15. ✅ 记忆压缩模式激活
16. ✅ 调度信号接收和处理
17. ✅ 疲劳轻量模式响应
18. ✅ 阶段词汇目标调整
19. ✅ 统一错误模型学科标签

---

## 限制条件

- 需要用户提供PDF文件或单词列表
- 查词功能依赖本地词汇库或在线词典
- 测试功能需要已建立的词汇记录
- 复习计划需要历史复习数据
- **写作输出需要词汇库达到一定规模**

---

## 使用建议

### 初期使用（基础期）
1. 先导入现有词汇（从PDF或手动输入）
2. 设置合理的每日新词数量（建议50词）
3. 坚持每日复习
4. **关注熟词僻义预警**

### 中期使用（强化期）
1. 定期查看统计dashboard
2. 关注高遗忘率词汇
3. **重点复习僻义词**
4. **使用真题语境文章进行阅读训练**
5. **开始写作替换练习（每周1-2次）**

### 后期使用（冲刺期）
1. 使用测试功能检验掌握程度
2. **重点突破僻义词和高频词**
3. **加强写作输出训练**
4. 导出词汇表进行离线复习
5. 根据复习数据调整学习策略

---

## 技能调用提示

### 词汇整理时
1. 确认PDF来源和格式
2. 设置词汇分类标准
3. **启用熟词僻义检测**
4. 选择保存路径

### 生成复习计划时
1. 确认学习天数和考试日期
2. 检查现有词汇库
3. **计算当前复习阶段**
4. 设置复习时间偏好

### 执行测试时
1. 选择测试类型和范围
2. **优先测试僻义词**
3. 设置题目数量
4. 确认结果保存方式

### 写作训练时
1. 选择写作类型（议论文/图表描述/信件）
2. **选择今日复习词中的写作必备词**
3. **设置替换练习数量**
4. 查看高级词汇替换建议
