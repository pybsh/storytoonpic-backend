import os

def resize_image(img, target_size=1000):
    """
    PIL 이미지 객체를 비율에 맞게 target_size로 축소하고, 이미 크기가 작은 경우 그대로 반환합니다.

    Args:
        img (PIL.Image.Image): 입력 이미지 객체.
        target_size (int, optional): 기준 축소 크기 (기본값 1000 픽셀).

    Returns:
        PIL.Image.Image: 축소된 PIL 이미지 객체.
    """
    try:
        # 이미지의 가로 및 세로 길이 가져오기
        original_width, original_height = img.size

        # 이미지의 가로와 세로 중 큰 값을 기준으로 크기 비교
        max_dimension = max(original_width, original_height)

        # 이미지가 이미 target_size보다 작으면 그대로 반환
        if max_dimension <= target_size:
            print(f"이미지가 이미 {target_size} 픽셀보다 작습니다. 축소하지 않습니다.")
            return img
        else:
            # 가로와 세로 중 큰 쪽을 기준으로 비율 계산
            if original_width > original_height:
                scale_factor = target_size / original_width
            else:
                scale_factor = target_size / original_height

            # 새로운 크기 계산
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            # 이미지 크기 조정
            resized_img = img.resize((new_width, new_height))

            print(f"이미지를 {original_width}x{original_height}에서 {new_width}x{new_height}로 축소합니다.")

            return resized_img

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None


def get_file_paths(folder_path, relative_to='.'):
    """
    주어진 폴더 내의 모든 파일 경로를 리스트로 반환하는 함수.

    Parameters:
    folder_path (str): 탐색할 폴더의 경로.
    relative_to (str): 반환할 경로의 기준 디렉토리. 기본값은 현재 디렉토리 '.' 입니다.

    Returns:
    list: 폴더 내의 모든 파일 경로를 포함하는 리스트.
    """
    file_paths = []

    # os.walk()를 사용하여 폴더 내 모든 파일을 탐색합니다.
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 파일의 전체 경로를 생성합니다.
            full_path = os.path.join(root, file_name)

            # 상대 경로로 변환하여 리스트에 추가합니다.
            relative_path = os.path.relpath(full_path, start=relative_to)
            file_paths.append(relative_path)

    return file_paths