from google.genai import types
import os
import subprocess
import shutil
import time

SCHEMA = types.FunctionDeclaration(
    name="play_audio",
    description="주어진 경로의 오디오 파일(mp3 등)을 재생합니다. (Linux/WSL 지원)",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "file_path": types.Schema(type="STRING", description="재생할 오디오 파일의 경로 (예: music.mp3)"),
        },
        required=["file_path"],
    ),
)

def play_with_pygame(file_path):
    """
    Linux Native 방식 (pygame)으로 재생 시도
    성공 시 True, 실패 시 False 반환
    """
    try:
        # pygame 모듈이 없으면 실패 처리
        import pygame
    except ImportError:
        return False, "pygame 모듈이 설치되지 않았습니다."

    try:
        # 믹서 초기화 시도
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        pygame.mixer.music.load(file_path)
        print(f"Linux(ALSA/PulseAudio) 재생 시작: {file_path}")
        pygame.mixer.music.play()

        # 재생이 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            # CPU 점유율 낮추기 위해 sleep 추가
            time.sleep(0.1)
            
        return True, "재생 완료 (Linux Native)"

    except Exception as e:
        return False, f"Linux 재생 실패: {e}"
    finally:
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
        except:
            pass

def play_with_wsl_bridge(file_path):
    """
    WSL -> Windows Bridge 방식으로 재생 시도
    """
    abs_path = os.path.abspath(file_path)

    # wslpath와 powershell.exe 확인
    if not (shutil.which("wslpath") and shutil.which("powershell.exe")):
        return False, "WSL 환경이 아니거나 필수 도구(wslpath, powershell.exe)가 없습니다."

    try:
        # WSL 경로 -> Windows 경로 변환
        result = subprocess.run(['wslpath', '-w', abs_path], capture_output=True, text=True, check=True)
        windows_path = result.stdout.strip()
        
        print(f"WSL 환경 감지됨. Windows 플레이어로 재생 시도: {windows_path}")
        
        # PowerShell을 통해 기본 미디어 플레이어 실행 (비동기로 실행되지 않도록 wait 할 수도 있음)
        # 여기서는 Start-Process로 비동기 실행 (플레이어 창이 뜸)
        subprocess.run(["powershell.exe", "-Command", f"Start-Process '{windows_path}'"], check=True)
        return True, "Windows 기본 플레이어에서 재생을 시작했습니다."
        
    except Exception as e:
        return False, f"WSL Bridge 재생 실패: {e}"

def main(file_path: str) -> str:
    """오디오 파일을 재생합니다."""
    
    # 1. 파일 존재 확인
    if not os.path.exists(file_path):
        return f"오류: 파일을 찾을 수 없습니다 -> {file_path}"
    
    # 2. Linux Native (pygame) 시도 (우선순위 높음)
    # PulseAudio 환경 변수가 설정되어 있거나, 리눅스 환경인 경우 우선 시도
    print("시스템: Linux Native(pygame) 재생을 시도합니다...")
    success, message = play_with_pygame(file_path)
    
    if success:
        return f'{{\n  "status": "success",\n  "message": "{message}",\n  "file_path": "{file_path}"\n}}'
    else:
        print(f"시스템: Linux Native 재생 실패 ({message})")

    # 3. 실패 시 Windows Bridge (WSL) 시도
    print("시스템: Windows Bridge(WSL) 재생을 시도합니다...")
    success, message = play_with_wsl_bridge(file_path)
    
    if success:
        return f'{{\n  "status": "success",\n  "message": "{message}",\n  "file_path": "{file_path}"\n}}'
    else:
        return f'{{\n  "status": "error",\n  "message": "재생 실패: 모든 방법이 실패했습니다. ({message})",\n  "file_path": null\n}}'

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(main(sys.argv[1]))
    else:
        print(SCHEMA.model_dump_json(indent=2))
