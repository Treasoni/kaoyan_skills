---
name: sync
description: This skill should be used when the user asks to sync study progress with MemOS, especially `/sync 拉取` to read the latest cross-device context or `/sync 上传` to save today's learning state from local notes.
version: 1.0.0
---

# MemOS Sync Skill

## Purpose

Use this skill when the user says:
- `/sync`
- `/sync 拉取`
- `/sync 上传`
- "同步学习进度"
- "拉取最新进度"
- "把今天学习情况上传到 MemOS"

This skill bridges local notes and MemOS so Codex can participate in the same workflow as Claude Code.

## Operating Modes

### 1. `/sync 拉取`

Goal: retrieve the latest study context before planning or studying.

Preferred data sources:
1. `MemoryOperatingSystem` MCP
2. local study progress files as fallback if MCP is unavailable

What to collect:
- user profile and exam target
- recent study records
- English vocabulary review status
- math progress
- electronics / 822 progress
- weak points from mistakes and understanding records

Expected output sections:
- `## 🔄 MemOS 同步报告`
- `### 📋 用户画像`
- `### 📚 最近学习记录`
- `### 📖 英语词汇状态`
- `### 🧮 数学学习进度`
- `### ⚡ 专业课学习进度`
- `### ⚠️ 复习提醒`
- `### 🎯 薄弱知识点提醒`
- `### 📝 下一步建议`

### 2. `/sync 上传`

Goal: save today's local learning state into MemOS after studying.

Preferred sources:
- `考研计划/每日计划/{date}-每日计划.md`
- `考研英语/📅 复习计划.md`
- `考研英语/📊 学习进度.md`
- `考研数学/**/📊 学习进度.md`
- `考研专业课/📊 学习进度.md`
- relevant chapter notes with `tags`

What to extract:
- date
- study duration
- subjects studied
- completion status
- vocabulary / math / electronics progress
- next step
- note tags formatted as hashtags

Expected output sections:
- `## 📤 上传到 MemOS`
- `### ✅ 已读取`
- `### 📦 已上传`
- `### ✅ 上传成功`

## Safety Rules

1. Sync should summarize and persist learning state, not rewrite source notes unless the user also asked for note updates.
2. Never edit protected sections or `> [!personal]` blocks during sync.
3. If MemOS MCP is unavailable, clearly say the result is a local-only fallback summary and no remote sync happened.

## Codex Compatibility Note

This skill depends on the project-local Codex MCP configuration in `.codex/config.toml`. Keep Claude settings in `.claude/` untouched.
