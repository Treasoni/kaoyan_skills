---
name: kaoyan-math-core
description: This skill manages the core infrastructure for 考研数学 (Chinese graduate entrance math exam) learning, including MemOS integration for persistent storage, dispatch signal processing, unified error tracking, cross-subject knowledge linking (math→electronics), and proactive knowledge point association.
version: 1.0.0
---

# 考研数学核心协调技能 (Kaoyan Math Core)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能是考研数学学习的核心协调层，负责：
1. **MemOS集成管理**：用户画像、错误记录持久化、知识点卡片
2. **调度信号处理**：接收并处理来自kaoyan-plan的调度信号
3. **统一错误模型**：数学错误记录的学科标签管理
4. **跨学科知识关联**：数学→电子技术知识图谱
5. **知识点联动**：知识点关系图、主动关联算法

**设计原则**：
- 其他数学技能通过本技能访问MemOS
- 当MemOS不可用时自动降级
- 提供统一的错误记录和跨学科关联接口

---

## 触发条件

### 触发此技能当：

**用户画像相关**：
- "数学学习配置"
- "更新数学画像"
- "数学水平设置"
- "考研数学配置"

**状态检查相关**：
- "数学状态"
- "数学进度"
- "数学欠账检查"
- "数学疲劳检查"

**跨学科相关**：
- "跨学科关联"
- "数学电子技术关联"
- "知识图谱"

### 不触发此技能当：
- 生成/更新笔记 → 使用 kaoyan-math-notes
- 查询知识点结构 → 使用 kaoyan-math-structure

---

## MemOS集成

### 核心原则
- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为无状态模式
- **数据持久化**: 错误记录、用户画像、学习历史均持久化存储

### MemOS功能特性
1. **用户画像追踪**: 记录考试类型（数一/数二/数三）、数学水平、学习偏好
2. **错误记录持久化**: 永久保存所有错误历史（条件遗漏、方法误选、推导跳步、计算失误）
3. **个性化提醒**: 基于历史错误生成千人千面的提示
4. **知识点卡片追踪**: 记录每个知识点的掌握程度
5. **画像刷新机制**: 30天未更新时提示确认学习配置

### 降级行为
当MemOS不可用时：
- ✅ 基础功能正常工作
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用个性化错误模式追踪

---

## 📁 详细模块文档

| 模块 | 文件 | 内容 |
|------|------|------|
| 代码实现 | [code.md](code.md) | MemOS集成函数、知识点联动、跨学科关联、调度信号处理、统一错误模型 |

---

## 核心函数概览

以下函数详细实现见 [code.md](code.md)：

| 函数名 | 用途 |
|--------|------|
| `load_user_context_from_memory` | 从MemOS加载用户上下文 |
| `save_mistake_to_memory` | 保存错误记录到MemOS |
| `generate_personalized_reminders` | 基于历史错误生成个性化提醒 |
| `check_context_freshness_math` | 检查用户画像是否需要刷新 |
| `generate_proactive_links` | 生成知识点关联提示 |
| `generate_cross_subject_reminders` | 生成跨学科提醒 |
| `check_dispatch_signals` | 检查调度信号 |
| `process_dispatch_signal` | 处理调度信号 |
| `save_mistake_with_subject_tag` | 保存错误记录（含学科标签） |

---

## 知识点联动

### 知识点关系图示例

| 知识点 | 前置知识 | 常结合 | 应用场景 |
|--------|----------|--------|----------|
| 洛必达法则 | 极限定义、导数定义 | 等价无穷小、泰勒公式 | 定积分应用、变限积分求导 |
| 泰勒公式 | 导数定义、高阶导数 | 洛必达法则、等价无穷小 | 级数展开、近似计算 |
| 变限积分求导 | 定积分定义、导数定义 | 洛必达法则、复合函数求导 | 积分方程、微分方程 |

---

## 跨学科知识关联

### 数学→电子技术知识图谱

| 数学知识点 | 关联的电子技术知识点 | 重要性 |
|------------|---------------------|--------|
| 复数运算 | 频率响应分析、交流电路、滤波器设计、阻抗计算 | ⚠️ Critical |
| 微分方程 | 暂态响应、RC/RL电路、一阶电路分析 | 💡 High |
| 积分 | RC充放电、能量计算、电容储能 | Medium |
| 拉普拉斯变换 | s域分析、传递函数、频域分析 | ⚠️ High |

---

## 调度信号处理

### 支持的调度动作

| 动作名 | 说明 | 上下文参数 |
|--------|------|------------|
| `high_difficulty_sop` | 高难度数学SOP | `{difficulty, time_block}` |
| `cross_subject_reminder` | 跨学科提醒 | `{topic, related_electronics}` |
| `weekly_error_analysis` | 周日错误分析 | `{aggregate}` |

---

## 统一错误模型

### 错误类型

| 错误类型 | 说明 | 标签 |
|----------|------|------|
| `condition_omission` | 条件遗漏 | `#condition_omission` |
| `method_error` | 方法误选 | `#method_error` |
| `calculation_error` | 计算失误 | `#calculation_error` |
| `logic_jump` | 推导跳步 | `#logic_jump` |

---

## MemOS标签系统

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#user_profile` | 用户画像 | 每用户1条 |
| `#mistake_record` | 错误历史 | 多条 |
| `#knowledge_card` | 知识点卡片 | 每知识点每用户1条 |
| `#kp_{knowledge_point}` | 知识点索引 | 多条 |
| `#mistake_type_{type}` | 错误类型索引 | 多条 |
| `#subject_math` | 数学学科标签 | 多条 |
| `#dispatch_signal` | 调度信号 | 多条 |

---

## 验证标准

1. ✅ 能够从MemOS加载用户上下文
2. ✅ 能够保存错误记录到MemOS
3. ✅ 能够生成个性化提醒
4. ✅ 能够检查用户画像新鲜度
5. ✅ 能够接收和处理调度信号
6. ✅ 能够生成跨学科提醒
7. ✅ 能够生成知识点关联
8. ✅ MemOS不可用时优雅降级
9. ✅ 统一错误模型学科标签正确

---

## 技能集成

### 被调用的技能

| 技能 | 调用场景 |
|------|----------|
| kaoyan-math-notes | 保存错误记录、获取个性化提醒 |
| kaoyan-math-structure | 获取知识点关系、跨学科关联 |

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-plan | 发送调度信号 |
| kaoyan-electronics | 跨学科知识关联 |

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
