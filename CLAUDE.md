# CS Ops Skills — Claude Code 가이드

LG U+ 홈CS 운영관리를 위한 AI 운영 시스템. Claude Code 세션에서 이 파일을 읽어 프로젝트 구조와 규칙을 파악한다.

---

## 프로젝트 개요

**목적:** CS 운영 전 영역(품질분석 → 코칭 → 성과관리 → VOC → STT분석 → 운영기획 → 리포팅)을 커버하는 AI 스킬 마켓플레이스.  
**설계 대상:** Claude Code, Claude Cowork 전용. Skills는 범용 AI 어시스턴트에서도 호환.  
**구성:** 8개 플러그인, 29개 스킬, 다수의 커맨드 워크플로우.

---

## 디렉토리 구조 (Wiki 구조)

```
cs-ops-skills/
├── CLAUDE.md                        ← 이 파일 (Claude Code 가이드)
├── README.md                        ← 사용자용 설치/사용 가이드
├── .claude-plugin/
│   └── manifest.json                ← 플러그인 목록 및 메타데이터
│
├── skills/
│   └── user/                        ← 모든 스킬의 집합 (flat index)
│       ├── qa-scoring.md
│       ├── autoqa-analysis.md
│       ├── ... (29개 스킬)
│       └── ko-grammar-check.md
│
├── cs-quality-analysis/             ← 플러그인: 상담 품질 분석
│   ├── commands/
│   │   └── evaluate.md
│   └── skills/
│       ├── qa-scoring/SKILL.md
│       ├── autoqa-analysis/SKILL.md
│       ├── elderly-customer-qa/SKILL.md
│       ├── compliance-check/SKILL.md
│       └── quality-trend/SKILL.md
│
├── cs-coaching/                     ← 플러그인: 코칭 및 피드백
│   └── skills/
│       ├── coaching-feedback/SKILL.md
│       ├── improvement-plan/SKILL.md
│       └── coaching-script/SKILL.md
│
├── cs-performance/                  ← 플러그인: KPI 및 성과 관리
│   ├── commands/
│   │   └── analyze-kpi.md
│   └── skills/
│       ├── kpi-analysis/SKILL.md
│       ├── tnps-prediction/SKILL.md
│       ├── agent-benchmarking/SKILL.md
│       └── target-setting/SKILL.md
│
├── cs-voc/                          ← 플러그인: VOC 및 고객 분석
│   ├── commands/
│   │   └── analyze-complaints.md
│   └── skills/
│       ├── voc-categorization/SKILL.md
│       ├── complaint-root-cause/SKILL.md
│       ├── sentiment-analysis/SKILL.md
│       └── nudge-analysis/SKILL.md
│
├── cs-stt/                          ← 플러그인: STT 대화 분석
│   ├── commands/
│   │   └── analyze-call.md
│   └── skills/
│       ├── conversation-analysis/SKILL.md
│       ├── script-compliance/SKILL.md
│       └── pii-detection/SKILL.md
│
├── cs-operations/                   ← 플러그인: 운영 기획
│   ├── commands/
│   │   └── plan-okr.md
│   └── skills/
│       ├── staffing-plan/SKILL.md
│       ├── process-improvement/SKILL.md
│       ├── meeting-notes/SKILL.md
│       └── okr-cs/SKILL.md
│
├── cs-reporting/                    ← 플러그인: 보고서 작성
│   ├── commands/
│   │   ├── weekly-report.md
│   │   └── monthly-report.md
│   └── skills/
│       ├── weekly-report/SKILL.md
│       ├── monthly-report/SKILL.md
│       └── executive-summary/SKILL.md
│
└── cs-toolkit/                      ← 플러그인: 유틸리티
    └── skills/
        ├── html-tool-spec/SKILL.md
        ├── data-mock/SKILL.md
        └── ko-grammar-check/SKILL.md
```

---

## 핵심 개념

### Skills
도메인 지식, 분석 프레임워크, 출력 템플릿을 담은 기본 단위.  
각 스킬은 `<plugin>/skills/<skill-name>/SKILL.md` 경로에 위치한다.

**SKILL.md 구조:**
```markdown
---
name: skill-name
description: 한 줄 설명 (용도, 사용 맥락 명시)
---

# 스킬 제목

[도메인 지식 및 분석 프레임워크]

## 출력 형식
ALWAYS use this exact template:
[출력 템플릿]

## 사용 예시
[3개 예시]
```

### Commands
`/command-name` 형식으로 실행하는 사용자 트리거 워크플로우.  
여러 스킬을 체인으로 연결해 복합 작업을 수행한다.  
각 커맨드는 `<plugin>/commands/<command-name>.md` 경로에 위치한다.

### Plugins
관련 스킬과 커맨드를 묶은 설치 단위.  
`.claude-plugin/manifest.json`에 플러그인 목록이 등록된다.

### skills/user/
모든 플러그인에 분산된 스킬을 한 디렉토리에 집약한 플랫 인덱스.  
파일명 = 스킬명 (예: `qa-scoring.md`).  
분산된 SKILL.md의 내용을 그대로 포함한다.

---

## 플러그인 × 스킬 맵

| 플러그인 | 스킬 (29개) |
|----------|------------|
| cs-quality-analysis | qa-scoring, autoqa-analysis, elderly-customer-qa, compliance-check, quality-trend |
| cs-coaching | coaching-feedback, improvement-plan, coaching-script |
| cs-performance | kpi-analysis, tnps-prediction, agent-benchmarking, target-setting |
| cs-voc | voc-categorization, complaint-root-cause, sentiment-analysis, nudge-analysis |
| cs-stt | conversation-analysis, script-compliance, pii-detection |
| cs-operations | staffing-plan, process-improvement, meeting-notes, okr-cs |
| cs-reporting | weekly-report, monthly-report, executive-summary |
| cs-toolkit | html-tool-spec, data-mock, ko-grammar-check |

---

## 새 스킬 추가 방법

1. 해당 플러그인 디렉토리에 `skills/<skill-name>/SKILL.md` 생성
2. front matter (`name`, `description`) + 본문 작성
3. `skills/user/<skill-name>.md`에 동일 내용 복사 (flat index 동기화)
4. 필요 시 커맨드 파일 추가: `<plugin>/commands/<command-name>.md`
5. `.claude-plugin/manifest.json`은 플러그인 단위이므로 새 스킬 추가 시 변경 불필요

## 새 플러그인 추가 방법

1. `cs-<domain>/` 디렉토리 생성
2. `skills/` 및 `commands/` 하위 구조 생성
3. `.claude-plugin/manifest.json`의 `plugins` 배열에 항목 추가
4. `README.md` 플러그인 목록 섹션 업데이트

---

## 코딩 컨벤션

- 모든 SKILL.md는 한국어로 작성
- 출력 템플릿 섹션 헤더는 반드시 `ALWAYS use this exact template:` 문구 사용
- 스킬 이름(kebab-case)과 디렉토리명 일치 유지
- `skills/user/` 파일명은 스킬 이름과 동일 (`<skill-name>.md`)
- 커맨드 파일은 커맨드명과 동일한 파일명 사용

---

## 주요 사용 패턴

스킬 직접 활용:
```
이 STT 텍스트에서 품질 이슈를 평가해줘 [텍스트 붙여넣기]
```

커맨드 체인 실행:
```
/evaluate 다음 STT 텍스트를 평가해줘 [텍스트]
/weekly-report 이번 주 KPI 데이터 [데이터]
```
