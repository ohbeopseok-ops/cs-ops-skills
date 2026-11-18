# 기존 스킬 비교·재사용 분석

조사 대상(실제로 읽은 것): ① 계정 스킬 `lesson-designer-ppt-builder` SKILL.md (84줄) ② 레포 `ohbeopseok-ops/cs-ops-skills` @1eb2ffa 의 8개 플러그인 중 `cs-toolkit/html-tool-spec`.
레포 전체 파일 목록에서 PPT·슬라이드·교안 전용 스킬은 **없음**(`find` 로 확인). 참조 영상 자료는 접근 불가로 비교 대상에서 제외.

## 승계(그대로 유지)
| 출처 | 규칙 | 이 스킬 반영 |
|---|---|---|
| lesson-designer | 입력 확인표, 모르면 가정 명시 | SKILL.md §0 |
| lesson-designer | 근거 없는 수치·정책·사례 금지, `[확인 필요]`, `[실제]/[가상]` | deck JSON + QA D5/D6 |
| lesson-designer | 교육 흐름 고정(문제 인식→…→효과 측정), 시간 합계 = 총 시간 | stage 레일, QA D2 |
| lesson-designer | 슬라이드 본문과 강사 멘트 분리(발표자 노트) | `notes` 필드, N8/N9/D1 |
| lesson-designer | 표지: 버전·작성일·대상·상태 "초안 (AI 생성, 관리자 검토 전)" | cover 컴포넌트, PPTX cover |
| lesson-designer | 성과 주장 금지선(비교 근거 없이 개선 서술 금지) | 차트 슬라이드, 요약 슬라이드 |
| lesson-designer | JOYLAB 토큰 `#FAFAF7 / #C17F24 / #2D7D6F`, Pretendard | executive·learning 기본 |
| lesson-designer | 갱신 시 원본 보존, 변경 이력 | 별도 브랜치, CHANGELOG |
| html-tool-spec | 단일 HTML, CDN 금지, localStorage 허용, `@media print`, 한글 폰트 내장/시스템 | 엔진 전반 |

## 변경·확장
| 항목 | 기존 | V1.0 |
|---|---|---|
| 출력 | .pptx 만 | HTML + PPTX (동일 JSON) |
| 검증 | PPT 육안 + python-pptx 장수 | Playwright 134 + PPTX 30 + 자체 검증 10 |
| 본문 크기 | PPT 18pt 이상 | HTML 22px 이상 / PPTX 18pt(보조 14·12pt) |
| 디자인 | 단일 JOYLAB | 3테마(목적별) |
| 인터랙션 | 없음 | 퀴즈·타이머·노트·목차 |
| html-tool-spec 권장 "1280px 최적화" | 1280 기준 | 1920 캔버스 스케일(1280에서도 위치 ±2px 동일, QA A3) |

## 재사용하지 않은 것
- `pptx` 스킬의 pptxgenjs 경로: python-pptx 로 충분하고 동일 JSON 을 쓰기 위해 제외.
- 두 스킬에 PPT용 이미지·로고 자산 없음 → 사내 로고는 만들지 않음(제공 시 적용).

## 데이터·기능 보존
기존 파일은 한 줄도 수정하지 않음(레포: 신규 디렉터리만 추가, `manifest.json` 미수정). 기존 스킬의 기능은 그대로 사용 가능.
