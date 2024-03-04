"""
Package for image_processor.
"""
import base64
import requests

def main():
    image_path = "coffeeman.png"

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    payload = {
        "image": encoded_image,
        "operations": [
            {"operation": "flip_vertical"},
            {"operation": "rotate", "angle": 90},
            {"operation": "convert_to_grayscale"}
        ]
    }

    response = requests.post("http://yourdomain.com/image_processor/process-image/", json=payload)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            processed_image_data = base64.b64decode(data["processed_image"])
            with open("processed_image.png", "wb") as processed_image_file:
                processed_image_file.write(processed_image_data)
            print("Image processed successfully.")
        else:
            print("Failed to process image:", data["message"])
    else:
        print("Failed to process image. HTTP Status Code:", response.status_code)

if __name__ == "__main__":
    main()
