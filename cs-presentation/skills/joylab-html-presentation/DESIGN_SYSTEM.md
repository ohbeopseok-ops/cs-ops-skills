# JoyLab Presentation Design System V1.0

상태: 초안 (AI 생성, 관리자 검토 전) · 작성일 2026-11-18

## 1. 공통 규격
| 항목 | 값 |
|---|---|
| 캔버스 | 1920×1080 (16:9). 뷰포트에 맞춰 `transform: scale` 레터박스 |
| 안전 영역 | 좌우 96px, 상단 64px, 하단 44px |
| 구조 | `s-head`(kicker + title) / `s-body` / `s-foot`(결론·근거·쪽번호) |
| 폰트 | Pretendard Variable 서브셋 내장 → Apple SD Gothic Neo → Malgun Gothic → Noto Sans CJK KR |
| 글자 크기 최소 | 22px (캡션·쪽번호), 본문 24–35px, 제목 56–62px, 표지 92px |
| 한 슬라이드 | 핵심 메시지 1개 = title 1개 |
| 기본 색 토큰 | 배경 `#FAFAF7` · 앰버 `#C17F24` · 틸 `#2D7D6F` · 오류 `#B3322F` |

## 2. 테마 (왜 이 색·형태인가)
### Executive Strategy — 경영진 보고형
결론이 가장 먼저, 가장 크게. 크림 바탕 + 잉크 + 앰버. 모서리 10px, 그림자 최소. 시그니처: 모든 슬라이드 하단 잉크색 **결론 바**.
토큰: bg `#FAFAF7` ink `#1A1A1A` ink2 `#57564F` accent `#C17F24` accent-text `#8A5510`(앰버는 작은 글자에 명암비 부족이라 텍스트용 별도 톤) card `#FFF`.

### Learning Experience — 교육·워크숍형
학습자가 "교육 흐름의 어디"인지가 핵심. 둥근 모서리 28px, 틸 중심, 카드는 연한 틴트. 시그니처: 상단 **학습 흐름 레일** (문제 인식→학습목표→핵심 개념→현장 사례→시연→실습→피드백→현장 적용→효과 측정, 현재 단계 알약).
토큰: bg `#FAFAF7` ink `#1D2B28` accent2 `#2D7D6F` cover-bg `#256A5E`(표지 흰 글자 명암비 확보).

### Research Intelligence — 리서치 분석형
"이 주장의 근거와 신뢰 등급"을 바로 확인. 심청록 다크 `#12201E`, 앰버 `#E0A040`·민트 `#5FBFAE` 강조, 모서리 6px. 시그니처: 하단 **근거 줄** + 배지 `사실 / 추론 / 제안 / 가정·가상` (색에만 의존하지 않고 글자 표기).

## 3. 테마 변수 계약 (`themes/*.css` 가 모두 정의해야 함)
`--bg --bg2 --ink --ink2 --line --accent --accent-ink --accent-text --accent2 --accent2-text --card --card-line --r --shadow --kicker --title-size --title-weight --chip-bg --chip-ink --bad --bad-bg --bad-ink --good --good-bg --good-ink --bubble-coach --chart-bar --th-bg --th-ink --cover-bg --cover-ink --cover-ink2 --cover-kicker --cover-line --letterbox`
새 테마 = 이 변수 + 시그니처 규칙 몇 줄. 컴포넌트 CSS 는 변수만 참조한다.

## 4. 표기 규칙 (정직성)
| 배지 | 뜻 | 쓰는 곳 |
|---|---|---|
| 사실 | 제공된 원문·지침에서 확인 | 지침 인용 |
| 추론 | 사실에서 이끌어 낸 분석 | 문제 인식 |
| 제안 | 이 덱이 권고하는 방안 | 실습·과제 |
| 가정·가상 | 시연용 사례·수치 | 사례, 샘플 차트 |
`[가상]` `[확인 필요]` 는 렌더에서 반드시 유지(QA D6).

## 5. 컴포넌트 카탈로그 (`type` → 필수 `data` 필드)
| type | 용도 | data |
|---|---|---|
| cover | 표지 | (meta 사용) |
| agenda | 목차·시간 | rows[{stage,topic,slides,minutes}], fixed_minutes |
| statement | 핵심 주장 + 질문 3 | statement(**굵게** 지원), questions[3] |
| cards | 3분할(목표) | cards[{tag,head,body,change}] ×3 |
| flow | 순서가 있는 4단계 | steps[{name,desc,ex}] ×4 |
| compare | 대비 5행 | left_head,right_head,rows[{k,l,r}] |
| case | 사례 2 대비 | situation,bad{label,quote,why},good{…} |
| dialogue | 대화 + 단계 표시 | lines[{who,text,step}] ≤5 |
| chart | 막대 차트 + 질문 3 | chart_title,unit,max,bars[{label,value}],asks[{q,a}] |
| grid | 순서 없는 8항목 | items[{k,q}] ×8 (번호 미사용) |
| practice | 실습 + 타이머 | steps ×4, timer_seconds, rubric ×4, deliverable |
| quiz | 4지선다 | question,options ×4,answer(0-3),explain |
| table | 과제표 3행 | cols ×4, rows[3][4] |
| summary | 요약 3 + 측정 계획 | takeaways ×3, plan_head, plan ×3 |
번호 마커(1·2·3)는 실제 순서가 있는 flow·summary 에서만 사용, 순서 없는 grid 는 막대 마커.

## 6. 엔진 단축키
← → ↑ ↓ Space PageUp/Down 이동 · Home/End · F 전체화면 · T 목차 · N 발표자 노트 · A 애니메이션 · P PDF 인쇄 · R 퀴즈 초기화 · 퀴즈에서 1–4 · `?` 도움말 · Esc 패널 닫기. URL `#7` 로 7장 직접 진입. 마우스를 움직이면 하단 컨트롤이 2.6초 표시.

## 7. 인쇄(PDF)
`@page 1920px×1080px`, 슬라이드 1장 = 1쪽, HUD·노트 제외, 배경색 유지. 브라우저 인쇄 대화상자에서 "배경 그래픽" 허용.
