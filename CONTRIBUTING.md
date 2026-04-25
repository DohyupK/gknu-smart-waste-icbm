# CONTRIBUTING

이 문서는 EcoSort-AIoT 팀원 4명이 동일한 방식으로 개발하고 리뷰하기 위한 협업 기준입니다.

## 1) 목적 / 적용 범위

- 이 규칙은 본 저장소의 모든 코드 변경(`src/`, `tests/`, 문서 포함)에 적용합니다.
- 모든 변경은 아래 순서를 따라야 합니다: 테스트 통과 -> PR 생성 -> 리뷰 승인 -> 머지.

## 2) Git Flow 규칙

- 기본 브랜치는 `main`입니다.
- 기능 개발은 반드시 `feature/<name>` 브랜치에서 진행합니다.
- `<name>`은 영문 소문자 `kebab-case`를 권장합니다.
- 예시: `feature/add-local-analytics`
- 1 기능 = 1 브랜치 원칙을 지킵니다.
- `main`에 직접 커밋하는 것은 금지합니다.

## 3) Test-First Policy

- 코드 수정 시 PR 생성 전에 `tests/` 단위 테스트를 모두 통과해야 합니다.
- 테스트 실행 예시:

```bash
python -m pytest tests/
```

- **테스트 실패 상태에서는 PR을 올릴 수 없습니다.**

## 4) Commit Message Convention

- 형식: `<type>: <summary>`
- 허용 접두어:
  - `feat:` 새로운 기능
  - `fix:` 버그 수정
  - `docs:` 문서 수정
  - `test:` 테스트 추가/수정
- 커밋 제목은 영문을 권장합니다.

좋은 예시:
- `feat: add waste label validation`
- `fix: handle empty detection result`

나쁜 예시:
- `update code`
- `fix stuff`

## 5) Code Review & Merge Rule

- PR은 작성자 본인을 제외한 최소 1명 이상의 승인을 받아야 머지할 수 있습니다.
- 승인 전 self-merge는 금지합니다.
- 리뷰 요청사항이 있으면 반영 후 재리뷰를 요청해야 합니다.

## 6) PR 제출 체크리스트

- [ ] `tests/` 단위 테스트를 통과했다.
- [ ] 변경 내용을 PR 본문에 요약했다.
- [ ] 리뷰어가 봐야 할 핵심 포인트를 작성했다.
- [ ] 관련 이슈/작업 항목이 있으면 링크했다.
