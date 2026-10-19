# /create-skill — 새 SKILL.md 작성/개선 및 트리거링 최적화

`skill-creator` 스킬을 사용해 cs-ops-skills의 SKILL.md를 만들거나 개선하는 체인 워크플로우.
[anthropics/skills](https://github.com/anthropics/skills)의 `skill-creator`를 포팅 (Apache 2.0, 원문 변경 없음).

## 실행 순서

1. **의도 파악** — 신규 작성인지 기존 스킬 개선인지, 트리거 문구·입출력 형식 확인
2. **SKILL.md 초안** — name/description/본문 작성 (description에 트리거 조건을 구체적으로 명시)
3. **테스트 케이스 실행** — 실제 사용자 발화를 가정한 프롬프트로 with-skill / baseline 비교
4. **사용자 리뷰** — `eval-viewer/generate_review.py`로 결과 확인 후 피드백 수집
5. **개선 반복** — 피드백 기반 수정, 만족할 때까지 반복
6. **트리거링 최적화 (선택)** — description이 다른 스킬과 충돌하거나 undertrigger될 때 `scripts/run_loop.py`로 자동 최적화

## 사용법

```
/create-skill new "[새 스킬 설명]"
/create-skill improve [기존 스킬 경로] "[개선 요청 내용]"
/create-skill optimize-trigger [기존 스킬 경로]  ← description 트리거링만 최적화
```

## 출력

- 완성된 SKILL.md (및 필요 시 scripts/references/assets)
- 테스트 케이스 실행 결과 + 사용자 리뷰 요약
- (트리거링 최적화 시) 개선 전/후 description과 점수

## 검증 원칙 (honest-agent)

"이 스킬이 더 잘 작동합니다"라고 단정하기 전에 반드시 eval 결과 또는 사용자 리뷰로 근거를 확인한다. 테스트 없이 개선을 추측·단정하지 않는다.

## 다음 커맨드 제안

새 스킬이 CS 품질/코칭/VOC 도메인이면: 해당 플러그인 폴더(`cs-quality-analysis`, `cs-coaching` 등)에 배치 후 README.md 스킬 목록 갱신 권장.
