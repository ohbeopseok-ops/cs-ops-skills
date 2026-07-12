---
description: 상담 녹취/STT 품질 평가 전체 사이클
argument-hint: [상담 STT 텍스트]
---

# /evaluate — 상담 품질 평가 전체 사이클

상담 텍스트를 입력받아 전체 품질 평가를 수행하는 체인 워크플로우.

## 실행 순서

1. **pii-detection** → 개인정보 마스킹 처리
2. **conversation-analysis** → 대화 구조 및 감성 분석
3. **compliance-check** → 스크립트/규정 준수 점검
4. **qa-scoring** → 항목별 가중 점수 및 등급 산출
5. (고령자 상담 감지 시) **elderly-customer-qa** → 특화 평가 추가

## 사용법

```
/evaluate [상담 STT 텍스트]
/evaluate elderly [고령자 상담 STT 텍스트]  ← 고령자 특화 평가
/evaluate batch [여러 건 평가 요청]
```

## 출력

- 개인정보 마스킹 텍스트
- 대화 분석 요약 (감성, 리스크 신호)
- 컴플라이언스 판정
- QA 점수표 및 등급
- 코칭 우선순위 권고

## 다음 커맨드 제안

평가 완료 후: `/coach [상담사명]` → 코칭 피드백 작성  
팀 분석: `/autoqa-report` → 다수 건 트렌드 분석  
즉시 보고: `/weekly-report` → 주간 보고서 반영
