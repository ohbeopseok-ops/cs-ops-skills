# CS Ops Skills — 인제스트 기록

> skills/user/ 및 주요 파일 변경 이력.

---

## 2026-04-05

### 초기 인제스트 (v1.0)

**브랜치:** `claude/ingest-user-skills-SYKB2`  
**커밋:** `502d90a`  
**작업자:** Claude (claude/ingest-user-skills-SYKB2 세션)

#### 생성 파일

| 파일 | 설명 |
|------|------|
| `CLAUDE.md` | Claude Code용 프로젝트 가이드. 디렉토리 위키 구조, 플러그인·스킬·커맨드 개념, 스킬 추가 방법, 코딩 컨벤션 문서화. |
| `skills/user/` | 8개 플러그인의 29개 SKILL.md를 flat index로 집약. |

#### 인제스트 스킬 목록 (29개)

| 스킬명 | 소속 플러그인 | 파일 |
|--------|-------------|------|
| `qa-scoring` | cs-quality-analysis | `skills/user/qa-scoring.md` |
| `autoqa-analysis` | cs-quality-analysis | `skills/user/autoqa-analysis.md` |
| `elderly-customer-qa` | cs-quality-analysis | `skills/user/elderly-customer-qa.md` |
| `compliance-check` | cs-quality-analysis | `skills/user/compliance-check.md` |
| `quality-trend` | cs-quality-analysis | `skills/user/quality-trend.md` |
| `coaching-feedback` | cs-coaching | `skills/user/coaching-feedback.md` |
| `improvement-plan` | cs-coaching | `skills/user/improvement-plan.md` |
| `coaching-script` | cs-coaching | `skills/user/coaching-script.md` |
| `kpi-analysis` | cs-performance | `skills/user/kpi-analysis.md` |
| `tnps-prediction` | cs-performance | `skills/user/tnps-prediction.md` |
| `agent-benchmarking` | cs-performance | `skills/user/agent-benchmarking.md` |
| `target-setting` | cs-performance | `skills/user/target-setting.md` |
| `voc-categorization` | cs-voc | `skills/user/voc-categorization.md` |
| `complaint-root-cause` | cs-voc | `skills/user/complaint-root-cause.md` |
| `sentiment-analysis` | cs-voc | `skills/user/sentiment-analysis.md` |
| `nudge-analysis` | cs-voc | `skills/user/nudge-analysis.md` |
| `conversation-analysis` | cs-stt | `skills/user/conversation-analysis.md` |
| `script-compliance` | cs-stt | `skills/user/script-compliance.md` |
| `pii-detection` | cs-stt | `skills/user/pii-detection.md` |
| `staffing-plan` | cs-operations | `skills/user/staffing-plan.md` |
| `process-improvement` | cs-operations | `skills/user/process-improvement.md` |
| `meeting-notes` | cs-operations | `skills/user/meeting-notes.md` |
| `okr-cs` | cs-operations | `skills/user/okr-cs.md` |
| `weekly-report` | cs-reporting | `skills/user/weekly-report.md` |
| `monthly-report` | cs-reporting | `skills/user/monthly-report.md` |
| `executive-summary` | cs-reporting | `skills/user/executive-summary.md` |
| `html-tool-spec` | cs-toolkit | `skills/user/html-tool-spec.md` |
| `data-mock` | cs-toolkit | `skills/user/data-mock.md` |
| `ko-grammar-check` | cs-toolkit | `skills/user/ko-grammar-check.md` |

#### 소스 기준

각 스킬 파일은 `<plugin>/skills/<skill-name>/SKILL.md` 원본을 그대로 복사.  
내용 변경 없음. 경로만 `skills/user/<skill-name>.md`로 평탄화.

---

## 변경 이력 형식 (후속 작업용)

```
## YYYY-MM-DD

### 작업 제목

**브랜치:** `<branch>`
**커밋:** `<sha>`
**작업자:** <이름/세션>

#### 추가
- `skills/user/<skill>.md` — <사유>

#### 수정
- `skills/user/<skill>.md` — <변경 내용>

#### 삭제
- `skills/user/<skill>.md` — <사유>
```
