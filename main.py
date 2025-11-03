import os
import base64


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

if __name__ == '__main__':

    path = os.path.join("data", "example.jpg")
    # Example usage
    base64_string = image_to_base64(path)
    print(base64_string)  # Use this string in the API request