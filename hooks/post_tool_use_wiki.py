#!/usr/bin/env python3
"""
PostToolUse hook: Wiki 자동 업데이트

Write / Edit 도구 실행 후 skills 관련 파일이 변경되면
wiki/log.md에 날짜별 변경 항목을 자동으로 기록한다.

감지 대상:
  - skills/user/<skill>.md
  - cs-<plugin>/skills/<skill>/SKILL.md

입력(stdin): Claude Code PostToolUse JSON
출력: 없음 (로그만 기록)
"""

import json
import re
import sys
from datetime import date
from pathlib import Path


# 스킬 파일 패턴
SKILL_PATTERNS = [
    re.compile(r"skills/user/[\w-]+\.md$"),
    re.compile(r"cs-[\w-]+/skills/[\w-]+/SKILL\.md$"),
]


def find_repo_root(file_path: Path) -> Path | None:
    """CLAUDE.md 또는 .claude-plugin 디렉토리가 있는 리포지토리 루트를 찾는다."""
    candidate = file_path if file_path.is_dir() else file_path.parent
    for _ in range(10):
        if (candidate / "CLAUDE.md").exists() or (candidate / ".claude-plugin").exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent
    return None


def is_skill_file(file_path: str) -> bool:
    """파일 경로가 스킬 관련 파일인지 확인한다."""
    normalized = file_path.replace("\\", "/")
    return any(p.search(normalized) for p in SKILL_PATTERNS)


def detect_action(tool_name: str) -> str:
    return "추가" if tool_name == "Write" else "수정"


def build_log_entry(relative_path: str, action: str) -> str:
    skill_name = Path(relative_path).stem
    return f"- `{relative_path}` — {action} (`{skill_name}`)\n"


def insert_into_log(log_text: str, today: str, entry: str) -> str:
    """
    오늘 날짜 섹션이 있으면 'PostToolUse 자동 기록' 블록에 항목을 추가하고,
    없으면 '변경 이력 형식' 푸터 앞에 새 섹션을 삽입한다.
    """
    today_header = f"## {today}"
    auto_block = "#### PostToolUse 자동 기록"

    if today_header in log_text:
        # 이미 오늘 섹션이 존재
        if auto_block in log_text:
            # auto_block 다음 줄에 항목 추가
            idx = log_text.index(auto_block) + len(auto_block)
            return log_text[:idx] + "\n\n" + entry + log_text[idx:].lstrip("\n")
        else:
            # 오늘 섹션에 auto_block 삽입
            idx = log_text.index(today_header) + len(today_header)
            block = f"\n\n{auto_block}\n\n{entry}"
            return log_text[:idx] + block + log_text[idx:]
    else:
        # 오늘 섹션이 없음 — 푸터 바로 앞에 삽입
        footer_marker = "## 변경 이력 형식"
        new_section = (
            f"## {today}\n\n"
            f"{auto_block}\n\n"
            f"{entry}\n"
            f"---\n\n"
        )
        if footer_marker in log_text:
            idx = log_text.index(footer_marker)
            return log_text[:idx] + new_section + log_text[idx:]
        else:
            return log_text.rstrip("\n") + f"\n\n---\n\n{new_section}"


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path_str = data.get("tool_input", {}).get("file_path", "")
    if not file_path_str or not is_skill_file(file_path_str):
        sys.exit(0)

    file_path = Path(file_path_str)
    repo_root = find_repo_root(file_path)
    if repo_root is None:
        sys.exit(0)

    log_path = repo_root / "wiki" / "log.md"
    if not log_path.exists():
        sys.exit(0)

    try:
        relative_path = str(file_path.relative_to(repo_root))
    except ValueError:
        relative_path = file_path_str

    action = detect_action(tool_name)
    entry = build_log_entry(relative_path, action)
    today = date.today().isoformat()

    log_text = log_path.read_text(encoding="utf-8")
    updated = insert_into_log(log_text, today, entry)
    log_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
