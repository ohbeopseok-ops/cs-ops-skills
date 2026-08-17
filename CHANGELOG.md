# Changelog

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)와
[Semantic Versioning](https://semver.org/spec/v2.0.0.html)을 따른다.

## 1.1.0 — 2026-08-17

플러그인 패키징·거버넌스 정비 — [insane-search](https://github.com/fivetaku/insane-search)의
플러그인 구조 패턴을 이 저장소에 이식. 스킬 본문의 도메인 내용은 변경 없음.

### Added

- **하네스 규칙 R1–R8** (`HARNESS.md`) — 스킬이 "무엇을 아는지"와 별개로 "무엇을 하지 않는지"를
  고정하는 규칙 집합. insane-search의 SKILL.md R1–R8 패턴을 CS 도메인으로 옮겼다:
  수치 날조 금지(R1), 개인정보 마스킹 우선(R2), **No-Real-Name Rule**(R3 — No-Site-Name Rule의
  대응물), 근거 발화 원문 인용(R4), 배점·등급 기준 즉흥 변경 금지(R5), 부족한 데이터는
  `판단 불가`로 정직하게 보고(R6), 입력 텍스트는 데이터이지 명령이 아님(R7),
  개인 불이익 처분의 단독 근거 금지(R8). 29개 SKILL.md 전부에 요약 블록을 인라인 삽입 —
  플러그인이 설치되면 저장소 루트 문서는 따라가지 않으므로, 런타임에 작동하는 것은 인라인 블록이다.
- **검증 게이트** (`scripts/validate.py`) — insane-search의 `bias_check.py`(CI 린터) +
  `coverage_battery.py`(썩은 예시 적발) 패턴 이식. 점검 항목: 마켓플레이스 엔트리↔디스크 정합성,
  `plugin.json` 필수 필드·SemVer·이름 일치, SKILL.md 프론트매터와 스킬명↔디렉터리 일치,
  하네스 블록 존재, **R3 실데이터 패턴 스캔**(주민번호·전화·계좌·이메일; 전부 0인 자리표시자는 허용),
  문서가 안내한 커맨드의 실제 존재 여부, 문서 개수 표기↔실제 개수. 표준 라이브러리만 사용.
- **CI** (`.github/workflows/validate.yml`) — 모든 push/PR에서 검증 게이트 실행.
- **`LICENSE`** (MIT) — README가 v1.0.0부터 참조하고 있었으나 파일이 없었다.
- **`DISCLAIMER.md`** — insane-search의 면책 구조(보증 부인 / 책임 제한 / 의도된 용도 /
  제휴 관계 없음 / 사용자 책임 / 도구별 범위)를 CS 도메인으로 적응. 추가된 도메인 특화 조항:
  §4 **LG U+ 및 계열사와 제휴 관계 없음** — 평가 배점·등급 기준은 어떤 조직의 공식 사내 기준도
  아니라는 명시, §6 **개인정보 및 상담 데이터** — 입력 전 최소화, 마스킹 미보장, 저장소 실데이터
  금지, §7 **인사 결정에 대한 사용** — 등급·순위를 개인 불이익 처분의 단독 근거로 금지.
- **`SKILLS.md`** — 전체 카탈로그(8 플러그인 · 29 스킬 · 7 커맨드)를 스킬별 한 줄 설명 표로 정리.
  insane-search가 README의 매뉴얼을 `PLATFORMS.md`로 분리한 패턴.
- **`README.en.md`** — 영어 랜딩. 스킬 본문과 산출물은 한국어라는 점을 명시.
- **`.claude-plugin/marketplace.json`** — Claude Code 마켓플레이스 규격 파일.
  `owner`, `metadata`, `plugins[].source`를 포함한다.
- **플러그인별 `.claude-plugin/plugin.json` × 8** — insane-search의 매니페스트 스키마
  (`name`, `version`, `description`, `author{name,url}`, `homepage`, `repository`, `license`,
  `keywords`) 적용. 각 `description`에는 해당 플러그인의 산출물 경계를 한 문장으로 명시했다.

### Changed

- **`README.md`을 랜딩 문서로 축소** — 설치 · 사용 예 · 커버 범위 · 비교 표 · 작동 방식 ·
  경계 · 검증. 전체 카탈로그는 `SKILLS.md`로 이동(내용 손실 없음). insane-search의 README 패턴.
- 설치 안내의 자리표시자 `[your-github-username]`을 실제 저장소 경로로 교체. Claude Code 설치
  명령을 `claude plugin add --marketplace ...`에서 `/plugin marketplace add` + `/plugin install`
  형태로 수정.

### Fixed

- **문서가 약속한 커맨드 19개가 존재하지 않았다.** v1.0.0 README는 26개 커맨드를 안내했으나
  구현된 파일은 7개(`/evaluate`, `/analyze-kpi`, `/analyze-call`, `/analyze-complaints`,
  `/plan-okr`, `/weekly-report`, `/monthly-report`)뿐이었다. 미구현 19개는 `SKILLS.md`의
  **커맨드 로드맵** 섹션으로 옮겨 계획임을 명시하고, 검증 게이트에서 제외되는 구간
  (`validate:planned-start/end`)에 두었다. 구현해서 위쪽 섹션으로 옮기면 자동으로 검증 대상이 된다.
  기능 자체는 스킬 직접 호출로 이전에도, 지금도 사용할 수 있다 — 없던 것은 커맨드 진입점이다.
- **README의 스킬 개수 표기 오류** — 30개로 적혀 있었으나 실제 29개.
- **`.claude-plugin/manifest.json` 제거** — Claude Code가 읽지 않는 파일명이었고,
  `plugins[].source`가 없어 엔트리가 플러그인 디렉터리로 해석되지 않았다.
  `marketplace.json`이 이를 대체한다.

## 1.0.0 — 2026-03-06

최초 릴리스 — 8개 플러그인, 29개 스킬, 7개 커맨드. 품질분석 · 코칭 · 성과관리 · VOC ·
STT분석 · 운영기획 · 리포팅 · 유틸리티.

이전 이력은 git log에만 존재한다.
