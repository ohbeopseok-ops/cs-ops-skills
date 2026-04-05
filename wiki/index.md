# CS Ops Skills — 스킬 목록 인덱스

> 전체 29개 스킬 목록. 플러그인별 분류, 설명, 파일 경로 포함.

---

## cs-quality-analysis — 상담 품질 분석

| 스킬 | 설명 | 경로 |
|------|------|------|
| `qa-scoring` | 상담 품질 평가 항목별 가중 점수 계산 및 등급 산출. 녹취/STT 텍스트를 기준에 따라 분석하고 항목별 점수와 종합 등급 산출. | `cs-quality-analysis/skills/qa-scoring/SKILL.md` |
| `autoqa-analysis` | AutoQA 시스템 데이터 기반 트렌드 분석. 자동 평가 데이터로 품질 추이, 취약 항목 패턴, 이상 징후 탐지. | `cs-quality-analysis/skills/autoqa-analysis/SKILL.md` |
| `elderly-customer-qa` | 고령자(65세 이상) 상담 품질 특화 평가. 일반 QA 기준에 고령자 보호 가산 항목 추가 적용. | `cs-quality-analysis/skills/elderly-customer-qa/SKILL.md` |
| `compliance-check` | 상담 스크립트 및 규정 준수 점검. 필수 멘트 이행 여부, 금지 표현 사용 여부, 규정 위반 항목 식별. | `cs-quality-analysis/skills/compliance-check/SKILL.md` |
| `quality-trend` | 상담 품질 추이 분석 및 예측. 기간별 품질 데이터로 추세·계절성·이상 구간 파악, 다음 기간 품질 예측. | `cs-quality-analysis/skills/quality-trend/SKILL.md` |

---

## cs-coaching — 코칭 및 피드백

| 스킬 | 설명 | 경로 |
|------|------|------|
| `coaching-feedback` | 상담사 맞춤 코칭 피드백 작성. SBI(Situation-Behavior-Impact) 모델 적용, 강점 강화·취약점 개선 구체적 피드백 생성. | `cs-coaching/skills/coaching-feedback/SKILL.md` |
| `improvement-plan` | 상담사 개인/팀 취약 항목 기반 개선 계획 수립. 진단 → 목표 → 실행 → 측정 구조의 PIP/TIP/EIP 생성. | `cs-coaching/skills/improvement-plan/SKILL.md` |
| `coaching-script` | 코칭 세션 진행 스크립트 자동 생성. 코칭 목적·상담사 수준·취약 항목에 맞는 대화 가이드와 예상 응답 포함. | `cs-coaching/skills/coaching-script/SKILL.md` |

---

## cs-performance — KPI 및 성과 관리

| 스킬 | 설명 | 경로 |
|------|------|------|
| `kpi-analysis` | CS 운영 KPI 현황 분석 및 원인 진단. 목표 대비 현황, 변화 원인, 개선 우선순위 분석. | `cs-performance/skills/kpi-analysis/SKILL.md` |
| `tnps-prediction` | T-NPS(전화 고객 순추천지수) 예측 및 리스크 상담사 식별. 품질·처리·고객반응 데이터 기반 T-NPS 예측 점수 산출. | `cs-performance/skills/tnps-prediction/SKILL.md` |
| `agent-benchmarking` | 상담사/팀 성과 벤치마킹 분석. 품질·효율·고객성과·성장 차원 다차원 비교, 우수자 특성 식별. | `cs-performance/skills/agent-benchmarking/SKILL.md` |
| `target-setting` | 데이터 기반 CS 운영 목표치 설정. 과거 실적·트렌드·벤치마크 분석으로 도전적·달성 가능한 KPI 목표 산출. | `cs-performance/skills/target-setting/SKILL.md` |

---

## cs-voc — VOC 및 고객 분석

| 스킬 | 설명 | 경로 |
|------|------|------|
| `voc-categorization` | VOC 유형 분류 및 태깅. 고객 불만·문의·제안을 체계적으로 분류하고 긴급도·개선 과제 도출. | `cs-voc/skills/voc-categorization/SKILL.md` |
| `complaint-root-cause` | 고객 불만 콜 근본 원인 분석. 5-Why + Fishbone으로 불만 발생 구조 진단, 재발 방지 대책 도출. | `cs-voc/skills/complaint-root-cause/SKILL.md` |
| `sentiment-analysis` | 고객 발화 및 VOC 텍스트 감성 분석. 감성 극성·강도·핵심 감정 키워드 추출, 위험 발화 탐지. | `cs-voc/skills/sentiment-analysis/SKILL.md` |
| `nudge-analysis` | 넛지 마케팅 상담 효과 분석. 성공률·고객 반응 패턴·효과적 넛지 타이밍 분석 및 스크립트 최적화. | `cs-voc/skills/nudge-analysis/SKILL.md` |

