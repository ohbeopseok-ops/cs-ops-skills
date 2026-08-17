한국어 | [English](README.en.md) · [← README](README.md)

# 전체 카탈로그

8개 플러그인 · 29개 스킬 · 7개 커맨드.
모든 스킬은 **[하네스 규칙 R1–R8](HARNESS.md)** 을 인라인으로 포함한다.

> **읽는 방법** — 스킬은 평소 대화 중 자동으로 붙는다. 아래 목록은 "무엇을 물어볼 수 있는지"를
> 파악하는 색인이며, 스킬 이름을 외워서 호출할 필요는 없다. 커맨드만 명시적으로 입력한다.

---

## 1. cs-quality-analysis — 상담 품질 분석

**Skills (5)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `qa-scoring` | 100점 가중 배점표로 항목별 점수와 종합 등급(S–D) 산출. 필수 항목 위반은 결격 처리 |
| `autoqa-analysis` | AutoQA 자동 평가 데이터의 품질 추이·취약 항목 패턴·이상 징후 탐지 |
| `elderly-customer-qa` | 고령자(65세 이상) 상담 특화 평가 — 일반 QA에 취약 항목 추가 적용 |
| `compliance-check` | 필수 멘트 이행, 금지 표현 사용, 규정 위반 항목 식별 |
| `quality-trend` | 기간별 품질 추세·계절성·이상 구간 파악 및 다음 기간 예측 |

**Commands (1)**

- `/evaluate` — 상담 STT 텍스트 품질 평가 전체 사이클 (마스킹 → 대화분석 → 준수점검 → QA 점수 → 고령자 특화)

---

## 2. cs-coaching — 코칭 및 피드백

**Skills (3)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `coaching-feedback` | SBI(Situation-Behavior-Impact) 모델 기반 맞춤 코칭 피드백 작성 |
| `improvement-plan` | 취약 항목 진단 → 목표 → 실행 방법 → 측정 지표로 구성된 개선 계획 |
| `coaching-script` | 코칭 목적·상담사 수준에 맞춘 세션 대화 가이드와 예상 응답 |

**Commands** — 없음 (스킬 직접 호출)

---

## 3. cs-performance — KPI 및 성과 관리

**Skills (4)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `kpi-analysis` | 목표 대비 현황, 변화 원인, 개선 우선순위 진단 |
| `tnps-prediction` | T-NPS 예측 점수 산출 및 리스크 상담사·개입 우선순위 도출 |
| `agent-benchmarking` | 개인/팀 KPI·품질 지표 다차원 비교로 우수자 특성과 개선 대상 식별 |
| `target-setting` | 과거 실적·트렌드·벤치마크 기반 달성 가능한 KPI 목표치 산출 |

**Commands (1)**

- `/analyze-kpi` — KPI 현황 분석 및 원인 진단

---

## 4. cs-voc — VOC 및 고객 분석

**Skills (4)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `voc-categorization` | 불만·문의·제안 체계적 분류 및 우선순위 산출 |
| `complaint-root-cause` | 5-Why + Fishbone으로 불만 발생 구조 진단, 재발 방지 대책 도출 |
| `sentiment-analysis` | 감성 극성(긍정/부정/중립)·강도·핵심 감정 키워드 추출 |
| `nudge-analysis` | 상담 중 넛지 마케팅의 성공률·고객 반응 패턴·효과적 타이밍 분석 |

**Commands (1)**

- `/analyze-complaints` — 불만 콜 심층 분석 (분류 → 근본원인 → 개선과제)

---

## 5. cs-stt — STT 대화 분석

**Skills (3)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `pii-detection` | 주민번호·계좌·전화·주소·이름 탐지 및 규정 준수 형식 마스킹 (**R2에 따라 항상 1단계**) |
| `conversation-analysis` | 고객–상담사 대화의 품질·감성·핵심 이슈·처리 결과 종합 평가 |
| `script-compliance` | 필수 안내 멘트·인사 스크립트·처리 프로세스 준수율 통계 산출 |

**Commands (1)**

- `/analyze-call` — STT 텍스트 전체 분석 (품질 + 감성 + 준수율)

