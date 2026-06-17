# Wiki 변경 로그

> 타임스탬프 순 역순. 새 항목은 맨 위에 추가.

---

## 2026-06-17

**초기 wiki 생성**
- `index.md` — 전체 카테고리 인덱스
- `schema.md` — 관리 규칙
- `qa-framework.md` — QA 평가 구조 (qa-scoring SKILL 기반)
- `tnps-model.md` — T-NPS 예측 모델 (tnps-prediction SKILL 기반)
- `coaching-system.md` — 코칭 프레임워크
- `kpi-map.md` — KPI 전체 맵
- `voc-workflow.md` — VOC 처리 워크플로우
- `stt-analysis.md` — STT 분석 기준
- `staffing-ops.md` — 인력 배치 기준
- `risk-thresholds.md` — 리스크 임계값
- `elderly-customer.md` — 고령자 상담 기준
- `report-templates.md` — 보고서 구조
- `feedback-patterns.md` — 코칭 피드백 패턴

**소스:** cs-ops-skills 플러그인 전체 SKILL.md 파일 인제스트

---

## 2026-06-17 (2차)

**schema.md 업데이트 — 2단계 CoT 인제스트 + 모순 처리 규칙 추가**
- Ingest를 분석(1단계) → 생성(2단계)로 분리
- 모순 감지 시 `⚠️ 충돌` 태그 규칙 추가
- Lint 항목을 6개로 세분화 + 심각도 분류
- 소스 캐싱 원칙 추가 (중복 인제스트 방지)

**신규 커맨드 추가**
- `cs-toolkit/commands/wiki-lint.md` — `/wiki-lint` 커맨드
- `cs-toolkit/commands/wiki-ingest.md` — `/wiki-ingest` 커맨드

**소스:** nashsu/llm_wiki 패턴 분석 결과

---

<!-- 새 항목 형식:
## YYYY-MM-DD
**[작업 유형: 추가/수정/삭제/lint]**
- 변경 내용 및 이유
**소스:** [어디서 온 지식인가]
-->
