---
name: knowledge-mindmap
description: 自动分析知识点目录结构，生成 Excalidraw 格式的详细思维导图。适用于考研数学、专业课等知识体系的可视化整理。触发词包括"知识点思维导图"、"生成思维导图"、"知识结构图"、"目录结构图"。
metadata:
  version: 2.1.0
---

# Knowledge Mindmap Generator v2.1

自动分析知识点目录结构，生成 Excalidraw 格式的详细思维导图。

## v2.1 新特性（最新）

- **按序号顺时针排列**：节点位置严格按照模块序号顺序顺时针排列，而非随机分布
- **序号识别算法**：自动从文件夹名提取序号（如 `0-数列的概念` → 0）
- **角度计算优化**：从顶部（-90°）开始按序号顺时针分布各节点

## v2.0 新特性

- **智能布局算法**：根据模块数量自动分布，避免重叠
- **多格式导入**：支持 Markdown 层级列表、JSON 笔记、Excel 表格
- **图形丰富性**：圆角、阴影、图标区分模块类型
- **交互性增强**：超链接到笔记原文，点击即可跳转
- **自动分层折叠**：模块过多时生成折叠结构

## 使用方法

### 基本用法

```
/knowledge-mindmap [目录路径]
```

### 高级选项

```
/knowledge-mindmap [目录路径] --format=[simple|detailed|folded]
/knowledge-mindmap [目录路径] --style=[compact|expanded|tree]
/knowledge-mindmap [目录路径] --max-modules=[数字]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--format` | 输出格式：simple（简洁）/ detailed（详细）/ folded（折叠） | detailed |
| `--style` | 布局样式：compact（紧凑）/ expanded（展开）/ tree（树形） | expanded |
| `--max-modules` | 折叠模式下核心模块最大数量 | 5 |

## 工作流程

### 1. 目录探索阶段

```
用户指定目录
    ↓
探索目录结构
    ↓
识别知识点模块
    ↓
提取核心内容
```

**自动识别的关键文件：**
- `📑 索引.md` - 模块总索引
- `📊 学习进度.md` - 学习进度追踪
- `📝 章节总结.md` - 全章总结
- `README.md` - 模块说明
- 各知识点笔记文件

### 2. 内容分析阶段

从笔记中提取：
- 模块标题和星级（⭐⭐⭐⭐⭐）
- 核心概念和定义
- 重要定理和公式
- 解题方法和技巧
- 易错点和注意事项

### 3. 智能布局阶段

**布局算法流程：**

```
分析模块数量和层级
    ↓
提取模块序号并排序
    ↓
选择最优布局模板
    ↓
按序号顺时针计算各模块坐标
    ↓
自动调整避免重叠
    ↓
生成连接线
```

---

## 智能布局算法

### 模块序号识别与排序

**核心原则**：节点位置按照模块序号顺序顺时针排列，而非随机分布。

```python
def extract_module_number(folder_name):
    """从文件夹名提取序号
    示例: "0-数列的概念" → 0
         "1-用定义" → 1
         "7-收敛速度问题" → 7
    """
    import re
    match = re.match(r'(\d+)-', folder_name)
    return int(match.group(1)) if match else 999

# 模块排序
sorted_modules = sorted(modules, key=lambda m: extract_module_number(m['name']))
```

### 模块数量自适应

| 模块数量 | 布局策略 | 画布尺寸 |
|---------|---------|---------|
| 1-3 个 | 线性布局 | 800×400 |
| 4-6 个 | 放射状布局 | 1000×600 |
| 7-10 个 | 环形布局 | 1200×800 |
| 11+ 个 | 分层折叠 | 1400×900 |

### 坐标计算公式（按序号顺时针）

**放射状布局（4-6 个模块）- 顺时针排列：**

```
中心坐标: (canvasWidth/2, canvasHeight/2)
模块角度: 360° / 模块数量
模块距离: min(canvasWidth, canvasHeight) * 0.35

# 按序号排序后，从顶部（-90°）开始顺时针排列
模块i坐标（i为排序后的序号，从0开始）:
  angle_degrees = -90° + (360° / 模块数量) * i
  angle_radians = angle_degrees * π / 180
  x = centerX + distance * cos(angle_radians)
  y = centerY + distance * sin(angle_radians)

示例：4个模块（0,1,2,3）
  模块0: -90°  (顶部)
  模块1:   0°  (右侧)
  模块2:  90°  (底部)
  模块3: 180°  (左侧)
```

