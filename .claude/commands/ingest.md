# /ingest 프롬프트 템플릿

## ETF 흐름 인제스트
```
raw/invest/etf-flows/[날짜]-[파일명].md 읽고
wiki/invest/etf-flows/[YYYY-WW].md 생성해줘.
wiki/invest/themes/ 관련 섹터 페이지도 업데이트하고
index.md, log.md 기록해줘.
```

## 종목 분석 인제스트
```
raw/invest/tickers/[날짜]-[파일명].html 읽고
wiki/invest/tickers/[티커].md 생성 또는 업데이트해줘.
LEGEND FUND 페르소나 판단도 wiki/invest/legend-fund/ 에 기록하고
이전 분석과 입장 변화 있으면 flagging해줘.
index.md, log.md 기록해줘.
```

## AI 도구 트렌드 인제스트
```
raw/ai-tools/trends/[날짜]-[파일명].md 읽고
wiki/ai-tools/tools/[도구명].md 업데이트해줘.
커뮤니티 온도 이력 테이블 추가하고
wiki/ai-tools/trends/ 월별 합성 업데이트.
index.md, log.md 기록해줘.
```

## SKILL.md 인제스트 (cs-ops-skills)
```
skills/user/[스킬명]/SKILL.md 읽고
wiki/skills/[스킬명].md 생성해줘.
연관 스킬 크로스링크 추가하고
wiki/domains/[도메인].md 업데이트.
index.md, log.md 기록해줘.
```

## Lint 실행
```
wiki/ 전체 헬스체크해줘.
고아 페이지, 모순, stale 항목, 미생성 페이지 리포트.
```
