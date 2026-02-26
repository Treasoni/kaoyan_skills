---
# MemOS元数据 (v3.0.0)
record_id: {record_id}
user_id: {user_id}
knowledge_point: {knowledge_point}
date: {date}
created_at: {created_at}

# 错误信息
mistake_type: {mistake_type}  # condition_omission | method_error | calculation_error | logic_jump
severity: {severity}  # critical | warning | attention

# 上下文
question_type: {question_type}
related_theorems: [{related_theorems}]
exam_year: {exam_year}  # 如果是真题

# 标签
tags: [#mistake_record, #kp_{knowledge_point}, #mistake_type_{mistake_type}, #user_{user_id}]
---

# 错误记录：{knowledge_point}

## 错误类型：{mistake_type_display}

## 原始理解 ❌
我当时是这样理解的：
$...$

## 我的错误思维过程
1. 我看到题目后，首先想到了……
2. 然后我认为……
3. 所以我得出结论……

## 为什么会这样想？
- **原因1**：可能是……
- **原因2**：我之前……
- **原因3**：这个条件我……

## 正确理解 ✅

### 正确思路
1. 首先应该注意到……
2. 正确的方法是……
3. 关键步骤是……

### 正确解答
$$
...
$$

## 关键对比

| 我的做法 | 正确做法 |
|---------|---------|
| 错误步骤1 | 正确步骤1 |
| 错误步骤2 | 正确步骤2 |
| 错误结论 | 正确结论 |

## 触发条件
这类错误通常发生在：
- [ ] 看到……时
- [ ] 题目涉及……时
- [ ] 时间紧张时
- [ ] 其他：……

## 我的提醒 📌

下次遇到类似情况时：
1. 首先检查：……
2. 一定要注意：……
3. 千万不要：……
4. 提醒口诀：……

## 相关知识点
- [[{knowledge_point}]] - 回顾该知识点
- [[{related_kp}]] - 需要同时复习

## 错误统计
- 这是第 **{count}** 次犯此类错误
- 上次错误时间：{last_mistake_date}
- 错误频率：{frequency}

## 防止措施
- [ ] 复习[[{knowledge_point}]]的定理条件
- [ ] 做5道相关练习题
- [ ] 制作错题卡片
- [ ] 3天后复习本记录
