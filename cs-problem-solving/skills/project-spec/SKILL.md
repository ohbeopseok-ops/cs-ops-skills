---
name: project-spec
description: Intent 분석과 Interview 답변을 구조화된 Project Spec으로 변환하고, 어떤 CS Ops 스킬/커맨드로 실행할지 라우팅을 확정한다. 프로젝트를 실행에 들어가기 전 최종 요구사항 문서가 필요할 때 사용.
---

# 프로젝트 스펙 (Project Spec)

Intent + Interview 대화를 실행 가능한 단일 문서로 응축한다. 이 문서가 이후 실행 단계(기존 CS Ops 스킬)에 그대로 전달할 수 있는 입력이 된다.

## 필수 필드

```
Project Name   프로젝트명
Problem        문제 정의 (Job 기반)
Objective      달성하려는 목표
Outcome        완료 판단 기준
Audience       결과 소비자
Baseline       현재 상태
Target         목표 수치/상태
Deadline       기한
Constraints    제약사항
Data           사용 가능한 데이터/자료
Risks          예상 리스크
KPI            성공 측정 지표
```

정보가 끝내 확인되지 않은 필드는 빈칸으로 두지 않는다 — "미확인 (합리적 기본값: ...)" 형태로 명시하고 실행 단계에서 그 가정을 드러낸다.

## 실행 라우팅

intent-classify에서 정한 업무 유형을 기준으로 실제 실행에 사용할 스킬/커맨드를 확정한다.

| 업무 유형 | 실행 스킬/커맨드 |
|-----------|------------------|
| 품질분석 | `/evaluate`, `qa-scoring`, `autoqa-analysis` |
| 코칭 | `coaching-feedback`, `improvement-plan` |
| 성과관리 | `/analyze-kpi`, `tnps-prediction`, `agent-benchmarking` |
| VOC | `/analyze-complaints`, `voc-categorization`, `complaint-root-cause` |
| STT분석 | `/analyze-call`, `conversation-analysis`, `script-compliance` |
| 운영기획 | `/plan-okr`, `staffing-plan`, `process-improvement` |
| 리포팅 | `/weekly-report`, `/monthly-report`, `executive-summary` |
| 범용/도구 | `html-tool-spec`, `data-mock` |

## 출력 형식

ALWAYS use this exact template:

```
## Project Spec

**Project Name:** [프로젝트명]

| 필드 | 내용 |
|------|------|
| Problem | [문제 정의] |
| Objective | [목표] |
| Outcome | [완료 기준] |
| Audience | [결과 소비자] |
| Baseline | [현재 상태] |
| Target | [목표 수치/상태] |
| Deadline | [기한] |
| Constraints | [제약사항] |
| Data | [사용 가능 데이터] |
| Risks | [예상 리스크] |
| KPI | [성공 지표] |

**실행 라우팅:** [업무 유형] → [스킬/커맨드 목록]

---
이 스펙대로 실행할까요, 수정할 항목이 있나요?
```

## 판단 지침

Baseline과 Target을 같은 단위로 맞춘다 — 정성 지표(Baseline)에 정량 목표(Target)를 붙이면 KPI가 측정 불가능해진다.
Risks는 최소 1개 이상 채운다 — "리스크 없음"은 대개 아직 검토하지 않았다는 뜻이다.
실행 라우팅은 기존 플러그인 스킬/커맨드 이름을 정확히 사용한다 — 존재하지 않는 스킬을 지어내지 않는다.

## 사용 예시

- (interview 종료 후) `지금까지 내용으로 프로젝트 스펙 만들어줘`
- `Target을 T-NPS +3pt로, Deadline은 이번 분기 말로 수정해줘`
