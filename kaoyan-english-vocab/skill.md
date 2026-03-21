---
name: kaoyan-english-vocab
description: This skill handles vocabulary organization and word lookup for 考研英语 (Chinese graduate entrance English exam). Use it when users want to extract vocabulary from PDF exports (墨墨/百词斩), generate real exam context articles, detect polysemy (rare word meanings), look up word information, or organize vocabulary cards.
version: 1.0.0
---

# 考研英语词汇整理技能 (Kaoyan English Vocab)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能专注于考研英语词汇的整理和查询，帮助用户：
1. **PDF词汇提取**：从单词APP（墨墨/百词斩等）导出的PDF中提取词汇
2. **词汇分类**：自动识别重点词汇、僻义词、一般词汇
3. **熟词僻义检测**：识别考研中的僻义陷阱并预警
4. **快速查词**：查询单词信息（含僻义预警）
5. **真题语境文章生成**：将目标词汇串联成真题风格的语境文章

**核心特色**：
- ⚠️ 僻义预警系统（Critical/Warning级别）
- 优先使用真题语境，非AI生成文章
- 自动生成结构化词汇卡片

---

## 触发条件

### 触发此技能当：

**词汇整理相关**：
- "整理考研英语单词" + 提供PDF/单词表
- "生成考研英语复习文章"
- "从PDF提取单词"
- "墨墨背单词导出"
- "百词斩导出"
- "真题语境文章"
- "外刊风格"
- "生成词汇表"
- "处理单词表" + 提供单词表文件
- "格式化单词"
- "分类单词"

**查词相关**：
- "查单词"（在考研语境下）
- "查询单词"
- "word lookup" + 单词
- 单词 + "什么意思"（考研语境）

**僻义相关**：
- "熟词僻义"
- "僻义词"
- "陷阱词"
- "考研陷阱"
- "一词多义"

### 不触发此技能当：
- 生成复习计划 → 使用 kaoyan-english-review
- 单词测试 → 使用 kaoyan-english-quiz
- 写作训练 → 使用 kaoyan-english-writing

---

## 核心功能

### ⚠️ 执行顺序（重要！）

当用户提供单词表时，**必须按以下顺序执行**：

```
[用户提供单词表]
      ↓
[步骤0: 整理和格式化原始单词表] ← 必须首先执行！
      ↓
[步骤1: 检测熟词僻义]
      ↓
[步骤2: 生成四类学习笔记]
```

### 功能0: 整理和格式化单词表（必须步骤）⚠️

**输入**: 用户提供的原始单词表（可能是从PDF/图片转换，格式混乱）

**处理流程**:
1. **格式统一化**：
   - 统一标题格式：`#### 单词名 ⭐⭐⭐`（含考研频率标记）
   - 清理多余符号：省略号统一为 `...`，去除多余空格
   - 修复截断的释义
   - 统一分隔符为 `---`

2. **添加记忆方法（必须！）**：
   - 🧠 **词根词缀法**：如 `conscience = con-(加强) + sci(知道) + -ence`
   - **联想记忆法**：如 `bleak → break → 破碎的希望`
   - **谐音记忆法**：如 `consult = "看搜" → 看了再搜`
   - 使用 `> 🧠 **记忆方法**` callout 格式

3. **补充词组搭配**：
   - 每个单词至少提供2-3个常用搭配
   - 使用表格格式：`| 词组搭配 | 释义 |`

4. **按词族分类**：
   - 将同源词归类（如 general 族：general, generalize, gene）
   - 每个词族使用独立的标题块

5. **按考研重点分类**：
   - ⭐⭐⭐ 高频词（必考词汇）
   - ⭐⭐ 中频词（常考词汇）
   - ⭐ 低频词（生僻词汇）

6. **僻义预警标记**：
   - 🔴 Critical：考研高频僻义陷阱
   - 🟡 Warning：中等频率僻义
   - 使用 `> ⚠️ **僻义预警**` 标注

