# kaoyan-electronics-circuit 代码架构

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

本文件提供电路图解析技能的整体架构和核心数据结构。

---

## 📐 架构概览

```
【输入】电路图截图 / 文字描述
    ↓
【识别】MCP 工具识别电路结构
    ↓
【提取】提取元件参数
    ↓
【分析】选择对应分析器（模电/数电）
    ↓
【输出】生成 Markdown 分析报告
```

---

## 🧠 核心数据结构

### 电路类型枚举

```python
class CircuitType(Enum):
    # 模电类型
    CE_AMPLIFIER = "共射放大"
    CC_AMPLIFIER = "共集放大"
    CB_AMPLIFIER = "共基放大"
    DIFFERENTIAL = "差分放大"
    FEEDBACK = "反馈放大"
    OPAMP = "运算电路"
    POWER_AMP = "功率放大"
    OSCILLATOR = "振荡电路"
    POWER_SUPPLY = "稳压电源"

    # 数电类型
    COMBINATIONAL = "组合逻辑"
    SEQUENTIAL = "时序逻辑"
    COUNTER = "计数器"
    SHIFT_REGISTER = "移位寄存器"
```

### 分析结果结构

```python
@dataclass
class AnalysisResult:
    circuit_type: CircuitType
    components: Dict          # 元件参数
    static_analysis: Dict     # 静态分析结果（模电）
    dynamic_analysis: Dict    # 动态分析结果（模电）
    drive_equations: List[str]    # 驱动方程（数电）
    state_equations: List[str]    # 状态方程（数电）
    state_table: str             # 状态转换表
    state_diagram: str           # 状态转换图（Mermaid）
    output_markdown: str         # 完整输出
```

---

## 🔧 核心 API

### 主入口

```python
def process_circuit_analysis(
    image_source: str = None,
    text_description: str = None,
    analysis_type: str = "full"  # static/dynamic/full
) -> AnalysisResult
```

### MCP 工具调用

| 功能 | MCP 工具 | 用途 |
|------|----------|------|
| 电路识别 | `mcp__zai-mcp-server__understand_technical_diagram` | 识别电路结构、连接关系 |
| 参数提取 | `mcp__zai-mcp-server__extract_text_from_screenshot` | 提取元件参数值 |

### 分析器选择

```python
def select_analyzer(circuit_type: CircuitType):
    ANALYZERS = {
        # 模电
        CircuitType.CE_AMPLIFIER: CEAmplifierAnalyzer,
        CircuitType.CC_AMPLIFIER: CCAmplifierAnalyzer,
        CircuitType.DIFFERENTIAL: DifferentialAnalyzer,
        CircuitType.OPAMP: OpAmpAnalyzer,
        # 数电
        CircuitType.COMBINATIONAL: CombinationalAnalyzer,
        CircuitType.SEQUENTIAL: SequentialAnalyzer,
    }
    return ANALYZERS.get(circuit_type, GenericAnalyzer)()
```

---

## 📊 分析流程

### 模电分析

| 步骤 | 内容 | 输出 |
|------|------|------|
| 静态分析 | 计算工作点 Q | $I_{BQ}, I_{CQ}, U_{CEQ}$ |
| 动态分析 | 画微变等效电路 | $A_u, R_i, R_o$ |
| 频率响应 | 分析带宽 | $f_L, f_H, BW$ |

### 数电分析

| 步骤 | 内容 | 输出 |
|------|------|------|
| 驱动方程 | 写触发器输入 | $J = f(X,Q), K = g(X,Q)$ |
| 状态方程 | 写次态函数 | $Q^{n+1} = h(J,K,Q^n)$ |
| 状态表 | 列所有转换 | Markdown 表格 |
| 状态图 | 画转换图 | Mermaid stateDiagram |
| 自启动 | 检查无效状态 | 是否能进入有效循环 |

---

## 📝 康华光符号体系

> ⚠️ 所有输出必须使用康华光《电子技术基础》（第7版）符号

### 模电符号

| 参数 | 符号 | LaTeX |
|------|------|-------|
| 基极静态电流 | $I_{BQ}$ | `I_{BQ}` |
| 集电极静态电流 | $I_{CQ}$ | `I_{CQ}` |
| 集射极静态电压 | $U_{CEQ}$ | `U_{CEQ}` |
| BJT 输入电阻 | $r_{be}$ | `r_{be}` |
| 电压增益 | $A_u$ | `A_u` |
| 输入/输出电阻 | $R_i, R_o$ | `R_i, R_o` |

### 数电符号

| 参数 | 符号 | LaTeX |
|------|------|-------|
| 现态 | $Q^n$ | `Q^n` |
| 次态 | $Q^{n+1}$ | `Q^{n+1}` |
| 时钟 | $CLK$ | `CLK` |

---

## 📁 模块索引

由于本技能主要调用 MCP 工具，无独立 scripts/ 目录。核心逻辑直接在 Claude 对话中执行。

| 功能 | 实现方式 |
|------|----------|
| 电路识别 | MCP `understand_technical_diagram` |
| 参数提取 | MCP `extract_text_from_screenshot` |
| 分析计算 | Claude 对话中执行 |
| 输出生成 | Claude 对话中执行 |

---

## 版本信息

- **创建日期**: 2026-03-12
- **版本**: 1.2.0 (精简导航模式)

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
