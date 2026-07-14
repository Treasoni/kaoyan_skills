---
name: kaoyan-english-writing
description: This skill handles writing output training for 考研英语 (Chinese graduate entrance English exam). Use it when users want to practice writing vocabulary replacement, Chinese-to-English translation exercises, word differentiation tasks, or access writing vocabulary libraries for argumentative essays, chart descriptions, and letter writing.
---

# 考研英语写作输出技能 (Kaoyan English Writing)

## 核心功能

1. **写作替换升级** - 用高级词汇替换简单表达
2. **汉译英练习** - 使用目标词汇翻译中文句子
3. **词义辨析** - 在写作语境中选择最合适的词
4. **写作词汇库** - 议论文、图表描述、信件写作必备词汇

**核心特色**：
- 从复习词汇中选择写作必备词
- 提供初级→高级的词汇替换对照
- 涵盖考研写作三大类型（议论文、图表、信件）

---

## 触发条件

**触发**：
- "写作替换"、"写作训练"、"高级词汇替换"
- "作文用词"、"写作词汇"、"词汇升级"
- "汉译英"、"翻译练习"
- "词义辨析"、"选词练习"

**不触发**：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 生成复习计划 → 使用 kaoyan-english-review
- 单词测试 → 使用 kaoyan-english-quiz

---

## 输出内容

- 写作替换练习题
- 汉译英翻译题
- 词义辨析选择题
- 写作词汇替换表

---

## 写作类型分类

| 类型 | 核心词汇 | 场景 |
|------|----------|------|
| 议论文 | contend, assert, imperative | 观点表达、程度描述 |
| 图表描述 | soar, surge, fluctuate | 数据变化、程度描述 |
| 信件写作 | inquire, dismayed, appreciation | 开头、结尾模板 |

---

## 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 保存写作记录 |
| kaoyan-english-vocab | 获取单词信息 |
| kaoyan-english-review | 获取今日复习词汇 |

---

*最后更新: 2026-03-27*