7. **写作词汇标注**：
   - 标注可替代的简单词汇（如 `conspicuous` → 替代 `obvious`）

8. **更新原始文件**：直接覆盖用户的原始单词表文件

**输出格式示例**:
```markdown
#### conscience ⭐⭐⭐
**n.** 良心，良知；愧疚

| 词组搭配 | 释义 |
|---------|------|
| a clear conscience | 问心无愧 |
| a guilty conscience | 内疚 |

> 🧠 **记忆方法**
> - **词根**：con-(加强) + sci(知道) + -ence → 内心知道对错 → 良心
> - **同根词**：conscious（有意识的）、science（科学）
> - **写作词汇**：ethical issue 讨论时常用
```

**输出格式**:
```markdown
# 单词表 - Day {N}

**日期**：{date}
**词汇量**：{count}词
**来源**：墨墨导出

---

## ⭐⭐⭐ 高频词（必考词汇）

### 词族1: {word}（{count}词）
#### {word}
{音标} {词性} {释义}
- 🔴 僻义预警：{rare_meaning}（考研{frequency}%考此义）
- 搭配：{collocations}

---

## ⭐⭐ 中频词（常考词汇）
...

---

## ⭐ 低频词（生僻词汇）
...

---

## 📊 统计信息
| 分类 | 数量 |
|------|------|
| 高频词 | {n} |
| 中频词 | {n} |
| 低频词 | {n} |
| 僻义预警 | {n} |

**下次复习日期**：{date + 2days}
```

### 功能1: PDF词汇提取 + 语境文章

**输入**: 用户从单词APP（墨墨/百词斩等）导出的PDF

**处理流程**:
1. 读取PDF内容，提取单词列表
2. **整理和格式化单词表**（执行功能0）
3. 为每个单词获取：音标、词性、释义、词频
4. **检测熟词僻义**：识别考研中的僻义陷阱
5. **优先检索真题语境**：真题语境池 → 外刊同源 → AI生成
6. 将单词串联成真题风格的语境文章
7. 在文章中高亮目标词汇

**输出**:
- **整理后的单词表**：覆盖原始文件
- Obsidian笔记：每日词汇记录（含僻义预警）
- 真题语境文章：包含目标词汇的连贯文章

### 功能2: 快速查词 + 僻义预警

**输入**: 单个单词或短语

**处理流程**:
1. 查询单词基本信息（音标、词性、释义）
2. **检测熟词僻义**：显示僻义预警级别
3. 提供真题例句（含僻义用法）
4. 显示常用搭配
5. 展示同义词/反义词/词族

**输出**: 紧凑的单词卡片（含⚠️僻义预警）

---

## 熟词僻义库

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

## 真题语境检索策略

> 📁 详细实现见 [code.md](code.md) 的 `generate_context_article` 函数

### 检索优先级

1. **真题语境池** → 优先使用近5年真题
2. **外刊同源库** → The Economist, The Guardian
3. **AI生成** → 模拟真题风格（最后选项）

### 文章要求

- ✅ 必须包含用户提供的**所有目标单词**
- ✅ **译文位置**：紧接在原文之后，词汇解析表之前（便于对照阅读）
- ✅ 风格模拟考研真题阅读理解

### 文章结构顺序（重要！）

```markdown
# 标题

> 元信息

## 📖 原文
{英文原文}

## 📖 参考译文  ← 译文紧接原文，方便对照
{中文译文}

## 📊 词汇解析表
{词汇解析}

## 📖 阅读理解练习
{练习题}
```

⚠️ **禁止**将译文放在文件末尾（用户难以找到）

---

## 词汇卡片格式

### 完整版格式

```markdown
---
# 基础信息
word: "address"
pronunciation: "/əˈdres/"
part_of_speech: "verb/noun"
difficulty: "important"
frequency: 5
first_seen: "2025-01-15"

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
```

---

## 文件组织结构

