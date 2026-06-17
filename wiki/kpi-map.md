# CS 운영 KPI 맵

> LG U+ 홈CS 핵심 성과지표 전체 맵. 지표 정의, 목표 기준, 상호 연계 관계.

**최종 수정:** 2026-06-17  
**관련 페이지:** [tnps-model](tnps-model.md) · [qa-framework](qa-framework.md) · [report-templates](report-templates.md)  
**소스:** [kpi-analysis SKILL](../cs-performance/skills/kpi-analysis/SKILL.md)

---

## KPI 계층 구조

```
[최상위 지표]
    T-NPS (전화 고객 순추천지수)
         ↑
[중간 지표]
    QA 평균 점수 | FCR | AHT | 이관율
         ↑
[운영 지표]
    항목별 QA 점수 | 상담사별 지표 | 콜 유형별 데이터
```

---

## 핵심 지표 정의

### T-NPS (Telephone Net Promoter Score)
- **정의:** 전화 상담 후 고객 추천 의향 (-100 ~ +100)
- **계산:** (추천 비율%) - (비추천 비율%)
- **목표:** [미확인 — 팀별 상이, 업데이트 필요]
- **연관:** QA(40%) + FCR(35%) + 고객반응(25%) → [tnps-model](tnps-model.md)

### FCR (First Call Resolution)
- **정의:** 재연결 없이 첫 통화에서 문제 해결한 비율
- **계산:** (단일 콜 해결 건수 / 전체 콜 수) × 100
- **목표:** [미확인]
- **레버리지:** T-NPS 예측의 35% 기여 — 개선 효과 빠름

### AHT (Average Handle Time)
- **정의:** 상담 시작~종료까지 평균 처리 시간
- **계산:** (통화 시간 + 후처리 시간) / 콜 수
- **주의:** AHT 단축이 목표가 아님 — FCR과 균형 필요
- **리스크 기준:** 팀 평균 +50% 이상 → MEDIUM RISK

### 이관율
- **정의:** 다른 부서/담당자로 이관된 콜 비율
- **리스크 기준:** 15% 이상 → MEDIUM RISK
- **원인:** 업무 숙지 부족 또는 권한 부재

### QA 평균 점수
- **정의:** 팀/개인 상담 품질 평균
- **연관 등급:** → [qa-framework](qa-framework.md)

---

## KPI 연계 관계

```
FCR↑ → AHT↓ (통상) + T-NPS↑ (가장 강한 레버)
QA↑ → T-NPS↑ (40% 비중)
이관율↓ → FCR↑ → T-NPS↑
AHT 과도 단축 → QA↓ 위험 (속도 vs 품질 트레이드오프)
```

---

## 목표 설정 원칙

1. 현재 수준에서 **+10~15%** 범위 내 단기 목표
2. 최하위 25% 상담사를 팀 중앙값으로 끌어올리는 것이 T-NPS에 가장 큰 효과
3. 개인 목표는 팀 목표와 연동, 상향 불일치 없게

→ 목표 설정 방법: [target-setting SKILL](../cs-performance/skills/target-setting/SKILL.md)  
→ 주간 보고서 KPI 섹션: [report-templates](report-templates.md)
