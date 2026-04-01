---
name: harness
description: CS Ops Skills 전체 운영 하네스. 모든 플러그인(품질분석·코칭·성과·VOC·STT·운영·리포팅·툴킷)의 스킬과 커맨드를 단일 진입점으로 연결하는 메타 스킬. 어떤 CS 운영 작업을 해야 할지 모를 때 시작점으로 사용.
---

# CS Ops Harness

CS Ops Skills 전체 시스템의 진입점. 작업 유형을 설명하면 적절한 스킬과 커맨드로 안내한다.

## 작업별 빠른 연결

### 상담 품질 평가
```
/evaluate [STT 텍스트]          ← 전체 품질 평가 사이클
/autoqa-report [데이터]          ← AutoQA 트렌드 분석
/elderly-audit [텍스트]          ← 고령자 상담 특화 점검
```
사용 스킬: `qa-scoring` · `autoqa-analysis` · `compliance-check` · `elderly-customer-qa` · `quality-trend`

### 코칭 및 피드백
```
/coach [상담사명]                ← 맞춤 코칭 피드백
/plan-improvement [상담사명]     ← 취약 항목 개선 계획
/coaching-session [주제]         ← 코칭 세션 스크립트
```
사용 스킬: `coaching-feedback` · `improvement-plan` · `coaching-script`

### KPI 및 성과 관리
```
/analyze-kpi [데이터]            ← KPI 현황 분석
/predict-tnps [데이터]           ← T-NPS 예측 및 리스크 식별
/benchmark [팀/상담사]           ← 벤치마킹 리포트
/set-targets [현황 데이터]       ← 목표치 설정
```
사용 스킬: `kpi-analysis` · `tnps-prediction` · `agent-benchmarking` · `target-setting`

### VOC 및 고객 분석
```
/analyze-voc [VOC 목록]          ← 분류 → 원인 → 개선 과제
/analyze-complaints [불만 데이터] ← 불만 콜 심층 분석
/nudge-check [데이터]            ← 넛지 마케팅 효과 분석
```
사용 스킬: `voc-categorization` · `complaint-root-cause` · `sentiment-analysis` · `nudge-analysis`

### STT 대화 분석
```
/analyze-call [STT 텍스트]       ← 품질+감성+준수율 통합 분석
/check-script [STT 텍스트]       ← 스크립트 준수율 점검
/mask-pii [텍스트]               ← 개인정보 탐지 및 마스킹
```
사용 스킬: `conversation-analysis` · `script-compliance` · `pii-detection`

### 운영 기획
```
/plan-staffing [인력 현황]       ← 인력 배치 최적화
/improve-process [프로세스]      ← 개선 과제 도출
/meeting-notes [회의 내용]       ← 회의록 자동 작성
/plan-okr [목표 현황]            ← CS OKR 수립
```
사용 스킬: `staffing-plan` · `process-improvement` · `meeting-notes` · `okr-cs`

### 보고서 작성
```
/weekly-report [KPI 데이터]      ← 주간 운영 보고서
/monthly-report [월간 데이터]    ← 월간 성과 보고서
/exec-summary [보고 내용]        ← 경영진 보고 요약
```
사용 스킬: `weekly-report` · `monthly-report` · `executive-summary`

### 유틸리티
```
/spec-tool [도구 설명]           ← HTML 도구 요구사항 명세
/mock-data [데이터 유형]         ← CS 운영 테스트 데이터 생성
/install-plugin [플러그인명]     ← 플러그인 설치 가이드
```
사용 스킬: `html-tool-spec` · `data-mock` · `ko-grammar-check` · `plugin-marketplace`

## 워크플로우 체인 예시

**불만 콜 → 코칭까지:**
```
/analyze-call → /evaluate → /coach
```

**주간 리뷰 전체:**
```
/autoqa-report → /analyze-voc → /analyze-kpi → /weekly-report
```

**신규 상담사 성과 점검:**
```
/benchmark → /predict-tnps → /plan-improvement → /set-targets
```

## 설치 방법

```bash
# 마켓플레이스
/plugin marketplace add ohbeopseok-ops/cs-ops-skills
/plugin install --all@cs-ops-skills

# 직접 복사 (폐쇄망)
cp -r skills/harness ~/.claude/skills/harness
```

## 사용 예시

- `상담사 품질 평가를 하고 싶어` → `/evaluate` 안내
- `이번 달 T-NPS가 떨어졌어` → `/predict-tnps` + `/analyze-voc` 체인 안내
- `주간 보고서 작성 전에 뭘 먼저 해야 해?` → 데이터 수집 → 분석 → 보고서 순서 안내
