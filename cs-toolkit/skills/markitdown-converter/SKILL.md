---
name: markitdown-converter
description: PDF, Excel, Word, PowerPoint, 오디오 등 다양한 파일을 마크다운으로 변환. markitdown 라이브러리 활용. QA 평가표, VOC 데이터, KPI 보고서, 회의록, 상담 녹취 등 CS 운영 문서를 AI 분석 가능한 형태로 변환 후 적합한 CS Ops 스킬과 연계.
---

# 문서-마크다운 변환 (Markitdown Converter)

[markitdown](https://github.com/microsoft/markitdown) 라이브러리를 활용한 CS 운영 문서 변환 프레임워크.  
PDF, Excel, Word, PPT, 오디오 파일을 마크다운으로 변환하여 CS Ops Skills 분석 파이프라인에 투입.

## 설치

```bash
pip install 'markitdown[all]'
```

## 지원 파일 형식

| 형식 | 확장자 | CS 활용 예시 |
|------|--------|-------------|
| PDF | `.pdf` | QA 평가 리포트, 운영 매뉴얼, 월간 보고서 |
| Excel | `.xlsx`, `.xls` | KPI 데이터, VOC 목록, 상담사 성과표 |
| Word | `.docx` | 회의록, 코칭 기록, 프로세스 문서 |
| PowerPoint | `.pptx` | 팀 보고 자료, 경영진 보고서 |
| 오디오 | `.mp3`, `.wav`, `.m4a` | 상담 녹음 파일 (STT 변환) |
| 이미지 | `.jpg`, `.png` | QA 스크린샷, 화면 캡처 |
| CSV | `.csv` | 원시 KPI/VOC 데이터 |
| HTML | `.html` | 웹 기반 보고서, 대시보드 캡처 |

## 변환 방법

### CLI (단일 파일)

```bash
# 기본 변환
markitdown 파일경로.xlsx > output.md

# 오디오 STT 변환 (OpenAI API 키 필요)
OPENAI_API_KEY=sk-... markitdown 녹취파일.mp3 > stt_output.md
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("파일경로.xlsx")
print(result.text_content)
```

### 오디오 STT (OpenAI 연동)

```python
from markitdown import MarkItDown
import openai

client = openai.OpenAI(api_key="sk-...")
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("상담녹음.mp3")
print(result.text_content)
```

## CS 문서 유형별 변환 → 스킬 연계

ALWAYS use this routing table:

```
[QA 평가 문서]
파일: QA평가표.xlsx, QA리포트.pdf
변환 후 스킬: qa-scoring → quality-trend → coaching-feedback
커맨드: /evaluate

[VOC 데이터]
파일: VOC목록.xlsx, 불만접수.csv
변환 후 스킬: voc-categorization → complaint-root-cause → sentiment-analysis
커맨드: /analyze-voc

[KPI 보고서]
파일: KPI현황.xlsx, 성과보고서.pdf
변환 후 스킬: kpi-analysis → tnps-prediction → target-setting
커맨드: /analyze-kpi

[STT / 상담 녹취]
파일: 상담녹음.mp3, 통화녹취.wav
변환 후 스킬: pii-detection → conversation-analysis → script-compliance
커맨드: /analyze-call

[회의록 / 운영 문서]
파일: 팀회의.docx, 운영계획.pdf
변환 후 스킬: meeting-notes → process-improvement → okr-cs
커맨드: /plan-okr

[경영진 보고 자료]
파일: 월간보고.pptx, 임원보고.pdf
변환 후 스킬: executive-summary → monthly-report
커맨드: /exec-summary
```

## 변환 품질 점검 체크리스트

```
[ ] 테이블 구조가 올바르게 변환됨 (컬럼명, 데이터 정렬)
[ ] 한국어 텍스트 인코딩 정상 (깨짐 없음)
[ ] 수치 데이터 단위 보존 (%, 점, 건, 초)
[ ] 날짜 형식 일관성 유지
[ ] 개인정보 포함 여부 확인 → pii-detection 실행 권장
[ ] 페이지/시트 분리 구조 확인
```

## 일괄 변환 (배치 처리)

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()
input_dir = Path("cs_documents/")
output_dir = Path("converted_md/")
output_dir.mkdir(exist_ok=True)

for file in input_dir.glob("*"):
    if file.suffix in [".pdf", ".xlsx", ".docx", ".pptx", ".csv"]:
        result = md.convert(str(file))
        out_path = output_dir / f"{file.stem}.md"
        out_path.write_text(result.text_content, encoding="utf-8")
        print(f"변환 완료: {file.name} → {out_path.name}")
```

## 사용 예시

- `QA평가표.xlsx 파일을 마크다운으로 변환하고 품질 분석해줘`
- `이번 달 VOC_목록.xlsx를 변환해서 VOC 분석 파이프라인에 넣어줘`
- `상담녹취.mp3를 STT 변환 후 전체 분석해줘`
- `월간보고.pdf를 변환해서 경영진 요약 보고서를 만들어줘`
- `KPI현황.xlsx를 변환하고 T-NPS 예측까지 해줘`