---

## cs-stt — STT 대화 분석

| 스킬 | 설명 | 경로 |
|------|------|------|
| `conversation-analysis` | STT 대화 텍스트 전체 분석. 대화 구조·감성·핵심 이슈·상담사 행동 패턴·리스크 신호 종합 평가. | `cs-stt/skills/conversation-analysis/SKILL.md` |
| `script-compliance` | STT 텍스트 상담 스크립트 준수율 분석. 필수 안내 멘트·인사 스크립트·처리 프로세스 준수 여부 통계화. | `cs-stt/skills/script-compliance/SKILL.md` |
| `pii-detection` | STT 대화에서 개인정보 탐지 및 마스킹. 주민번호·계좌번호·전화번호·주소 등 PII 식별·규정 준수 형식 처리. | `cs-stt/skills/pii-detection/SKILL.md` |

---

## cs-operations — 운영 기획

| 스킬 | 설명 | 경로 |
|------|------|------|
| `staffing-plan` | CS 운영 인력 배치 최적화 계획 수립. 콜 볼륨 패턴·서비스수준 목표·상담사 스킬 기반 배치 계획 생성. | `cs-operations/skills/staffing-plan/SKILL.md` |
| `process-improvement` | CS 운영 프로세스 개선 과제 도출 및 실행 계획 수립. 비효율 구간 식별·개선 방안·실행 로드맵 작성. | `cs-operations/skills/process-improvement/SKILL.md` |
| `meeting-notes` | 회의 내용을 구조화된 회의록으로 작성. 결정사항·액션 아이템·후속 일정이 명확한 회의록 생성. | `cs-operations/skills/meeting-notes/SKILL.md` |
| `okr-cs` | CS 운영팀 OKR 수립. 센터/팀 목표를 KPI 기반으로 정성 목표·정량 핵심 결과로 구조화. | `cs-operations/skills/okr-cs/SKILL.md` |

---

## cs-reporting — 보고서 작성

| 스킬 | 설명 | 경로 |
|------|------|------|
| `weekly-report` | 주간 CS 운영 보고서 자동 작성. KPI 현황·품질 이슈·주요 활동·다음 주 계획 포함. | `cs-reporting/skills/weekly-report/SKILL.md` |
| `monthly-report` | 월간 CS 운영 성과 보고서 작성. 월간 KPI·품질 트렌드·VOC 분석·주요 성과와 과제 종합. | `cs-reporting/skills/monthly-report/SKILL.md` |
| `executive-summary` | 경영진 보고용 CS 운영 요약 작성. 복잡한 운영 데이터를 1-2페이지로 압축, 신호등 판정 포함. | `cs-reporting/skills/executive-summary/SKILL.md` |

---

## cs-toolkit — 유틸리티

| 스킬 | 설명 | 경로 |
|------|------|------|
| `html-tool-spec` | 폐쇄망 환경 HTML/JavaScript 도구 요구사항 명세서 작성. 기능 명세·UI 구조·데이터 처리·폐쇄망 제약 사항 포함. | `cs-toolkit/skills/html-tool-spec/SKILL.md` |
| `data-mock` | CS 운영 도구 테스트용 가상 데이터 생성. 상담사 성과·QA 평가·STT 샘플·VOC 목록 등 현실적 테스트 데이터. | `cs-toolkit/skills/data-mock/SKILL.md` |
| `ko-grammar-check` | 한국어 업무 문서 교정. 보고서·코칭 피드백·안내 멘트·이메일 등 맞춤법·문법·표현 적절성 점검. | `cs-toolkit/skills/ko-grammar-check/SKILL.md` |

---

## 통계

| 항목 | 수 |
|------|-----|
| 플러그인 | 8 |
| 스킬 | 29 |
| skills/user/ 인제스트 파일 | 29 |

> **flat index 경로:** `skills/user/<skill-name>.md`
