import os
import sys

# 리소스 파일 경로를 동적으로 찾는 함수
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# TMX 파일 경로 설정 예시
tmx_path = resource_path("Assets/worlds/tmx/W11.tmx")
image_path = resource_path("Assets/images")
# 이제 tmx_path를 사용하여 TMX 파일을 로드합니다.
