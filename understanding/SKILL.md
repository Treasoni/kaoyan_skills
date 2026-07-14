---
name: understanding
description: This skill should be used when the user wants to verify whether their understanding of a concept, derivation, note, screenshot, or worked problem is correct, and expects a structured `[!personal]` understanding record with logic-chain checking.
version: 1.0.0
---

# Understanding Verification Skill

## Purpose

Use this skill when the user says things like:
- `/understanding`
- "检查我的理解"
- "帮我验证这个推导"
- "看看我这样理解对不对"
- "根据这张图/这段笔记检查逻辑"

This skill is for learning verification, not just answer checking. The focus is whether the user's reasoning chain is sound.

## Input Types

Handle any of these:
- plain text explanations
- local note paths
- screenshots or images
- mixed text plus image context

If the user provides an image, inspect it directly when possible. If the image content is too ambiguous to verify faithfully, ask for the key text rather than guessing.

## What To Check

### Correctness
- definitions and concepts
- formulas and symbols
- conclusions

### Logic-chain integrity
- whether each inference step is justified
- whether any key derivation step was skipped
- whether the user understands why the conclusion holds, not only what the conclusion is

### Common failure modes
- concept confusion
- formula misuse
- sign / condition / domain mistakes
- missing prerequisites
- logic jumps without explanation

## Output Format

Always produce a reusable `[!personal]` callout block. Choose one of these modes:

### 1. Fully correct

```markdown
> [!personal] 我的理解记录 🧠
>
> **[标题/问题]**
> - ...
>
> **[结论/总结]**
> - ...
>
> ---
>
> 💡 **相关联的概念**：
> - ...
```

### 2. Partly correct

```markdown
> [!personal] 我的理解记录 🧠（已修正）
>
> ✅ **理解正确部分**：
> - ...
>
> ❌ **理解错误部分**：
> - ...
> - **正确解释**：...
>
> ⚠️ **需要补充的内容**：
> - ...
>
> **[修正后的完整理解]**：
> - ...
```

### 3. Fundamentally incorrect

```markdown
> [!personal] 我的理解记录 🧠（已重新整理）
>
> ❌ **原理解的问题**：
> - ...
>
> **正确理解应该是**：
> - ...
>
> **关键提醒**：
> - ...
```

## Formatting Rules

1. Use LaTeX for math and formulas.
2. Prefer display math for longer equations, fractions, limits, and integrals.
3. Be explicit about which part is right and which part is wrong.
4. Keep the tone encouraging, but do not hide logical problems.

## Important Constraint

If the user skipped a critical derivation step, do not silently fill it in and move on. Explicitly point out the gap and ask for or provide the missing step so the record reflects real understanding.
