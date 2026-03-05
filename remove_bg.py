import cv2
import numpy as np
import glob
import os

def remove_sprite_background(image_path, tolerance=15):
    # 1. 이미지 읽기
    img = cv2.imread(image_path)
    if img is None:
        return

    h, w = img.shape[:2]
    
    # 2. 배경 마스크 생성 (크기는 원본보다 +2 픽셀)
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # 오차 범위 설정 (JPG 열화나 희미한 찌꺼기 무시)
    diff = (tolerance, tolerance, tolerance)
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY

    # 3. 핵심: 이미지의 네 모서리 좌표 설정
    # (어떤 스프라이트 시트든 모서리는 보통 빈 공간, 즉 배경임)
    corners = [
        (0, 0),             # 좌측 상단
        (w - 1, 0),         # 우측 상단
        (0, h - 1),         # 좌측 하단
        (w - 1, h - 1)      # 우측 하단
    ]

    # 4. 네 모서리에서 각각 마법봉(Flood Fill)을 쏴서 연결된 배경을 마스크에 기록
    for pt in corners:
        cv2.floodFill(img, mask, pt, (0, 0, 0), diff, diff, flags)

    # 5. 알파 채널 추가 후 마스크 영역 투명화
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    rgba[mask[1:-1, 1:-1] == 255, 3] = 0

    # 6. 결과물 저장 (원본 파일명_transparent.png)
    filename, ext = os.path.splitext(image_path)
    output_path = f"{filename}_transparent.png"
    cv2.imwrite(output_path, rgba)
    print(f"처리 완료: {output_path}")

def process_all_sprites_in_folder(folder_path, tolerance=15):
    print(f"--- '{folder_path}' 폴더 내의 스프라이트 처리를 시작합니다 ---")
    
    # 폴더 내의 모든 png, jpg 파일 찾기
    search_pattern = os.path.join(folder_path, "*.[pj][np][g]")
    target_files = glob.glob(search_pattern)
    
    if not target_files:
        print("처리할 이미지가 없습니다.")
        return

    for file_path in target_files:
        # 이미 투명화된 파일은 건너뛰기
        if "_transparent" in file_path:
            continue
        remove_sprite_background(file_path, tolerance)
        
    print("--- 모든 작업이 완료되었습니다 ---")

# ==========================================
# 실행 방법
# ==========================================
# 스크립트가 있는 폴더에 'sprites' 라는 폴더를 만들고 이미지들을 몰아넣은 뒤 실행하세요.
# tolerance 값을 올리면 더 넓은 범위의 비슷한 색이 지워집니다. (기본 15)

target_folder = "./" # 리소스가 있는 폴더 경로
process_all_sprites_in_folder(target_folder, tolerance=20)