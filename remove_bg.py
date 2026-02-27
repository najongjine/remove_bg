from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    try:
        # 1. 원본 이미지 불러오기
        input_image = Image.open(input_path)
        
        # 2. 배경 제거 실행
        output_image = remove(input_image)
        
        # 3. 투명 배경을 포함하여 PNG로 결과 저장
        output_image.save(output_path)
        print(f"성공적으로 배경이 제거되었습니다! 저장된 경로: {output_path}")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

# === 사용 예시 ===
# 본인의 이미지 파일 이름으로 경로를 수정하세요.
input_file = r'my_photo.jpg'  # 원본 이미지 경로
output_file = r'result.png'   # 저장할 이미지 경로 (반드시 png)

remove_background(input_file, output_file)