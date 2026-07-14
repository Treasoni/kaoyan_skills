#!/usr/bin/env bash
# Install and audit prompt-cache conventions for Claude Code and Claude Code projects.

set -euo pipefail

MODE="check"
PLATFORM="both"
TARGET_DIR="."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSET_DIR="${PROMPT_CACHE_ASSET_DIR:-$SCRIPT_DIR}"

if [ ! -f "$ASSET_DIR/llm-usage-event.schema.json" ] && [ -d "$SCRIPT_DIR/../assets" ]; then
  ASSET_DIR="$SCRIPT_DIR/../assets"
fi

usage() {
  cat <<'USAGE'
Usage:
  prompt-cache-bootstrap.sh [--check|--apply] [--platform codex|claude|both] [--target DIR]

Modes:
  --check              Report missing cache configuration and suspicious prompt content (default).
  --apply              Install rules, entry-point references, telemetry assets, and regression cases.

Options:
  --platform PLATFORM  Configure codex, claude, or both (default: both).
  --target DIR         Target project root (default: current directory).
  --help               Show this help message.

Examples:
  bash prompt-cache-bootstrap.sh --check --target ../my-project
  bash prompt-cache-bootstrap.sh --apply --platform both --target ../my-project
USAGE
}

log() {
  printf '%s\n' "prompt-cache: $*"
}

warn() {
  printf '%s\n' "prompt-cache: warning: $*" >&2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --check)
      MODE="check"
      ;;
    --apply)
      MODE="apply"
      ;;
    --platform)
      if [ "$#" -lt 2 ]; then
        warn "--platform requires codex, claude, or both"
        exit 2
      fi
      PLATFORM="$2"
      shift
      ;;
    --target)
      if [ "$#" -lt 2 ]; then
        warn "--target requires a directory"
        exit 2
      fi
      TARGET_DIR="$2"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      warn "unknown option: $1"
      usage >&2
      exit 2
      ;;
  esac
  shift
done

case "$PLATFORM" in
  codex|claude|both) ;;
  *)
    warn "platform must be codex, claude, or both"
    exit 2
    ;;
esac

if [ ! -d "$TARGET_DIR" ]; then
  warn "target directory not found: $TARGET_DIR"
  exit 1
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

platform_enabled() {
  local name="$1"
  [ "$PLATFORM" = "both" ] || [ "$PLATFORM" = "$name" ]
}

rule_content() {
  cat <<'RULES'
# Prompt Cache Rules

## Prompt Order

For every high-frequency request, keep this order:

1. Stable role, task boundaries, and safety rules.
2. Stable tool constraints, output format, and quality requirements.
3. Stable examples, only when they materially improve the result.
4. Dynamic parameters: user request, file excerpts, dates, runtime state, and IDs.

Keep stable content at the beginning and dynamic content at the end. Reuse the same stable prefix for the same task type.

## Stability

- Do not put timestamps, random IDs, UUIDs, git status, live TODOs, or user input in the stable prefix.
- Do not casually reorder or reword stable prompt sections, punctuation, or whitespace.
- Keep one authoritative template for each high-frequency task.
- Keep model settings and tool definitions stable when cache reuse matters.
- Keep dynamic parameter names and order stable; use `none` for missing values.

## Context Loading

- Prefer paths, headings, anchors, and summaries before loading full content.
- Load only the file sections needed for the current task.
- Do not preload build output, dependencies, logs, mirrored configuration, or unrelated examples.
- Save reusable long results as structured files and reference them instead of pasting them again.

## Subagents

- Put fixed responsibilities, output format, and prohibitions before the parameter block.
- Put all task-specific values in a final `Parameters` block.
- Return structured summaries, links, citations, and conclusions instead of full source text.

## Standard Template

```text
You are {stable_role}.

Task boundaries:
{stable_boundaries}

Output format:
{stable_output_format}

Quality requirements:
{stable_quality_requirements}

Prohibitions:
{stable_prohibitions}

Parameters:
- Task: {dynamic_task}
- User request: {dynamic_request}
- Input reference: {dynamic_input_reference}
- Current state: {dynamic_state}
- Extra constraints: {dynamic_constraints}
```
RULES
}

