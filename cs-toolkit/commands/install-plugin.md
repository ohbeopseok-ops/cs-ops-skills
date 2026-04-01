# /install-plugin — CS Ops Skills 플러그인 설치 가이드

환경에 맞는 플러그인 설치 방법을 안내하는 워크플로우.

## 실행 순서

1. **환경 확인** → 인터넷 연결 여부, Claude Code 버전 확인
2. **설치 방식 선택** → 마켓플레이스 / 직접 복사 중 안내
3. **plugin-marketplace** → 단계별 설치 명령어 제공
4. **설치 검증** → 설치된 플러그인 목록 및 커맨드 동작 확인

## 사용법

```
/install-plugin                          ← 전체 설치 가이드
/install-plugin cs-quality-analysis      ← 특정 플러그인 설치 안내
/install-plugin --offline                ← 폐쇄망 환경 설치 안내
/install-plugin --all                    ← 전체 플러그인 일괄 설치
```

## 출력

- 환경별 설치 명령어 (마켓플레이스 / 직접 복사)
- 설치 후 사용 가능한 커맨드 목록
- 문제 발생 시 트러블슈팅 가이드

## 다음 커맨드 제안

설치 완료 후: `/evaluate` → 상담 품질 평가 바로 시작  
보고서 필요: `/weekly-report` → 주간 보고서 작성  
코칭 시작: `/coach` → 상담사 코칭 피드백 생성
