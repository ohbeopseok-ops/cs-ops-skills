---
name: joylab-html-presentation
description: 교육·보고·리서치용 프레젠테이션을 단일 오프라인 HTML(1920x1080)과 PPTX로 제작하고 Playwright로 검증한다. HTML 발표자료, 웹 슬라이드, 교안 HTML, 발표용 덱 제작 요청 시 사용.
---

# JoyLab HTML Presentation V1.0

하나의 deck JSON 원본에서 **단일 HTML(오프라인)** 과 **PPTX** 를 만들고, 자동 QA 를 통과시킨 뒤에만 완료를 선언한다.
브랜치 `feature/joylab-html-presentation-v1` 에서 개발. 기존 파일은 수정하지 않았다.

## 언제 쓰나
"HTML 발표자료", "웹 슬라이드", "교안 HTML로", "발표용 덱", "/html-deck" 등. 단순 .pptx 편집·읽기만이면 `pptx` 스킬을 쓴다.
기존 `lesson-designer-ppt-builder` 는 교수설계(목표·시간·평가) 규칙의 출처이며 이 스킬이 그 규칙을 승계한다 (`docs/REUSE_ANALYSIS.md`).

## 0. 입력 (없으면 가정으로 진행하고 맨 위에 명시)
주제·문제 / 대상·수준(초·중·고급) / 총 시간(기본 60분) / 기대 행동 변화 1~3개 / 테마 / 근거 자료.
정책·평가기준·수치는 사용자가 준 최신 자료만 쓴다. 근거 없는 수치·정책·고객 사례는 만들지 않는다. 필요하면 `[확인 필요]`, 사례는 `[실제]`/`[가상]` 표기.

## 1. 테마 선택
| 테마 | 목적 | 시그니처 | 맞는 상황 |
|---|---|---|---|
| `executive` Executive Strategy | 결론 우선 보고 | 하단 "결론" 바 | 경영진·실장 보고, 의사결정 |
| `learning` Learning Experience | 학습 위치 인지 | 상단 학습 흐름 레일(9단계) | 교육·워크숍 |
| `research` Research Intelligence | 근거·신뢰 등급 확인 | 사실/추론/제안/가정 배지 + 근거 줄 | 분석 리포트, 투자·AI 리서치 |
상세: `DESIGN_SYSTEM.md`

## 2. 작업 순서
1. 원본 JSON 작성 (`src/deck/test-deck.json` 구조 참고). 슬라이드마다 `type`, `stage`, `minutes`, `title`(핵심 메시지 1개), `basis`(fact/inference/proposal/assumption), `sowhat`, `source`, `notes`(강사용), `data`.
2. 시간 합계 = `meta.total_minutes`, 목차 합 = 총 시간 확인 (QA D2 가 검사).
3. `python3 src/build.py --deck <json> --themes executive,learning,research` → `dist/*.html`
4. `python3 src/build_pptx.py --deck <json>` → `dist/*.pptx`
5. `python3 qa/qa_playwright.py --deck <json>` 와 `python3 qa/qa_pptx.py --render --deck <json>`
6. FAIL 이 있으면 원인을 **결함 / 검사 오류**로 구분해 고치고 재실행. UNVERIFIED 는 통과로 세지 않고 보고서에 그대로 적는다.
7. 결과는 `docs/VERIFICATION_REPORT.md` 형식(근거 병기)으로 보고.

## 3. 컴포넌트 (type)
`cover agenda statement cards flow compare case dialogue chart grid practice quiz table summary` — 필드 명세는 `DESIGN_SYSTEM.md §5`.
새 컴포넌트는 `src/build.py` 의 `c_*` 함수 + `src/components.css` 에 추가하고, 모든 콘텐츠 블록에 `data-box`, 장식에는 `data-deco` 를 붙인다 (QA 가 이를 기준으로 겹침·이탈을 검사).

## 4. 하드 규칙
- 외부 CDN·API·폰트·이미지 URL 금지. 폰트는 `src/fonts/` 서브셋 base64 내장(Pretendard, OFL).
- 본문 최소 22px(1920 기준), 슬라이드당 핵심 메시지 1개, 도식·차트·카드 우선.
- 표지에 버전·작성일·대상·상태(`초안 (AI 생성, 관리자 검토 전)`) 표기. 공식 승인 자료처럼 표시하지 않는다.
- 차트·사례의 가상 수치에는 `[가상]` 을 제목·kicker·출처에 표기하고, 인과 주장은 비교 근거(전후·대조군·기간·표본) 없이 쓰지 않는다.
- 외부에서 가져온 자료를 못 가져왔으면 추정하지 말고 그 사실을 보고서에 쓴다.

## 5. 한계 (V1.0)
- 참조 영상 `c_tmZ0Z9By0` 자료는 접근 불가로 **미반영**. 3개 테마는 JoyLab 독자 설계 (`CHANGELOG.md`, `docs/VERIFICATION_REPORT.md §1`).
- 헤드리스 Chrome 기준 검증. Windows/macOS 실기기, PowerPoint 렌더는 미검증.
