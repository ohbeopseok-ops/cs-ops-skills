#!/usr/bin/env python3
"""
Stop hook: SKILL.md 구조 검증

세션 종료 시 변경된 SKILL.md / skills/user/*.md 파일의
필수 구조(front matter, ALWAYS use this exact template)를 검증한다.
문제가 있는 파일 목록을 stdout에 출력한다 (차단하지 않음).

입력(stdin): Claude Code Stop JSON
출력(stdout): 검증 결과 (경고 메시지)
"""

import json
import re
import sys
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\s*\nname:\s*\S+.*\ndescription:\s*.+\n---", re.DOTALL)
TEMPLATE_MARKER = "ALWAYS use this exact template:"


def find_repo_root() -> Path | None:
    candidate = Path.cwd()
    for _ in range(10):
        if (candidate / "CLAUDE.md").exists() or (candidate / ".claude-plugin").exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent
    return None


def validate_skill_file(path: Path) -> list[str]:
    issues = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return [f"읽기 실패: {path}"]

    if not FRONT_MATTER_RE.match(text):
        issues.append("front matter 누락 또는 형식 오류 (name/description 필수)")

    if TEMPLATE_MARKER not in text:
        issues.append(f"'{TEMPLATE_MARKER}' 마커 누락")

    return issues


def main() -> None:
    # Stop 훅은 stdin이 비어있을 수 있음
    raw = sys.stdin.read()
    try:
        json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        pass

    repo_root = find_repo_root()
    if repo_root is None:
        sys.exit(0)

    skill_files = list(repo_root.glob("cs-*/skills/*/SKILL.md")) + \
                  list(repo_root.glob("skills/user/*.md"))

    errors: list[tuple[Path, list[str]]] = []
    for path in skill_files:
        issues = validate_skill_file(path)
        if issues:
            errors.append((path, issues))

    if errors:
        print("⚠️  SKILL.md 구조 검증 경고:")
        for path, issues in errors:
            rel = path.relative_to(repo_root)
            for issue in issues:
                print(f"  {rel}: {issue}")
    else:
        print(f"✅ SKILL.md 구조 검증 완료 ({len(skill_files)}개 파일 이상 없음)")


if __name__ == "__main__":
    main()
