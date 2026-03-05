import cv2
import numpy as np

def remove_bg_magic_wand(input_path, output_path, tolerance=15):
    # 1. 원본 이미지 불러오기 (기본적으로 3채널 BGR로 불러옴)
    img = cv2.imread(input_path)
    if img is None:
        print("이미지를 찾을 수 없습니다. 파일명과 확장자를 확인해주세요.")
        return

    h, w = img.shape[:2]
    
    # 2. 배경 영역을 기록할 마스크 생성 
    # (OpenCV floodFill 규칙상 마스크는 원본 이미지보다 가로세로 2픽셀씩 커야 함)
    mask = np.zeros((h+2, w+2), np.uint8)

    # 3. 오차 범위 설정 (JPG 열화나 희미한 선을 무시하기 위함)
    diff = (tolerance, tolerance, tolerance)
    
    # 4. Flood Fill 실행 (마스크만 생성하는 옵션 적용)
    # 4: 상하좌우 연결성 / (255 << 8): 배경을 255(흰색)로 칠함 / FLOODFILL_MASK_ONLY: 원본 훼손 없이 마스크만 업데이트
    flags = 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
    
    # (0,0) 좌표(보통 가장자리 배경)부터 시작하여 비슷한 색상을 찾아 mask에 기록
    cv2.floodFill(img, mask, (0,0), (0,0,0), diff, diff, flags)
    
    # 5. 이제 원본 이미지에 알파 채널(투명도) 추가 (BGR -> BGRA)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 6. 마스크에서 255로 칠해진 부분(배경)의 알파 채널을 0(투명)으로 변경
    # mask가 원본보다 2픽셀 더 크므로 [1:-1, 1:-1]로 테두리를 잘라내어 크기를 맞춥니다.
    rgba[mask[1:-1, 1:-1] == 255, 3] = 0
    
    # 7. 결과 저장
    cv2.imwrite(output_path, rgba)
    print(f"변환 완료: {output_path}")

# 실행
remove_bg_magic_wand("character sheet test.png", "character sheet test_bg_removed.png", tolerance=20)