**环形布局（7-10 个模块）- 顺时针排列：**

```
内环（核心模块）: 距离中心 150px
外环（普通模块）: 距离中心 300px
辅助系统: 底部独立区域

# 从顶部开始按序号顺时针排列各模块
角度起始: -90°（12点钟方向）
角度间隔: 360° / 模块数量
排序后依次放置
```

**示例：数列极限（8个模块 0-7）**

```
模块0: -90°  →  顶部
模块1: -45°  →  右上
模块2:   0°  →  右侧
模块3:  45°  →  右下
模块4:  90°  →  底部
模块5: 135°  →  左下
模块6: 180°  →  左侧
模块7: 225°  →  左上
```

### 避免重叠检测

```python
def check_overlap(box1, box2, margin=20):
    """检测两个矩形是否重叠，margin 为安全间距"""
    return not (
        box1.x + box1.width + margin < box2.x or
        box2.x + box2.width + margin < box1.x or
        box1.y + box1.height + margin < box2.y or
        box2.y + box2.height + margin < box1.y
    )

def adjust_position(box, others, step=10, max_attempts=50):
    """自动调整位置避免重叠"""
    for _ in range(max_attempts):
        if all(not check_overlap(box, other) for other in others):
            return box
        box.x += step
    return box
```

---

## 多格式导入支持

### 1. Markdown 层级列表

**输入格式：**
```markdown
- 数列极限
  - 0-数列的概念
    - 数列定义
    - 子列概念
  - 2-用性质 ⭐⭐⭐⭐⭐
    - 唯一性
    - 有界性
    - 保号性
```

**解析规则：**
- 缩进表示层级关系
- `⭐⭐⭐⭐⭐` 标记核心模块
- 子项自动成为模块内容

### 2. JSON 笔记格式

**输入格式：**
```json
{
  "title": "数列极限",
  "modules": [
    {
      "id": "module-1",
      "title": "用性质",
      "level": 5,
      "content": ["唯一性", "有界性", "保号性"],
      "file": "2-用性质/README.md"
    }
  ]
}
```

### 3. Excel 表格格式

| 列名 | 说明 | 必填 |
|------|------|------|
| 模块ID | 唯一标识 | 是 |
| 模块名称 | 显示标题 | 是 |
| 层级 | 1-5星 | 否 |
| 内容 | 分号分隔 | 否 |
| 链接 | 笔记路径 | 否 |

---

## 图形丰富性

### 模块类型图标

| 类型 | 图标 | 颜色 | 用途 |
|------|------|------|------|
| **定义** | 📖 | `#3b82f6` | 概念、定义类 |
| **定理** | 📐 | `#8b5cf6` | 定理、性质类 |
| **方法** | 🔧 | `#f59e0b` | 解题方法类 |
| **公式** | 📝 | `#10b981` | 重要公式类 |
| **易错** | ⚠️ | `#ef4444` | 易错点提醒 |
| **核心** | ⭐ | `#f59e0b` | 五星重点 |

### 视觉样式

```json
{
  "核心模块": {
    "strokeWidth": 3,
    "strokeColor": "#f59e0b",
    "backgroundColor": "#fef3c7",
    "roundness": {"type": 3},
    "shadow": true
  },
  "普通模块": {
    "strokeWidth": 2,
    "strokeColor": "#3b82f6",
    "backgroundColor": "#eff6ff",
    "roundness": {"type": 3},
    "shadow": false
  },
  "辅助系统": {
    "strokeWidth": 2,
    "strokeColor": "#9ca3af",
    "strokeStyle": "dashed",
    "backgroundColor": "#f3f4f6"
  }
}
```

### 圆角设置

```json
{
  "roundness": {"type": 3}  // 圆角矩形
}
```

---

## 交互性增强

### 超链接功能

为每个模块添加指向原笔记的链接：

```json
{
  "id": "box-2",
  "type": "rectangle",
  "link": "2-用性质/README.md",
  ...
}
```

