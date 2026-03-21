# kaoyan-plan 计划模板

本文档包含 kaoyan-plan 技能的所有输出模板。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 目录

1. [模板1: 每日计划（极简版）](#模板1-每日计划极简版)
2. [模板2: 每日计划（标准版）](#模板2-每日计划标准版)
3. [模板3: 周计划（标准/高级）](#模板3-周计划标准高级)
4. [模板4: 周日复盘（强制触发）](#模板4-周日复盘强制触发)
5. [模板5: 补课计划（欠账处理）](#模板5-补课计划欠账处理)

---

## 模板1: 每日计划（极简版）

```markdown
# 今日学习计划 - {date}

## 今日概览
- **空闲时间**: {free_hours}小时
- **今日重点**: {priority_task}

## 学习计划
- [ ] 08:00-10:00 | {subject1} | {task1}
- [ ] 10:00-12:00 | {subject2} | {task2}
- [ ] 14:00-16:00 | {subject3} | {task3}
- [ ] 19:00-21:00 | {subject4} | {task4}

## 备注
{notes}
```

---

## 模板2: 每日计划（标准版）

```markdown
# 今日学习计划 - {date}

## 今日概览
- **阶段**: {phase}
- **距离考试**: {days}天
- **今日精力**: {energy_level}
- **今日重点**: {priority_task}

## 上午计划 (08:00-12:00)
- [ ] {time1} | {subject1} | {task1}
- [ ] {time2} | {subject2} | {task2}

## 下午计划 (14:00-18:00)
- [ ] {time3} | {subject3} | {task3}
- [ ] {time4} | {subject4} | {task4}

## 晚上计划 (19:00-23:00)
- [ ] {time5} | {subject5} | {task5}
- [ ] {time6} | 复盘 | 今日总结

## 备注
{notes}
```

---

## 模板3: 周计划（标准/高级）

```markdown
# 本周学习计划 - 第{week}周

## 本周概览
- **日期**: {start_date} 至 {end_date}
- **阶段**: {phase}
- **距离考试**: {days}天

## 本周目标
- [ ] {goal1}
- [ ] {goal2}
- [ ] {goal3}

## 每日概要
| 日期 | 上午 | 下午 | 晚上 |
|------|------|------|------|
| 周一 | {morning1} | {afternoon1} | {evening1} |
| 周二 | {morning2} | {afternoon2} | {evening2} |
| ... | ... | ... | ... |

## 调整建议
{suggestions}
```

---

## 模板4: 周日复盘（强制触发）

```markdown
# 周日复盘 - 第{week}周 ({date})

## 本周完成度
| 科目 | 计划时长 | 实际时长 | 完成率 | 欠账 |
|------|----------|----------|--------|------|
| 数学 | {math_plan}h | {math_actual}h | {math_rate}% | {math_debt}h |
| 英语 | {eng_plan}h | {eng_actual}h | {eng_rate}% | {eng_debt}h |
| 专业课 | {major_plan}h | {major_actual}h | {major_rate}% | {major_debt}h |
| 政治 | {pol_plan}h | {pol_actual}h | {pol_rate}% | {pol_debt}h |

## 🔴 错题重做（必做，2小时）
- [ ] 19:30-20:00 | 数学错题本 | 30分钟
- [ ] 20:00-20:30 | 英语阅读错题 | 30分钟
- [ ] 20:30-21:00 | 专业课错题 | 30分钟
- [ ] 21:00-21:30 | 政治选择题错题 | 30分钟

## 进度对齐检查
- [ ] 本周目标达成：{goals_status}
- [ ] 欠账处理决策：{debt_decision}
- [ ] 下周重点调整：{next_week_focus}

## 下周计划
{next_week_plan}
```

---

## 模板5: 补课计划（欠账处理）

```markdown
# 今日计划（含补课） - {date}

## ⚠️ 欠账提醒
昨日未完成任务：{debt_tasks}
欠账时长：{debt_hours}小时

## 补课安排
- [ ] {time1} | {subject1} | 【补课】{task1}

## 今日新内容
- [ ] {time2} | {subject2} | {task2}

## 调整说明
今日已压缩{compressed_subject}时间用于补课
```

---

## 模板变量说明

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `{date}` | 日期 | 2025-02-26 |
| `{free_hours}` | 空闲时长 | 8 |
| `{priority_task}` | 今日重点 | 高数第五章 |
| `{phase}` | 学习阶段 | 基础期/强化期/冲刺期 |
| `{days}` | 距离考试天数 | 280 |
| `{energy_level}` | 今日精力 | 正常/有点累 |
| `{subject1-N}` | 科目名称 | 数学/英语/专业课 |
| `{task1-N}` | 任务内容 | 第五章练习 |
| `{week}` | 周数 | 5 |
| `{start_date}` | 周开始日期 | 2025-02-24 |
| `{end_date}` | 周结束日期 | 2025-03-02 |
| `{debt_tasks}` | 欠账任务列表 | 高数练习、英语阅读 |
| `{debt_hours}` | 欠账时长 | 2 |

---

> 📋 **返回主文档**: [skill.md](skill.md)
