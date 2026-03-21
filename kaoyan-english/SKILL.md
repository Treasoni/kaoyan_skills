---
name: kaoyan-english
description: This skill routes English vocabulary learning requests to specialized sub-skills for 考研英语 (Chinese graduate entrance English exam) preparation. It handles vocabulary organization from PDF exports, spaced repetition schedules, quizzes, polysemy (rare word meanings) detection, word lookup, and writing output practice with MemOS integration for persistent tracking.
version: 4.0.0
---

# 考研英语技能路由器 (Kaoyan English Router)

## 技能概述

本技能是考研英语学习的**路由入口**，负责识别用户意图并路由到对应的子技能：

```
kaoyan-english (路由器)
    ↓ 识别意图后调用
    ├─→ kaoyan-english-core     (核心协调层：MemOS集成、调度信号)
    ├─→ kaoyan-english-vocab    (词汇整理+查词+PDF提取)
    ├─→ kaoyan-english-review   (复习计划+统计追踪)
    ├─→ kaoyan-english-quiz     (单词测试)
    └─→ kaoyan-english-writing  (写作输出训练)
```

## v4.0.0 更新说明

原技能（v3.2.0，约1830行）已拆分为5个独立子技能：
- **kaoyan-english-core**: MemOS集成管理、调度信号处理、记忆压缩模式
- **kaoyan-english-vocab**: PDF词汇提取、查词、熟词僻义检测、真题语境文章
- **kaoyan-english-review**: SM-2复习计划、统计追踪、分阶段策略
- **kaoyan-english-quiz**: 词义测试、搭配测试、僻义测试
- **kaoyan-english-writing**: 写作替换、汉译英、词义辨析

**拆分优势**：
- 每个子技能功能专注，易于维护
- 触发条件更精准，减少冲突
- 用户可直接调用特定功能的子技能

---

## 子技能速查

| 子技能 | 功能描述 | 触发关键词 |
|--------|----------|------------|
| **kaoyan-english-vocab** | 词汇整理+查词 | "整理单词"、"查单词"、"生成词汇表"、"PDF导出"、"真题语境文章"、"**处理单词表**"、"**格式化单词**"、"**分类单词**" |
| **kaoyan-english-review** | 复习计划+统计 | "复习计划"、"间隔重复"、"学习统计"、"今日复习"、"词汇统计" |
| **kaoyan-english-quiz** | 单词测试 | "单词测试"、"词汇quiz"、"测试单词"、"词义测试"、"僻义测试" |
| **kaoyan-english-writing** | 写作输出训练 | "写作替换"、"写作训练"、"高级词汇"、"汉译英"、"词义辨析" |
| **kaoyan-english-core** | 核心协调层 | "英语学习配置"、"英语状态"、"英语欠账检查"、"英语疲劳检查" |

---

## 路由逻辑

当用户请求涉及考研英语词汇学习时，本技能会：

1. **分析用户意图**：识别用户想要完成的具体任务
2. **选择子技能**：根据意图匹配最合适的子技能
3. **调用子技能**：将用户请求传递给对应的子技能处理
4. **返回结果**：将子技能的处理结果返回给用户

### 意图分类规则

```python
# 伪代码
def route_english_request(user_input):
    """路由英语学习请求"""

    # 1. 词汇整理/查词相关
    if any(keyword in user_input for keyword in [
        "整理单词", "查单词", "PDF导出", "真题语境文章",
        "墨墨背单词", "百词斩", "熟词僻义",
        "处理单词表", "格式化单词", "分类单词",  # 新增
        "整理单词表", "单词表整理", "单词整理",   # 新增
        "格式化单词表", "分类单词表"              # 新增
    ]):
        return invoke_skill("kaoyan-english-vocab", user_input)

    # 2. 复习计划/统计相关
    elif any(keyword in user_input for keyword in [
        "复习计划", "间隔重复", "学习统计", "今日复习",
        "词汇统计", "倒计时复习"
    ]):
        return invoke_skill("kaoyan-english-review", user_input)

    # 3. 测试相关
    elif any(keyword in user_input for keyword in [
        "单词测试", "词汇quiz", "测试单词", "词义测试",
        "僻义测试", "搭配测试"
    ]):
        return invoke_skill("kaoyan-english-quiz", user_input)

    # 4. 写作训练相关
    elif any(keyword in user_input for keyword in [
        "写作替换", "写作训练", "高级词汇", "汉译英",
        "词义辨析", "作文用词"
    ]):
        return invoke_skill("kaoyan-english-writing", user_input)

    # 5. 核心配置相关
    elif any(keyword in user_input for keyword in [
        "英语学习配置", "英语状态", "英语欠账检查",
        "英语疲劳检查", "英语进度"
    ]):
        return invoke_skill("kaoyan-english-core", user_input)

    # 6. 通用英语学习请求 - 智能推断
    elif "英语" in user_input or "English" in user_input:
        # 根据上下文推断用户意图
        context = analyze_context(user_input)
        return route_by_context(context)

    # 7. 默认：询问用户具体需求
    else:
        return ask_for_clarification()
```

