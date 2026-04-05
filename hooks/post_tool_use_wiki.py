#!/usr/bin/env python3
"""
PostToolUse Hook — Wiki Raw Auto-Save
cs-ops-skills / JOYLAB 위키 자동 저장 레이어

역할:
  - 스킬 출력 파일 감지 → raw/ 폴더에 타임스탬프 복사
  - LLM 호출 없음, 파일 복사만 수행
  - 인제스트 권장 메시지 출력 (실행은 오실장님 결정)

기존 역할 (유지):
  - SKILL.md 포맷 강제 검증
"""

import json
import sys
import os
import shutil
from datetime import datetime
from pathlib import Path

# ── 설정 ──────────────────────────────────────────────────────────────────────

# 위키 raw/ 경로 (환경에 따라 수정)
WIKI_RAW_PATHS = {
    "joylab": Path(r"C:\Users\오법석\OneDrive\Documents\joylab-wiki\raw"),
    "cs_ops": Path(r"C:\Users\오법석\cs-ops-skills\wiki\_raw"),  # 내부 참고용
}

# 스킬 출력 감지 규칙
# key: 출력 파일 경로에 포함된 패턴
# value: { domain, raw_subdir, wiki_target, ingest_hint }
SKILL_OUTPUT_RULES = {
    "etf-flow": {
        "domain": "joylab",
        "raw_subdir": "invest/etf-flows",
        "wiki_target": "wiki/invest/etf-flows/",
        "ingest_hint": '"/ingest ETF 흐름 [날짜]"',
    },
    "stock-research": {
        "domain": "joylab",
        "raw_subdir": "invest/tickers",
        "wiki_target": "wiki/invest/tickers/",
        "ingest_hint": '"/ingest 종목분석 [티커]"',
    },
    "youtube-invest-report": {
        "domain": "joylab",
        "raw_subdir": "invest/tickers",
        "wiki_target": "wiki/invest/tickers/ + wiki/invest/legend-fund/",
        "ingest_hint": '"/ingest LEGEND FUND [티커]"',
    },
    "last30days": {
        "domain": "joylab",
        "raw_subdir": "ai-tools/trends",
        "wiki_target": "wiki/ai-tools/",
        "ingest_hint": '"/ingest AI트렌드 [주제]"',
    },
    "etf-flow-blog": {
        "domain": "joylab",
        "raw_subdir": "invest/etf-flows",
        "wiki_target": "wiki/invest/etf-flows/",
        "ingest_hint": '"/ingest ETF 흐름 [날짜]"',
    },
    "joylab-ebook": {
        "domain": "joylab",
        "raw_subdir": "content/ebooks",
        "wiki_target": "wiki/content/",
        "ingest_hint": '"/ingest 전자책 [제목]"',
    },
}

# SKILL.md 포맷 필수 항목 (기존 검증 로직 유지)
REQUIRED_SKILL_FIELDS = ["name", "description"]

# ── 유틸 ──────────────────────────────────────────────────────────────────────

def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def detect_skill_from_content(content: str) -> str | None:
    """파일 내용에서 스킬명 감지"""
    for skill_key in SKILL_OUTPUT_RULES:
        if skill_key.replace("-", "_") in content.lower() or skill_key in content.lower():
            return skill_key
    return None

def detect_skill_from_path(path: str) -> str | None:
    """파일 경로에서 스킬명 감지"""
    path_lower = path.lower()
    for skill_key in SKILL_OUTPUT_RULES:
        if skill_key.replace("-", "_") in path_lower or skill_key in path_lower:
            return skill_key
    return None

def is_skill_output(path: str, content: str) -> str | None:
    """스킬 출력 파일인지 판단 → 매칭 스킬명 반환"""
    # HTML 리포트, 마크다운 분석 파일만 대상
    ext = Path(path).suffix.lower()
    if ext not in [".html", ".md", ".txt"]:
        return None
    # 임시 파일 제외
    if any(x in path for x in ["tmp", "temp", "__pycache__", ".git"]):
        return None
    # 스킬명 감지 (경로 우선, 내용 보조)
    detected = detect_skill_from_path(path) or detect_skill_from_content(content[:500])
    return detected

def save_to_raw(src_path: str, content: str, skill_key: str) -> Path | None:
    """raw/ 폴더에 타임스탬프 복사"""
    rule = SKILL_OUTPUT_RULES[skill_key]
    domain = rule["domain"]
    raw_base = WIKI_RAW_PATHS.get(domain)
    if not raw_base:
        return None

    subdir = raw_base / rule["raw_subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    src = Path(src_path)
    dest_name = f"{timestamp()}-{src.name}"
    dest = subdir / dest_name

    # 이미 존재하면 덮어쓰지 않음 (같은 날 같은 파일)
    if dest.exists():
        return dest

    try:
        if src.exists():
            shutil.copy2(src, dest)
        else:
            dest.write_text(content, encoding="utf-8")
        return dest
    except Exception:
        return None

# ── SKILL.md 포맷 검증 (기존 로직 유지) ──────────────────────────────────────

def validate_skill_md(path: str, content: str) -> list[str]:
    """SKILL.md 필수 항목 검증 → 오류 목록 반환"""
    if not path.endswith("SKILL.md"):
        return []
    errors = []
    for field in REQUIRED_SKILL_FIELDS:
        if field + ":" not in content:
            errors.append(f"필수 항목 누락: {field}")
    return errors

# ── 메인 ──────────────────────────────────────────────────────────────────────

def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Write 계열 도구만 처리
    if tool_name not in ("Write", "str_replace_based_edit_tool", "create_file"):
        sys.exit(0)

    path = tool_input.get("path", "")
    content = tool_input.get("content", tool_input.get("new_str", ""))

    if not path:
        sys.exit(0)

    # ── 1. SKILL.md 포맷 검증 (기존) ─────────────────────────────────────────
    skill_errors = validate_skill_md(path, content)
    if skill_errors:
        print(f"⚠️  SKILL.md 포맷 오류:", file=sys.stderr)
        for e in skill_errors:
            print(f"   - {e}", file=sys.stderr)
        # 경고만, 실행 차단 안 함

    # ── 2. 스킬 출력 감지 → raw/ 저장 ───────────────────────────────────────
    detected_skill = is_skill_output(path, content)
    if not detected_skill:
        sys.exit(0)

    rule = SKILL_OUTPUT_RULES[detected_skill]
    saved_path = save_to_raw(path, content, detected_skill)

    if saved_path:
        print(f"\n💾 Wiki Raw 저장 완료")
        print(f"   스킬: {detected_skill}")
        print(f"   저장 위치: {saved_path}")
        print(f"   인제스트 → {rule['ingest_hint']}")
        print(f"   대상 위키: {rule['wiki_target']}\n")
    else:
        # 저장 실패해도 조용히 넘어감 (훅이 작업 방해하면 안 됨)
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
