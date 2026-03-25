---
name: kaoyan-english-writing
description: This skill handles writing output training for 考研英语 (Chinese graduate entrance English exam). Use it when users want to practice writing vocabulary replacement, Chinese-to-English translation exercises, word differentiation tasks, or access writing vocabulary libraries for argumentative essays, chart descriptions, and letter writing.
version: 1.0.0
---

# 考研英语写作输出技能 (Kaoyan English Writing)

## 技能概述

本技能专注于考研英语写作的词汇训练，帮助用户：
1. **写作替换升级**：用高级词汇替换简单表达
2. **汉译英练习**：使用目标词汇翻译中文句子
3. **词义辨析**：在写作语境中选择最合适的词
4. **写作词汇库**：议论文、图表描述、信件写作必备词汇

**核心特色**：
- 从复习词汇中选择写作必备词
- 提供初级→高级的词汇替换对照
- 涵盖考研写作三大类型（议论文、图表、信件）

---

## 触发条件

### 触发此技能当：

**写作训练相关**：
- "写作替换"
- "写作训练"
- "高级词汇替换"
- "作文用词"
- "写作词汇"
- "词汇升级"
- "写作练习"

**翻译相关**：
- "汉译英"
- "翻译练习"
- "中译英"
- "英译中"

**辨析相关**：
- "词义辨析"
- "选词练习"
- "同义词辨析"

### 不触发此技能当：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 生成复习计划 → 使用 kaoyan-english-review
- 单词测试 → 使用 kaoyan-english-quiz

---

## 核心功能

### 功能: 写作输出转化

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

## 写作词汇库

### 议论文必备

#### 表达观点

| 高级词汇 | 初级替换 | 例句 |
|---------|----------|------|
| contend | think/claim | Many scholars **contend** that... |
| assert | say/state | Critics **assert** that... |
| exemplify | show/illustrate | This case **exemplifies**... |
| maintain | say/hold | Experts **maintain** that... |

#### 表示程度

| 高级词汇 | 初级替换 | 例句 |
|---------|----------|------|
| imperative | necessary | It is **imperative** that... |
| profound | deep/big | have **profound** impact on... |
| negligible | very small | be **negligible** compared to... |

#### 表示因果关系

| 高级词汇 | 初级替换 | 例句 |
|---------|----------|------|
| consequence | result | as a **consequence** of... |
| correlation | relationship | there is a **correlation** between... |
| attributable | caused by | be **attributable** to... |

#### 表示转折

| 高级词汇 | 初级替换 | 例句 |
|---------|----------|------|
| conversely | however | **Conversely**, some argue that... |
| notwithstanding | despite | **Notwithstanding** these challenges... |

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

## 模板

### 写作输出测试模板

```markdown
# 写作输出测试 - Day {day_number}

**日期**: {date}
**目标词汇**: {今日复习词中的写作必备词}

---

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

---

## 写作词汇替换表

| 初级词汇 | 高级替换 | 适用场景 |
|---------|----------|----------|
| think | contend, assert, maintain | 议论文 |
| important | crucial, vital, essential | 通用 |
| big | substantial, significant, considerable | 描述数据 |
| very | exceedingly, extremely, remarkably | 程度修饰 |
| so...that | such...that, to the extent that | 句式升级 |
```

---

## 工作流程

```
[从MemOS加载用户上下文]
      ↓
[获取今日复习词]
      ↓
[选择写作必备词]
      ↓
[生成写作替换题]
      ↓
[生成汉译英题]
      ↓
[生成词义辨析题]
      ↓
[提供词汇替换表]
      ↓
[保存到Obsidian]
```

---

## 验证标准

1. ✅ 能够生成写作替换升级题
2. ✅ 能够生成汉译英练习题
3. ✅ 能够生成词义辨析题
4. ✅ 能够提供高级词汇替换建议
5. ✅ 能够按写作类型分类词汇（议论文/图表/信件）
6. ✅ 警告格式使用⚠️图标
7. ✅ 例题格式使用[!example] callout

---

## 限制条件

- 需要已建立的词汇库
- 写作训练需要词汇库达到一定规模

---

## 技能集成

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 保存写作记录 |
| kaoyan-english-vocab | 获取单词信息 |
| kaoyan-english-review | 获取今日复习词汇 |
| obsidian-markdown | 创建写作训练笔记 |

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
writing_filename = filenames["writing"]  # "Writing-Day-017-2026-03-16.md"
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

*创建日期: 2026-03-10*
*版本: 1.1.0*
*最后更新: 2026-03-24（统一文件命名规范：Writing-Day）*
