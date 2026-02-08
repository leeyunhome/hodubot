# 코딩 스타일 가이드

## 파일 관리
- 터미널에서 `python -c` 등을 통해 직접 실행한다.
- **불필요한 파일 생성 금지**: 프로젝트 구조를 깔끔하게 유지한다.

## 라이브러리 및 SDK
- **Google GenAI SDK**: `google.genai` 라이브러리 사용 (구버전 `google.generativeai` 금지).
- **모델**: `gemini-3-flash-preview` 사용.

## CLI 출력 스타일
- **초기화**: `main()` 시작 시 `os.system("clear")` 호출.
- **입력 프롬프트**: `input("호두 > ")` 형식.
- **AI 응답**: `print(f"AI: {response}")` 형식.

## 로깅
- **log.md**: 대화 내용을 Markdown 형식으로 기록 (`"a"` 모드).
- **기록 형식**: 역할(User/Gemini/Tool->Gemini/Error)과 타임스탬프 포함.
- **기록 대상**: LLM 모델과의 데이터 교환만 기록.

## 도구(Function Calling)
- **개별 파일 구조**: 각 도구는 `tools/` 폴더 내 개별 `.py` 파일로 구현.
- **파일 규약**: `SCHEMA` (FunctionDeclaration)와 `main()` 함수 필수.
- **동적 로드**: `list_files.py`를 `subprocess`로 실행 → `importlib`로 동적 로드.
- **자동 호출 비활성화**: `automatic_function_calling` 비활성화, 수동 처리.
- **연쇄 호출 지원**: `while` 루프로 여러 도구 순차 호출 처리.
- **보안**: 파일 시스템 접근 도구는 현재 디렉토리 하위 경로로만 제한.

## 도구별 특수 기능
- **save_text_file**: 디렉토리 자동 생성, 덮어쓰기 방지 (`overwrite` 파라미터).
- **play_audio**: Linux(ALSA/PulseAudio) 우선, WSL 환경은 PowerShell 브릿지 지원.
- **오디오 분석**: 재생 성공 시 오디오 파일을 모델에 전송하여 분석 가능.

## 시스템 프롬프트
- **memory/instruction.md**: 봇 성격/지시사항을 별도 파일로 관리.
- `system_instruction`으로 모델에 전달.

## 코드 구조
- **간결함 우선**: 별도 함수 분리 최소화, 메인 루프에 직접 작성.