---
name: kaoyan-electronics-core
description: 核心协调层 - 管理822电子技术基础的MemOS集成、调度信号处理、统一错误模型、跨学科知识关联（数学↔电子技术）、数学前置检查、考点权重与优先级算法
---

# 822电子技术基础 - 核心协调层 (Core)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能是822电子技术基础学习的核心协调层，负责：

1. **MemOS集成管理**：用户画像、错误记录持久化、知识点卡片
2. **调度信号处理**：接收并处理来自kaoyan-plan的调度信号
3. **统一错误模型**：电子技术错误记录的学科标签管理
4. **跨学科知识关联**：数学→电子技术知识图谱
5. **数学前置检查**：学习频率响应前检查复数运算基础
6. **考点权重与优先级算法**：动态分配复习时间

**设计原则**：
- 其他电子技术技能通过本技能访问MemOS
- 当MemOS不可用时自动降级
- 提供统一的错误记录和跨学科关联接口

---

## 触发条件

### 触发此技能当：

**用户画像相关**：
- "电子技术学习配置"
- "更新电子技术画像"
- "822配置"
- "专业课配置"

**状态检查相关**：
- "电子技术状态"
- "电子技术进度"
- "电子技术欠账检查"
- "专业课疲劳检查"

**跨学科相关**：
- "跨学科关联"
- "数学电子技术关联"
- "数学前置检查"

### 不触发此技能当：
- 分析电路图 → 使用 kaoyan-electronics-circuit
- 解题步骤/SOP → 使用 kaoyan-electronics-sop
- 查询知识点结构 → 使用 kaoyan-electronics-structure

---

## MemOS集成

### 核心原则
- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为无状态模式
- **数据持久化**: 错误记录、用户画像、学习历史均持久化存储

### MemOS功能特性
1. **用户画像追踪**: 记录考试类型（822）、目标院校（湖南大学）、学习偏好
2. **错误记录持久化**: 永久保存所有错误历史（电路误读、参数混淆、计算错误、条件遗漏）
3. **个性化提醒**: 基于历史错误生成千人千面的提示
4. **知识点卡片追踪**: 记录每个知识点的掌握程度和考试权重
5. **画像刷新机制**: 30天未更新时提示确认学习配置

### 数据模型

```yaml
# 用户画像
user_profile:
  user_id: string
  exam_type: "822电子技术基础"
  target_school: "湖南大学"
  exam_date: date
  focus_modules: [模电, 数电]
  days_to_exam: int  # 距离考试天数

# 错误记录
mistake_record:
  knowledge_point: string  # 如："负反馈类型判断"
  mistake_type: enum
    - concept_confusion    # 概念混淆
    - calculation_error    # 计算错误
    - circuit_misread      # 电路误读
    - forgot_condition     # 忘记条件
  original_understanding: string
  correction: string
  timestamp: datetime

# 知识点卡片（增强版）
knowledge_card:
  knowledge_point: string
  module: 模电|数电
  mastery_level: int  # 0-100
  mistake_count: int
  exam_frequency: int  # 1-10，考试频率权重
  exam_importance: int  # 1-10，考试重要性
  days_to_exam: int  # 距离考试天数
  priority_score: int  # 综合优先级
  sop_templates: [string]  # 关联的SOP模板
  related_points: [string] # 关联知识点
```

### 降级行为
当MemOS不可用时：
- ✅ 基础功能正常工作
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用个性化错误模式追踪

---

## 考点权重与优先级算法

### 优先级计算公式

每日任务生成时，根据以下公式计算知识点优先级：

$$
\text{priority\_score} = \frac{\text{exam\_frequency} \times \text{exam\_importance}}{\text{mastery\_level} + 1} \times \alpha
$$

其中：
- $\alpha$：时间衰减因子
  - 距离考试 > 180天：$\alpha = 0.8$（基础阶段）
  - 距离考试 90-180天：$\alpha = 1.0$（强化阶段）
  - 距离考试 30-90天：$\alpha = 1.5$（冲刺阶段）
  - 距离考试 < 30天：$\alpha = 2.0$（押题阶段）

### 任务分配策略

