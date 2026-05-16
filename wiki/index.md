# CS Ops Skills — 스킬 인덱스

전체 스킬 목록. 플러그인 → 스킬 순으로 정리.

---

## CS Ops Skills (업무용)

### cs-quality-analysis — 상담 품질 분석

| 스킬 | 위치 | 설명 |
|------|------|------|
| `qa-scoring` | `cs-quality-analysis/skills/qa-scoring/SKILL.md` | 상담 품질 평가 및 점수 산출 |
| `autoqa-analysis` | `cs-quality-analysis/skills/autoqa-analysis/SKILL.md` | AutoQA 트렌드 분석 |
| `elderly-customer-qa` | `cs-quality-analysis/skills/elderly-customer-qa/SKILL.md` | 고령자 상담 특화 품질 기준 |
| `compliance-check` | `cs-quality-analysis/skills/compliance-check/SKILL.md` | 스크립트 준수율 점검 |
| `quality-trend` | `cs-quality-analysis/skills/quality-trend/SKILL.md` | 품질 추이 분석 |

---

### cs-coaching — 코칭 및 피드백

| 스킬 | 위치 | 설명 |
|------|------|------|
| `coaching-feedback` | `cs-coaching/skills/coaching-feedback/SKILL.md` | 상담사별 맞춤 코칭 피드백 생성 |
| `improvement-plan` | `cs-coaching/skills/improvement-plan/SKILL.md` | 취약 항목 기반 개선 계획 수립 |
| `coaching-script` | `cs-coaching/skills/coaching-script/SKILL.md` | 코칭 세션 스크립트 자동 생성 |

---

### cs-performance — KPI 및 성과 관리

| 스킬 | 위치 | 설명 |
|------|------|------|
| `kpi-analysis` | `cs-performance/skills/kpi-analysis/SKILL.md` | KPI 현황 분석 및 원인 진단 |
| `tnps-prediction` | `cs-performance/skills/tnps-prediction/SKILL.md` | T-NPS 예측 및 리스크 상담사 식별 |
| `agent-benchmarking` | `cs-performance/skills/agent-benchmarking/SKILL.md` | 상담사/팀 벤치마킹 리포트 |
| `target-setting` | `cs-performance/skills/target-setting/SKILL.md` | 데이터 기반 목표치 설정 |

---

### cs-voc — VOC 및 고객 분석

| 스킬 | 위치 | 설명 |
|------|------|------|
| `voc-categorization` | `cs-voc/skills/voc-categorization/SKILL.md` | VOC 유형 분류 |
| `complaint-root-cause` | `cs-voc/skills/complaint-root-cause/SKILL.md` | 불만 원인 심층 분석 |
| `sentiment-analysis` | `cs-voc/skills/sentiment-analysis/SKILL.md` | 고객 감성 분석 |
| `nudge-analysis` | `cs-voc/skills/nudge-analysis/SKILL.md` | 넛지 마케팅 효과 분석 |

---

### cs-stt — STT 대화 분석

| 스킬 | 위치 | 설명 |
|------|------|------|
| `conversation-analysis` | `cs-stt/skills/conversation-analysis/SKILL.md` | STT 대화 전체 분석 |
| `script-compliance` | `cs-stt/skills/script-compliance/SKILL.md` | 스크립트 준수율 분석 |
| `pii-detection` | `cs-stt/skills/pii-detection/SKILL.md` | 개인정보 탐지 및 마스킹 |

---

### cs-operations — 운영 기획

| 스킬 | 위치 | 설명 |
|------|------|------|
| `staffing-plan` | `cs-operations/skills/staffing-plan/SKILL.md` | 인력 배치 최적화 계획 |
| `process-improvement` | `cs-operations/skills/process-improvement/SKILL.md` | 프로세스 개선 과제 도출 |
| `meeting-notes` | `cs-operations/skills/meeting-notes/SKILL.md` | 회의록 자동 작성 |
| `okr-cs` | `cs-operations/skills/okr-cs/SKILL.md` | CS 운영 OKR 수립 |

---

### cs-reporting — 보고서 작성

| 스킬 | 위치 | 설명 |
|------|------|------|
| `weekly-report` | `cs-reporting/skills/weekly-report/SKILL.md` | 주간 운영 보고서 자동 작성 |
| `monthly-report` | `cs-reporting/skills/monthly-report/SKILL.md` | 월간 성과 보고서 작성 |
| `executive-summary` | `cs-reporting/skills/executive-summary/SKILL.md` | 경영진 보고용 요약 작성 |

---

### cs-toolkit — 유틸리티

| 스킬 | 위치 | 설명 |
|------|------|------|
| `html-tool-spec` | `cs-toolkit/skills/html-tool-spec/SKILL.md` | HTML 도구 요구사항 명세서 작성 |
| `data-mock` | `cs-toolkit/skills/data-mock/SKILL.md` | CS 운영 테스트 데이터 생성 |
| `ko-grammar-check` | `cs-toolkit/skills/ko-grammar-check/SKILL.md` | 한국어 문서 교정 |

---

## JOYLAB 콘텐츠 스킬 (개인 전용)

### joylab-content — 멀티플랫폼 콘텐츠 자동화

| 스킬 | 위치 | 설명 | 환경 |
|------|------|------|------|
| `joylab-content-team` | `joylab-content/skills/content-team/SKILL.md` | URL 1개 → 네이버/Tistory/Threads/유튜브/뉴스레터/쇼츠 6종 콘텐츠 자동 생성 | 집 전용 |

**트리거**: `/content [URL]`  
**태그**: `home-only` · `content` · `multi-platform` · `joylab`  
**서브에이전트**: `content-planner` → 6개 writer 병렬 → `content-reviewer` (`.claude/agents/` 참조)

---

## 통계

| 구분 | 수 |
|------|----|
| CS Ops 플러그인 | 8 |
| CS Ops 스킬 | 26 |
| JOYLAB 스킬 | 1 |
| **전체 스킬** | **27** |
