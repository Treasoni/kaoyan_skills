---
name: parse-words
description: This skill should be used when the user asks to parse highlighted English words from an article, especially `==highlighted==` vocabulary in 考研英语 reading notes, and generate an in-place vocabulary analysis section without overwriting the original article.
version: 1.0.0
---

# Parse Highlighted Words Skill

## Purpose

Use this skill when the user says things like:
- `/parse-words`
- "解析高亮单词"
- "整理这篇文章里 ==高亮== 的词"
- "把文中标亮的词做成词汇解析"

The goal is to extract `==...==` marked words or phrases from an article, explain them in context, and append a structured vocabulary block back into the source note.

## Core Rules

1. Context first. Meanings must be inferred from the article's sentence-level usage.
2. Avoid hallucinated rare meanings. Only mark 熟词僻义 when the context clearly supports it.
3. Incremental update only. Append the new analysis block into the existing note instead of rewriting the article.
4. Protect personal content. Never modify:
   - `## 个人笔记` / `## My Insights`
   - `## 随手记` / `## Quick Notes`
   - `## 学习心得` / `## Learnings`
   - `## 踩坑记录` / `## Pitfalls`
   - `## 待探索` / `## TODO`
   - any `> [!personal]` block

## Workflow

### 1. Read and extract

- Read the target article.
- Collect all `==word==` and `==phrase==` items.
- Preserve the original sentence for each item.

### 2. Normalize entries

- Lowercase vocabulary where appropriate.
- If the highlight is a phrase, keep the phrase and also identify the core tested word when useful.
- Record:
  - word or phrase
  - sentence context
  - likely part of speech
  - in-context meaning

### 3. Detect rare or shifted meanings

Pay special attention to 考研英语常见熟词僻义. If a word is used in a shifted meaning, mark it with `⚠️` and contrast:
- basic/common meaning
- article-specific meaning

If uncertain, do not force a rare-meaning label.

### 4. Generate the analysis block

Use a structure like:

```markdown
---

### 高亮词汇解析（==高亮==部分）

| 单词 | 文中用法 | 释义 | 记忆方法 |
|------|----------|------|----------|

---

## 🧠 记忆方法体系

### 一、词根词缀法
### 二、联想记忆法
### 三、语境记忆法
### 四、僻义专项记忆

---

## 📝 记忆顺序建议

### 第一优先级（必记僻义）⚠️
### 第二优先级（核心动词）
### 第三优先级（名词概念）

---

## 💡 复习建议
```

## Insertion Rules

Prefer inserting the generated block:
1. after the article's phrase/collocation section
2. before reading exercises or question sections

If the note already contains a vocabulary analysis block, update or replace that block only. Do not duplicate the whole article.

## Quality Bar

Before editing, verify:
- all highlighted items were captured
- meanings match the actual sentence context
- tables are valid Markdown
- the insertion does not touch protected blocks