---

## 6. cs-operations — 운영 기획

**Skills (4)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `staffing-plan` | 콜 볼륨 패턴·서비스수준 목표·상담사 스킬 고려한 인력 배치 계획 |
| `process-improvement` | 비효율 구간 식별 → 개선 방안 → 실행 로드맵 |
| `meeting-notes` | 결정사항·액션 아이템·후속 일정이 명확한 구조화 회의록 |
| `okr-cs` | 센터/팀 목표를 KPI 기반 측정 가능한 OKR로 구조화 |

**Commands (1)**

- `/plan-okr` — CS 운영 OKR 수립

---

## 7. cs-reporting — 보고서 작성

**Skills (3)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `weekly-report` | KPI 현황·품질 이슈·주요 활동·다음 주 계획 포함 주간 보고서 |
| `monthly-report` | 월간 KPI 달성·품질 트렌드·VOC 분석·주요 과제 종합 보고서 |
| `executive-summary` | 1–2페이지 경영진 요약 — 핵심 수치, 신호등 판정, 이슈와 조치 |

**Commands (2)**

- `/weekly-report` — 주간 운영 보고서 자동 작성
- `/monthly-report` — 월간 성과 보고서 작성

---

## 8. cs-toolkit — 유틸리티

**Skills (3)**

| 스킬 | 무엇을 하는가 |
| :--- | :--- |
| `html-tool-spec` | 폐쇄망 HTML/JS 도구의 기능·UI·데이터 처리·제약 사항 명세서 |
| `data-mock` | 성과·QA·STT·VOC 가상 테스트 데이터 생성 (실데이터 대체 — R3) |
| `ko-grammar-check` | 한국어 업무 문서 맞춤법·문법·표현 적절성 교정 |

**Commands** — 없음 (스킬 직접 호출)

---

## 커맨드 로드맵

아래 커맨드는 **아직 구현되지 않았다.** 해당 기능은 지금도 스킬 직접 호출로 사용할 수 있으며
(예: "상담사 김OO의 코칭 피드백을 작성해줘"), 커맨드는 그 체인을 한 줄로 줄이는 편의 장치다.

<!-- validate:planned-start -->

| 커맨드 | 플러그인 | 체인 |
| :--- | :--- | :--- |
| `/autoqa-report` | cs-quality-analysis | autoqa-analysis → quality-trend |
| `/audit-quality` | cs-quality-analysis | qa-scoring → compliance-check → quality-trend |
| `/elderly-audit` | cs-quality-analysis | elderly-customer-qa → compliance-check |
| `/coach` | cs-coaching | qa-scoring → coaching-feedback |
| `/plan-improvement` | cs-coaching | coaching-feedback → improvement-plan |
| `/coaching-session` | cs-coaching | improvement-plan → coaching-script |
| `/predict-tnps` | cs-performance | sentiment-analysis → tnps-prediction |
| `/benchmark` | cs-performance | kpi-analysis → agent-benchmarking |
| `/set-targets` | cs-performance | kpi-analysis → target-setting |
| `/analyze-voc` | cs-voc | voc-categorization → complaint-root-cause → sentiment-analysis |
| `/nudge-check` | cs-voc | nudge-analysis |
| `/check-script` | cs-stt | script-compliance |
| `/mask-pii` | cs-stt | pii-detection |
| `/plan-staffing` | cs-operations | kpi-analysis → staffing-plan |
| `/improve-process` | cs-operations | process-improvement |
| `/meeting-notes` | cs-operations | meeting-notes |
| `/exec-summary` | cs-reporting | monthly-report → executive-summary |
| `/spec-tool` | cs-toolkit | html-tool-spec |
| `/mock-data` | cs-toolkit | data-mock |

<!-- validate:planned-end -->

> 이 표는 `scripts/validate.py`의 커맨드 존재 검사에서 제외된다
> (`validate:planned-start` / `validate:planned-end` 구간). 구현하는 즉시 위쪽 플러그인 섹션으로
> 옮기면 검증 대상이 된다 — 문서가 있는데 파일이 없는 상태를 게이트가 잡아낸다.
