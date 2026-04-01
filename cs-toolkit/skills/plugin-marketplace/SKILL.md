---
name: plugin-marketplace
description: Claude Code 플러그인 마켓플레이스 관리. GitHub 저장소를 마켓으로 등록하고, 개별 플러그인을 설치/제거하는 방법 안내. cs-ops-skills 설치, 업데이트, 플러그인 목록 확인에 사용.
---

# 플러그인 마켓플레이스 관리 (Plugin Marketplace)

Claude Code 플러그인 마켓플레이스를 통해 GitHub 저장소 기반 플러그인을 설치·관리하는 가이드.

## 마켓플레이스 등록

GitHub 저장소를 마켓으로 추가:

```bash
/plugin marketplace add ohbeopseok-ops/cs-ops-skills
```

등록 후 마켓에서 개별 플러그인 설치 가능.

## 플러그인 설치

### 마켓에서 설치

```bash
# 단일 플러그인
/plugin install cs-quality-analysis@cs-ops-skills
/plugin install cs-coaching@cs-ops-skills
/plugin install cs-performance@cs-ops-skills
/plugin install cs-voc@cs-ops-skills
/plugin install cs-stt@cs-ops-skills
/plugin install cs-operations@cs-ops-skills
/plugin install cs-reporting@cs-ops-skills
/plugin install cs-toolkit@cs-ops-skills
```

### 직접 복사 (오프라인/폐쇄망 환경)

```bash
# 저장소 클론 후
git clone https://github.com/ohbeopseok-ops/cs-ops-skills.git

# 개별 플러그인 스킬 복사
cp -r cs-ops-skills/cs-quality-analysis/skills/* ~/.claude/skills/
cp -r cs-ops-skills/cs-coaching/skills/* ~/.claude/skills/
cp -r cs-ops-skills/cs-reporting/skills/* ~/.claude/skills/

# 커맨드 복사
cp -r cs-ops-skills/cs-quality-analysis/commands/* ~/.claude/commands/
cp -r cs-ops-skills/cs-reporting/commands/* ~/.claude/commands/
```

## 설치된 마켓 및 플러그인 확인

```bash
# 등록된 마켓 목록
/plugin marketplace list

# 설치된 플러그인 목록
/plugin list

# 특정 플러그인 상세 정보
/plugin info cs-quality-analysis
```

## 플러그인 업데이트 및 제거

```bash
# 전체 업데이트
/plugin update --all

# 단일 업데이트
/plugin update cs-ops-skills

# 제거
/plugin remove cs-quality-analysis@cs-ops-skills
```

## cs-ops-skills 플러그인 목록

| 플러그인 | 설명 | 주요 커맨드 |
|----------|------|-------------|
| `cs-quality-analysis` | 상담 품질 평가, AutoQA 분석 | `/evaluate`, `/autoqa-report` |
| `cs-coaching` | 코칭 피드백, 개선 계획 | `/coach`, `/plan-improvement` |
| `cs-performance` | KPI, T-NPS, 벤치마킹 | `/analyze-kpi`, `/predict-tnps` |
| `cs-voc` | VOC 분류, 불만 원인 분석 | `/analyze-voc`, `/analyze-complaints` |
| `cs-stt` | STT 분석, 개인정보 마스킹 | `/analyze-call`, `/mask-pii` |
| `cs-operations` | 인력 배치, OKR, 회의록 | `/plan-staffing`, `/plan-okr` |
| `cs-reporting` | 주간/월간 보고서, 경영진 요약 | `/weekly-report`, `/monthly-report` |
| `cs-toolkit` | HTML 명세, 테스트 데이터, 교정 | `/spec-tool`, `/mock-data` |

## 사용 예시

- `cs-ops-skills 마켓을 추가하고 싶어`
- `cs-quality-analysis 플러그인을 설치해줘`
- `설치된 플러그인 목록을 보여줘`
- `폐쇄망 환경에서 cs-reporting만 설치하는 방법을 알려줘`