**链接格式：**
- 相对路径：`2-用性质/README.md`
- Wiki链接：`[[2-用性质/README]]`
- 外部链接：`https://...`

### 点击跳转

用户在 Excalidraw 视图中点击模块时：
1. 自动打开对应的笔记文件
2. 或跳转到指定章节

### 实现 JSON

```json
{
  "id": "module-properties",
  "type": "rectangle",
  "x": 520,
  "y": 50,
  "width": 200,
  "height": 200,
  "link": "obsidian://open?vault=考研复习&file=考研数学/高数-数列极限/2-用性质/README",
  "strokeColor": "#f59e0b",
  ...
}
```

---

## 自动分层折叠

### 折叠策略

当模块数量超过阈值（默认10个）时：

1. **识别核心模块**：根据星级和重要性
2. **折叠次要模块**：归入"更多..."折叠区
3. **保留辅助系统**：始终显示在底部

### 折叠模式布局

```
                    [核心模块1]
                        ↑
[核心模块2] ←← [中心主题] →→ [核心模块3]
                        ↓
                   [更多模块...]  ← 点击展开
                        ↓
                   [辅助系统]
```

### 展开后的子图

```
[更多模块]
    ├── 模块4: 四则运算
    ├── 模块5: 收敛速度
    └── 模块6: 压缩映射
```

### JSON 实现

```json
{
  "id": "folded-group",
  "type": "rectangle",
  "x": 500,
  "y": 600,
  "width": 200,
  "height": 80,
  "strokeColor": "#9ca3af",
  "strokeStyle": "dashed",
  "text": "更多模块（点击展开）\n+4 个模块",
  "link": "#expanded-view"
}
```

---

## 输出格式

### Obsidian Excalidraw 格式

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw, mindmap]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [...],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
\`\`\`
%%
```

---

## 设计规范

### 颜色编码

| 元素类型 | 边框颜色 | 背景颜色 | 用途 |
|---------|---------|---------|------|
| **中心节点** | `#1e40af` | `#dbeafe` | 椭圆形，主题核心 |
| **五星模块** | `#f59e0b` | `#fef3c7` | 核心考点，粗边框 |
| **四星模块** | `#8b5cf6` | `#f3e8ff` | 重要内容 |
| **普通模块** | `#3b82f6` | `#eff6ff` | 基础知识点 |
| **辅助系统** | `#9ca3af` | `#f3f4f6` | 虚线边框 |
| **折叠区** | `#6b7280` | `#f9fafb` | 可展开区域 |

### 尺寸规范

| 模块类型 | 宽度 | 高度 | 字体大小 |
|---------|------|------|---------|
| 中心节点 | 300-400px | 120-140px | 28-32px |
| 五星模块 | 200-240px | 200-280px | 15px |
| 普通模块 | 200-260px | 150-200px | 15px |
| 辅助系统 | 500-620px | 180-200px | 14px |
| 折叠区 | 200px | 80px | 14px |

---

## JSON 元素模板

### 带链接的核心模块

```json
{
  "id": "star-module-1",
  "type": "rectangle",
  "x": 300,
  "y": 20,
  "width": 240,
  "height": 280,
  "angle": 0,
  "strokeColor": "#f59e0b",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid",
  "strokeWidth": 3,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a6",
  "roundness": {"type": 3},
  "seed": 112,
  "version": 1,
  "versionNonce": 113,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": "obsidian://open?vault=考研复习&file=考研数学/高数-数列极限/2-用性质/README",
  "locked": false
}
```

### 带图标的文本

