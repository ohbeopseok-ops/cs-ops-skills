# /solve — 막연한 요청을 실행 프로젝트로 전환

Intent → Interview → Spec → Execution 라우팅 → Critic → Revision → Action 전체 사이클을 실행하는 JOYLAB 체인 워크플로우.

## 실행 순서

1. **intent-classify** → Job/Outcome/Why Now/Limits/Audience/Baseline 분해 + 업무 유형 분류
2. **joylab-interview** → 정보 충분도에 따라 최대 10개, 1~2개씩 질문 (충분하면 생략)
3. **project-spec** → 구조화된 스펙 + 실행 라우팅 확정
4. (라우팅된 CS Ops 스킬/커맨드 실행) → 예: `/evaluate`, `/analyze-kpi`, `/analyze-complaints` 등
5. **critic-review** → Fact/Logic/Assumption/Execution/Risk/Simplicity 검증
6. (사용자 선택: 원안 유지 / Critic 전체 적용 / 선택 수정)
7. **action-conversion** → TODAY / THIS WEEK / LATER 액션 목록 생성

## 사용법

```
/solve [막연한 업무 요청]
/solve skip-interview [이미 정보가 충분한 요청]  ← Interview 단계 생략
```

## 출력

- Intent 분석표
- (필요 시) Interview 질문/답변
- Project Spec
- 실행 결과 (라우팅된 스킬 기준)
- Critic Review + 선택지
- Action Plan (Today/This Week/Later)

## 다음 커맨드 제안

액션에 코칭이 포함된 경우: `/coach [상담사명]`
경영진 보고가 필요한 경우: `/weekly-report` 또는 `/exec-summary`