install_asset() {
  local source_file="$1"
  local target_file="$2"

  if [ ! -f "$source_file" ]; then
    warn "template asset is missing: $source_file"
    exit 1
  fi

  if [ -f "$target_file" ]; then
    log "kept existing $target_file"
    return
  fi

  mkdir -p "$(dirname "$target_file")"
  cp "$source_file" "$target_file"
  log "created $target_file"
}

install_observability() {
  local observability_dir="$TARGET_DIR/.llm/prompt-cache"

  install_asset "$ASSET_DIR/llm-usage-event.schema.json" "$observability_dir/llm-usage-event.schema.json"
  install_asset "$ASSET_DIR/prompt-cache-regression-cases.json" "$observability_dir/regression-cases.json"
}

entry_block() {
  local rule_path="$1"
  cat <<RULES
<!-- prompt-cache-bootstrap:begin -->
## Prompt Cache

- Follow \`$rule_path\` for high-frequency prompt design.
- Keep stable instructions and output formats before dynamic user input, file excerpts, dates, IDs, and runtime state.
- Reuse canonical templates and load long context only when needed.
<!-- prompt-cache-bootstrap:end -->
RULES
}

install_rule() {
  local platform_dir="$1"
  local entry_file="$2"
  local relative_rule_path="$3"
  local rule_file="$TARGET_DIR/$platform_dir/rules/common/prompt-cache.md"
  local entry_path="$TARGET_DIR/$entry_file"

  if [ ! -f "$rule_file" ]; then
    mkdir -p "$(dirname "$rule_file")"
    rule_content > "$rule_file"
    log "created $rule_file"
  else
    log "kept existing $rule_file"
  fi

  if [ -f "$entry_path" ] && grep -qF '<!-- prompt-cache-bootstrap:begin -->' "$entry_path"; then
    log "entry block already present in $entry_path"
    return
  fi

  if [ ! -f "$entry_path" ]; then
    printf '# Project Instructions\n' > "$entry_path"
  fi

  {
    printf '\n'
    entry_block "$relative_rule_path"
  } >> "$entry_path"
  log "updated $entry_path"
}

check_rule() {
  local platform_dir="$1"
  local entry_file="$2"
  local rule_file="$TARGET_DIR/$platform_dir/rules/common/prompt-cache.md"
  local entry_path="$TARGET_DIR/$entry_file"

  if [ -f "$rule_file" ]; then
    log "found $rule_file"
  else
    warn "missing $rule_file"
  fi

  if [ -f "$entry_path" ] && grep -qF '<!-- prompt-cache-bootstrap:begin -->' "$entry_path"; then
    log "found cache entry block in $entry_path"
  else
    warn "missing cache entry block in $entry_path"
  fi
}

check_observability() {
  local observability_dir="$TARGET_DIR/.llm/prompt-cache"
  local asset

  for asset in "llm-usage-event.schema.json" "regression-cases.json"; do
    if [ -f "$observability_dir/$asset" ]; then
      log "found $observability_dir/$asset"
    else
      warn "missing $observability_dir/$asset"
    fi
  done
}

scan_prompts() {
  local root="$1"
  local prompt_dir
  local found=0

  for prompt_dir in "$root/prompts" "$root/.co""dex/prompts" "$root/.claude/prompts"; do
    [ -d "$prompt_dir" ] || continue
    found=1
    while IFS= read -r -d '' file; do
      if grep -nEi 'timestamp|uuid|random id|git status|current time|当前时间|任务[[:space:]]*ID|随机[[:space:]]*ID' "$file"; then
        warn "review dynamic value placement in $file (it should be in the final Parameters block)"
      fi
    done < <(find "$prompt_dir" -type f \( -name '*.md' -o -name '*.txt' \) -print0)
  done

  if [ "$found" -eq 0 ]; then
    log "no prompt directories found; skipped dynamic-value scan"
  fi
}

if [ "$MODE" = "apply" ]; then
  if platform_enabled codex; then
    install_rule ".co""dex" "AGENTS.md" ".co""dex/rules/common/prompt-cache.md"
  fi
  if platform_enabled claude; then
    install_rule ".claude" "CLAUDE.md" ".claude/rules/common/prompt-cache.md"
  fi
  install_observability
  log "installation complete; run --check to review the project"
else
  if platform_enabled codex; then
    check_rule ".co""dex" "AGENTS.md"
  fi
  if platform_enabled claude; then
    check_rule ".claude" "CLAUDE.md"
  fi
  check_observability
  scan_prompts "$TARGET_DIR"
fi
