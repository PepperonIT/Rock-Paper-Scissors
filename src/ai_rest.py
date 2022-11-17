from serialize_image import serialize_image_array
import requests
import base64
import json
import cv2


def predict_on_images(images):
    """
    Send images to the server and get predictions.

    Returns
    -------
    int:
        Returns the gesture id. If no gesture is found, returns -1. If no 
        hand was found, returns -2. If an error occured, returns -3.
    """
    # Prepare request
    serialized_images = []
    for gesture_image in images:
        serialized = serialize_image_array(gesture_image)
        serialized = base64.b64encode(serialized).encode("utf8")
        serialized_images.append(serialized)

    request_body = json.dumps({
        "image_list": serialized_images,
        "dtype": images[0].dtype.name,
        "shape": images[0].shape
    })
    request_headers = {"Content-Type": "application/json"}
    request_url = "https://pepper.lillbonum.se/predict/hand"

    # Send HTTP request
    response = requests.get(request_url, data=request_body, headers=request_headers)
    if response.status_code != 200:
        print("Status code: " + str(response.status_code))
        print("Error: " + response.text)
        return -3
    else:
        response_json = response.json()

    i = 0
    for image in images:
        cv2.imwrite("image" + str(i) + ".png", image)
        i += 1

    # Do something with the reponse
    print("response: {}".format(response_json))
    if response_json["prediction"] == "ROCK":
        return 0
    elif response_json["prediction"] == "PAPER":
        return 1
    elif response_json["prediction"] == "SCISSORS":
        return 2
    elif response_json["prediction"] == "NOTHING":
        return -1
    else:
        return -2
