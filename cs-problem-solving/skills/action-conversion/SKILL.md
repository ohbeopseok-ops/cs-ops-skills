---
name: action-conversion
description: 최종 확정된 결과(Project Spec 실행 결과 또는 Critic Review 이후 개선안)를 오늘/이번 주/후속으로 나눈 실행 액션 목록으로 변환한다. 분석이나 계획 결과물을 실제 담당자가 실행할 수 있는 할 일 목록으로 바꿀 때 사용.
---

# 실행 액션 전환 (Action Conversion)

좋은 분석이나 계획도 "오늘 무엇을 하는가"로 바뀌지 않으면 결과물로 끝난다. 최종 결과를 실행 단위로 분해한다.

## 분류 기준

```
TODAY       오늘 안에 시작하거나 끝낼 수 있는 것
THIS WEEK   이번 주 내 완료 목표
LATER       후속 과제 (의존성이 있거나 우선순위가 낮은 것)
```

## 액션 필드

```
Action     구체적 실행 내용 (동사로 시작)
Owner      담당자 또는 담당 역할
Deadline   기한
KPI        이 액션의 완료를 판단할 지표
Status     Not Started / In Progress / Done
```

## 출력 형식

ALWAYS use this exact template:

```
## Action Plan

### TODAY
| Action | Owner | Deadline | KPI | Status |
|--------|-------|----------|-----|--------|
| [액션] | [담당] | [기한] | [지표] | Not Started |

### THIS WEEK
| Action | Owner | Deadline | KPI | Status |
|--------|-------|----------|-----|--------|
| [액션] | [담당] | [기한] | [지표] | Not Started |

### LATER
| Action | Owner | Deadline | KPI | Status |
|--------|-------|----------|-----|--------|
| [액션] | [담당] | [기한] | [지표] | Not Started |

---
**액션 총 개수:** [n]개 (TODAY [n] / THIS WEEK [n] / LATER [n])
```

## 판단 지침

액션 0개인 프로젝트는 완료 상태로 넘기지 않는다 — 최소 1개는 TODAY 또는 THIS WEEK에 배치한다.
담당자가 불명확하면 "미배정"으로 두지 말고 요청자에게 배정을 확인한다.
KPI가 없는 액션은 "완료됐는지 어떻게 확인하는가"를 스스로에게 물어 보완한다.

## 사용 예시

- `이 주간보고서 결과를 오늘/이번주/후속 액션으로 나눠줘`
- `KPI 분석 결과에서 실행 액션만 뽑아줘`
- `이 프로젝트 액션 목록에 담당자를 배정해줘`
