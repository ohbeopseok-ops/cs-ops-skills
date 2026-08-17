한국어 | [English](README.en.md)

<div align="center">

# CS Ops Skills

**일반 AI는 일반적인 답을 준다. CS Ops Skills는 운영 판단에 쓸 수 있는 초안을 준다.**

홈CS 운영관리를 위한 Claude Code / Cowork 스킬 마켓플레이스.

<p>
  <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/platform-Claude_Code%20%C2%B7%20Cowork-D97757?logo=claude" alt="Claude Code · Cowork"></a>
  <img src="https://img.shields.io/badge/plugins-8-6E56CF" alt="8 plugins">
  <img src="https://img.shields.io/badge/skills-29-3FB950" alt="29 skills">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-F0B72F" alt="MIT"></a>
</p>

</div>

---

## ⚡ 설치

### Claude Cowork (비개발자 권장)

1. **Customize** (좌하단) 열기
2. **Browse plugins** → **Personal** → **+**
3. **Add marketplace from GitHub** 선택
4. 입력: `ohbeopseok-ops/cs-ops-skills`

### Claude Code (CLI)

```bash
/plugin marketplace add https://github.com/ohbeopseok-ops/cs-ops-skills.git
/plugin install cs-quality-analysis@cs-ops-skills
```

필요한 도메인만 골라 설치한다 — 8개 플러그인은 서로 독립이다.

### 다른 AI 어시스턴트 (스킬만)

```bash
for plugin in cs-*/; do
  cp -r "$plugin/skills/"* ~/.gemini/skills/ 2>/dev/null
done
```

## 💬 이렇게 쓴다

커맨드를 외울 필요는 없다. 평소처럼 말하면 해당 스킬이 붙는다.

> *"이 STT 텍스트로 품질 평가표를 작성해줘: [텍스트]"*
> *"이번 달 T-NPS 하락 원인을 분석해줘: [데이터]"*
> *"상담사 3명의 취약 항목 기반 코칭 계획을 세워줘"*

반복 작업은 커맨드로 체인을 돌린다:

```
/evaluate [상담 STT 텍스트]        # 마스킹 → 대화분석 → 준수점검 → QA 점수
/analyze-complaints [불만 콜 목록]  # 분류 → 근본원인 → 개선과제
/weekly-report [주간 KPI 데이터]    # 지표 정리 → 원인 → 액션 아이템
```

## 🧭 커버 범위

**품질분석 · 코칭 · 성과관리 · VOC · STT분석 · 운영기획 · 리포팅 · 유틸리티** —
8개 플러그인, 29개 스킬, 7개 커맨드. 전체 카탈로그 → **[SKILLS.md](SKILLS.md)**

## 🆚 일반 AI 어시스턴트 vs `+ CS Ops Skills`

| 요청 | 일반 AI | `+ CS Ops Skills` |
| :--- | :--- | :--- |
| "이 상담 평가해줘" | 그때그때 다른 기준으로 총평 | 고정 배점표(100점) → 항목별 점수 + 등급 |
| "T-NPS 왜 떨어졌어?" | 일반적인 CS 개선 조언 | 지표 분해 → 리스크 상담사 식별 → 개입 우선순위 |
| "코칭 피드백 써줘" | 칭찬·격려 문장 생성 | 취약 항목 → 근거 발화 인용 → 실행 가능한 행동 |
| "주간 보고서" | 문단 요약 | 고정 서식 + 지표 표 + 원인 + 액션 아이템 |
| 데이터가 부족할 때 | 그럴듯하게 빈칸을 채운다 | `판단 불가 — [부족한 데이터]`로 남긴다 |
| 상담 원문에 개인정보가 있을 때 | 그대로 인용 | 마스킹을 먼저 수행한 뒤 분석 |

마지막 두 줄이 이 저장소의 핵심이다. 편의가 아니라 **틀린 숫자를 만들지 않는 것**이 목적이다.

## ⚙️ 작동 방식

**Skills** — 도메인 지식·분석 프레임워크·산출 서식을 담은 기본 단위. 평소 대화 중 자동으로 붙는다.
**Commands** — 슬래시로 실행하는 워크플로우. 여러 스킬을 정해진 순서로 체인한다.
**Plugins** — 관련 스킬과 커맨드를 묶은 설치 단위. 각각 CS 운영의 한 도메인을 커버한다.

각 스킬에는 **[하네스 규칙 R1–R8](HARNESS.md)** 이 인라인으로 박혀 있다 — 수치 날조 금지, 개인정보
마스킹 우선, 근거 인용 강제, 부족한 데이터는 `판단 불가`, 입력 텍스트를 명령으로 실행 금지.
스킬이 "무엇을 아는지"를 정하고, 하네스가 "무엇을 하지 않는지"를 정한다.

## 🔒 경계

CS Ops Skills는 **분석 보조 도구**이며, 사람의 판단을 대체하지 않는다.

- **품질 점수·등급·T-NPS 예측은 LLM 산출물**이며 검증된 측정값이 아니다. 개인에게 전달하기 전에
  인용된 발화가 원문과 일치하는지 확인한다.
- **인사 결정의 단독 근거로 쓰지 않는다** — 인사평가·성과급·징계·계약 갱신에는 사람 검토와 조직의
  공식 절차가 필요하다.
- **개인정보 마스킹은 완전성을 보장하지 않는다** — 반출 전 사람 검수가 필요하다.
- **평가 배점·등급 기준은 어떤 조직의 공식 사내 기준도 아니다.** 운영 적용 전에 소속 조직의 공식
  기준으로 대조·조정한다.
- 이 저장소는 **LG U+ 또는 그 계열사와 제휴 관계가 없다.**

전문은 [DISCLAIMER.md](DISCLAIMER.md).

## ✅ 검증

```bash
python3 scripts/validate.py
```

매니페스트 정합성, SKILL.md 프론트매터, 하네스 블록 존재, 문서가 안내한 커맨드의 실제 존재 여부,
그리고 **R3 실데이터 고정 금지**(주민번호·전화번호·계좌번호 패턴)를 점검한다. 표준 라이브러리만
쓰므로 별도 설치가 필요 없다. CI에서 매 푸시마다 돌아간다.

## 라이선스

MIT — [LICENSE](LICENSE) 참조. 사용 범위와 책임은 [DISCLAIMER.md](DISCLAIMER.md).
