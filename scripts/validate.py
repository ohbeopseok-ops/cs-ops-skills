#!/usr/bin/env python3
"""cs-ops-skills 검증 게이트.

insane-search의 `bias_check.py` + `coverage_battery.py` 패턴을 이 저장소에 맞게 옮긴 것.
구조 정합성(매니페스트·프론트매터·이름), 하네스 규칙 R3(실데이터 고정 금지),
그리고 문서에 적힌 예시가 썩지 않았는지(문서가 약속한 커맨드가 실제로 존재하는지)를 점검한다.

    python3 scripts/validate.py            # 전체 리포트
    python3 scripts/validate.py --quiet    # 실패 시에만 출력 (CI)

종료 코드: 0 = 통과, 1 = 실패.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 프론트매터가 아닌 본문에서 description을 잘못 잡지 않도록 프론트매터만 파싱한다.
FRONTMATTER_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
HARNESS_MARKER = "harness:v1"

# R3 — 실데이터 고정 금지. 자리표시자(전부 0)는 허용한다.
PII_PATTERNS = [
    ("주민등록번호", re.compile(r"\b\d{6}-[1-4]\d{6}\b")),
    ("전화번호", re.compile(r"\b01[016789]-(?!0{3,4}-0{4})\d{3,4}-\d{4}\b")),
    ("카드/계좌번호", re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{4}\b")),
    ("이메일", re.compile(r"\b[\w.+-]+@(?!example\.(?:com|org)\b)[\w-]+\.[\w.-]+\b")),
]

# 문서에서 커맨드 존재 검사를 건너뛸 구간 (계획 중인 커맨드 목록 등)
PLANNED_START = "<!-- validate:planned-start -->"
PLANNED_END = "<!-- validate:planned-end -->"

# 문서에서 `/command` 형태를 뽑아낸다. 슬래시 커맨드는 소문자+하이픈 규칙.
DOC_COMMAND = re.compile(r"`/([a-z][a-z0-9-]*)`")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checks: list[tuple[str, str]] = []

    def ok(self, label: str, detail: str = "") -> None:
        self.checks.append((label, detail))

    def fail(self, message: str) -> None:
        self.errors.append(message)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """SKILL.md 프론트매터를 얕게 파싱한다 (PyYAML 의존 없음)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    key: str | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if line[:1] in (" ", "\t") and key:  # 접힌 블록(>, |)의 이어지는 줄
            fields[key] = f"{fields[key]} {line.strip()}".strip()
            continue
        match = FRONTMATTER_KEY.match(line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
    return None  # 닫는 --- 없음


def strip_planned(text: str) -> str:
    """계획 구간을 제거해, 문서가 '지금 존재한다'고 주장하는 부분만 남긴다."""
    out: list[str] = []
    skipping = False
    for line in text.split("\n"):
        if PLANNED_START in line:
            skipping = True
            continue
        if PLANNED_END in line:
            skipping = False
            continue
        if not skipping:
            out.append(line)
    return "\n".join(out)


def check_marketplace(report: Report) -> list[Path]:
    """마켓플레이스 매니페스트 ↔ 실제 플러그인 디렉터리 정합성."""
    path = ROOT / ".claude-plugin" / "marketplace.json"
    if not path.exists():
        report.fail(".claude-plugin/marketplace.json 없음")
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.fail(f"marketplace.json 파싱 실패: {exc}")
        return []

    for field in ("name", "owner", "plugins"):
        if field not in data:
            report.fail(f"marketplace.json에 '{field}' 필드 없음")

    listed: dict[str, Path] = {}
    for entry in data.get("plugins", []):
        name = entry.get("name")
        if not name:
            report.fail("marketplace.json plugins[]에 name 없는 엔트리 존재")
            continue
        source = entry.get("source")
        if not source:
            report.fail(f"[{name}] marketplace 엔트리에 'source' 없음 — 설치 시 해석 불가")
            continue
        if not entry.get("description"):
            report.fail(f"[{name}] marketplace 엔트리에 description 없음")
        plugin_dir = (ROOT / source).resolve()
        if not plugin_dir.is_dir():
            report.fail(f"[{name}] source 경로가 없음: {source}")
            continue
        listed[name] = plugin_dir

    on_disk = {p.name for p in sorted(ROOT.glob("cs-*")) if p.is_dir()}
    for orphan in sorted(on_disk - set(listed)):
        report.fail(f"[{orphan}] 디렉터리가 존재하지만 marketplace.json에 등재되지 않음")

    report.ok("marketplace.json", f"{len(listed)}개 플러그인 등재, 디스크와 일치")
    return [listed[name] for name in sorted(listed)]


def check_plugin_manifests(report: Report, plugin_dirs: list[Path]) -> None:
    required = ("name", "version", "description", "author", "license", "keywords")
    for plugin_dir in plugin_dirs:
        rel = plugin_dir.relative_to(ROOT)
        path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not path.exists():
            report.fail(f"[{rel}] .claude-plugin/plugin.json 없음")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.fail(f"[{rel}] plugin.json 파싱 실패: {exc}")
            continue
        for field in required:
            if not data.get(field):
                report.fail(f"[{rel}] plugin.json에 '{field}' 없음/빈값")
        if data.get("name") != plugin_dir.name:
            report.fail(
                f"[{rel}] plugin.json name('{data.get('name')}')이 디렉터리명과 불일치"
            )
        version = data.get("version", "")
        if version and not SEMVER.match(version):
            report.fail(f"[{rel}] version '{version}'이 SemVer 형식 아님")
    report.ok("plugin.json", f"{len(plugin_dirs)}개 플러그인 매니페스트 검사")


def check_skills(report: Report) -> int:
    skills = sorted(ROOT.glob("cs-*/skills/*/SKILL.md"))
    if not skills:
        report.fail("SKILL.md를 찾지 못함")
        return 0
    for skill in skills:
        rel = skill.relative_to(ROOT)
        text = skill.read_text(encoding="utf-8")
        fields = parse_frontmatter(text)
        if fields is None:
            report.fail(f"[{rel}] 프론트매터 없음 또는 닫히지 않음")
            continue
        name = fields.get("name", "")
        if not name:
            report.fail(f"[{rel}] 프론트매터에 name 없음")
        elif name != skill.parent.name:
            report.fail(f"[{rel}] name('{name}')이 디렉터리명('{skill.parent.name}')과 불일치")
        description = fields.get("description", "")
        if not description:
            report.fail(f"[{rel}] 프론트매터에 description 없음 — 스킬이 트리거되지 않음")
        elif len(description) > 1024:
            report.fail(f"[{rel}] description {len(description)}자 — 1024자 초과")
        if HARNESS_MARKER not in text:
            report.fail(f"[{rel}] 하네스 블록 없음 (HARNESS.md R1–R8)")
    report.ok("SKILL.md", f"{len(skills)}개 스킬 프론트매터·하네스 블록 검사")
    return len(skills)


def check_pii(report: Report) -> None:
    """R3 — 스킬·커맨드 파일에 실데이터가 박히지 않았는지."""
    targets = sorted(
        [*ROOT.glob("cs-*/skills/**/*.md"), *ROOT.glob("cs-*/commands/**/*.md")]
    )
    hits = 0
    for path in targets:
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for label, pattern in PII_PATTERNS:
                match = pattern.search(line)
                if match:
                    hits += 1
                    report.fail(f"[{rel}:{lineno}] R3 위반 — {label} 패턴: {match.group(0)}")
    if not hits:
        report.ok("R3 실데이터 스캔", f"{len(targets)}개 파일, 개인정보 패턴 없음")


def check_docs(report: Report, skill_count: int) -> None:
    """문서가 약속한 개수·커맨드가 실제와 맞는지 (썩은 예시 적발)."""
    command_files = sorted(ROOT.glob("cs-*/commands/*.md"))
    available = {p.stem for p in command_files}
    plugin_count = len([p for p in ROOT.glob("cs-*") if p.is_dir()])

    for doc_name in ("README.md", "README.en.md", "SKILLS.md"):
        doc = ROOT / doc_name
        if not doc.exists():
            continue
        text = strip_planned(doc.read_text(encoding="utf-8"))

        for referenced in sorted(set(DOC_COMMAND.findall(text))):
            if referenced not in available:
                report.fail(
                    f"[{doc_name}] `/{referenced}` 를 안내하지만 commands/{referenced}.md 없음"
                )

        for count, unit in re.findall(r"(\d+)\s*개\s*(플러그인|스킬|커맨드)", text):
            actual = {
                "플러그인": plugin_count,
                "스킬": skill_count,
                "커맨드": len(command_files),
            }[unit]
            if int(count) != actual:
                report.fail(
                    f"[{doc_name}] '{count}개 {unit}'로 표기했지만 실제 {actual}개"
                )

        if "[your-github-username]" in text:
            report.fail(f"[{doc_name}] 설치 안내에 자리표시자 '[your-github-username]' 남아있음")

    for referenced_doc in ("LICENSE", "DISCLAIMER.md", "HARNESS.md"):
        if not (ROOT / referenced_doc).exists():
            report.fail(f"{referenced_doc} 없음 (문서에서 참조됨)")

    report.ok(
        "문서 정합성",
        f"플러그인 {plugin_count} · 스킬 {skill_count} · 커맨드 {len(command_files)}",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="cs-ops-skills 검증 게이트")
    parser.add_argument("--quiet", action="store_true", help="실패 시에만 출력 (CI용)")
    args = parser.parse_args()

    report = Report()
    plugin_dirs = check_marketplace(report)
    check_plugin_manifests(report, plugin_dirs)
    skill_count = check_skills(report)
    check_pii(report)
    check_docs(report, skill_count)

    if report.errors:
        print(f"✖ 검증 실패 — {len(report.errors)}건", file=sys.stderr)
        for error in report.errors:
            print(f"  · {error}", file=sys.stderr)
        return 1

    if not args.quiet:
        for label, detail in report.checks:
            print(f"✔ {label:24} {detail}")
        print(f"\n✔ 검증 통과 — {len(report.checks)}개 항목")
    return 0


if __name__ == "__main__":
    sys.exit(main())