```
考研英语/
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
├── 📚 真题语境池/                # 真题例句库
│   ├── 英语一/
│   │   ├── 阅读理解/
│   │   ├── 完形填空/
│   │   └── 翻译/
│   └── 英语二/
│       └── ...
│
├── 📰 外刊同源库/                # 外刊例句库
│   ├── The Economist/
│   └── The Guardian/
│
└── ⚠️ 熟词僻义库/                # 僻义词索引
    ├── critical级别.md
    ├── warning级别.md
    └── 完整列表.md
```

---

## Day编号计算规则 ⚠️

**生成新文件前必须计算正确的Day编号！**

### 计算步骤

1. **检查现有文件**：
   ```bash
   find 考研英语/📰 真题语境文章 -name "*.md" | sort | tail -5
   ```

2. **提取最大Day编号**：
   - 从文件名格式 `Day-XXX-YYYY-MM-DD.md` 提取 XXX
   - 例如：`Day-015-2026-03-14.md` → Day编号 = 15

3. **计算新Day编号**：
   - 新Day编号 = 最大Day编号 + 1
   - 例如：最大是 Day-015 → 新文件使用 Day-016

4. **文件命名格式**：
   - 真题文章：`Day-{XXX}-{YYYY-MM-DD}.md`
   - 测试记录：`Quiz-Day-{XXX}-{YYYY-MM-DD}.md`
   - 词汇统计：`Statistics-Day-{XXX}-{YYYY-MM-DD}.md`
   - 写作输出：`Day-{XXX}-{YYYY-MM-DD}.md`

### 注意事项

- ❌ **禁止**硬编码 "Day-001"
- ✅ **必须**先检查现有文件再生成新编号
- ✅ 所有4类文件使用**相同的Day编号**

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

| 单词 | 音标 | 词性 | 释义 | ⚠️僻义 | 💡记忆提示 | 📝常见搭配 |
|------|------|------|------|--------|----------|------------|
| exemplify | /ɪɡˈzemplɪfaɪ/ | v. | 举例说明 | | 词根: exempl(例子)+ify动词化 | exemplify the point |
| address | /əˈdres/ | vt./n. | 处理；地址 | [critical] | 搭配记忆: address the problem | address the issue, address concerns |

---

## ⚠️ 僻义预警

### address [critical]
- 常见义：地址
- **考研僻义（80%）**: 处理、解决
- 搭配：address the problem, address an issue

---

## 真题语境文章

{article_including_all_target_words}

> ⚠️ **词汇覆盖检查**: 本文已包含所有 {total_count} 个目标单词

---

## 📖 文章译文

{chinese_translation}

---

## 📖 阅读理解练习

### 模板2: 真题语境卡片

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
```

---

## 熟词僻义检测

> 📁 详细实现见 [code.md](code.md) 的 `detect_polysemy` 函数

### 检测逻辑

1. 检索考研大纲词表
2. 对比大纲释义与常见释义
3. 计算语义重叠度
4. 重叠度 < 50% → 触发僻义预警

### 预警级别

| 级别 | 重叠度 | 说明 |
|------|--------|------|
| ⚠️ Critical | < 30% | 高频陷阱词，必须重点记忆 |
| ⚡ Warning | 30-50% | 中等陷阱词，需要留意 |

---

## 验证标准

1. ✅ 能够从PDF中提取单词列表
2. ✅ 能够识别并分类重点词汇、僻义词和一般词汇
3. ✅ **能够优先使用真题语境而非AI生成文章**
4. ✅ **能够正确检测和预警熟词僻义**
5. ✅ 能够快速查询单词信息（含僻义预警）
6. ✅ 能够生成结构化词汇卡片
7. ✅ 警告格式使用⚠️图标
8. ✅ 例题格式使用[!example] callout

---

## 限制条件

- 需要用户提供PDF文件或单词列表
- 查词功能依赖本地词汇库或在线词典
- 真题语境依赖于预建的真题例句库

---

## 技能集成

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 保存词汇卡片到MemOS |
| obsidian-markdown | 创建词汇卡片笔记 |
| pdf | 读取PDF内容 |
| docx | 导出Word文档 |

### 被调用场景

| 调用者 | 场景 |
|--------|------|
| kaoyan-english-review | 获取单词信息生成复习计划 |
| kaoyan-english-quiz | 获取单词信息生成测试题 |
| kaoyan-english-writing | 获取单词信息用于写作训练 |

---

## Day编号计算规则 ⚠️ (更新于2026-03-16)

**重要**：本技能使用 `kaoyan-english-core` 提供的共享Day编号计算函数。

### 推荐做法

```python
# 使用共享函数获取验证后的Day编号
from kaoyan_english_core import get_validated_day_number, generate_day_filenames

