# CS Ops Wiki — 인덱스

> LG U+ 홈CS 운영 지식베이스. LLM이 유지·확장하는 인터링크 마크다운 문서 모음.

**업데이트:** 2026-06-17  
**총 페이지:** 12  
**커맨드:** `/wiki-ingest` · `/wiki-lint`  
**커버 도메인:** 품질관리 · 코칭 · 성과 · VOC · STT · 운영기획 · 리포팅

---

## 사용법

```
# 질문할 때
"wiki를 참고해서 [질문]"

# 새 지식 추가 (2단계 CoT 자동 적용)
/wiki-ingest [소스 경로 또는 내용]

# 정기 점검
/wiki-lint

# 자동 수정 가능한 이슈만 처리
/wiki-lint --fix
```

---

## 카테고리별 페이지 목록

### 핵심 개념 (Core Concepts)
| 페이지 | 설명 |
|--------|------|
| [qa-framework.md](qa-framework.md) | QA 평가 구조, 가중치, 등급 기준 |
| [tnps-model.md](tnps-model.md) | T-NPS 예측 모델 및 리스크 분류 |
| [coaching-system.md](coaching-system.md) | 코칭 프레임워크 및 피드백 구조 |
| [kpi-map.md](kpi-map.md) | CS 운영 KPI 전체 맵 |

### 운영 프로세스 (Processes)
| 페이지 | 설명 |
|--------|------|
| [voc-workflow.md](voc-workflow.md) | VOC 분류 → 분석 → 개선 워크플로우 |
| [stt-analysis.md](stt-analysis.md) | STT 대화 분석 기준 및 개인정보 처리 |
| [staffing-ops.md](staffing-ops.md) | 인력 배치 및 운영 계획 기준 |

### 판단 기준 (Decision Rules)
| 페이지 | 설명 |
|--------|------|
| [risk-thresholds.md](risk-thresholds.md) | 리스크 임계값 — 언제 개입할 것인가 |
| [elderly-customer.md](elderly-customer.md) | 고령자 상담 특화 기준 |

### 템플릿 & 산출물 (Outputs)
| 페이지 | 설명 |
|--------|------|
| [report-templates.md](report-templates.md) | 주간/월간/경영진 보고서 구조 |
| [feedback-patterns.md](feedback-patterns.md) | 효과적 코칭 피드백 패턴 모음 |

### 메타 (Meta)
| 페이지 | 설명 |
|--------|------|
| [log.md](log.md) | 변경 이력 타임스탬프 |
| [schema.md](schema.md) | wiki 관리 규칙 및 컨벤션 |

---

## 빠른 참조

**QA 등급 한눈에:** S(95+) · A(85-94) · B(70-84) · C(55-69) · D(54↓)  
**T-NPS 리스크:** 추천(75+) · 중립(55-74) · 비추천위험(54↓)  
**코칭 우선순위:** HIGH RISK → 즉시 · MEDIUM → 1주 내 · LOW → 월간
