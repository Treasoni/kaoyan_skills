---
name: kaoyan-electronics
description: 湖南大学822电子技术基础考研学习技能 - 支持电路图智能解析、典型题型SOP库、知识图谱主动关联、MemOS记忆追踪
version: 1.2.0
author: Claude Code
dependencies:
  - MemOS集成
  - 电路图识别MCP工具
tags:
  - 考研
  - 电子技术基础
  - 822
  - 湖南大学
  - 模电
  - 数电
  - 电路图分析
  - MemOS
---

# 822电子技术基础学习技能 v1.1.0

> 专为湖南大学822电子技术基础考研设计，集成电路图智能解析、标准化SOP流程、知识点图谱与MemOS记忆追踪系统。

## 考试概述

- **考试代码**: 822电子技术基础
- **目标院校**: 湖南大学
- **参考教材**: 康华光《电子技术基础》（第7版）模拟部分 + 数字部分
- **考试分值**: 模电约50% + 数电约50%

## 考试范围

### 模电部分

1. **基本电子器件** - 二极管、稳压管、场效应管、BJT特性
2. **基本放大器** - 静态工作点、$A_u$、$R_i$、$R_o$、频率响应
3. **差分放大器** - $A_{ud}$、$A_{uc}$、$K_{CMRR}$
4. **功率放大器** - 效率$\eta$、$P_{om}$、交越失真
5. **集成运放** - 比例、加法、减法、有源滤波、电压比较
6. **反馈放大器** - 反馈类型判断、深度负反馈增益计算
7. **波形产生电路** - 正弦波、非正弦波产生
8. **线性稳压电源** - 构成、功能分析、参数计算

### 数电部分

1. **数制与代码** - 二进制、十进制、十六进制转换
2. **逻辑运算** - 代数法、卡诺图化简
3. **基本逻辑单元** - 逻辑门、触发器（RS/JK/D/T/T'）
4. **组合逻辑单元** - 编码器、译码器、选择器、比较器、运算器
5. **时序逻辑电路** - 计数器、移位寄存器
6. **逻辑电路设计** - 组合逻辑分析设计、同步时序分析设计
7. **存储器** - 分类、特性、容量扩展
8. **脉冲电路** - 单稳态、多谐振荡器、施密特触发器
9. **A/D D/A转换** - 分类、原理、参数、应用

---

## MemOS集成说明 (v1.0.0)

本技能集成MemOS系统，提供跨设备同步的学习进度追踪和个性化错误提醒。

### MemOS核心函数

```yaml
# 记录错误到MemOS
record_mistake(knowledge_point, mistake_type, original_understanding, correction)

# 获取用户错误历史
get_user_mistakes(user_id, knowledge_point=None)

# 生成个性化提醒
generate_personalized_reminders(user_id)

# 更新知识点掌握度
update_mastery_level(user_id, knowledge_point, delta)
```

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
  priority_score: int  # 综合优先级 = exam_frequency × exam_importance / (mastery_level + 1) × α
  sop_templates: [string]  # 关联的SOP模板
  related_points: [string] # 关联知识点
```

### 优雅降级

当MemOS不可用时，技能自动降级为本地模式：
- 错误记录存储在当前会话
- 个性化提醒基于当前对话历史
- 不影响核心学习功能

### 个性化提醒示例

```
⚠️ 你在"反馈类型判断"方面已出错5次
   - 混淆电压反馈和电流反馈的判断方法
   - 提醒：短路输出端法是关键

⚠️ 你在"计数器设计"方面已出错3次
   - 忘记检查自启动特性
   - 提醒：无效状态必须能进入有效循环
```

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

### 权重配置示例

- 反馈类型判断：exam_frequency=10, exam_importance=10（必考大题）
- 存储器扩展：exam_frequency=2, exam_importance=3（低频考点）

详细权重配置见：`scripts/data/exam_weights.yaml`



---

## 电路图识别功能说明

本技能支持电路图智能解析，通过MCP工具实现电路结构识别和参数提取。

### 支持的输入方式

1. **电路图截图** - 上传电路图图片
2. **文字描述** - 用文字描述电路结构

### 处理流程

```
【电路图截图/文字描述】
      ↓
【MCP工具识别】understand_technical_diagram + extract_text_from_screenshot
      ↓
【提取元件信息】电阻、电容、晶体管、运放等
      ↓
【分析电路拓扑】连接关系、信号流向
      ↓