```json
{
  "id": "text-star-1",
  "type": "text",
  "x": 320,
  "y": 30,
  "width": 200,
  "height": 260,
  "angle": 0,
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a7",
  "roundness": {"type": 3},
  "seed": 114,
  "version": 1,
  "versionNonce": 115,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false,
  "text": "2-用性质\n⭐⭐⭐⭐⭐\n\n• 唯一性\n• 有界性\n• 保号性\n  - 脱帽法\n  - 戴帽法\n  - 最值问题",
  "rawText": "2-用性质\n⭐⭐⭐⭐⭐\n\n• 唯一性\n• 有界性\n• 保号性\n  - 脱帽法\n  - 戴帽法\n  - 最值问题",
  "fontSize": 15,
  "fontFamily": 5,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "2-用性质\n⭐⭐⭐⭐⭐\n\n• 唯一性\n• 有界性\n• 保号性\n  - 脱帽法\n  - 戴帽法\n  - 最值问题",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### 智能连接线

```json
{
  "id": "arrow-smart-1",
  "type": "arrow",
  "x": 600,
  "y": 300,
  "width": 150,
  "height": 180,
  "angle": 0,
  "strokeColor": "#f59e0b",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a22",
  "roundness": {"type": 2},
  "seed": 144,
  "version": 1,
  "versionNonce": 145,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false,
  "points": [[0, 0], [-80, -160], [-150, -180]],
  "lastCommittedPoint": [0, 0],
  "startBinding": {"elementId": "center", "focus": 0, "gap": 10},
  "endBinding": {"elementId": "star-module-1", "focus": 0, "gap": 10},
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

---

## 文本处理规则

### 字符替换

| 原字符 | 替换为 | 说明 |
|-------|-------|------|
| `"` | `『』` | 双引号 |
| `()` | `「」` | 圆括号 |

### 文本格式

```
模块标题
⭐⭐⭐⭐⭐ (如有)

• 要点1
  - 子要点
• 要点2
• 要点3
```

### 字体规范

- **字体家族**：`fontFamily: 5`（Excalifont）
- **行高**：`lineHeight: 1.25`
- **对齐方式**：`textAlign: "left"`, `verticalAlign: "top"`

---

## 自动保存流程

### 1. 生成文件名

格式：`{主题名称}.思维导图.md`

示例：
- `数列极限.思维导图.md`
- `函数极限与连续.思维导图.md`

### 2. 保存位置

保存到用户指定的目录，或当前工作目录。

### 3. 用户反馈

生成完成后报告：
- 文件保存位置（可点击跳转）
- 如何在 Obsidian 中查看
- 思维导图结构概览
- 点击模块可跳转到原笔记

---

## 常见问题排查

### JSON 语法错误

**问题**：思维导图无法显示，提示解析错误。

**检查项**：
1. 确保所有字符串值正确引用
2. 检查是否有未闭合的括号
3. 确保数值类型没有多余引号（如 `"x": 730"` 应为 `"x": 730`）
4. 检查 `points` 数组格式是否正确

### 布局问题

**问题**：元素重叠或位置不当。

**解决方案**：
- 使用智能布局算法自动调整
- 设置 `--style=compact` 紧凑布局
- 减少显示的模块数量

### 链接不工作

**问题**：点击模块无法跳转。

**检查项**：
1. 确保 `link` 字段使用正确的 Obsidian URI 格式
2. 检查文件路径是否正确
3. 确保 vault 名称匹配

---

## 示例输出

```
思维导图已生成！

保存位置：[[考研数学/高数-数列极限/数列极限.思维导图.md]]

使用方法：
1. 在 Obsidian 中打开此文件
2. 按 Ctrl+E（Mac: Cmd+E）切换到阅读模式
3. 点击任意模块可跳转到原笔记

结构概览：
- 中心主题：数列极限
- 核心模块（⭐⭐⭐⭐⭐）：用性质、海涅定理、夹逼准则、单调有界
- 基础模块：数列概念、定义、四则运算、收敛速度
- 辅助系统：索引、进度、总结、错题本

交互功能：
✓ 点击模块跳转到原笔记
✓ 五星模块金色高亮
✓ 智能布局避免重叠
```

---

## 注意事项

1. **JSON 语法严格**：确保 JSON 格式完全正确，任何语法错误都会导致解析失败
2. **坐标系统**：左上角为原点 (0,0)，x 向右增大，y 向下增大
3. **元素 ID 唯一**：每个元素必须有唯一的 `id`
4. **文本长度**：避免单个文本元素过长，适当分行
5. **星级标注**：保留原有的星级标注（⭐），便于识别重点
6. **链接格式**：使用 Obsidian URI 格式确保跳转功能正常
7. **模块数量**：超过10个模块建议使用折叠模式
