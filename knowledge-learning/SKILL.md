---
name: knowledge-learning
description: This skill should be used when the user asks to learn about a topic, understand a concept, get explanations about technical subjects, or requests knowledge about any domain.
version: 1.0.0
---

# Knowledge Learning Skill

## Overview

This skill helps users learn various topics and concepts through **interactive, adaptive learning** rather than one-way knowledge dumping. It focuses on:
- Intelligent information sourcing (search only when needed)
- Interactive learning with questions and confirmation
- Flexible output format based on context
- Layered understanding (concept → detail → application)

## When This Skill Applies

This skill should be invoked when the user:
- Asks to learn about a topic ("帮我学习 Python", "我想了解 Python")
- Requests concept explanations ("什么是微服务架构？", "解释一下 React hooks")
- Wants to understand technical subjects ("学习机器学习")
- Seeks knowledge explanations in any domain

## Workflow

### 1. Understand the Learning Request
- Identify the main topic the user wants to learn
- Extract any specific aspects the user is interested in

**Identify user's learning goal:**
- 概念理解 (Conceptual understanding) - 用户想建立心智模型
- 考试准备 (Exam preparation) - 需要重点、考点、记忆技巧
- 实际项目 (Practical project use) - 需要代码示例、最佳实践
- 面试准备 (Interview preparation) - 需要常见面试题、深入原理

**Determine user's background level:**
- Beginner (初学者) - 需要更多类比，少用术语
- Intermediate (中级) - 需要机制解释 + 示例
- Advanced (高级) - 需要权衡、边界情况、设计原理

**Determine the depth of explanation needed** (overview vs. detailed)
- Ask clarifying questions if the request is ambiguous

### 2. Determine Knowledge Type (Decide Whether to Search)

**NOT all topics require WebSearch**. Classify the topic:

| Knowledge Type | Needs WebSearch? | Reason |
|----------------|------------------|--------|
| 基础理论 (算法、数学、操作系统原理) | ❌ No | Fundamental, stable over time |
| 经典概念 (TCP三次握手、设计模式) | ❌ No | Established, doesn't change yearly |
| 框架/库特定版本 | ✅ Yes | API changes, version-specific |
| 框架最新特性 | ✅ Yes | Need current year (2026) |
| 市场趋势/技术对比 | ✅ Yes | Landscape evolves |
| 语言语法基础 | ❌ No | Core language is stable |
| 语言新特性 | ✅ Yes | Need 2026 for latest features |

**Use WebSearch ONLY when:**
- User explicitly asks for "latest" or "2026" or "newest"
- Topic is about frameworks, libraries, tools, or market trends
- Topic is volatile and changes frequently

**Examples of when NOT to search:**
- "解释 TCP 三次握手" → Use internal knowledge
- "什么是快速排序算法" → Use internal knowledge
- "学习设计模式中的单例模式" → Use internal knowledge

### 3. Adaptive Interactive Learning

**Ask ONLY when appropriate**, not after every layer. Use judgment:

**When to ask:**
- User appears confused (expresses confusion, asks follow-up questions)
- User seems engaged but not understanding (gives hesitant responses)
- Complex concept is being explained
- Transitioning to a significantly deeper level

**When NOT to ask:**
- User seems confident and gives clear follow-up
- User just wants quick overview
- User is actively asking questions already
- Simple concept was just explained

**Judgment cues:**
- User says "我不懂" → Ask for clarification
- User says "继续" → Don't interrupt with questions
- User is asking deeper questions → They're engaged, keep flowing
- User says "简单点" → Switch to simpler explanation

**Learning Phases:**

#### Phase 1: Concept Layer (Overview)
- Provide a simple, high-level overview
- Use analogies to relate to everyday experiences
- **Ask only if**: Concept is complex or user seems uncertain

#### Phase 2: Detail Layer (After user confirms or asks deeper)
- Dive into specific aspects user is interested in
- Provide examples and use cases
- **Ask only if**: User hasn't shown clear understanding

