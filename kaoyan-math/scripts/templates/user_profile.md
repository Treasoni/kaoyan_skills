---
# MemOS元数据 (v3.0.0)
user_id: {user_id}
conversation_id: {conversation_id}
created_at: {created_at}
updated_at: {updated_at}

# 标签
tags: [#user_profile, #user_{user_id}]
---

# 用户画像：考研数学学习

## 基本信息

### 考试信息
- **考试类型**：{exam_type}  # 数一 | 数二 | 数三
- **考试日期**：{exam_date}
- **距离考试**：{days_to_exam} 天

### 学习水平
- **当前水平**：{current_level}  # basic | intermediate | advanced
- **目标分数**：{target_score}

### 学习偏好
- **重点模块**：{focus_modules}  # [高数, 线代, 概率]
- **学习风格**：{learning_style}  # theory_first | practice_first | balanced

## 错误统计

### 总体统计
- **总错误次数**：{total_mistakes}
- **条件遗漏**：{condition_mistakes} 次
- **方法误选**：{method_mistakes} 次
- **计算失误**：{calculation_mistakes} 次
- **逻辑跳步**：{logic_jump_mistakes} 次

### 主要错误模式
1. **{main_mistake_1}** - {count1} 次
   - 触发场景：{trigger_1}
   - 防范措施：{prevention_1}

2. **{main_mistake_2}** - {count2} 次
   - 触发场景：{trigger_2}
   - 防范措施：{prevention_2}

## 知识点掌握情况

### 已掌握 ⭐⭐⭐
- {mastered_kp_1}
- {mastered_kp_2}
- {mastered_kp_3}

### 熟悉中 ⭐⭐
- {familiar_kp_1}
- {familiar_kp_2}
- {familiar_kp_3}

### 学习中 ⭐
- {learning_kp_1}
- {learning_kp_2}
- {learning_kp_3}

### 待学习 🆕
- {unfamiliar_kp_1}
- {unfamiliar_kp_2}
- {unfamiliar_kp_3}

## 学习历史

### 最近学习记录
| 日期 | 知识点 | 学习类型 | 掌握程度变化 |
|------|--------|----------|-------------|
| {date_1} | {kp_1} | {type_1} | {change_1} |
| {date_2} | {kp_2} | {type_2} | {change_2} |
| {date_3} | {kp_3} | {type_3} | {change_3} |

### 复习提醒
- 需要复习的知识点：{review_kps}
- 建议复习频率：{review_frequency}

## 学习配置

### 画像刷新配置
- **上次更新**：{last_refreshed}
- **自动刷新间隔**：30 天
- **待刷新**：{pending_refresh}

### 当前学习阶段
根据距离考试天数，当前处于：
- **阶段**：{current_phase}  # 基础期 | 强化期 | 冲刺期 | 极限冲刺期
- **阶段策略**：{phase_strategy}
- **建议重点**：{phase_focus}

## 学习建议

### 基于错误模式的建议
1. **条件遗漏问题**
   - 建议：学习定理时重点记忆适用条件
   - 方法：制作定理条件检查清单

2. **方法误选问题**
   - 建议：总结不同方法的适用场景
   - 方法：制作方法对比表

3. **计算失误问题**
   - 建议：增加练习量，提高计算熟练度
   - 方法：每日做10道计算题

### 基于学习进度的建议
- 当前阶段建议：{phase_suggestions}
- 重点关注模块：{focus_suggestions}
- 学习方法建议：{method_suggestions}

## 配置更新记录

| 日期 | 更新内容 | 更新人 |
|------|----------|--------|
| {update_date_1} | {update_content_1} | {updater_1} |
| {update_date_2} | {update_content_2} | {updater_2} |