【生成结构化笔记】静态分析 + 动态分析
```

### 模电电路分析标准流程

#### 1. 静态分析
计算直流工作点：
- BJT: $I_B$、$I_C$、$U_{CE}$
- FET: $I_D$、$U_{GS}$、$U_{DS}$

#### 2. 动态分析
画微变等效电路：
- 计算增益 $A_u = \frac{U_o}{U_i}$
- 计算输入电阻 $R_i$
- 计算输出电阻 $R_o$

#### 3. 频率响应
分析$f_L$、$f_H$、$BW$

### 数电电路分析标准流程

#### 1. 组合逻辑
- 写逻辑表达式
- 卡诺图化简
- 画逻辑图
- 功能扩展

#### 2. 时序逻辑
- 写驱动方程
- 写状态方程
- 画状态转换图
- 分析自启动

---

## 康华光教材符号体系优先

> ⚠️ **重要**: 本技能严格遵循康华光《电子技术基础》（第7版）符号体系，避免与其他教材混淆。

### 符号对照表

| 物理量 | 康华光符号 | 说明 |
|--------|-----------|------|
| 基极静态电流 | $I_{BQ}$ | 下标Q表示静态(Quiescent) |
| 集电极静态电流 | $I_{CQ}$ | 下标Q表示静态 |
| 集射极静态电压 | $U_{CEQ}$ | 下标Q表示静态 |
| BJT输入电阻 | $r_{be}$ | 小写r表示动态电阻 |
| 跨导 | $g_m$ | 场效应管参数 |
| 夹断电压 | $U_{GS(off)}$ | FET参数 |
| 开启电压 | $U_{GS(th)}$ | MOSFET参数 |

### 关键转换关系

$$
r_{be} = r_{bb'} + (1+\beta)\frac{26}{I_E}
$$

$$
g_m = \frac{I_D}{U_{GS(th)}}
$$

### 与其他教材的区别

| 康华光 | 其他教材 | 说明 |
|--------|----------|------|
| $r_{be}$ | $h_{ie}$ | BJT输入电阻 |
| $U_{GS(off)}$ | $U_P$ | 夹断电压 |
| $U_{GS(th)}$ | $U_T$ | 开启电压 |
| $I_{BQ}$ | $I_B$ | 静态基极电流（Q下标） |

⚠️ AI在分析电路时，**必须使用康华光符号体系**，不得使用其他教材的符号表示。

---

## LaTeX电子符号标准

### 基本器件符号

| 器件 | LaTeX | 说明 |
|------|-------|------|
| 电阻 $R$ | `R` | 欧姆 |
| 电容 $C$ | `C` | 法拉 |
| 电感 $L$ | `L` | 亨利 |
| 二极管 $D$ | `D` | - |
| 三极管 $T$ | `T` | BJT |
| 场效应管 $FET$ | `FET` | MOSFET/JFET |
| 运放 $A$ | `A` | Op-Amp |

### 模电常用公式

```markdown
# 静态工作点
$$
I_B = \frac{V_{CC} - U_{BE}}{R_b}
$$
$$
I_C = \beta I_B
$$
$$
U_{CE} = V_{CC} - I_C R_c
$$