| 优先级分数 | 每日建议时间 | 策略 |
|-----------|-------------|------|
| > 50 | 60-90分钟 | 重点突破，每天必练 |
| 20-50 | 30-45分钟 | 强化训练，隔天练习 |
| 10-20 | 15-20分钟 | 保持手感，每周复习 |
| < 10 | 0-10分钟 | 考前突击，考前一周 |

### 高频考点清单

⚠️ 以下知识点为**必考大题**，务必重点掌握：

**模电必考**：
1. 反馈放大器 - 反馈类型判断 + 深度负反馈计算
2. 基本放大器 - 静态分析 + 动态分析
3. 集成运放 - 虚短虚断应用

**数电必考**：
1. 时序逻辑电路 - 分析与设计
2. 计数器 - 设计与分析
3. 触发器 - 特性方程应用
4. 组合逻辑电路 - 分析与设计

### 权重配置文件

详细权重配置见：`/kaoyan-electronics/scripts/data/exam_weights.yaml`

---

## 数学前置检查

学习电子技术某些内容前，自动检查数学基础是否扎实。

### 前置知识映射

```yaml
MATH_PREREQUISITES:
  "频率响应分析":
    required_math:
      - topic: "复数运算"
        level: "basic"
        check: "能正确进行复数加减乘除运算"
        refresher: "复数运算回顾：j²=-1, Z=R+jX"
      - topic: "对数运算"
        level: "basic"
        check: "能理解对数坐标（波特图）"
        refresher: "对数坐标：20log|H(jω)|"
    warning: "⚠️ 开始「频率响应」前，建议先确认数学基础是否扎实"

  "暂态响应":
    required_math:
      - topic: "微分方程"
        level: "intermediate"
        check: "能求解一阶线性微分方程"
        refresher: "一阶RC方程：τ·du/dt + u = U"
      - topic: "指数函数"
        level: "basic"
        check: "理解指数函数的图像和性质"
        refresher: "指数衰减：e^(-t/τ)"
    warning: "⚠️ 「暂态响应」需要微分方程基础"

  "滤波器设计":
    required_math:
      - topic: "拉普拉斯变换"
        level: "intermediate"
        check: "理解s域分析"
        refresher: "传递函数：H(s)=Uo(s)/Ui(s)"
    warning: "⚠️ 「滤波器设计」需要拉普拉斯变换基础"
```

### 前置检查函数

详细实现见 [code.md](code.md) 中的 `check_math_prerequisites` 函数。

---

## 跨学科提醒

### 数学关联提醒

学习电子技术时，主动提示相关的数学知识。

```python
def generate_math_reminder(electronics_topic):
    """生成数学关联提醒"""
    reminders = {
        "频率响应": {
            "math_topic": "复数运算",
            "reminder": "⚠️ 「频率响应」分析需要「复数运算」基础",
            "key_point": "阻抗 Z = R + jX，幅值 |Z| = √(R²+X²)",
            "exam_tip": "波特图绘制需要掌握对数坐标转换"
        },
        "暂态响应": {
            "math_topic": "微分方程",
            "reminder": "💡 「暂态响应」本质是「微分方程」在电路中的应用",
            "key_point": "时间常数 τ = RC，uc(t) = U₀(1-e^(-t/τ))",
            "exam_tip": "牢记τ的物理意义：达到63.2%终值的时间"
        },
        "RC电路": {
            "math_topic": "积分",
            "reminder": "「RC电路」充放电涉及「积分」概念",
            "key_point": "电容储能 W = (1/2)CU²"
        }
    }
    return reminders.get(electronics_topic)
```

### 跨学科提醒显示格式

```markdown
## ⚠️ 跨学科提醒

> 当前学习：**频率响应分析**
>
> **数学基础**：复数运算
>
> **关键点**：
> - 阻抗 Z = R + jX
> - 幅值 |Z| = √(R²+X²)
> - 相角 φ = arctan(X/R)
>
> **考试提示**：波特图绘制需要掌握对数坐标转换
>
> 💡 建议先复习 [[复数运算]] 再深入学习频率响应
```

### 数学→电子技术知识图谱

