# kaoyan-electronics-sop 代码模块

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 概述

本文件提供 kaoyan-electronics-sop 技能的代码实现逻辑，包括 SOP 选择、符号转换、格式生成等核心功能。

---

## 核心依赖

```python
import re
from typing import Dict, List, Optional, Tuple
```

---

## 主入口 API

### 1. SOP 选择器

```python
def select_sop(user_input: str, circuit_type: str = None) -> Dict:
    """
    根据用户输入和电路类型选择合适的 SOP 模板。

    参数:
        user_input: 用户输入内容
        circuit_type: 电路类型（可选）

    返回:
        {
            "sop_id": "SOP1",
            "sop_name": "共射放大电路分析",
            "sop_type": "模电",
            "template_path": "/kaoyan-electronics/scripts/templates/sop_library.md#sop1"
        }
    """
    SOP_KEYWORDS = {
        # 模电 SOP
        "SOP1": ["共射", "放大电路", "Au", "电���增益", "CE"],
        "SOP2": ["共集", "共基", "射极跟随器", "CC", "CB"],
        "SOP3": ["反馈", "反馈类型", "深度负反馈", "正反馈", "负反馈"],
        "SOP4": ["差分", "差动", "共模", "差模", "CMRR"],
        "SOP5": ["运放", "运算", "虚短", "虚断", "比较器"],
        "SOP6": ["功放", "功率", "OCL", "OTL", "效率"],
        "SOP7": ["振荡", "波形", "起振", "正弦波"],
        "SOP8": ["稳压", "整流", "滤波", "电源"],
        # 数电 SOP
        "SOP9": ["卡诺图", "化简", "逻辑函数", "最简"],
        "SOP10": ["组合逻辑", "分析组合"],
        "SOP11": ["设计组合", "组合电路设计"],
        "SOP12": ["时序逻辑", "分析时序", "状态方程"],
        "SOP13": ["设计时序", "时序电路设计"],
        "SOP14": ["计数器分析", "分析计数"],
        "SOP15": ["计数器设计", "设计计数", "任意进制"],
        "SOP16": ["移位", "寄存器"],
        "SOP17": ["ADC", "DAC", "转换", "A/D", "D/A"],
    }

    # 关键词匹配
    for sop_id, keywords in SOP_KEYWORDS.items():
        for kw in keywords:
            if kw in user_input:
                return get_sop_info(sop_id)

    # 默认返回通用引导
    return {
        "sop_id": None,
        "sop_name": "通用引导",
        "message": "请描述具体的电路类型或题目要求，我将为您选择合适的 SOP 模板。"
    }
```

### 2. SOP 信息获取

```python
def get_sop_info(sop_id: str) -> Dict:
    """获取 SOP 模板信息"""

    SOP_INFO = {
        "SOP1": {
            "sop_id": "SOP1",
            "sop_name": "共射放大电路分析",
            "sop_type": "模电",
            "steps": ["计算静态工作点Q", "计算动态参数", "检查放大区条件"],
            "key_formulas": ["I_BQ", "I_CQ", "U_CEQ", "r_be", "A_u"],
        },
        "SOP3": {
            "sop_id": "SOP3",
            "sop_name": "负反馈类型判断",
            "sop_type": "模电",
            "steps": ["判断输出取样方式", "判断输入比较方式", "判断反馈极性", "计算深度负反馈增益"],
            "key_formulas": ["A_uf ≈ 1/F"],
        },
        "SOP5": {
            "sop_id": "SOP5",
            "sop_name": "运算电路分析",
            "sop_type": "模电",
            "steps": ["判断工作区", "应用虚短虚断", "列方程求解"],
            "key_formulas": ["U+ = U-", "I+ = I- = 0"],
        },
        # ... 其他 SOP 信息
    }

    return SOP_INFO.get(sop_id, {})
```

---

## 康华光符号转换

### 符号映射表

```python
# 康华光符号体系映射
KANG_SYMBOLS = {
    # 静态工作点
    "I_BQ": {"latex": "I_{BQ}", "desc": "基极静态电流"},
    "I_CQ": {"latex": "I_{CQ}", "desc": "集电极静态电流"},
    "U_CEQ": {"latex": "U_{CEQ}", "desc": "集射极静态电压"},
    "U_BEQ": {"latex": "U_{BEQ}", "desc": "基射极静态电压"},

    # 动态参数
    "r_be": {"latex": "r_{be}", "desc": "BJT输入电阻"},
    "r_ce": {"latex": "r_{ce}", "desc": "BJT输出电阻"},
    "g_m": {"latex": "g_m", "desc": "跨导"},

    # FET 参数
    "U_GS_off": {"latex": "U_{GS(off)}", "desc": "夹断电压"},
    "U_GS_th": {"latex": "U_{GS(th)}", "desc": "开启电压"},
    "I_DSS": {"latex": "I_{DSS}", "desc": "饱和漏极电流"},
}

# 其他教材符号 → 康华光符号 转换
TO_KANG_CONVERSION = {
    "h_ie": "r_be",
    "h_fe": "β",
    "U_P": "U_GS(off)",
    "U_T": "U_GS(th)",
    "I_B": "I_BQ",  # 静态时
    "I_C": "I_CQ",  # 静态时
}
```

### 符号转换函数

```python
def convert_to_kang_symbol(symbol: str) -> str:
    """将其他教材符号转换为康华光符号"""
    return TO_KANG_CONVERSION.get(symbol, symbol)

def format_latex(symbol_key: str) -> str:
    """格式化为 LaTeX 符号"""
    if symbol_key in KANG_SYMBOLS:
        return f"${KANG_SYMBOLS[symbol_key]['latex']}$"
    return f"${symbol_key}$"
```

---

