---
name: digest
description: 自我学习阶段。回顾本次学习会话，记录学习心得和错误到 .learnings/，当文件超阈值时自动压缩去重，更新 RULES.md，促进系统持续改进。触发时机：用户审核通过 evaluate 产出并明确要求记录学习后，Phase 6。
---

# Skill: digest（自我学习）

## 触发时机
用户审核通过 evaluate 产出后，且用户明确要求记录会话学习时。

## 输入
- `SYSTEM_ROOT`: StudySystem 根路径，如 `{VAULT_PATH}/StudySystem`
- `topic`: 主题名称

## 执行步骤

### Step 1: 检查压缩阈值

在记录新条目之前，检查是否需要先做压缩：

```bash
wc -l .learnings/LEARNINGS.md .learnings/ERRORS.md 2>/dev/null || echo "0 .learnings/LEARNINGS.md\n0 .learnings/ERRORS.md"
```

如果任一文件超过 100 行，先执行压缩流程：

1. 读取 `.learnings/LEARNINGS.md` 和 `.learnings/ERRORS.md` 中的所有条目
2. 按主题/模式分组，去重
3. 写入/更新 `.learnings/RULES.md`：
   - `## Do` — 值得坚持的做法
   - `## Don't` — 需要避免的错误
   - `## Watch For` — 需要特别注意的情况
   - 每行一条规则，合并重复出现：`(3x) 用 X 而非 Y`
   - 丢弃只出现一次的孤立噪声
4. 归档旧条目到 `.learnings/archive/YYYY-MM-DD.md`
5. 截断 `.learnings/LEARNINGS.md` 和 `.learnings/ERRORS.md` 只保留头部

### Step 2: 确保 .learnings/ 目录存在

```bash
mkdir -p .learnings
```

如果 `.learnings/LEARNINGS.md` 或 `.learnings/ERRORS.md` 不存在，创建最小头部。

### Step 3: 回顾本次会话

扫描评估发现和会话过程中遇到的任何问题：
- 是否有论断被判定为不准确？ → 记录到 `.learnings/LEARNINGS.md`，类别 `correction`
- 整理资料是否有缺口？ → 记录到 `.learnings/LEARNINGS.md`，类别 `knowledge_gap`
- collect/curate/write/beautify 阶段是否有报错？ → 记录到 `.learnings/ERRORS.md`
- 是否有值得未来 Study System 运行时参考的模式？ → 记录到 `.learnings/LEARNINGS.md`，类别 `best_practice`

### Step 4: 记录条目

使用自改进格式记录：

**学习条目**（追加到 `.learnings/LEARNINGS.md`）：
```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high
**Status**: pending
**Area**: docs

### Summary
One-line description

### Details
What happened, what was learned

### Suggested Action
What to do differently next time

---
```

**错误条目**（追加到 `.learnings/ERRORS.md`）：
```markdown
## [ERR-YYYYMMDD-XXX] phase_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Brief description of what failed

### Error
```
Actual error message
```

### Context
What was being attempted

---
```

### Step 4.5: RULES.md 冲突检测与同步

**每次追加新条目到 LEARNINGS.md 后，必须执行本步骤**，检查新条目是否与 `.learnings/RULES.md` 中现有规则存在冲突。

#### 4 类冲突定义

1. **方向冲突**：新条目的 Suggested Action 与 RULES.md Do/Don't 区直接矛盾
   - 例：RULES.md 写 `Do: 表格 LaTeX 用 \lvert \rvert`，新条目写 `用 | 即可`
2. **例外冲突**：新条目声明自己是某规则的例外
   - 例：RULES.md 写 `Don't: Callout 内不要 $$`，新条目写 `嵌套 callout 内层允许 $$`
3. **优先级冲突**：新条目要求覆盖某规则
   - 例：RULES.md 写 `X 应该 Y`，新条目写 `用户明确要求时 X 可以不 Y`
4. **模式遗漏**：新条目提到的问题模式尚未在 Watch For 区追踪
   - 例：新增了"嵌套 callout 证明"问题，但 Watch For 区无 `obsidian.proof_*` 模式键

#### 执行流程

1. 读取新追加条目的 `Summary` / `Details` / `Suggested Action`
2. 读取 `.learnings/RULES.md` 全文（Do / Don't / Watch For 三个区块）
3. 逐条比对，识别冲突类型（见上）
4. 输出**冲突报告**（无冲突时跳过本步骤）：

   ```markdown
   ## 🔍 RULES.md 冲突检测报告

   **新条目**: [LRN-YYYYMMDD-XXX] category
   **冲突项**: N 处

   | # | 类型 | 现有规则 | 新条目主张 | 建议处理 |
   |---|------|----------|------------|----------|
   | 1 | 例外冲突 | Don't: 单层 callout 不要 `$$` | 嵌套 callout 内层允许 `$$` | Don't 改为 "单层 callout 不要 `$$`；嵌套 callout 内层例外" |
   | 2 | 模式遗漏 | Watch For 无 `obsidian.proof_*` | 新增嵌套 callout 证明模式 | Watch For 补充 `obsidian.proof_collapsible` |
   ```

5. **关键：等待用户确认**。使用 AskUserQuestion 询问：
   - 选项 1：全部按建议处理
   - 选项 2：仅处理部分冲突（让用户指明）
   - 选项 3：暂不同步，保留 pending 状态
6. 用户确认后：
   - 按"建议处理"列修改 RULES.md 对应区块（Do/Don't/Watch For）
   - 在新学习条目里追加 `### Resolution` 字段（说明同步动作与日期）
   - 将 `Status` 从 `pending` 改为 `resolved`
   - 若新增了 Watch For 模式键，补充 `### Related Rules: Pattern-Key: xxx`
   - 增加原 `(Nx)` 计数（合并到 RULES.md 时与去重流程一致）

#### 未确认时的回退

- 仅记录冲突报告，不修改 RULES.md
- LEARNINGS.md 条目 Status 保持 `pending`
- 在本步骤末尾向用户提示：`检测到 N 处冲突，请确认是否同步 RULES.md`

### Step 5: 无意义则不记录

如果本次会话没有错误且没有值得记录的学习点，跳过记录 —— 不创建空条目。质量比数量重要。

## 产出
- `.learnings/LEARNINGS.md`：追加新学习条目（如有）
- `.learnings/ERRORS.md`：追加新错误条目（如有）
- `.learnings/RULES.md`：
  - 压缩后的去重规则（仅当触发压缩时）
  - **冲突同步后的更新条目**（仅当 Step 4.5 检测到冲突且用户确认时）
- `.learnings/archive/YYYY-MM-DD.md`：归档文件（如触发压缩）

## 禁止行为
- 不要修改笔记本身
- 不要编造学习条目
- 不要跳过压缩阈值检查
- 不要归档未压缩的条目
- 不要在无意义时强行记录
- **不要未经用户确认就修改 RULES.md** — 冲突同步是确认制，不是自动制
- **不要将新规则提升到 CLAUDE.md** — 新规则仅写入 `.learnings/RULES.md`，由 hook 在 agent 启动时注入

## 硬停止 (Hard Stop)

本阶段任务完成。向用户展示捕获的学习摘要和压缩结果（如有）。

**严禁调用其他阶段技能。**
询问用户："学习记录完成。可以结束了吗？"
