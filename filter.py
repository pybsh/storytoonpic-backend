import cv2
import numpy as np
from matplotlib import pyplot as plt

# 이미지 불러오기
image = cv2.imread('./photo/test/1.jpg')

# 크레용 필터 적용 함수
def apply_crayon_effect(image):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # GaussianBlur를 사용하여 이미지를 흐리게 처리
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    # 흐리게 한 이미지에서 원본 이미지를 빼서 윤곽선을 강조
    sketch = cv2.divide(gray, blurred, scale=256.0)

    # 컬러 이미지를 hsv로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 채도를 높여서 크레용의 생생한 색상 효과를 얻음
    hsv[:, :, 1] = cv2.add(hsv[:, :, 1], 100)

    # 변환된 hsv 이미지를 다시 BGR로 변환
    vibrant_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 텍스처를 추가하여 크레용 느낌을 더함
    noise = np.random.normal(0, 25, vibrant_image.shape).astype(np.uint8)
    crayon_image = cv2.add(vibrant_image, noise)

    # 최종적으로 윤곽선을 합성
    final_image = cv2.bitwise_and(crayon_image, crayon_image, mask=sketch)

    return final_image

# 크레용 효과 적용
crayon_image = apply_crayon_effect(image)

# 결과를 출력
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(crayon_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