## LaTeX 公式生成

### 模电公式模板

```python
def generate_static_analysis_latex(params: Dict) -> str:
    """生成静态分析 LaTeX 公式块"""

    return f"""
## 静态分析

### 基极回路方程
$$
I_{{BQ}} = \\frac{{V_{{CC}} - U_{{BEQ}}}}{{R_b}} = \\frac{{{params.get('Vcc', 'V_{{CC}}')} - 0.7}}{{{params.get('Rb', 'R_b')}}}
$$

### 集电极电流
$$
I_{{CQ}} = \\beta I_{{BQ}} = {params.get('beta', '\\beta')} \\times I_{{BQ}}
$$

### 管压降
$$
U_{{CEQ}} = V_{{CC}} - I_{{CQ}} R_c = {params.get('Vcc', 'V_{{CC}}')} - I_{{CQ}} \\times {params.get('Rc', 'R_c')}
$$
"""

def generate_dynamic_analysis_latex(params: Dict) -> str:
    """生成动态分析 LaTeX 公式块"""

    return f"""
## 动态分析

### 输入电阻
$$
r_{{be}} = r_{{bb'}} + (1+\\beta)\\frac{{26}}{{I_{{EQ}}}}
$$

### 电压增益
$$
A_u = -\\frac{{\\beta R'_L}}{{r_{{be}}}}
$$
其中：$R'_L = R_c // R_L$

### 输入/输出电阻
$$
R_i = R_b // r_{{be}}
$$
$$
R_o = R_c
$$
"""
```

---

## Mermaid 波形图生成

### 计数器时序图

```python
def generate_counter_timing_diagram(bits: int, cycles: int = 8) -> str:
    """
    生成计数器时序图的 Mermaid 代码。

    参数:
        bits: 计数器位数
        cycles: 显示的时钟周期数

    返回:
        Mermaid gantt 图代码
    """
    mermaid_code = """```mermaid
gantt
    title {bits}位二进制计数器时序
    dateFormat X
    axisFormat %L

    section 时钟
    CLK    :0, {cycle_pattern}

    section 输出
""".format(bits=bits, cycle_pattern=", ".join(["1"] * cycles))

    # 生成各输出位的波形
    for i in range(bits):
        values = []
        period = 2 ** i
        for clk in range(cycles):
            values.append(str((clk // period) % 2))
        waveform = ", ".join(values)
        mermaid_code += f"    Q{i}     :0, {waveform}\n"

    mermaid_code += "```"
    return mermaid_code
```

### 状态转换图

```python
def generate_state_diagram(states: List[str], transitions: List[Tuple[str, str, str]]) -> str:
    """
    生成状态转换图的 Mermaid 代码。

    参数:
        states: 状态列表
        transitions: 转换列表 [(from, to, label), ...]

    返回:
        Mermaid stateDiagram 代码
    """
    mermaid_code = """```mermaid
stateDiagram-v2
    direction LR
"""

    for from_state, to_state, label in transitions:
        mermaid_code += f"    {from_state} --> {to_state}: {label}\n"

    mermaid_code += "```"
    return mermaid_code
```

---

## 答题检查清单生成

```python
def generate_checklist(sop_id: str) -> List[str]:
    """根据 SOP ID 生成答题检查清单"""

    CHECKLISTS = {
        "SOP1": [
            "静态工作点使用Q下标（$I_{BQ}, I_{CQ}, U_{CEQ}$）",
            "$r_{be}$计算正确",
            "$R'_L$考虑了负载电阻",
            "增益负号表示反相",
            "检查了放大区条件"
        ],
        "SOP3": [
            "短路法判断输出取样",
            "观察法判断输入比较",
            "瞬时极性法判断极性",
            "深度负反馈增益计算正确",
            "反馈类型结论完整（4个词）"
        ],
        "SOP5": [
            "✅ 首先判断工作区（最关键！）",
            "线性区才用虚短虚断",
            "非线性区用比较器特性"
        ],
    }

    return CHECKLISTS.get(sop_id, [])
```

---

## 笔记格式生成

```python
def generate_modian_note(topic: str, content: Dict) -> str:
    """生成模电笔记 Markdown 模板"""

    return f"""# {topic}

## 基本概念
{content.get('concept', '[定义、原理]')}

## 核心公式
$$
{content.get('formula', '[公式]')}
$$

## 分析方法
1. {content.get('step1', '步骤一')}
2. {content.get('step2', '步骤二')}

## 常见题型
- 题型1: {content.get('type1', '[描述]')}

## 注意事项
- ⚠️ {content.get('warning', '[注意点]')}

## 关联知识点
- {content.get('related', '[知识点]')}
"""

def generate_shudian_note(topic: str, content: Dict) -> str:
    """生成数电笔记 Markdown 模板"""

    return f"""# {topic}

## 功能描述
{content.get('function', '[功能、应用]')}

## 真值表/状态表
| 输入 | 输出 |
|------|------|
| ... | ... |

## 逻辑表达式
$$
{content.get('expression', '[表达式]')}
$$

## 工作波形
{content.get('waveform', '[描述波形变化]')}
"""
```

---

## 数据文件引用

| 文件 | 路径 | 用途 |
|------|------|------|
| SOP模板库 | `/kaoyan-electronics/scripts/templates/sop_library.md` | 完整17个SOP模板 |
| LaTeX指南 | `/kaoyan-electronics/scripts/templates/latex_guide_electronics.md` | 电子符号LaTeX标准 |
| Mermaid指南 | `/kaoyan-electronics/scripts/templates/mermaid_guide_electronics.md` | 波形图生成规范 |

---

## 版本信息

- **创建日期**: 2026-03-27
- **版本**: 1.1.0 (模块化重构)

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