| 数学知识点 | 关联的电子技术知识点 | 重要性 |
|------------|---------------------|--------|
| 复数运算 | 频率响应分析、交流电路、滤波器设计、阻抗计算 | ⚠️ Critical |
| 微分方程 | 暂态响应、RC/RL电路、一阶电路分析 | 💡 High |
| 积分 | RC充放电、能量计算、电容储能 | Medium |
| 拉普拉斯变换 | s域分析、传递函数、频域分析 | ⚠️ High |

---

## 统一错误模型集成

### 学科标签

所有错误记录添加学科标签以支持跨技能聚合。

```python
def save_unified_electronics_mistake(mistake_data, user_id):
    """保存电子技术错误记录（统一格式）"""
    mistake_data["subject"] = "electronics"

    # 电子技术专用错误类型
    if mistake_data.get("type") == "circuit_misread":
        mistake_data["tags"].append("#circuit_misread")
    elif mistake_data.get("type") == "parameter_confusion":
        mistake_data["tags"].append("#param_confusion")

    # 查找数学关联
    cross_refs = find_math_refs(mistake_data.get("knowledge_point"))
    if cross_refs:
        mistake_data["cross_subject_refs"] = cross_refs

    # 保存到MemOS
    add_message(messages=[{...}], user_id=user_id)
```

### 电子技术专用错误类型

| 错误类型 | 说明 | 标签 |
|----------|------|------|
| `circuit_misread` | 电路误读 | `#circuit_misread` |
| `parameter_confusion` | 参数混淆（如rbe与re） | `#param_confusion` |
| `calculation_error` | 计算错误 | `#calculation` |
| `condition_omission` | 条件遗漏 | `#condition` |
| `concept_confusion` | 概念混淆 | `#concept` |

---

## 调度信号处理

### 检查调度信号

从kaoyan-plan接收调度信号并执行相应动作。

详细实现见 [code.md](code.md) 中的 `check_dispatch_signals` 和 `process_dispatch_signal` 函数。

### 支持的调度动作

| 动作名 | 说明 | 上下文参数 |
|--------|------|------------|
| `check_math_prerequisites` | 数学前置检查 | `{topic, required_math}` |
| `circuit_analysis_sop` | 电路分析SOP | `{circuit_type}` |
| `weekly_error_analysis` | 周日错误分析 | `{aggregate}` |

---

## 📁 详细模块文档

| 模块 | 文件 | 内容 |
|------|------|------|
| 代码实现 | [code.md](code.md) | MemOS集成函数、数学前置检查、跨学科关联、调度信号处理、统一错误模型 |

---

## MemOS标签系统

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#user_profile` | 用户画像 | 每用户1条 |
| `#mistake_record` | 错误历史 | 多条 |
| `#knowledge_card` | 知识点卡片 | 每知识点每用户1条 |
| `#kp_{knowledge_point}` | 知识点索引 | 多条 |
| `#mistake_type_{type}` | 错误类型索引 | 多条 |
| `#subject_electronics` | 电子技术学科标签 | 多条 |
| `#dispatch_signal` | 调度信号 | 多条 |

---

## 验证标准

1. ✅ 能够从MemOS加载用户上下文
2. ✅ 能够保存错误记录到MemOS
3. ✅ 能够生成个性化提醒
4. ✅ 能够检查用户画像新鲜度
5. ✅ 能够接收和处理调度信号
6. ✅ 能够生成跨学科提醒
7. ✅ 能够执行数学前置检查
8. ✅ MemOS不可用时优雅降级
9. ✅ 统一错误模型学科标签正确

---

## 技能集成

### 被调用的技能

| 技能 | 调用场景 |
|------|----------|
| kaoyan-electronics-sop | 保存错误记录、获取个性化提醒 |
| kaoyan-electronics-structure | 获取知识点关系、跨学科关联 |
| kaoyan-electronics-circuit | 电路分析错误记录 |

### 依赖技能

| 技能 | 用途 |
|------|------|
| kaoyan-plan | 发送调度信号 |
| kaoyan-math-core | 跨学科知识关联（数学基础） |

---

*创建日期: 2026-03-12*
*版本: 1.0.0*
