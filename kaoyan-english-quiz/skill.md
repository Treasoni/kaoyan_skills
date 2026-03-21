---
name: kaoyan-english-quiz
description: This skill handles vocabulary quizzes and testing for 考研英语 (Chinese graduate entrance English exam). Use it when users want to test vocabulary knowledge with meaning quizzes, collocation exercises, polysemy-focused tests, or track quiz results with detailed error analysis.
version: 1.0.0
---

# 考研英语单词测试技能 (Kaoyan English Quiz)

## 技能概述

本技能专注于考研英语词汇的测试和评估，帮助用户：
1. **词义选择测试**：四选一词义测试（含僻义选项）
2. **搭配填空测试**：常用搭配填空练习
3. **僻义词专项测试**：针对熟词僻义的强化测试
4. **测试结果统计**：得分、错词、僻义词错误分析
5. **薄弱项识别**：自动识别需要加强的词汇

**核心特色**：
- 优先测试僻义词（高频陷阱）
- 多种题型覆盖（词义、搭配、拼写）
- 与kaoyan-english-core集成，支持MemOS持久化
- 自动记录错误到统一错误模型

---

## 触发条件

### 触发此技能当：

**测试相关**：
- "考研英语单词测试"
- "单词quiz"
- "词汇测试"
- "测试单词"
- "词义测试"
- "搭配测试"
- "僻义测试"
- "单词quiz"
- "测试词汇量"

### 不触发此技能当：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 生成复习计划 → 使用 kaoyan-english-review
- 写作训练 → 使用 kaoyan-english-writing

---

## 核心功能

### 功能1: 单词测试

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

---

## 测试题型

### 题型1: 词义选择

四选一词义测试，重点考查僻义词。

```markdown
## 词义选择

1. exemplify
   - [ ] A. 忽略
   - [ ] B. 举例说明
   - [ ] C. 夸大
   - [ ] D. 简化

2. address (在考研中最常见的意义是)
   - [ ] A. 地址
   - [ ] B. 处理、解决 ⚠️ 僻义
   - [ ] C. 称呼
   - [ ] D. 演讲
```

### 题型2: 搭配填空

测试常用词组搭配。

```markdown
## 搭配填空

3. The report _____ the need for reform.
   - [ ] A. exemplifies
   - [ ] B. exemplify

4. We must _____ the root causes of inequality.
   - [ ] A. address
   - [ ] B. addresses
   - [ ] C. addressing
```

### 题型3: 僻义词专项

专门针对熟词僻义的强化测试。

```markdown
## ⚠️ 僻义词专项测试

5. school 在"Chicago school of economics"中的意思是：
   - [ ] A. 学校
   - [ ] B. 流派，学派 ⚠️ 僻义

6. novel 在"a novel approach"中的意思是：
   - [ ] A. 长篇小说
   - [ ] B. 新颖的，创新的 ⚠️ 僻义
```

---

## 模板

### 测试题模板

```markdown
# 单词测试 - Day {day_number}

**日期**: {date}
**测试范围**: {review_words | polysemy_words | random}
**题目数量**: {count}
**时间限制**: {minutes}分钟

---

## 词义选择

1. exemplify
   - [ ] A. 忽略
   - [ ] B. 举例说明
   - [ ] C. 夸大
   - [ ] D. 简化

2. address (在考研中最常见的意义是)
   - [ ] A. 地址
   - [ ] B. 处理、解决
   - [ ] C. 称呼
   - [ ] D. 演讲

## ⚠️ 僻义测试

3. school 在"Chicago school of economics"中的意思是：
   - [ ] A. 学校
   - [ ] B. 流派，学派

## 搭配填空

4. The report _____ the need for reform.
   - [ ] A. exemplifies
   - [ ] B. exemplify

---

## 答案与解析

### 词义选择
1. **B. 举例说明** - exemplify: 举例说明，例证
2. **B. 处理、解决** - ⚠️ address在考研中80%考查"处理"义

### 僻义测试
3. **B. 流派，学派** - ⚠️ school在学术语境中指"学派"

### 搭配填空
4. **A. exemplifies** - 第三人称单数，主语report是单数

---

## 成绩统计

| 项目 | 结果 |
|------|------|
| 总分 | ___ / 100 |
| 正确率 | ___% |
| 僻义词错误 | {count}个 |
| 需加强词汇 | {words} |

---

## 薄弱项分析

### 高频错误词
- address (僻义错误)
- school (搭配错误)

### 建议复习
- [ ] 重新学习address的僻义用法
- [ ] 复习school的学术语境用法
- [ ] 加强搭配练习
```

---

## 工作流程

```
[从MemOS加载用户上下文]
      ↓
[选择测试范围]
      ↓
[生成测试题]
      ↓
[优先包含僻义词]
      ↓
[执行测试]
      ↓
[统计结果]
      ↓
[记录错误到MemOS]
```

---

## 测试数据模型

```yaml
test_record:
  test_id: string
  user_id: string
  test_type: enum (meaning_quiz | collocation_quiz | polysemy_quiz)
  date: date
  created_at: datetime

  test_data:
    word_count: int
    questions: array
    polysemy_count: int  # 僻义词数量

  results:
    score: float
    correct_count: int
    incorrect_count: int
    polysemy_errors: array  # 僻义词错误列表
    weak_words: array  # 薄弱词汇列表

  memos_test_id: string
```

---

## 验证标准

1. ✅ 能够生成词义选择测试题
2. ✅ 能够生成搭配填空测试题
3. ✅ **能够优先测试僻义词**
4. ✅ 能够统计测试结果
5. ✅ 能够识别薄弱词汇
6. ✅ 能够记录错误到MemOS
7. ✅ 能够生成僻义词专项报告
8. ✅ 警告格式使用⚠️图标
9. ✅ 例题格式使用[!example] callout

---

## 限制条件

- 需要已建立的词汇库
- 测试功能依赖MemOS记录历史数据

---

## 技能集成

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 记录测试结果、错误追踪 |
| kaoyan-english-vocab | 获取单词信息 |
| kaoyan-english-review | 获取待复习词汇 |
| obsidian-markdown | 创建测试笔记 |

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
quiz_filename = filenames["quiz"]  # "Quiz-Day-017-2026-03-16.md"
```

### 函数说明

| 函数 | 说明 | 位置 |
|------|------|------|
| `get_validated_day_number()` | 双重验证获取Day编号 | core/code.md §8.1 |
| `generate_day_filenames()` | 生成四类文件名 | core/code.md §8.1 |
| `calculate_day_number()` | 基于日期计算Day编号 | core/code.md §8.1 |

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
