---
name: html-tool-spec
description: 폐쇄망 환경 HTML/JavaScript 도구의 요구사항 명세서 작성. 도구 목적, 기능 명세, UI 구조, 데이터 처리 방식, 폐쇄망 제약 사항을 포함한 개발 사양서 생성. 신규 도구 기획, 기존 도구 개선 요청, 개발 전 요구사항 정리에 사용.
---

# HTML 도구 요구사항 명세서 (HTML Tool Spec)

LG U+ 폐쇄망 환경에 최적화된 standalone HTML/JS 도구 개발 사양서 생성 프레임워크.

## 폐쇄망 환경 제약 사항 (항상 적용)

```
[필수 제약]
- 외부 CDN 불가 → 모든 라이브러리 인라인 포함
- 서버 통신 불가 → 브라우저 내 완결 처리
- localStorage 허용 → 세션 내 데이터 유지
- 파일 저장 → Blob/download 방식
- 인쇄 지원 → @media print CSS 포함

[권장 사양]
- 단일 HTML 파일 (CSS/JS 내장)
- 반응형 UI (1280px 기준 최적화)
- 한국어 폰트 (내장 또는 시스템 폰트)
- 브라우저: Chrome 최신 버전 기준
```

## 명세서 출력 형식

ALWAYS use this exact template:

```
## HTML 도구 요구사항 명세서

**도구명:** [도구명]  
**버전:** v1.0  
**작성일:** [날짜]  
**작성자:** [이름]  
**우선순위:** [긴급 / 일반 / 장기]

---

### 1. 도구 개요

**목적:** [한 문장 목적 설명]

**주요 사용자:**
- 주 사용자: [역할]
- 보조 사용자: [역할]

**사용 빈도:** [일 N회 / 주 N회]  
**현재 처리 방법:** [현재 어떻게 하고 있는가]  
**기대 효과:** [시간 절약 / 오류 감소 / 정확도 향상]

---

### 2. 핵심 기능 명세

**기능 1: [기능명]**
- 입력: [입력 데이터 형태]
- 처리: [처리 로직]
- 출력: [출력 형태]
- 우선순위: [Must / Should / Nice-to-have]

**기능 2: [기능명]** (동일 구조)

**기능 3: [기능명]** (동일 구조)

---

### 3. UI 구조

```
[화면 레이아웃 텍스트 와이어프레임]

┌─────────────────────────────────────┐
│ [헤더: 도구명 + 버전]               │
├─────────────────────────────────────┤
│ [입력 영역]                         │
│  [입력 필드1]  [입력 필드2]         │
│  [파일 업로드 / 붙여넣기 영역]      │
├─────────────────────────────────────┤
│ [실행 버튼]  [초기화 버튼]          │
├─────────────────────────────────────┤
│ [결과 출력 영역]                    │
│  [테이블 / 차트 / 텍스트]           │
├─────────────────────────────────────┤
│ [저장/내보내기] [인쇄]              │
└─────────────────────────────────────┘
```

---

### 4. 데이터 처리

**입력 데이터 형식:**
- [CSV / Excel / 직접 입력 / 붙여넣기]
- 필수 컬럼: [컬럼명1, 컬럼명2, ...]
- 선택 컬럼: [컬럼명]

**처리 로직:**
1. [처리 단계1]
2. [처리 단계2]
3. [처리 단계3]

**출력 형식:**
- 화면: [테이블 / 차트 / 요약 카드]
- 저장: [CSV / Excel / PDF / 인쇄]

---

### 5. 예외 처리 / 유효성 검사

| 케이스 | 처리 방법 | 사용자 메시지 |
|--------|-----------|---------------|
| 필수 입력 누락 | 경고 표시 | "○○를 입력해주세요" |
| 잘못된 형식 | 필드 하이라이트 | "형식을 확인해주세요" |
| 데이터 없음 | 빈 결과 안내 | "해당 조건의 데이터가 없습니다" |

---

### 6. 폐쇄망 제약 사항

- [ ] 외부 라이브러리 불필요 (또는 인라인 내장 필요)
- [ ] 단일 HTML 파일로 완결
- [ ] 저장 기능: Blob 다운로드 방식
- [ ] 개인정보 표시 주의: [마스킹 필요 여부]

---

### 7. 개발 우선순위

**Must Have (MVP):**
- [기능1]
- [기능2]

**Should Have (v1.1):**
- [기능]

**Nice to Have (향후):**
- [기능]

---

### 8. 다이얼로그 모션 (Dialog Motion)

HTML 도구에 모달/다이얼로그를 사용할 때 아래 CSS + JS 패턴을 적용한다.  
외부 라이브러리 불필요 — 인라인 CSS/JS로 완결된다.

**CSS (전역 한 번만 추가)**

```css
/* Dialog motion — no external deps */
:root {
  --modal-open-dur: 250ms;
  --modal-close-dur: 150ms;
  --modal-scale: 0.96;
  --modal-scale-close: 0.96;
  --modal-ease: cubic-bezier(0.22, 1, 0.36, 1);
}

/* Overlay */
.t-modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  opacity: 0;
  transition: opacity var(--modal-close-dur) ease;
}
.t-modal-overlay[data-open] {
  opacity: 1;
  transition: opacity var(--modal-open-dur) ease;
}

/* Dialog box */
.t-modal {
  transform: scale(var(--modal-scale));
  opacity: 0;
  transition:
    transform var(--modal-close-dur) var(--modal-ease),
    opacity    var(--modal-close-dur) ease;
}
.t-modal-overlay[data-open] .t-modal {
  transform: scale(1);
  opacity: 1;
  transition:
    transform var(--modal-open-dur) var(--modal-ease),
    opacity    var(--modal-open-dur) ease;
}

/* Closing state — scale back down, then hide */
.t-modal-overlay.is-closing .t-modal {
  transform: scale(var(--modal-scale-close));
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .t-modal, .t-modal-overlay {
    transition: none !important;
  }
}
```

**HTML 구조**

```html
<div class="t-modal-overlay" id="myModal" role="dialog" aria-modal="true" hidden>
  <div class="t-modal">
    <h2>제목</h2>
    <p>내용</p>
    <button onclick="closeModal('myModal')">닫기</button>
  </div>
</div>
```

**JS 오케스트레이션**

```js
function openModal(id) {
  const overlay = document.getElementById(id);
  overlay.hidden = false;
  // reflow → animate in
  void overlay.offsetWidth;
  overlay.setAttribute('data-open', '');
}

function closeModal(id) {
  const overlay = document.getElementById(id);
  const dur = parseFloat(
    getComputedStyle(overlay).getPropertyValue('--modal-close-dur')
  ) * 1000;
  overlay.classList.add('is-closing');
  overlay.removeAttribute('data-open');
  setTimeout(() => {
    overlay.classList.remove('is-closing');
    overlay.hidden = true;
  }, dur);
}
```

**주의사항**

- `.is-closing` 제거를 `setTimeout` 없이 즉시 하면 다음 열기 시 닫힘 scale에서 시작함
- 애니메이션 재생 보장을 위해 `hidden` 제거 후 `void el.offsetWidth` reflow 필수
- `prefers-reduced-motion` 블록은 항상 포함 (접근성 감사 통과 조건)

---

### 9. 참고 자료

- 참고 도구: [기존 유사 도구]
- 관련 문서: [관련 자료]
- 담당자: [이름] / [연락처]
```

## 사용 예시

- `STT 기반 품질 자동 분석 도구 명세서를 작성해줘`
- `고령자 상담 점검 도구 요구사항을 정리해줘`
- `기존 KPI 대시보드 개선 요청 사양서를 만들어줘`
