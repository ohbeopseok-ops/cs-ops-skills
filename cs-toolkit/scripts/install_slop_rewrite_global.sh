#!/usr/bin/env bash
# slop-rewrite 전역 스킬 등록 (Claude Code). 여러 번 실행해도 안전하다.
# 사용: bash install-global.sh [클론경로]   (기본: 이 스크립트가 있는 폴더)
set -euo pipefail

REPO_URL="https://github.com/byungjunjang/slop-rewrite.git"
ROOT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

if [ ! -f "$ROOT/.claude/skills/slop-rewrite/SKILL.md" ]; then
  echo "저장소가 없어 클론합니다: $ROOT"
  git clone "$REPO_URL" "$ROOT"
fi

declare -A DESC=(
  [slop-rewrite]='한국어 문서 윤문·퇴고·AI 티 제거·검토는 slop-rewrite 파이프라인으로 한다. 트리거 · "윤문해줘", "퇴고해줘", "AI 티 없애줘", "검토만", "/slop-rewrite".'
  [styleguide-builder]='한국어 글 코퍼스(블로그/URL/.md 폴더)에서 문체 가이드라인과 검사 키트를 만든다. 트리거 · "문체 가이드라인 만들어", "내 블로그 문체 분석", "/styleguide-builder".'
  [taste-builder]='산출물을 코멘트용 아티팩트로 올리고 코멘트·대화의 글쓰기 취향을 취향 문서로 증류한다. 트리거 · "코멘트 달 수 있게 올려줘", "취향으로 기록해줘", "/taste-builder".'
)

for name in slop-rewrite styleguide-builder taste-builder; do
  body="$ROOT/.claude/skills/$name/SKILL.md"
  [ -f "$body" ] || { echo "본체 없음: $body" >&2; exit 1; }
  mkdir -p "$SKILLS_DIR/$name"
  cat > "$SKILLS_DIR/$name/SKILL.md" <<EOT
---
name: $name
description: ${DESC[$name]}
---
본체는 \`$body\` 다. 그 파일을 읽고 따르며, 상대 경로 명령은 \`$ROOT\` 에서 돌린다. 원칙·스타일가이드·취향은 그 폴더의 것을 쓴다.
EOT
  echo "등록: $SKILLS_DIR/$name"
done
echo "완료. Claude Code를 새로 시작하면 전역 스킬 3개가 보입니다."
