# HTML / PPTX 제작 가이드

## 1. 어느 형식으로 만들까
| 상황 | 권장 |
|---|---|
| 강의·워크숍에서 퀴즈·타이머·노트를 쓰며 직접 발표 | **HTML** (폐쇄망 PC 에서도 파일 1개로 실행) |
| 사내 표준 양식에 끼워 넣기, 동료가 수정, 메일 첨부 | **PPTX** |
| 배포·보관용 | HTML 에서 인쇄한 **PDF** |
같은 JSON 에서 둘 다 생성되므로 내용 수정은 JSON 한 곳에서만 한다.

## 2. 빠른 시작
```bash
cd cs-presentation/skills/joylab-html-presentation
pip install playwright python-pptx fonttools brotli pillow   # 빌드는 표준 라이브러리, QA/PPTX/폰트만 추가 필요
python3 src/build.py                    # dist/joylab-test-deck-{executive,learning,research}.html
python3 src/build_pptx.py               # dist/*.pptx
python3 qa/qa_playwright.py             # 134 검사, FAIL 시 종료코드 1
python3 qa/qa_pptx.py --render          # LibreOffice 설치 시 PDF 렌더까지
python3 qa/qa_selftest.py               # QA 가 결함을 잡는지 확인(음성 대조군)
```
Windows: `python` 사용, Chrome 경로는 `--chrome "C:\Program Files\Google\Chrome\Application\chrome.exe"` 또는 `CHROME_PATH`.

## 3. 새 덱 만들기
1. `src/deck/test-deck.json` 복사 → 새 파일. `meta` 수정(제목·대상·총 시간·`status` 는 승인 전까지 "초안").
2. 슬라이드 순서·`type` 선택(`DESIGN_SYSTEM.md §5`). **title 은 그 슬라이드의 결론 1문장**.
3. `minutes` 합계 = `meta.total_minutes`. 목차(agenda) 행 합 + `fixed_minutes` 도 동일해야 함.
4. 사례·대사·샘플 수치는 `[가상]`, 근거 없는 값은 `[확인 필요]`. `basis` 로 사실/추론/제안/가정을 구분.
5. `notes` 에 강사 멘트(슬라이드 본문과 분리). 퀴즈 `answer` 위치는 문항마다 분산.
6. 빌드 → QA → 눈으로 3테마 전체 확인.

## 4. HTML 발표 방법
- 파일을 Chrome/Edge 로 연다(Windows·macOS). `F` 전체화면, `N` 노트(발표자 화면용 별도 창은 V1.0 미지원 — 노트 패널을 화면 하단에 띄움), `T` 목차.
- 프로젝터에 노트가 보이면 안 될 때: 노트는 `N` 을 누르기 전에는 숨겨져 있다. 발표 전 `N` 상태(localStorage `jl-notes`)를 끄고 시작한다.
- 애니메이션: `A` 로 끄기. 운영체제 "동작 줄이기" 설정이면 기본 꺼짐.
- PDF: `P` → 대상 "PDF로 저장", 여백 없음, **배경 그래픽 체크**. 쪽 크기는 CSS 가 1920×1080 으로 지정.
- 공유 링크 `파일.html#9` 는 9장에서 열림.

## 5. PPTX 사용·한계
- 네이티브 도형·표·차트(편집 가능). 슬라이드마다 발표자 노트 입력됨. 퀴즈는 정답·해설이 **노트**에 들어가고 클릭 응답은 없음.
- 타이머·애니메이션·목차 패널은 PPTX 로 옮겨지지 않음(HTML 전용).
- 폰트는 파일에 내장되지 않음. Pretendard 미설치 PC 는 대체 폰트 → 줄바꿈이 달라질 수 있어 발표 전 한 번 훑어본다. `--font "맑은 고딕"` 으로 바꿔 생성 가능.
- 본문 글자: PPTX 는 화면 폭이 13.33in 라 HTML 22px ≈ 11pt. 이 시스템은 PPTX 본문 18pt, 보조 14pt, 쪽번호·출처 12pt 로 별도 기준 적용(기존 스킬의 "본문 18pt 이상" 승계, 보조 요소만 예외).

## 6. 폐쇄망 체크리스트
- [ ] `grep -E "https?://" dist/*.html` 결과 0건 (QA S1)
- [ ] 오프라인(네트워크 끊김) 상태로 열어 15장 이동 (QA O1)
- [ ] 한글이 폰트 서브셋 밖 글자(희귀 한자·이모지)를 쓰면 시스템 폰트로 대체됨 (QA T2 가 검출)
- [ ] 보안 정책상 HTML 실행이 막히면 PDF 또는 PPTX 로 배포

## 7. 문제 해결
| 증상 | 원인·조치 |
|---|---|
| QA L3 넘침 | 문장을 줄이거나 컴포넌트 칸 수를 줄인다(카드 글자 수 우선) |
| QA T5 명암비 | 테마 변수에서 해당 색을 어둡게/밝게. 앰버는 작은 글자에 `--accent-text` 사용 |
| QA D5 숫자 | 화면에 JSON 에 없는 숫자가 있음 → 창작 수치 여부 확인 |
| 전체화면이 안 됨 | 브라우저 정책. 사용자 입력(키 F) 후에만 허용됨 |
| 인쇄 시 배경이 흰색 | 인쇄 옵션 "배경 그래픽" 체크 |