#### Phase 3: Application Layer (If user wants to apply)
- Show how to use the knowledge in practice
- Provide code examples or step-by-step guides
- **Ask**: "想尝试一下吗？可以给你一个练习题" (engage, don't interrupt)

#### Phase 4: Verification (Check understanding)
- Ask the user a question to verify understanding
- Or ask user to explain it back in their own words
- Provide feedback on their explanation

### Adaptive Difficulty Guidelines

Adjust explanation based on detected user level:

| User Level | Approach | Content Focus |
|-------------|----------|----------------|
| **初学者** | 多类比、少术语、慢节奏 | What 和 Why，少谈 How |
| **中级** | 机制解释 + 代码示例 | How 为主，核心原理 |
| **高级** | 权衡、边界、设计原理 | Why 和 Trade-offs，最佳实践 |

**Beginner 模式:**
- Start with everyday analogies
- Avoid jargon or explain it immediately
- One concept at a time
- Visual descriptions when possible

**Intermediate 模式:**
- Explain mechanisms and "how it works"
- Provide practical code examples
- Show common patterns and pitfalls
- Connect to related concepts

**Advanced 模式:**
- Discuss trade-offs and design decisions
- Cover edge cases and performance considerations
- Compare alternatives and when to use what
- Share production experiences and anti-patterns

### 4. Output Format (Flexible)

**NOT forced to use Obsidian Markdown**. Choose format based on context:

| Situation | Output Format |
|-----------|---------------|
| 用户问简单解释 | 直接对话，简洁回答 |
| 用户想记笔记 | 使用 obsidian-markdown 技能 |
| 用户进行对话学习 | 混合格式：对话为主，结构化为辅 |
| 用户明确要求 Markdown 结构 | 使用 obsidian-markdown 技能 |
| 用户讨论或辩论 | 对话格式，引用、反问 |

**Invoke obsidian-markdown skill ONLY when:**
- User explicitly asks for "笔记" or "Markdown"
- User says "帮我整理成笔记"
- Learning session is complete and user wants to save
- Context indicates note-taking is appropriate

## Interactive Learning Techniques

### 1. Ask Clarifying Questions
When the request is broad, first ask:

- "你想了解 [主题] 的哪方面？基础概念？实际应用？还是最新发展？"
- "你的背景是什么？是初学者还是有经验？"
- "你是想快速了解还是要深入学习？"

### 2. Interactive Question Methods

When interactive UI is available, use `AskUserQuestion` tool.
Otherwise, ask in natural dialogue.

**Using AskUserQuestion (when available):**

```python
AskUserQuestion(
    questions=[
        {
            "question": "你想从哪个角度学习这个主题？",
            "header": "学习角度",
            "options": [
                {"label": "基础概念", "description": "了解核心原理和机制"},
                {"label": "实际应用", "description": "如何在实际项目中使用"},
                {"label": "深入原理", "description": "底层实现和设计思想"},
                {"label": "最新动态", "description": "该领域的最新发展和趋势"}
            ],
            "multiSelect": False
        }
    ]
)
```

**Using natural dialogue (fallback):**

"你想从哪个角度学习这个主题？
- A. 基础概念 - 了解核心原理
- B. 实际应用 - 如何使用
- C. 深入原理 - 底层实现
- D. 最新动态 - 发展趋势"

**Tool availability guideline:**
- Try to use AskUserQuestion for structured choices
- If tool unavailable, fall back to natural questions
- Don't assume tool availability in skill design
- Always provide alternative approach

### 3. Confirm Understanding
After explaining a concept, ask:

- "这部分清楚了吗？"
- "需要我举个具体的例子吗？"
- "有什么疑问吗？"

### 4. Provide Examples and Counter-Examples
- Show positive examples
- Show common mistakes (counter-examples)
- Ask: "你能看出这两个的区别吗？"

### 5. Layered Explanation
Start simple, then go deeper:

**Layer 1**: "X 就像 Y" (analogy)
**Layer 2**: Basic technical explanation
**Layer 3**: Detailed mechanics (if user wants more)

### 6. Socratic Method (Ask instead of tell)
Sometimes guide the user to discover the answer:

- "你觉得为什么需要这么做？"
- "如果是你，你会怎么设计？"
- "猜猜这个输出会是什么？"

## Guidelines

### Content Principles

1. **Make It Accessible**
   - Start with a simple analogy
   - Explain technical jargon in simple terms
   - Use concrete examples for abstract concepts

2. **Engage the User**
   - Ask questions to gauge understanding
   - Encourage user to think and respond
   - Don't just dump information

3. **Respect the Learning Pace**
   - One concept at a time
   - Wait for user confirmation before going deeper
   - Let user lead the direction

### When Using Obsidian Markdown

Only use when appropriate. Structure like:

```markdown
# [Topic Name]

> [!info] 概述
> 简单的类比解释

## 核心概念

### 概念1
> [!tip] 关键点
> 重要提示

### 概念2
解释...

## 实际应用

> [!example] 示例
> 具体例子...

## 常见误区

> [!warning] 注意
> 容易犯的错误...

## 相关概念
[[相关概念1]] | [[相关概念2]]
]]
```

## Examples

### Example 1: Learning a Stable Concept (No Search)

User: "解释一下 TCP 三次握手"

Process:
1. **Determine**: This is a classic, stable concept → NO WebSearch needed
2. **Interactive response**:
   - "TCP 三次握手就像是打电话确认对方接听了...（类比）"
   - "**Ask**: 这个类比清楚了吗？想了解具体的技术细节吗？"
3. Wait for user response
4. If user wants more details, provide technical explanation
5. Ask: "这部分理解了吗？"

### Example 2: Learning Latest Framework Features (Search)

User: "React 2026 有什么新特性？"

Process:
1. **Determine**: User asks for "latest" and "2026" → YES, WebSearch needed
2. Search for: "React 2026 new features", "React latest changes"
3. Present findings interactively:
   - "React 2026 主要有这些新特性...（列出）"
   - "**Ask**: 你对哪个特性最感兴趣？我可以详细解释"
4. Wait for user response
5. Dive deeper based on user's choice

### Example 3: Structured Note-Taking (Use obsidian-markdown)

User: "帮我整理一下微服务架构的笔记"

Process:
1. User explicitly asks for "笔记" → Use obsidian-markdown
2. Create structured note with callouts, sections
3. Present the note to user

### Example 4: Adaptive Interactive Learning

User: "我想学习递归"

Process:
1. **Detect goal**: Need clarification - ask user's goal
2. **Detect level**: If unclear, ask about experience
3. Start with analogy: "递归就像俄罗斯套娃..."
4. **Adaptive**: If beginner, stay simple; if advanced, show complexity analysis
5. Provide code example
6. **Adaptive question**:
   - Beginner: "这个函数会输出什么？"
   - Advanced: "你能分析一下这个递归的时空复杂度吗？"
7. **Judgment**: If user responds confidently, continue; if hesitant, ask follow-up
8. **Goal-specific**:
   - For interview: "这是一个常见的面试题变种..."
   - For project: "在项目中，递归要注意..."
   - For exam: "考试重点：终止条件、递归关系..."

## Important Notes

- **NOT all topics need WebSearch** - use judgment based on knowledge type
- **NOT forced to use obsidian-markdown** - adapt to context and user preference
- **NOT ask after every layer** - ask only when appropriate, don't interrupt flow
- Learning should be **adaptive** - adjust to user's level and goal
- Use **AskUserQuestion when available**, fall back to natural dialogue
- Detect user's **learning goal** (exam/project/interview/curiosity)
- Adjust **explanation depth** based on user level (beginner/intermediate/advanced)
- Focus on **understanding** not just memorization
- When unsure what the user wants, **ask** instead of assume
