import ollama


def get_info_from_image(file_dirs):
    responses = []
    for path in file_dirs:
        print(f"Path: {path}")
        with open(path, "rb") as f:
            response = ollama.generate(
                model="llava",
                prompt=f"Just briefly describe what AI needs to hear your description and draw the same",
                images=[f.read()],
            )
        print(response['response'])
        print("=" * 20)
        responses.append(response['response'])
    return responses


if __name__ == "__main__":
    exif = {'./photo/test/0.jpg': {'DateTime': '2024:05:30 12:45:47', 'Latitude': 33.25136944444444,
                                   'Longitude': 126.56046944444444},
            './photo/test/1.jpg': {'DateTime': '2024:05:30 16:32:55', 'Latitude': 33.23952777777778,
                                   'Longitude': 126.55835833333333},
            './photo/test/2.jpg': {'DateTime': '2024:05:31 10:41:47', 'Latitude': 33.24487222222222,
                                   'Longitude': 126.41303888888889},
            './photo/test/3.jpg': {'DateTime': '2024:05:31 09:18:02', 'Latitude': 33.23847222222222,
                                   'Longitude': 126.43897222222222}}

    get_info_from_image(exif)
