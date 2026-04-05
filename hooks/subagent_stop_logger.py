#!/usr/bin/env python3
"""
SubagentStop hook: 서브에이전트 완료 로거

서브에이전트(Agent 도구) 종료 시 세션 ID, 완료 시각,
결과 요약을 stdout에 출력한다.

입력(stdin): Claude Code SubagentStop JSON
출력(stdout): 완료 로그 (정보용, 차단하지 않음)
"""

import json
import sys
from datetime import datetime


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}

    session_id = data.get("session_id", "unknown")
    stop_hook_active = data.get("stop_hook_active", False)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[SubagentStop] {timestamp} | session={session_id[:8]}... | stop_hook_active={stop_hook_active}")


if __name__ == "__main__":
    main()
