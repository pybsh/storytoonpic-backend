import exifread


def get_exif_data(file_path):
    """
    Extract EXIF data from an image file.
    :param file_path: Path to the image file.
    :return: Dictionary containing the EXIF data.
    """
    with open(file_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
    return tags


def get_decimal_coordinates(tags):
    """
    Convert EXIF GPS coordinates to decimal format.
    :param tags: EXIF tags containing GPS info.
    :return: Tuple containing (latitude, longitude).
    """

    def convert_to_degrees(value):
        """
        Helper function to convert the GPS coordinates stored in EXIF to degrees in float format.
        :param value: GPS coordinate value.
        :return: Coordinate in degrees as a float.
        """
        d, m, s = value.values
        return float(d.num) / float(d.den) + (float(m.num) / float(m.den) / 60.0) + (
                float(s.num) / float(s.den) / 3600.0)

    lat = tags.get('GPS GPSLatitude')
    lat_ref = tags.get('GPS GPSLatitudeRef')
    lon = tags.get('GPS GPSLongitude')
    lon_ref = tags.get('GPS GPSLongitudeRef')

    if not lat or not lon or not lat_ref or not lon_ref:
        return None, None

    lat = convert_to_degrees(lat)
    if lat_ref.values[0] != 'N':
        lat = -lat

    lon = convert_to_degrees(lon)
    if lon_ref.values[0] != 'E':
        lon = -lon

    return lat, lon


def get_image_metadata(file_paths):
    """
    Extract location and date/time information from image files.
    :param file_paths: List of paths to image files.
    :return: Dictionary with image file paths as keys and metadata as values.
    """
    metadata_dict = {}

    for file_path in file_paths:
        tags = get_exif_data(file_path)

        if not tags:
            metadata_dict[file_path] = {'Error': 'No EXIF data found'}
            continue

        # Get the date and time the photo was taken
        datetime_taken = tags.get('EXIF DateTimeOriginal')
        datetime_str = datetime_taken.values if datetime_taken else 'Unknown'

        # Get GPS coordinates
        lat, lon = get_decimal_coordinates(tags)

        metadata_dict[file_path] = {
            'DateTime': datetime_str,
            'Latitude': lat,
            'Longitude': lon
        }

    return metadata_dict


# Example usage
if __name__ == '__main__':
    file_paths = ['./photo/test/0.jpg']
    metadata = get_image_metadata(file_paths)
    print(metadata)
