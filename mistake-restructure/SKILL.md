---
name: mistake-restructure
description: 错题本结构优化技能。自动分析错题关联、按知识点分类索引、生成关联网络图。触发词："重构错题本"、"整理错题结构"、"优化错题索引"。
---

# 错题本重构 (Mistake Restructure)

## 触发条件

- 用户说"重构错题本"、"整理错题结构"
- 用户说"优化错题索引"、"错题分类"
- 用户要求提高错题复习效率

---

## 核心功能

1. **知识点分类** - 自动识别错题主题，按知识点分组
2. **关联网络** - 分析错题间联系，生成 Mermaid 关联图
3. **双向链接** - 为相关错题添加交叉引用标签
4. **备份保护** - 重构前自动备份原文件

---

## 使用方法

### 命令行调用

```bash
# 重构指定错题本
python .claude/skills/mistake-restructure/scripts/restructure.py \
  --input "考研数学/高数-函数极限与连续/错题本.md"

# 预览模式（不修改文件）
python .claude/skills/mistake-restructure/scripts/restructure.py \
  --input "考研数学/高数-数列极限/错题本.md" \
  --preview
```

### 技能调用

```
/mistake-restructure 重构 高数-函数极限与连续 的错题本
```

---

## 输出规范

重构后的错题本结构：
1. **分类索引** - 按知识点分组的错题表格
2. **关联图** - Mermaid 格式的关联网络
3. **关联标签** - 每道错题末尾的交叉引用

---

## 依赖

```bash
pip install pyyaml
```

---

*创建日期: 2026-03-25*
