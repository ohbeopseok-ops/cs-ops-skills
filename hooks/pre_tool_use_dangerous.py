#!/usr/bin/env python3
"""
PreToolUse hook: 위험 Bash 명령 차단

패턴에 매칭되는 위험한 명령 실행을 차단한다.
exit code 2 + JSON stdout → Claude Code가 도구 실행을 거부.

입력(stdin): Claude Code PreToolUse JSON
출력(stdout): {"decision": "block", "reason": "..."} (차단 시)
"""

import json
import re
import sys

# (패턴, 사유) 목록
DANGEROUS_PATTERNS = [
    (r"\brm\s+-rf\s+/(?!\w)", "루트 경로 대상 rm -rf 감지"),
    (r"git\s+push\s+.*--force(?!-with-lease)", "git push --force 감지 (--force-with-lease는 허용)"),
    (r"git\s+reset\s+--hard\b", "git reset --hard 감지"),
    (r"git\s+clean\s+.*-f", "git clean -f 감지"),
    (r":\(\)\s*\{.*:\|:.*\}", "fork bomb 패턴 감지"),
    (r">\s*/dev/sd[a-z]\b", "/dev/sd* 직접 쓰기 감지"),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777 감지"),
    (r"\bdrop\s+database\b", "DROP DATABASE 감지", re.IGNORECASE),
]


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    for item in DANGEROUS_PATTERNS:
        pattern, reason = item[0], item[1]
        flags = item[2] if len(item) > 2 else 0
        if re.search(pattern, command, flags):
            print(json.dumps({"decision": "block", "reason": f"[위험 명령 차단] {reason}"}, ensure_ascii=False))
            sys.exit(2)


if __name__ == "__main__":
    main()
