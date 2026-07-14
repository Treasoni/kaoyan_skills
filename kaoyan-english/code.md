# 考研英语技能路由器 - 实现代码

## 路由逻辑

### 意图分类规则

```python
# 伪代码
def route_english_request(user_input):
    """路由英语学习请求"""

    # 0. 【最高优先级】检测文件路径 - 默认执行完整词汇处理流程
    if is_file_path(user_input) or is_directory_path(user_input):
        # 自动执行完整的词汇处理流程，不询问用户
        return execute_full_vocab_workflow(user_input)

    # 1. 词汇整理/查词相关 - 执行完整流程
    if any(keyword in user_input for keyword in [
        "整理单词", "查单词", "PDF导出", "真题语境文章",
        "墨墨背单词", "百词斩", "熟词僻义",
        "处理单词表", "格式化单词", "分类单词",
        "整理单词表", "单词表整理", "单词整理",
        "格式化单词表", "分类单词表"
    ]):
        return execute_full_vocab_workflow(user_input)  # 执行完整流程

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

    # 6. 通用英语学习请求 - 默认执行完整流程
    elif "英语" in user_input or "English" in user_input or "单词" in user_input:
        # 默认执行完整词汇处理流程
        return execute_full_vocab_workflow(user_input)

    # 7. 默认：执行完整词汇处理流程（不再询问）
    else:
        return execute_full_vocab_workflow(user_input)


def execute_full_vocab_workflow(user_input):
    """执行完整的词汇处理流程"""

    # ⚠️ 步骤0: Day 编号计算（必须首先执行！）
    #   - 从用户输入的文件路径中提取日期
    #   - 调用 kaoyan-english-core 的 Day 计算模块
    #   - 双重验证：日期计算 + 现有文件检查
    #   - 生成四类文件的统一文件名
    #
    #   from kaoyan_english_core.day_calculator import (
    #       get_validated_day_number,
    #       generate_day_filenames
    #   )
    #
    #   target_date = extract_date_from_path(user_input)  # 例如 "2026-04-06"
    #   day_number = get_validated_day_number(target_date, "考研英语/📰 真题语境文章")
    #   filenames = generate_day_filenames(target_date, day_number)
    #
    #   禁止事项：
    #   - ❌ 禁止手动硬编码 Day 编号（如直接写 "Day-001"）
    #   - ❌ 禁止跳过 Day 编号计算步骤
    #   - ❌ 禁止使用错误的 Day 编号

    # 步骤1: 整理和格式化单词表
    #   - 读取用户提供的单词表文件
    #   - 按词族分类
    #   - 按考频分级（⭐至⭐⭐⭐）
    #   - 添加记忆方法（词根词缀法）
    #   - 补充词组搭配
    #   - 标记僻义预警
    #   - 更新原始文件
    #   - 输出路径: 考研英语/英语单词/{日期}-整理版.md

    # 步骤2: 生成四类笔记（⚠️ 使用步骤0计算的 Day 编号！）
    #   - 📊 词汇统计 → 考研英语/📊 词汇统计/Statistics-Day-{day_number}-{target_date}.md
    #   - 📰 真题语境文章 → 考研英语/📰 真题语境文章/Context-Day-{day_number}-{target_date}.md
    #   - 📝 测试记录 → 考研英语/📝 测试记录/Quiz-Day-{day_number}-{target_date}.md
    #   - ✍️ 写作输出 → 考研英语/✍️ 写作输出/Writing-Day-{day_number}-{target_date}.md

    # 步骤3: 更新学习进度
    #   - 更新 考研英语/📊 学习进度.md

    return "完整词汇处理流程执行完成"


def is_file_path(user_input):
    """检测是否为文件路径"""
    return "/" in user_input or user_input.endswith(".md")


def is_directory_path(user_input):
    """检测是否为目录路径"""
    return "/" in user_input and not user_input.endswith(".md")
```

---

## 文件输出路径规范

> **强制要求**：生成四类笔记时，**必须**放到以下对应的文件夹中，**禁止**放到其他位置！

| 笔记类型 | 文件名格式 | **必须存放的路径** |
|----------|-----------|-------------------|
| 📊 词汇统计 | `Statistics-Day-{XXX}-{YYYY-MM-DD}.md` | `考研英语/📊 词汇统计/` |
| 📰 真题语境文章 | `Context-Day-{XXX}-{YYYY-MM-DD}.md` | `考研英语/📰 真题语境文章/` |
| 📝 测试记录 | `Quiz-Day-{XXX}-{YYYY-MM-DD}.md` | `考研英语/📝 测试记录/` |
| ✍️ 写作输出 | `Writing-Day-{XXX}-{YYYY-MM-DD}.md` | `考研英语/✍️ 写作输出/` |
| 整理版单词表 | `{日期}-整理版.md` | `考研英语/英语单词/` |

### 错误示例（禁止！）

```
❌ 考研英语/英语单词/Statistics-Day-027-2026-03-27.md  # 错误位置！
❌ 考研英语/英语单词/Context-Day-027-2026-03-27.md     # 错误位置！
```

### 正确示例

```
✅ 考研英语/📊 词汇统计/Statistics-Day-027-2026-03-27.md
✅ 考研英语/📰 真题语境文章/Context-Day-027-2026-03-27.md
✅ 考研英语/📝 测试记录/Quiz-Day-027-2026-03-27.md
✅ 考研英语/✍️ 写作输出/Writing-Day-027-2026-03-27.md
✅ 考研英语/英语单词/2026-3-27-整理版.md
```

---

## 编码规范（避免乱码）

> **强制要求**：生成包含中文的文件时，必须检查是否有乱码！

### 常见乱码模式

| 乱码 | 正确内容 | 说明 |
|-----|---------|------|
| `足��` | `足够` | 字符被截断 |
| `满��地` | `满意地` | 字符被截断 |

### 文件生成后验证

1. 读取生成的文件内容
2. 检查是否包含乱码字符（如 `���`、`��` 等）
3. 如果发现乱码，立即修复

---

## 整理版单词表模板格式规范

详细模板格式规范请参考：`kaoyan-english-vocab` 技能文件中的 **"⚠️ 整理版单词表模板格式规范"** 部分

### 核心格式要点

| 要素 | 格式要求 |
|------|----------|
| **标题** | `# 考研英语单词表 - Day XX` |
| **元信息** | 日期、词汇量、来源、距离考试天数 |
| **频率分级** | `## ⭐⭐⭐/⭐⭐/⭐` 三级分类 |
| **词族分组** | `### 词族N: xxx族（X词）` |
| **单词标题** | `#### 单词名 ⭐⭐⭐` |
| **词性释义** | `**词性** 释义` |
| **词组搭配** | 表格格式 `| 词组搭配 | 释义 |` |
| **记忆方法** | `> 🧠 **记忆方法**` callout（必须！） |
| **僻义预警** | `> ⚠️ **僻义预警** [warning/critical]` |
| **分隔线** | 每个单词后用 `---` |
| **统计信息** | `## 📊 统计信息` 表格 |
| **僻义汇总** | `## ⚠️ 僻义预警汇总` |

### 禁止事项

- ❌ 省略记忆方法（所有单词必须有！）
- ❌ 省略词族分类
- ❌ 省略统计信息
- ❌ 使用非标准标题格式
