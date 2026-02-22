# Word Template Generator
基于 Claude Code 的 Word 模板处理与文档生成系统

---

## 项目定位

Word Template Generator 是一个 **AgentSkill**，用于处理 Word 文档模板并批量生成文档。

本项目的目标是：

> 让 Word 文档生成自动化、智能化
> 从模板 + 素材 → 成品的零代码解决方案

适用于：

- 合同、发票、报告等标准化文档生成
- 需要批量生成格式统一的 Word 文档
- 使用 Jinja2 模板语法进行动态填充

---

## 核心理念

传统文档生成流程：

设计模板 → 手动填充 → 重复操作 → 容易出错

本系统工作流程：

模板分析
↓
素材整理
↓
智能映射
↓
结构生成
↓
文档渲染

---

## 系统架构

```
用户输入
  ├── Word 模板 (.docx)
  └── 素材文件夹/
       ├── 文本文件
       ├── Excel 表格
       └── 图片资源
         ↓
Claude (数据提取与结构化)
  ├── 分析模板占位符
  ├── 智能映射素材
  └── 生成 JSON 上下文
         ↓
Runtime Tool (文档渲染)
  ├── python-docx 读取模板
  ├── Jinja2 渲染内容
  └── 输出成品文档
```

---

## 支持的占位符语法

### 简单变量
```
Dear {{name}},
Your order {{order_id}} is confirmed.
```

### 列表循环
```
{% for item in items %}
- {{item.name}}: {{item.price}}
{% endfor %}
```

### 条件逻辑
```
{% if is_vip %}
VIP Member Exclusive Offer
{% endif %}
```

### 表格行循环
```
| Product | Quantity | Unit Price |
|---------|----------|------------|
{%tr for product in products %}
| {{product.name}} | {{product.qty}} | {{product.price}} |
{%tr endfor %}
```

---

## 素材文件夹智能映射

推荐命名约定：

| 占位符 | 对应文件 | 说明 |
|--------|----------|------|
| `{{name}}` | name.txt | 纯文本内容 |
| `{{items}}` | items.xlsx | 表格数据转 JSON 数组 |
| `{{logo}}` | logo.png | 图片路径对象 |
| `{{content}}` | content.docx | 嵌入其他 Word 内容 |

---

## 使用示例

### 示例 1：简单合同生成

**模板 (contract_template.docx)**:
```
Contract No: {{contract_no}}

Party A: {{party_a}}
Party B: {{party_b}}

Date: {{date}}
```

**用户输入**:
```
Generate a contract using this template:
/Users/user/contract_template.docx

Party A: Zhang San Company
Party B: Li Si Enterprise
Date: 2026-02-22
Contract No: HT-2026-001
```

---

### 示例 2：带表格的发票生成

**模板 (invoice_template.docx)**:
```
Invoice No: {{invoice_no}}

| Product | Quantity | Unit Price | Total |
|---------|----------|------------|-------|
{%tr for item in items %}
| {{item.name}} | {{item.qty}} | {{item.price}} | {{item.total}} |
{%tr endfor %}

Total: {{total_amount}}
```

---

### 示例 3：使用素材文件夹自动生成

**Materials 文件夹结构**:
```
materials/
├── title.txt           # 季度销售报告
├── project_info.txt    # 项目详情...
├── data_items.xlsx     # 表格数据
└── chart.png           # 图表
```

**用户输入**:
```
Generate document using this template and materials:
Template: /Users/user/report_template.docx
Materials: /Users/user/materials/
```

---

## JSON Schema 数据结构

生成的上下文 JSON 符合以下结构：

```json
{
  "title": "string",
  "content": "string",
  "items": [
    {"name": "string", "value": "number"}
  ],
  "image": {"path": "string", "width": "number"},
  "metadata": {
    "date": "string",
    "author": "string",
    "version": "string"
  }
}
```

---

## 使用边界

本系统提供：

- 模板分析与占位符提取
- 智能素材映射
- 结构化 JSON 生成
- 渲染指导与参考代码

但不替代：

- Python 运行环境
- 实际的 .docx 文件操作
- 复杂格式的手动调整

> Claude 是指挥官，不是执行者
> 实际渲染需要外部 Runtime Tool

---

## 适合人群

- 需要批量生成标准化文档的企业
- 使用 Word 模板进行报告生成的人员
- 希望自动化文档工作流的技术团队
- 使用 Obsidian + Claude Code 的用户

---

## 依赖安装

Runtime Tool 需要以下依赖：

```bash
pip install python-docx docxtpl openpyxl pandas pillow
```

| 依赖 | 用途 |
|------|------|
| python-docx | 读取 .docx 文件 |
| docxtpl | Jinja2 模板渲染 |
| openpyxl | Excel 文件支持 |
| pandas | 数据处理 |
| pillow | 图片处理 |

---

## 项目目标

实现：

- 文档生成零代码化
- 模板与数据分离
- 素材自动映射
- 批量处理高效化
