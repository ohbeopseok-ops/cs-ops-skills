# /decision-note — 원자료를 판단 추적형 노트로 변환

**실행:** source-schema (원자료 분해 + 메타데이터) → decision-note (판단 추적형 노트 작성)

**사용법:**
```
/decision-note [원자료 텍스트 또는 붙여넣기]
/decision-note 인터뷰 로그: [텍스트]  ← 인터뷰/VOC 등 raw material 입력
```

**출력:** claim_type별 후보 노트 목록 → 그중 decision(판단) 성격의 항목을 판단 추적형 노트 템플릿(당시 문제/판단/근거/반대 근거/실행/평가 지표/관련 노트)으로 완성.

**다음 커맨드 제안:** `/audit-knowledge` (누적된 판단 노트를 정기적으로 점검)
