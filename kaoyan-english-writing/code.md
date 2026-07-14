# 考研英语写作输出技能 - 实现代码

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

## 写作输出测试模板

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
> **答案1**: Many scholars **contend** that technology plays a crucial role.
> **答案2**: The rapid development of AI **exemplifies** the profound impact of technology.

---

## 题型2: 观点表达（使用目标词汇）

> 题目: 表达"环境保护重要"这一观点
> 必用词汇: imperative, mitigate, consequence

> [!example] 参考答案
> **答案**: It is **imperative** that we take immediate action to **mitigate** the negative **consequences** of climate change.

---

## 题型3: 词义辨析（为写作选词）

> 题目: 想表达"这个问题很严重"，应选择：
> - [ ] A. This problem is serious.
> - [ ] B. This issue is **critical**.
> - [ ] C. This matter is **grave**.

> [!example] 解析
> **答案**: 选 B 或 C
> - serious (基础词): 中学词汇，写作中避免过度使用 ⚠️
> - critical (考研高级词): 表示"关键的，危急的" ⭐⭐⭐
> - grave (正式词汇): 更正式，表示"严重的" ⭐⭐

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

## Day编号计算规则

本技能使用 `kaoyan-english-core` 提供的共享Day编号计算函数。

```python
from kaoyan_english_core import get_validated_day_number, generate_day_filenames

day_number = get_validated_day_number("2026-03-16")  # 返回：17
filenames = generate_day_filenames("2026-03-16", day_number)
writing_filename = filenames["writing"]  # "Writing-Day-017-2026-03-16.md"
```
