#!/usr/bin/env bash
# install-skills.sh — 安装/同步 skills/ 到目标技能目录（bash 跨平台版，行为与 install-skills.ps1 一致）
#
# 用法：
#   ./install-skills.sh                            # 安装：只覆盖有差异的技能（默认装到 ~/.codex/skills）
#   ./install-skills.sh --mode check               # 只检测漂移，不改动任何文件（有漂移退出码 1）
#   ./install-skills.sh --dest ~/.claude/skills    # 指定目标目录（多 harness：~/.claude/skills、~/.zcode/skills 等）
#   ./install-skills.sh --source /path/to/repo     # 指定源仓库根目录（默认脚本所在目录）
#
# 行为约定（与 install-skills.ps1 一致）：
# - install 按整目录重建目标技能目录，会清掉源端已删除的文件（真正的同步语义）。
# - 只处理源端 skills/ 下存在的技能目录；绝不触碰目标目录下其它内容（如 .system）。
# - check 模式：无漂移退出码 0，有漂移退出码 1，可直接用于 CI 或定期自检。
# - 文件比对用 cmp 字节级比较，无外部依赖（不要求 sha256sum）。

set -u

MODE="install"
SOURCE_ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST_ROOT="${HOME}/.codex/skills"

while [ $# -gt 0 ]; do
  case "$1" in
    --mode)   MODE="${2:?--mode 需要 install 或 check}"; shift 2 ;;
    --source) SOURCE_ROOT="${2:?--source 需要一个目录}"; shift 2 ;;
    --dest)   DEST_ROOT="${2:?--dest 需要一个目录}"; shift 2 ;;
    *) echo "[错误] 未知参数：$1（支持 --mode install|check / --source <dir> / --dest <dir>）" >&2; exit 2 ;;
  esac
done

case "$MODE" in install|check) ;; *) echo "[错误] MODE 只能是 install 或 check：$MODE" >&2; exit 2 ;; esac

SRC_SKILLS="${SOURCE_ROOT}/skills"
if [ ! -d "$SRC_SKILLS" ]; then
  echo "[错误] 未找到源目录：$SRC_SKILLS"
  exit 2
fi

# 容忍带引号的波浪号路径（--dest '~/x'）
case "$DEST_ROOT" in
  "~"*) DEST_ROOT="${DEST_ROOT/#\~/$HOME}" ;;
esac

list_files() { # $1 = 目录；输出相对路径（按字节排序，保证跨平台一致）
  (cd "$1" && find . -type f | sed 's|^\./||' | LC_ALL=C sort)
}

skills=(); statuses=()
for src_dir in "$SRC_SKILLS"/*/; do
  [ -d "$src_dir" ] || continue
  name="$(basename "$src_dir")"
  dst_dir="$DEST_ROOT/$name"
  st="same"
  if [ ! -d "$dst_dir" ]; then
    st="missing"
  else
    src_list="$(list_files "$src_dir")"
    dst_list="$(list_files "$dst_dir")"
    if [ "$src_list" != "$dst_list" ]; then
      st="drift"
    else
      while IFS= read -r f; do
        [ -n "$f" ] || continue
        if ! cmp -s "$src_dir/$f" "$dst_dir/$f"; then st="drift"; break; fi
      done <<< "$src_list"
    fi
  fi
  skills+=("$name"); statuses+=("$st")
done

if [ "${#skills[@]}" -eq 0 ]; then
  echo "[错误] 源目录为空：$SRC_SKILLS"
  exit 2
fi

echo ""
echo "源  ：$SRC_SKILLS"
echo "目标：$DEST_ROOT"
echo "模式：$MODE"
echo '-----------------------------------------'
i=0
while [ "$i" -lt "${#skills[@]}" ]; do
  case "${statuses[$i]}" in
    same)    l='一致    ' ;;
    missing) l='未安装' ;;
    drift)   l='有差异' ;;
  esac
  echo "  [$l] ${skills[$i]}"
  i=$((i + 1))
done

if [ "$MODE" = "check" ]; then
  echo '-----------------------------------------'
  drift=0
  i=0
  while [ "$i" -lt "${#skills[@]}" ]; do
    [ "${statuses[$i]}" != "same" ] && drift=$((drift + 1))
    i=$((i + 1))
  done
  if [ "$drift" -eq 0 ]; then
    echo '结果：无漂移，源与安装端完全一致。'
    exit 0
  fi
  echo "结果：$drift 个技能存在漂移（未安装或有差异）。运行不带参数的 install-skills.sh 可修复。"
  exit 1
fi

mkdir -p "$DEST_ROOT"
i=0; updated=0
while [ "$i" -lt "${#skills[@]}" ]; do
  if [ "${statuses[$i]}" != "same" ]; then
    rm -rf "$DEST_ROOT/${skills[$i]}"
    cp -R "$SRC_SKILLS/${skills[$i]}" "$DEST_ROOT/"
    echo "  已安装/更新：${skills[$i]}"
    updated=$((updated + 1))
  fi
  i=$((i + 1))
done
echo '-----------------------------------------'
echo "完成：共 ${#skills[@]} 个技能，本次更新 $updated 个。"
echo '提示：需重启对应智能体（Codex / Claude Code / ZCode 等）并新开会话，技能元数据才会被加载。'
exit 0
