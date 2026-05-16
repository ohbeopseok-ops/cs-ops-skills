# 스킬 변경 로그

신규 스킬 추가, 수정, 삭제 이력.

---

## 2026-05-17

### 추가 — `joylab-content-team`

- **위치**: `joylab-content/skills/content-team/SKILL.md`
- **설명**: URL 1개 → 네이버/Tistory/Threads/유튜브/뉴스레터/쇼츠 6종 콘텐츠 자동 생성
- **태그**: `home-only` · `content` · `multi-platform` · `joylab`
- **트리거**: `/content [URL]`
- **환경**: 집 전용 (웹 fetch 필요, 폐쇄망 사용 불가)
- **서브에이전트 8개** (`.claude/agents/` 등록):
  - `content-planner` — URL 분석 → `brief.md` 생성
  - `content-writer-naver` — 네이버 블로그 (SEO/C-Rank)
  - `content-writer-tistory` — Tistory (AdSense 최적화)
  - `content-writer-threads` — Threads 10개 시리즈
  - `content-writer-youtube` — 유튜브 리뷰 대본
  - `content-writer-newsletter` — 뉴스레터 초안
  - `content-writer-shorts` — 쇼츠 대본 3개
  - `content-reviewer` — 전체 검수 → `review_report.md`

---

## 2026-05-16

### 초기 릴리스 — CS Ops Skills Marketplace v1.0

CS 운영 전 영역 커버 8개 플러그인, 26개 스킬 최초 등록.

| 플러그인 | 스킬 수 |
|----------|---------|
| `cs-quality-analysis` | 5 |
| `cs-coaching` | 3 |
| `cs-performance` | 4 |
| `cs-voc` | 4 |
| `cs-stt` | 3 |
| `cs-operations` | 4 |
| `cs-reporting` | 3 |
| `cs-toolkit` | 3 |
| **합계** | **26** |
