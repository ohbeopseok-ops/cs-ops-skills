# /convert-doc — 문서 변환 후 CS 분석 파이프라인 실행

**실행:** markitdown-converter → [문서 유형별 자동 라우팅]

**사용법:**
```
/convert-doc [파일경로 또는 변환된 텍스트]
/convert-doc qa [QA 평가 문서]       ← qa-scoring → quality-trend
/convert-doc voc [VOC 데이터 파일]   ← voc-categorization → complaint-root-cause
/convert-doc kpi [KPI 보고서]        ← kpi-analysis → tnps-prediction
/convert-doc stt [상담 녹취 파일]    ← pii-detection → conversation-analysis
/convert-doc report [보고 자료]      ← executive-summary → monthly-report
```

**다음 커맨드 제안:** `/evaluate` → `/analyze-voc` → `/analyze-kpi` → `/analyze-call`