# 电压增益
$$
A_u = \frac{U_o}{U_i} = -\frac{\beta R'_L}{r_{be}}
$$

# 反馈深度
$$
F = 1 + AF
$$

# 共模抑制比
$$
K_{CMRR} = \left| \frac{A_{ud}}{A_{uc}} \right|
$$
```

### 数电常用公式

```markdown
# 逻辑函数
$$
Y = A \cdot B + C \cdot D
$$

# 卡诺图相邻项
$$
ABC + AB\overline{C} = AB(C + \overline{C}) = AB
$$

# 触发器特性方程
$$
Q^{n+1} = JQ^n + \overline{K}Q^n \quad (JK)
$$
$$
Q^{n+1} = D \quad (D触发器)
$$
```

---

## 核心功能设计

### 功能1: 电路图智能解析

**触发条件**: 用户上传电路图截图或描述电路结构

**处理步骤**:
1. 使用 `understand_technical_diagram` 识别电路结构
2. 使用 `extract_text_from_screenshot` 提取元件参数
3. 根据电路类型选择对应SOP
4. 生成结构化分析笔记

**输出格式**:
```markdown
# [电路类型]分析

## 电路识别
- 类型：[电路类型]
- 元件：[元件列表及参数]

## 静态分析
[静态分析过程和结果]

## 动态分析
[动态分析过程和结果]

## 频率响应/自启动检查
[相应分析]
```

### 功能2: 典型题型SOP库

本技能包含17个考点的标准化SOP模板，确保答题规范、完整。

**使用方法**:
1. 识别题目类型
2. 调用对应SOP模板
3. 按步骤执行
4. 检查是否遗漏条件

**SOP模板列表**:
- SOP1: 共射放大电路分析
- SOP2: 负反馈类型判断
- SOP3: 运算电路分析
- SOP4: 逻辑函数化简
- SOP5: 时序逻辑电路分析
- ... (详见SOP模板库)

### 功能3: 知识图谱主动关联

本技能内置模电和数电知识图谱，主动提示知识点之间的关联。

**触发场景**:
- 用户学习某知识点时，主动提示前置知识
- 提示跨章节关联
- 建议练习题型

**示例**:
```yaml
学习"负反馈放大器"时提示:
  prerequisites:
    - 基本放大器
    - 频率响应
  cross_chapter_prompts:
    - "注意：深度负反馈是高频考点"
    - "提醒：反馈类型判断是难点，需要大量练习"
```

---

## 用户工作流

### 场景1: 分析电路图

```yaml
用户: [上传电路图] 帮我分析这个电路

AI处理:
  1. understand_technical_diagram(电路图)
  2. extract_text_from_screenshot(电路图)
  3. 识别电路类型 -> 选择SOP
  4. 按SOP步骤分析
  5. 生成LaTeX格式笔记

AI输出:
  - 电路结构识别
  - 静态分析（含公式）
  - 动态分析（含公式）
  - 结论与要点
```

### 场景2: 解题指导

```yaml
用户: 这道题怎么做？[题目描述]

AI处理:
  1. 识别题目类型
  2. 调用对应SOP
  3. 按步骤引导
  4. 检查用户错误
  5. 记录到MemOS（如可用）

AI输出:
  - 解题步骤
  - 关键公式
  - 常见错误提醒
  - 相关练习建议
```

### 场景3: 知识点复习

```yaml
用户: 帮我复习负反馈

AI处理:
  1. 加载负反馈知识图谱
  2. 显示前置知识
  3. 显示核心概念
  4. 显示跨章节关联
  5. 提供练习题

AI输出:
  - 知识点卡片
  - 前置知识检查
  - 核心公式/方法
  - 关联提示
  - 练习题
```

---

## 笔记格式标准

### 模电笔记格式

```markdown
# [知识点名称]

## 基本概念
[定义、原理]

## 核心公式
$$
[公式1]
$$
$$
[公式2]
$$

## 分析方法
1. 步骤一
2. 步骤二
3. 步骤三

## 常见题型
- 题型1: [描述]
- 题型2: [描述]

## 注意事项
- ⚠️ [注意点1]
- ⚠️ [注意点2]

## 关联知识点
- [知识点1]
- [知识点2]
```

### 数电笔记格式

```markdown
# [知识点名称]

## 功能描述
[功能、应用]

## 真值表/状态表
| 输入 | 输出 |
|------|------|
| ... | ... |

## 逻辑表达式
$$
[表达式]
$$

## 工作波形
[描述波形变化]

## 典型应用
- 应用1: [描述]
- 应用2: [描述]

## 注意事项
- ⚠️ [注意点1]
- ⚠️ [注意点2]
```

---

## SOP模板库

### 模电SOP

#### SOP1: 共射放大电路分析

```markdown
## 步骤1: 计算静态工作点
- 基极回路: $I_B = \frac{V_{CC} - U_{BE}}{R_b}$
- 集电极电流: $I_C = \beta I_B$
- 管压降: $U_{CE} = V_{CC} - I_C R_c$

## 步骤2: 画微变等效电路
- BJT用h参数模型替代
- 电容视为短路
- 直流电源对地短路

## 步骤3: 计算动态指标
- $A_u = -\frac{\beta R'_L}{r_{be}}$
- $R_i = R_b // r_{be}$
- $R_o = R_c$

## 步骤4: 频率响应分析
- $f_L$: 低频截止频率
- $f_H$: 高频截止频率
- $BW = f_H - f_L$
```

#### SOP2: 负反馈类型判断

```markdown
## 步骤1: 判断输出取样方式
- 短路输出端→若反馈信号消失→电压反馈
- 短路输出端→若反馈信号仍存在→电流反馈

## 步骤2: 判断输入比较方式
- 反馈信号与输入信号串联→串联反馈
- 反馈信号与输入信号并联→并联反馈

## 步骤3: 判断反馈极性
- 瞬时极性法→净输入减小→负反馈
- 瞬时极性法→净输入增大→正反馈

## 步骤4: 计算深度负反馈增益
$$
A_{uf} \approx \frac{1}{F}
$$
```

#### SOP3: 运算电路分析

```markdown
## 步骤1: 识别运放工作状态
- 线性区→虚短（$U_+ = U_-$）
- 线性区→虚断（$I_+ = I_- = 0$）

## 步骤2: 列节点电流方程
- $I_1 + I_2 + ... = I_f$

## 步骤3: 推导输入输出关系
- 利用虚短虚断条件
- 求解 $U_o = f(U_i)$

## 步骤4: 验证结果
- 检查量纲是否正确
- 检查特殊情况是否合理
```

### 数电SOP

#### SOP4: 逻辑函数化简

```markdown
## 步骤1: 写出逻辑表达式
- 从真值表或逻辑图写出

## 步骤2: 填卡诺图
- 按变量数选择卡诺图规模
- 正确填入函数值

## 步骤3: 圈组化简
- 按2^n圈组（n=0,1,2,...）
- 每个圈尽可能大
- 圈的个数尽可能少

## 步骤4: 写最简表达式
- 每个圈对应一个乘积项
- 所有圈相或
```

#### SOP5: 时序逻辑电路分析

```markdown
## 步骤1: 写驱动方程
- 从电路图写出各触发器的输入方程

## 步骤2: 写状态方程
- 将驱动方程代入触发器特性方程

## 步骤3: 写输出方程
- 确定电路输出与状态的关系

## 步骤4: 画状态转换图
- 列出所有现态和次态
- 画出转换关系

## 步骤5: 检查自启动
- 检查无效状态能否进入有效循环
```

---

## 知识点图谱

### 模电知识图谱

```yaml
基本放大器:
  prerequisites:
    - BJT/FET特性曲线
    - 直流工作点概念
  combinations:
    - 多级放大
    - 负反馈
  applications:
    - 差分放大
    - 功率放大
  cross_chapter_prompts:
    - "注意：掌握三种基本组态（共射/共基/共集）的对比"
    - "建议：静态分析和动态分析要分开进行"

负反馈放大器:
  prerequisites:
    - 基本放大器
    - 频率响应
  combinations:
    - 运算电路
    - 波形产生
  applications:
    - 稳定增益
    - 展宽频带
  cross_chapter_prompts:
    - "注意：深度负反馈是高频考点"
    - "提醒：反馈类型判断是难点，需要大量练习"
    - "关联：负反馈改善性能的本质是牺牲增益"

差分放大器:
  prerequisites:
    - 共射/共基放大
    - 对称性概念
  combinations:
    - 集成运放
  applications:
    - 直流放大
    - 抑制共模干扰
  cross_chapter_prompts:
    - "注意：共模抑制比是关键指标"
    - "提醒：掌握双入双出、单入双出等四种接法"

功率放大器:
  prerequisites:
    - 基本放大器
    - 图解法
  combinations:
    - OCL电路
    - OTL电路
  applications:
    - 音频放大
    - 电机驱动
  cross_chapter_prompts:
    - "注意：甲类、乙类、甲乙类的效率对比"
    - "提醒：交越失真的消除方法"

集成运放:
  prerequisites:
    - 差分放大
    - 负反馈
  combinations:
    - 运算电路
    - 有源滤波
  applications:
    - 信号运算
    - 信号处理
  cross_chapter_prompts:
    - "注意：虚短虚断是解题关键"
    - "提醒：线性应用和非线性应用要区分"

波形产生电路:
  prerequisites:
    - 集成运放
    - 正反馈
  combinations:
    - 正弦波振荡
    - 非正弦波产生
  applications:
    - 信号源
    - 时钟发生
  cross_chapter_prompts:
    - "注意：起振条件和平衡条件"
    - "提醒：RC、LC、石英晶体振荡器的特点"

稳压电源:
  prerequisites:
    - 二极管特性
    - 运算放大器
  combinations:
    - 串联型稳压
    - 开关型稳压
  applications:
    - 直流电源
    - 适配器
  cross_chapter_prompts:
    - "注意：稳压系数和输出电阻的计算"
    - "提醒：保护电路的作用"
```

### 数电知识图谱

```yaml
逻辑运算与化简:
  prerequisites:
    - 数制转换
    - 逻辑代数基础
  combinations:
    - 组合逻辑设计
    - PLA设计
  applications:
    - 逻辑化简
    - 逻辑设计
  cross_chapter_prompts:
    - "注意：卡诺图适用于4-6变量函数"
    - "提醒：无关项的处理是重要考点"
    - "关联：化简后要用与非门等实现"

组合逻辑电路:
  prerequisites:
    - 逻辑门
    - 逻辑化简
  combinations:
    - 编码器
    - 译码器
    - 选择器
  applications:
    - 数据处理
    - 地址译码
  cross_chapter_prompts:
    - "注意：分析从输入到输出，设计从输出到输入"
    - "提醒：使能端的作用要掌握"

触发器:
  prerequisites:
    - 逻辑门
    - 时钟概念
  combinations:
    - 时序逻辑
    - 计数器
  applications:
    - 数据存储
    - 状态记忆
  cross_chapter_prompts:
    - "注意：各触发器特性方程要牢记"
    - "提醒：异步置数端优先级最高"

时序逻辑电路:
  prerequisites:
    - 触发器
    - 组合逻辑
  combinations:
    - 计数器
    - 移位寄存器
  applications:
    - 频率测量
    - 序列检测
  cross_chapter_prompts:
    - "注意：同步和异步时序的区别"
    - "提醒：自启动检查必不可少"

计数器:
  prerequisites:
    - 触发器特性
    - 时钟概念
  combinations:
    - 译码器
    - 显示电路
  applications:
    - 频率测量
    - 定时控制
  cross_chapter_prompts:
    - "注意：同步计数器和异步计数器的区别"
    - "建议：掌握74LS161/74LS160的功能表"
    - "关联：计数器设计常与状态转换图结合"

存储器:
  prerequisites:
    - 触发器
    - 地址译码
  combinations:
    - ROM扩展
    - RAM扩展
  applications:
    - 数据存储
    - 程序存储
  cross_chapter_prompts:
    - "注意：ROM和RAM的区别"
    - "提醒：字扩展和位扩展的方法"

脉冲电路:
  prerequisites:
    - 触发器
    - 电容充放电
  combinations:
    - 单稳态
    - 多谐振荡器
  applications:
    - 脉冲整形
    - 时钟产生
  cross_chapter_prompts:
    - "注意：555定时器的典型应用"
    - "提醒：施密特触发器的滞回特性"

ADC/DAC:
  prerequisites:
    - 运算放大器
    - 数字电路基础
  combinations:
    - A/D转换
    - D/A转换
  applications:
    - 数字信号处理
    - 数据采集
  cross_chapter_prompts:
    - "注意：分辨率、转换精度、转换速度"
    - "提醒：逐次逼近型和双积分型的区别"
```

---

## 数学前置检查 (v1.2.0新增)

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

```python
def check_math_prerequisites(topic, user_context):
    """检查数学前置知识

    Args:
        topic: 要学习的电子技术主题
        user_context: 用户上下文（含数学学习记录）

    Returns:
        前置检查结果和建议
    """
    prereqs = MATH_PREREQUISITES.get(topic)

    if not prereqs:
        return {"needed": False}

    results = []
    for req in prereqs["required_math"]:
        math_topic = req["topic"]
        # 检查用户数学掌握程度
        mastery = get_math_mastery_level(user_context, math_topic)

        results.append({
            "topic": math_topic,
            "required_level": req["level"],
            "current_level": mastery,
            "passed": mastery >= req["level"],
            "refresher": req["refresher"]
        })

    all_passed = all(r["passed"] for r in results)

    return {
        "needed": True,
        "topic": topic,
        "warning": prereqs["warning"] if not all_passed else None,
        "results": results,
        "all_passed": all_passed
    }
```

---

## 跨学科提醒 (v1.2.0新增)

### 数学关联提醒

学习电子技术时，主动提示相关的数学知识。

```python
def generate_math_reminder(electronics_topic):
    """生成数学关联提醒

    Args:
        electronics_topic: 当前学习的电子技术主题

    Returns:
        数学关联提醒
    """
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

### 跨学科提醒显示

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

---

## 统一错误模型集成 (v1.2.0新增)

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

    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "unified_mistake_record",
                    "data": mistake_data
                },
                "tags": [
                    "#mistake_record",
                    "#subject_electronics",
                    f"#kp_{mistake_data.get('knowledge_point', '')}",
                    f"#mistake_type_{mistake_data.get('type', 'unknown')}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save mistake: {e}")


def find_math_refs(electronics_topic):
    """查找与电子技术相关的数学知识点"""
    refs = {
        "频率响应": ["复数运算", "对数运算"],
        "暂态响应": ["微分方程", "指数函数"],
        "滤波器设计": ["拉普拉斯变换", "复数运算"],
        "RC电路": ["积分", "微分方程"],
        "RL电路": ["微分方程", "指数函数"]
    }
    return refs.get(electronics_topic, [])
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

## 调度信号处理 (v1.2.0新增)

### 检查调度信号

从kaoyan-plan接收调度信号并执行相应动作。

```python
def check_dispatch_signals(user_id):
    """检查来自kaoyan-plan的调度信号"""
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_kaoyan-electronics #user_{user_id}",
            top_k=5
        )

        pending = []
        for signal in signals:
            if not signal.get("processed"):
                pending.append(signal)

        return pending
    except Exception as e:
        log_warning(f"Failed to check dispatch signals: {e}")
        return []


def process_dispatch_signal(signal):
    """处理调度信号"""
    action = signal.get("action")
    context = signal.get("context", {})

    if action == "check_math_prerequisites":
        topic = context.get("topic")
        return {
            "mode": "prerequisite_check",
            "topic": topic,
            "required_math": context.get("required_math", []),
            "instructions": f"检查学习「{topic}」所需的数学基础"
        }

    elif action == "circuit_analysis_sop":
        circuit_type = context.get("circuit_type")
        return {
            "mode": "circuit_analysis",
            "circuit_type": circuit_type,
            "instructions": f"使用标准SOP分析{circuit_type}"
        }

    elif action == "weekly_error_analysis":
        return {
            "mode": "weekly_review",
            "aggregate": context.get("aggregate", True)
        }

    return None
```

### 支持的调度动作

| 动作名 | 说明 | 上下文参数 |
|--------|------|------------|
| `check_math_prerequisites` | 数学前置检查 | `{topic, required_math}` |
| `circuit_analysis_sop` | 电路分析SOP | `{circuit_type}` |
| `weekly_error_analysis` | 周日错误分析 | `{aggregate}` |

---

## 实例演示

### 示例1: 电路图解析

**用户输入**:
```
[上传共射放大电路截图]
帮我分析这个电路
```

**AI处理**:
1. 使用 `understand_technical_diagram` 识别电路结构
2. 使用 `extract_text_from_screenshot` 提取元件参数
3. 按SOP步骤分析静态、动态

**AI输出**:
```markdown
# 共射放大电路分析

## 电路识别
- 类型：共射放大电路
- 元件：$R_b=200k\Omega$, $R_c=3k\Omega$, $V_{CC}=12V$, $\beta=50$

## 静态分析
$$
I_B = \frac{12 - 0.7}{200} = 56.5\mu A
$$
$$
I_C = 50 \times 56.5\mu A = 2.83mA
$$
$$
U_{CE} = 12 - 2.83 \times 3 = 3.51V
$$

## 动态分析
$$
r_{be} = 300 + (1+50)\frac{26}{2.83} = 0.77k\Omega
$$
$$
A_u = -\frac{50 \times 3//3}{0.77} = -97.4
$$
$$
R_i = 200//0.77 \approx 0.77k\Omega
$$
$$
R_o = 3k\Omega
$$

## 结论
该电路工作在放大区，电压放大倍数约-97.4，信号反相。
```

### 示例2: 负反馈类型判断

**用户输入**:
```
我对反馈类型判断总是搞混
电压反馈和电流反馈怎么区分？
```

**AI处理**:
1. 识别用户困惑点
2. 生成对比说明
3. 记录到错误模式
4. 提供记忆口诀

**AI输出**:
```markdown
## 负反馈类型判断 ⚠️

### 你的错误模式
你在"反馈类型判断"方面已出错多次

### 电压反馈 vs 电流反馈

| 判断方法 | 电压反馈 | 电流反馈 |
|----------|----------|----------|
| **判断标准** | 反馈信号取自输出端 | 反馈信号取自非输出端 |
| **短路法** | 短路输出→反馈消失 | 短路输出→反馈仍存在 |
| **特征** | $X_f \propto U_o$ | $X_f \propto I_o$ |

### 记忆口诀 📌
```
电压反馈看输出：短路负载反馈无
电流反馈看输出：短路负载反馈留
```

### 串联 vs 并联

| 判断方法 | 串联反馈 | 并联反馈 |
|----------|----------|----------|
| **连接方式** | 反馈信号与输入串联 | 反馈信号与输入并联 |
| **信号关系** | $U_d = U_i - U_f$ | $I_d = I_i - I_f$ |
| **位置** | 反馈加到发射极 | 反馈加到基极 |

### 练习题
1. 判断反馈类型：[电路图]
2. 判断反馈类型：[电路图]
3. 计算深度负反馈增益：[电路图]
```

### 示例3: 数字逻辑设计

**用户输入**:
```
用JK触发器设计同步五进制计数器
```

**AI处理**:
1. 按时序逻辑设计SOP执行
2. 生成完整设计过程
3. 检查自启动

**AI输出**:
```markdown
# 同步五进制计数器设计

## 设计步骤

### 步骤1: 状态编码
使用3位二进制编码：
- S0=000, S1=001, S2=010, S3=011, S4=100

### 步骤2: 状态转换表
| $Q_2^n Q_1^n Q_0^n$ | $Q_2^{n+1} Q_1^{n+1} Q_0^{n+1}$ | $J_2 K_2$ | $J_1 K_1$ | $J_0 K_0$ |
|---------------------|---------------------------|----------|----------|----------|
| 000 | 001 | 0× | 0× | 1× |
| 001 | 010 | 0× | 1× | ×1 |
| 010 | 011 | 0× | ×0 | 1× |
| 011 | 100 | 1× | ×1 | ×1 |
| 100 | 000 | ×1 | 0× | 0× |

### 步骤3: 卡诺图化简
$$
J_2 = Q_1 Q_0, \quad K_2 = 1
$$
$$
J_1 = Q_0, \quad K_1 = Q_0
$$
$$
J_0 = \overline{Q_2}, \quad K_0 = 1
$$

### 步骤4: 逻辑图
```
[逻辑电路图]
```

### 步骤5: 自启动检查
无效状态：
- 101 → 010 ✓
- 110 → 010 ✓
- 111 → 000 ✓

所有无效状态都能进入有效循环，设计可靠。
```

---

## 验证标准

### 电路图识别验证
- [ ] 上传典型共射电路图，验证元件识别正确
- [ ] 上传运放电路，验证拓扑分析准确
- [ ] 验证参数提取准确率 > 90%

### SOP流程验证
- [ ] 测试负反馈类型判断SOP
- [ ] 测试计数器设计SOP
- [ ] 验证输出格式符合考试要求

### MemOS验证
- [ ] 记录错误，验证持久化
- [ ] 基于历史错误生成个性化提醒
- [ ] 测试优雅降级

### LaTeX验证
- [ ] 验证所有电路公式正确渲染
- [ ] 验证真值表格式正确

### 跨技能集成验证 (v1.2.0新增)
- [ ] 数学前置检查功能
- [ ] 跨学科提醒显示
- [ ] 统一错误模型学科标签
- [ ] 调度信号接收和处理
- [ ] 跨学科知识关联查询

---

## 技术实现要点

1. **电路图识别**: 使用 `understand_technical_diagram` 和 `extract_text_from_screenshot` MCP工具
2. **LaTeX支持**: 所有公式使用标准LaTeX格式，确保在Obsidian中正确渲染
3. **MemOS集成**: 优先使用MemOS，不可用时优雅降级到本地模式
4. **知识图谱**: 内置17个考点的关联关系，主动提示前置知识和跨章节关联
5. **SOP模板**: 提供标准化的解题步骤，确保答题规范、完整

---

## 版本历史

- **v1.2.0** (2025-02-26): 跨技能联合架构版
  - 数学前置检查功能
  - 跨学科提醒（数学↔电子技术）
  - 统一错误模型集成
  - 调度信号处理
  - 跨学科知识关联

- **v1.1.0** (2025-02-26): 实战优化版
  - 康华光教材符号体系适配
  - Mermaid波形图生成支持
  - 考点权重动态记忆
  - 运算电路工作区判断防错

- **v1.0.0** (2025-02-26): 初始版本，包含全功能
  - 电路图智能解析
  - 17个考点SOP模板
  - 知识图谱主动关联
  - MemOS记忆追踪