---

## 使用示例

### 示例1: 词汇整理

**用户输入**："我整理了一批考研单词，想生成复习文章"

**路由流程**:
1. 识别关键词："整理单词"、"复习文章"
2. 匹配子技能：`kaoyan-english-vocab`
3. 调用子技能处理请求

### 示例2: 复习计划

**用户输入**："帮我生成今天的英语复习计划"

**路由流程**:
1. 识别关键词："复习计划"、"今天"
2. 匹配子技能：`kaoyan-english-review`
3. 调用子技能处理请求

### 示例3: 单词测试

**用户输入**："测试一下我最近学的单词"

**路由流程**:
1. 识别关键词："测试"、"单词"
2. 匹配子技能：`kaoyan-english-quiz`
3. 调用子技能处理请求

### 示例4: 写作训练

**用户输入**："我想练习写作词汇替换"

**路由流程**:
1. 识别关键词："写作"、"词汇替换"
2. 匹配子技能：`kaoyan-english-writing`
3. 调用子技能处理请求

---

## 直接调用子技能

用户也可以直接调用子技能，跳过路由器：

```markdown
# 直接调用示例
- 使用 kaoyan-english-vocab 查询单词 "address"
- 使用 kaoyan-english-review 生成今日复习计划
- 使用 kaoyan-english-quiz 进行词义测试
- 使用 kaoyan-english-writing 练习写作替换
- 使用 kaoyan-english-core 检查词汇欠账
```

---

## 技能集成

### 子技能依赖关系

```
kaoyan-english (路由器)
    ↓
    ├─→ kaoyan-english-core (MemOS集成，被其他技能调用)
    │        ↓
    │        ├─→ kaoyan-english-vocab (调用core保存词汇卡片)
    │        ├─→ kaoyan-english-review (调用core读取历史数据)
    │        ├─→ kaoyan-english-quiz (调用core记录测试结果)
    │        └─→ kaoyan-english-writing (调用core保存写作记录)
```

### 协同技能

| 技能 | 协同场景 |
|------|----------|
| kaoyan-plan | 提供每日计划时间分配，发送调度信号 |
| obsidian-markdown | 创建和管理Obsidian笔记 |
| pdf | 读取PDF单词导出 |
| docx | 生成Word文档导出 |

---

## 迁移说明

### 从 v3.2.0 迁移到 v4.0.0

**功能对等**：所有v3.2.0的功能在v4.0.0的子技能中都保留。

| v3.2.0 功能 | v4.0.0 子技能 |
|-------------|---------------|
| PDF词汇提取 | kaoyan-english-vocab |
| 熟词僻义检测 | kaoyan-english-vocab |
| 快速查词 | kaoyan-english-vocab |
| 真题语境文章 | kaoyan-english-vocab |
| SM-2复习计划 | kaoyan-english-review |
| 统计dashboard | kaoyan-english-review |
| 单词测试 | kaoyan-english-quiz |
| 写作替换练习 | kaoyan-english-writing |
| MemOS集成 | kaoyan-english-core |
| 调度信号处理 | kaoyan-english-core |

---

## 验证标准

1. ✅ 能够正确识别用户意图
2. ✅ 能够路由到正确的子技能
3. ✅ 子技能功能完整（不丢失原功能）
4. ✅ 用户使用体验不变
5. ✅ 支持直接调用子技能

---

## 文件路径

### 子技能文件

- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-core/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-vocab/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-review/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-quiz/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-english-writing/skill.md`

---

*创建日期: 2026-02-26*
*最后更新: 2026-03-18 (v4.0.1 添加单词表整理触发关键词)*
*维护者: Claude Code + 用户协作*
