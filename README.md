# CS Ops Skills Marketplace

> LG U+ 홈CS 운영관리를 위한 AI 운영 시스템. 8개 플러그인, 30개 스킬, 20개 체인 워크플로우.  
> 품질분석 → 코칭 → 성과관리 → VOC → STT분석 → 운영기획 → 리포팅 전 영역 커버.

Claude Code, Cowork 전용 설계. Skills는 범용 AI 어시스턴트에서도 호환.

---

## Quick Start

상담사 품질 평가? → `/evaluate`  
코칭 피드백 작성? → `/coach`  
T-NPS 예측 분석? → `/predict-tnps`  
VOC 분석 리포트? → `/analyze-voc`  
STT 대화 분석? → `/analyze-call`  
주간 보고서 작성? → `/weekly-report`  

---

## 왜 CS Ops Skills인가

일반 AI는 일반적인 답을 준다. CS Ops Skills는 **LG U+ 홈CS 운영 구조**에 맞는 프레임워크를 준다.

각 스킬은 15년 CS 운영 경험을 인코딩한다 — 평가 가중치, 코칭 구조, KPI 연계, T-NPS 예측 로직이 워크플로우에 내장된다. 결과: 더 빠른 문서가 아니라 **더 나은 운영 판단**.

---

## 작동 방식

**Skills** — 도메인 지식, 분석 프레임워크, 가이드 워크플로우를 담은 기본 단위.  
**Commands** — `/command-name`으로 실행하는 사용자 트리거 워크플로우. 여러 스킬을 체인으로 연결.  
**Plugins** — 관련 스킬과 커맨드를 묶은 설치 단위. 각 플러그인은 CS 운영의 특정 도메인을 커버.

---

## 설치

### Claude Cowork (비개발자 권장)
1. **Customize** (좌하단) 열기
2. **Browse plugins** → **Personal** → **+**
3. **Add marketplace from GitHub** 선택
4. 입력: `[your-github-username]/cs-ops-skills`

### Claude Code (CLI)
```bash
claude plugin add --marketplace [your-github-username]/cs-ops-skills
```

### 다른 AI 어시스턴트 (스킬만)
```bash
# Gemini CLI용
for plugin in cs-*/; do
  cp -r "$plugin/skills/"* ~/.gemini/skills/ 2>/dev/null
done
```

---

## 플러그인 목록

### 1. cs-quality-analysis — 상담 품질 분석
상담 품질 평가, AutoQA 트렌드, 고령자 상담 기준, 스크립트 준수, 품질 추이

**Skills (4):** `qa-scoring` · `elderly-customer-qa` · `compliance-check` · `quality-trend`

**Commands (4):**
- `/evaluate` — 상담 녹취/STT 품질 평가 전체 사이클
- `/autoqa-report` — AutoQA 데이터 기반 트렌드 분석
- `/audit-quality` — 팀/개인 품질 감사
- `/elderly-audit` — 고령자 상담 특화 품질 점검

---

### 2. cs-coaching — 코칭 및 피드백
코칭 피드백 작성, 개선 계획 수립, 코칭 스크립트 생성

**Skills (3):** `coaching-feedback` · `improvement-plan` · `coaching-script`

**Commands (3):**
- `/coach` — 상담사별 맞춤 코칭 피드백 생성
- `/plan-improvement` — 취약 항목 기반 개선 계획 수립
- `/coaching-session` — 코칭 세션 스크립트 자동 생성

---

### 3. cs-performance — KPI 및 성과 관리
KPI 분석, T-NPS 예측, 상담사 벤치마킹, 목표 설정

**Skills (4):** `kpi-analysis` · `tnps-prediction` · `agent-benchmarking` · `target-setting`

**Commands (4):**
- `/analyze-kpi` — KPI 현황 분석 및 원인 진단
- `/predict-tnps` — T-NPS 예측 및 리스크 상담사 식별
- `/benchmark` — 상담사/팀 벤치마킹 리포트
- `/set-targets` — 데이터 기반 목표치 설정

---

### 4. cs-voc — VOC 및 고객 분석
VOC 유형 분류, 불만 원인 분석, 감성 분석, 넛지 마케팅 분석

**Skills (4):** `voc-categorization` · `complaint-root-cause` · `sentiment-analysis` · `nudge-analysis`

**Commands (3):**
- `/analyze-voc` — VOC 분류 → 원인 분석 → 개선 과제 도출
- `/analyze-complaints` — 불만 콜 심층 분석
- `/nudge-check` — 넛지 마케팅 효과 분석

---

### 5. cs-stt — STT 대화 분석
STT 대화 분석, 스크립트 준수율 분석, 개인정보 탐지/마스킹

**Skills (2):** `conversation-analysis` · `pii-detection`

**Commands (3):**
- `/analyze-call` — STT 텍스트 전체 분석 (품질+감성+준수율)
- `/check-script` — 스크립트 준수율 점검
- `/mask-pii` — 개인정보 탐지 및 마스킹 처리

---

### 6. cs-operations — 운영 기획
인력 배치, 프로세스 개선, 회의록, OKR

**Skills (4):** `staffing-plan` · `process-improvement` · `meeting-notes` · `okr-cs`

**Commands (4):**
- `/plan-staffing` — 인력 배치 최적화 계획
- `/improve-process` — 프로세스 개선 과제 도출
- `/meeting-notes` — 회의록 자동 작성
- `/plan-okr` — CS 운영 OKR 수립

---

### 7. cs-reporting — 보고서 작성
주간/월간 보고서, 경영진 요약

**Skills (3):** `weekly-report` · `monthly-report` · `executive-summary`

**Commands (3):**
- `/weekly-report` — 주간 운영 보고서 자동 작성
- `/monthly-report` — 월간 성과 보고서 작성
- `/exec-summary` — 경영진 보고용 요약 작성

---

### 8. cs-toolkit — 유틸리티
HTML 도구 요구사항 정의, 테스트 데이터 생성, 한국어 문서 교정

**Skills (3):** `html-tool-spec` · `data-mock` · `ko-grammar-check`

**Commands (2):**
- `/spec-tool` — HTML 도구 요구사항 명세서 작성
- `/mock-data` — CS 운영 테스트 데이터 생성

---

## 주요 사용 예시

**스킬 직접 활용:**
- `이 STT 텍스트에서 품질 이슈를 평가해줘 [텍스트 붙여넣기]`
- `이번 달 T-NPS 하락 원인을 분석해줘`
- `상담사 김철수의 코칭 피드백을 작성해줘`

**커맨드 체인:**
- `/evaluate 다음 STT 텍스트를 평가해줘 [텍스트]`
- `/analyze-voc 이번 주 접수된 VOC 목록 [데이터]`
- `/weekly-report 이번 주 KPI 데이터 [데이터]`

---

## 라이선스

MIT — [LICENSE](LICENSE) 참조.
