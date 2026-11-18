# CHANGELOG

## [1.0.0] — 2026-11-18 (초안, 관리자 검토 전)
브랜치: `feature/joylab-html-presentation-v1` (기존 파일 변경 없음, 신규 디렉터리 `cs-presentation/` 만 추가)

### Added
- 단일 오프라인 HTML 엔진: 1920×1080 스케일, 키보드, 전체화면, 목차, 진행률, 발표자 노트, 퀴즈, 실습 타이머, 애니메이션 ON/OFF, PDF 인쇄, 해시 이동, 터치 스와이프
- 3개 테마(Executive Strategy / Learning Experience / Research Intelligence), 14종 컴포넌트
- deck JSON → HTML/PPTX 빌더, 15슬라이드 테스트 덱
- Playwright QA(134 검사) + PPTX QA(30 검사) + QA 자체 검증(결함 주입 10종)
- Pretendard Variable 한글 서브셋(463KB, OFL-1.1) 내장

### Known gaps
- **참조 영상 `c_tmZ0Z9By0` 미반영**: 이 환경에서 YouTube 접근이 차단되어(프록시 403, 웹 검색에서도 식별 불가) 영상 설명란의 3개 스타일 프롬프트·코드·라이선스를 확보하지 못함. 추정하지 않았고 3개 테마는 독자 설계. 자료 확보 후 비교·보강 예정
- `.claude-plugin/manifest.json` 등록은 기존 파일 보존을 위해 하지 않음
- Windows/macOS 실기기, PowerPoint 렌더, 전체화면 실사용은 미검증(PPTX 렌더는 LibreOffice 기준)

### QA 중 발견·수정한 결함 (이력)
- 폰트 서브셋에 `§` 누락 → 추가
- 학습형 표지 보조 글자 명암비 4.22:1 → 표지 배경 `#256A5E`, 글자 `#EAF6F2`
- 연구형 퀴즈 정답/오답 마커 흰 글자 대비 부족 → `--good-ink/--bad-ink`
- 4단계 화살표를 의사요소로 카드 밖에 그려 스크롤 영역 초과 → 그리드 셀 요소로 변경
- 편집 중 생긴 고아 CSS 선언이 `.fl-idx` 규칙을 무효화(글자 16px) → 제거(QA T4가 검출)
