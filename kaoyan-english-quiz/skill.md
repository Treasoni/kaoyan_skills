---
name: kaoyan-english-quiz
description: This skill handles vocabulary quizzes and testing for 考研英语 (Chinese graduate entrance English exam). Use it when users want to test vocabulary knowledge with meaning quizzes, collocation exercises, polysemy-focused tests, or track quiz results with detailed error analysis.
---

# 考研英语单词测试技能 (Kaoyan English Quiz)

## 核心功能

1. **词义选择测试** - 四选一词义测试（含僻义选项）
2. **搭配填空测试** - 常用搭配填空练习
3. **僻义词专项测试** - 针对熟词僻义的强化测试
4. **测试结果统计** - 得分、错词、僻义词错误分析
5. **薄弱项识别** - 自动识别需要加强的词汇

**核心特色**：
- 优先测试僻义词（高频陷阱）
- 多种题型覆盖（词义、搭配、拼写）
- 与kaoyan-english-core集成，支持MemOS持久化

---

## 触发条件

**触发**：
- "单词测试"、"词汇quiz"、"测试单词"
- "词义测试"、"搭配测试"、"僻义测试"

**不触发**：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 生成复习计划 → 使用 kaoyan-english-review
- 写作训练 → 使用 kaoyan-english-writing

---

## 测试题型

| 题型 | 说明 | 示例 |
|------|------|------|
| 词义选择 | 四选一，重点考查僻义词 | address = 处理/解决 ⚠️ |
| 搭配填空 | 词组搭配 | exemplifies the need |
| 僻义专项 | 熟词僻义强化 | school = 学派 |

---

## 输出内容

- 测试题（支持打印或交互式）
- 答案与解析
- 成绩统计表
- 薄弱项分析
- 僻义词专项报告

---

## 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-english-core | 记录测试结果、错误追踪 |
| kaoyan-english-vocab | 获取单词信息 |
| kaoyan-english-review | 获取待复习词汇 |

---

*最后更新: 2026-03-27*
