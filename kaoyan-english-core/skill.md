---
name: kaoyan-english-core
description: This skill manages the core infrastructure for 考研英语 (Chinese graduate entrance English exam) vocabulary learning, including MemOS integration for persistent storage, dispatch signal processing, memory compression mode, unified error tracking, and dynamic phase-based vocabulary targeting.
version: 1.0.0
---

# 考研英语核心协调技能 (Kaoyan English Core)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能是考研英语词汇学习的核心协调层，负责：
1. **MemOS集成管理**：用户画像、词汇卡片持久化、复习历史记录
2. **调度信号处理**：接收并处理来自kaoyan-plan的调度信号
3. **记忆压缩模式**：当其他科目欠账时激活英语时间压缩
4. **统一错误模型**：英语错误记录的学科标签管理
5. **动态权重响应**：根据考试倒计时阶段调整词汇学习目标

**设计原则**：
- 其他英语技能通过本技能访问MemOS
- 当MemOS不可用时自动降级
- 提供统一的错误记录和追踪接口

---

## 触发条件

### 触发此技能当：

**用户画像相关**：
- "英语学习配置"
- "更新英语画像"
- "英语水平设置"
- "考研英语配置"

**状态检查相关**：
- "英语状态"
- "英语进度"
- "英语欠账检查"
- "英语疲劳检查"
- "词汇欠账"
- "待复习词汇"

**调度信号相关**：
- "英语调度信号"
- "英语压缩模式"
- "英语复习模式"

### 不触发此技能当：
- 词汇整理/查词 → 使用 kaoyan-english-vocab
- 生成复习计划 → 使用 kaoyan-english-review
- 单词测试 → 使用 kaoyan-english-quiz
- 写作训练 → 使用 kaoyan-english-writing

---

## MemOS集成

### 核心原则
- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为无状态模式
- **数据持久化**: 词汇学习记录、用户画像、复习历史均持久化存储

### MemOS功能特性
1. **用户画像追踪**: 记录英语水平、考试信息、学习偏好
2. **词汇卡片持久化**: SM-2算法状态永久保存
3. **复习历史记录**: 完整的复习会话历史
4. **测试结果追踪**: 测试成绩和错误分析
5. **词汇疲劳追踪**: 防止学习倦怠的智能提醒
6. **欠账熔断机制**: 超过200个待复习词时自动触发复习模式
7. **画像刷新机制**: 30天未更新时提示确认学习配置

### 降级行为
当MemOS不可用时：
- ✅ 基础功能正常工作
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用智能追踪（疲劳、欠账熔断等）

---

## 📁 详细模块文档

| 模块 | 文件 | 内容 |
|------|------|------|
| 代码实现 | [code.md](code.md) | MemOS集成函数、调度信号处理、记忆压缩模式、动态权重响应、统一错误模型 |

---

## 核心函数概览

以下函数详细实现见 [code.md](code.md)：

| 函数名 | 用途 |
|--------|------|
| `load_user_context_from_memory` | 从MemOS加载用户上下文 |
| `save_word_card_to_memory` | 保存词汇卡片到MemOS |
| `record_review_session` | 记录复习会话（含upsert逻辑） |
| `check_context_freshness_english` | 检查用户画像是否需要刷新 |
| `check_vocabulary_debt_with_memory` | 检查词汇欠账（含熔断机制） |
| `check_vocabulary_fatigue_intervention` | 检查词汇学习疲劳 |
| `check_dispatch_signals` | 检查调度信号 |
| `process_dispatch_signal` | 处理调度信号 |
| `activate_memory_compression_mode` | 激活记忆压缩模式 |
| `get_phase_vocabulary_target` | 根据阶段获取词汇学习目标 |
| `save_unified_english_mistake` | 保存英语错误记录 |

---

## 调度信号处理

### 支持的调度动作

| 动作名 | 说明 | 上下文参数 |
|--------|------|------------|
| `vocabulary_review_mode` | 轻量词汇复习 | `{mode, duration}` |
| `memory_compression_mode` | 记忆压缩模式 | `{compress_hours, transfer_to}` |
| `polysemy_focus` | 僻义词专项 | `{focus, count}` |
| `weekly_error_analysis` | 周日错误分析 | `{aggregate}` |

---

## 记忆压缩模式

当kaoyan-plan检测到其他科目欠账时，可触发英语记忆压缩模式。

### 压缩模式下的调整

| 功能 | 正常模式 | 压缩模式 |
|------|----------|----------|
| 每日新词 | 50个 | 20个 |
| 复习重点 | 均衡 | 仅僻义词+高频词 |
| 语境文章 | 生成 | 跳过 |
| 测试 | 完整 | 仅快速测试 |
| 写作训练 | 包含 | 跳过 |

---

## 动态权重响应

### 阶段策略表

| 阶段 | 天数 | 每日新词 | 复习比例 | 僻义权重 |
|------|------|----------|----------|----------|
| 基础期 | >300 | 50 | 30% | 1.0x |
| 强化期 | 180-300 | 40 | 50% | 1.2x |
| 十月强化期 | 90-180 | 30 | 60% | 1.5x |
| 冲刺期 | 30-90 | 10 | 90% | 2.0x |
| 极限冲刺 | <30 | 0 | 100% | 2.0x |

---

## 统一错误模型

### 英语专用错误类型

| 错误类型 | 说明 | 标签 |
|----------|------|------|
| `polysemy_error` | 多义词错误 | `#polysemy_critical` |
| `collocation_error` | 搭配错误 | `#collocation` |
| `condition_omission` | 条件遗漏 | `#condition` |
| `concept_confusion` | 概念混淆 | `#concept` |

---

## MemOS标签系统

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#user_profile` | 用户画像 | 每用户1条 |
| `#word_card` | 词汇卡片 | 每词每用户1条 |
| `#word_{word}` | 单词索引 | 可多条（不同用户） |
| `#review_session_current` | 今日当前复习会话 | 每用户每日1条 |
| `#review_session_history` | 历史复习会话归档 | 多条 |
| `#date_{YYYY-MM-DD}` | 日期索引 | 多条 |
| `#test_result` | 测试记录 | 多条 |
| `#dispatch_signal` | 调度信号 | 多条 |
| `#mistake_record` | 错误记录 | 多条 |
| `#subject_english` | 英语学科标签 | 多条 |

---

## 验证标准

1. ✅ 能够从MemOS加载用户上下文
2. ✅ 能够保存词汇卡片到MemOS
3. ✅ 能够记录复习会话（含upsert逻辑）
4. ✅ 能够检查用户画像新鲜度
5. ✅ 能够检查词汇欠账并触发熔断
6. ✅ 能够检测词汇疲劳并建议干预
7. ✅ 能够接收和处理调度信号
8. ✅ 能够激活记忆压缩模式
9. ✅ 能够根据阶段调整词汇目标
10. ✅ MemOS不可用时优雅降级
11. ✅ 统一错误模型学科标签正确

---

## 限制条件

- MemOS集成是可选的，不可用时不影响基础功能
- 调度信号依赖kaoyan-plan发送
- 记忆压缩模式需要kaoyan-plan触发

---

## 技能集成

### 被调用的技能

| 技能 | 调用场景 |
|------|----------|
| kaoyan-english-vocab | 保存词汇卡片 |
| kaoyan-english-review | 读取历史数据、保存复习记录 |
| kaoyan-english-quiz | 记录测试结果 |
| kaoyan-english-writing | 保存写作记录 |

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-plan | 发送调度信号 |

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