# 获取Day编号（双重验证）
day_number = get_validated_day_number("2026-03-16")  # 返回：17

# 生成文件名
filenames = generate_day_filenames("2026-03-16", day_number)
# {
#     "context_article": "Day-017-2026-03-16.md",
#     "statistics": "Statistics-Day-017-2026-03-16.md"
# }
```

### 核心函数位置

详细实现请参考：`.claude/skills/kaoyan-english-core/code.md` 第8节

### Day编号对应关系

| 日期 | Day编号 |
|------|---------|
| 2026-02-28 | Day 001 |
| 2026-03-01 | Day 002 |
| 2026-03-15 | Day 016 |
| 2026-03-16 | Day 017 |
| 2026-03-17 | Day 018 |

---

## Markdown 表格规范 ⚠️

> **重要**：生成词汇统计、语境文章等包含表格的文件时，**必须**遵守以下规范！

### 规范1: 表格前必须有空行

Markdown 表格必须与前面的内容之间有空行，否则表格不会被正确渲染。

```markdown
# ❌ 错误 - 表格不会渲染
**重点单词**：
| 单词 | 核心含义 |
|------|---------|
| test | 测试 |

# ✅ 正确 - 表格会正确渲染
**重点单词**：

| 单词 | 核心含义 |
|------|---------|
| test | 测试 |
```

### 规范2: 表格内禁止使用粗体标记

表格内的 `**粗体**` 标记会干扰管道符 `|` 的解析，导致表格结构错乱。

```markdown
# ❌ 错误 - 粗体标记会破坏表格
| 单词 | 常见义 | **僻义（考研重点）** |
|------|--------|---------------------|
| **spectrum** | 光谱 | 范围 |

# ✅ 正确 - 使用纯文本
| 单词 | 常见义 | 僻义（考研重点） |
|------|--------|------------------|
| spectrum | 光谱 | 范围 |
```

### 规范3: 表格内需要强调时的替代方案

如果需要在表格中强调某些内容，使用以下替代方案：

| 替代方案 | 示例 | 说明 |
|---------|------|------|
| 前缀符号 | `⚠️ 僻义：xxx` | 使用 emoji 或符号标记 |
| 括号标注 | `(重点)` | 使用括号添加说明 |
| 列后注释 | 在表格后用文字说明 | 表格外使用粗体强调 |

### 规范4: 完整表格示例

```markdown
**重点单词**：

| 单词 | 核心含义 | 考研考点 |
|------|---------|---------|
| resolution | 决心/解决/分辨率 | 分辨率（科技类）；conflict resolution |
| resign | 辞职/顺从 | 僻义：resign oneself to 顺从 |
| resident | 居民/住院医生 | 僻义：住院医生 |
| represent | 代表 | represent sb's interests |
| reproduce | 复制/繁殖 | reproduce results 复现结果 |

**记忆口诀**：re-开头多表示"回"或"再"
```

### 验证清单

生成包含表格的文件后，检查：

- [ ] 每个表格前都有空行
- [ ] 表格内没有 `**` 粗体标记
- [ ] 表头分隔行格式正确（`|---|---|`）
- [ ] 所有行的列数一致

---

*创建日期: 2026-03-10*
*版本: 1.2.0*
*最后更新: 2026-03-21（添加 Markdown 表格规范）*
