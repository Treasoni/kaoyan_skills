# 考研项目技能体系地图

## 1. 当前审查结论

本项目技能数量较多，但主要问题不是“能力太多”，而是缺少统一层级：

| 问题 | 表现 | 重构方向 |
| --- | --- | --- |
| 入口过多 | 用户可能直接面对 40+ 个技能名 | 日常只暴露 L1 入口 |
| 子技能边界不统一 | 数学、英语、专业课各自有 core/notes/review/sop 等命名体系 | 统一成“路由器 + 子模块”模式 |
| 工具技能混入学习技能 | pdf、docx、opencli、Obsidian 等与学习任务平铺 | 作为 L3 工具，按需启用 |
| Claude 侧能力缺口 | 审查时 `.claude/skills` 缺少 `parse-words`、`sync`、`understanding` | 已镜像补齐，后续保持一致性检查 |
| 技能维护成本高 | 部分技能过长、旧入口命名不统一 | 用 `/skill-refactor` 和标准 `SKILL.md` 管理 |

---

## 2. 目标架构

```text
用户请求
  |
  v
L1 入口路由
  |-- /sync
  |-- /kaoyan-plan
  |-- /kaoyan-math
  |-- /kaoyan-english
  |-- /kaoyan-electronics
  |-- /understanding
  |-- /mistake-book
  |
  v
L2 领域模块
  |-- math: core / notes / structure
  |-- english: core / vocab / review / quiz / writing
  |-- electronics: core / sop / circuit / structure
  |
  v
L3 工具能力
  |-- 文件: pdf / docx / word-template-generator
  |-- Obsidian: obsidian-cli / obsidian-markdown / obsidian-bases / json-canvas
  |-- 图示: excalidraw-diagram / math-graph / knowledge-mindmap
  |-- 搜索: smart-search / defuddle / kaoyan-info
  |-- 维护: skill-refactor / digest / fix-table-pipe
```

---

## 3. 日常任务入口

| 用户意图 | 首选入口 | 备注 |
| --- | --- | --- |
| 今天怎么安排、补课、复盘、完成汇报 | `/kaoyan-plan` | 统一处理计划与进度落盘 |
| 数学概念、笔记、题目、结构 | `/kaoyan-math` | 由路由器决定 notes/core/structure |
| 英语单词、阅读词汇、复习、测试、写作 | `/kaoyan-english` | 高亮词汇解析优先 `/parse-words` |
| 822 专业课、电路图、SOP、知识结构 | `/kaoyan-electronics` | 先参考 `考研专业课/📘 822电子技术基础考研学习体系.md`，图片/电路题优先 circuit |
| 822 电路图生成、模电图、微变等效图 | `/kaoyan-electronics` -> `kaoyan-electronics-circuit` | 先读 `references/circuit-diagram-generation.md`，默认生成 Obsidian Excalidraw |
| 我这样理解对不对、推导检查 | `/understanding` | 输出可写入 `[!personal]` 的记录 |
| 记录错题、提炼错题、优化错题索引 | `/mistake-book` 或 `mistake-*` | 先判断学科与知识模块 |
| 同步上下文 | `/sync 拉取` / `/sync 上传` | 每日开始与结束使用 |

---

## 4. 子模块边界

### 数学
| 子技能 | 只在何时调用 |
| --- | --- |
| `kaoyan-math-notes` | 生成/更新数学笔记、补充推导、整理听课疑问 |
| `kaoyan-math-structure` | 查询章节结构、知识点关系、前后置关系 |
| `kaoyan-math-core` | 状态、欠账、MemOS、跨学科关联 |

### 英语
| 子技能 | 只在何时调用 |
| --- | --- |
| `kaoyan-english-vocab` | 单词表整理、查词、词族、考频、PDF 导出处理 |
| `kaoyan-english-review` | 间隔重复、复习计划、复习统计 |
| `kaoyan-english-quiz` | 单词/僻义测试 |
| `kaoyan-english-writing` | 写作替换、汉译英、输出训练 |
| `kaoyan-english-core` | 状态、配置、MemOS、欠账 |

### 专业课
| 子技能 | 只在何时调用 |
| --- | --- |
| `kaoyan-electronics-circuit` | 电路图、静态分析、动态分析、图片题 |
| `kaoyan-electronics-sop` | 解题流程、题型模板、反馈判断、计数器设计 |
| `kaoyan-electronics-structure` | 知识图谱、章节复习、前置知识 |
| `kaoyan-electronics-core` | 状态、配置、MemOS、数学前置检查 |

---

## 5. 新技能准入规则

新建技能前必须满足至少两条：
- 触发语义稳定，能被一句话描述清楚。
- 输出格式稳定，反复使用时能节省明显时间。
- 涉及独立文件格式、外部工具或长期状态。
- 不适合放进现有 L1 入口或 L2 子模块。

不满足时，优先把规则加入现有技能、模板或 `.learnings/RULES.md`。

---

## 6. 维护检查清单

每次修改技能体系后检查：
- `AGENTS.md` 与 `CLAUDE.md` 核心规则一致。
- `.agents/skills` 与 `.claude/skills` 能力等价。
- 新增学习规则没有直接写进 `CLAUDE.md`，而是进入 `.learnings/RULES.md`。
- `SKILL.md` 不超过 300 行；长模板和代码已拆到外部文件。
- Obsidian 表格、LaTeX 管道符、证明折叠块符合项目规则。
