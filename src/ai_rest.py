from serialize_image import serialize_image_array
import requests
import base64
import json


def predict_on_images(images, server_address):
    """
    Send images to the server and get predictions.

    Parameters
    ----------
    images: list(numpy.ndarray)
        A list of images to send to the server.
    server_address: str
        The address of the server to send the images to. Should not include a trailing slash.

    Returns
    -------
    tuple(gesture:int, image_url:str):
        Returns the gesture as an ``int``. If no gesture is found, returns -1. If no 
        hand was found, returns -2. If an error occured, returns -3. 

        The ``image_url`` is the url to the image that was generated on the server.
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
    request_url = "{}/predict/hand".format(server_address)

    # Send HTTP request
    response = requests.get(request_url, data=request_body, headers=request_headers)
    if response.status_code != 200:
        print("Status code: " + str(response.status_code))
        print("Error: " + response.text)
        return -3, None
    else:
        response_json = response.json()

    # Do something with the reponse
    print("response: {}".format(response_json))

    gesture_image_url = response_json.get("images", None)
    gesture_image_url = gesture_image_url.get("processed", "") if gesture_image_url is not None else ""
    if response_json["prediction"] == "ROCK":
        return 0, gesture_image_url
    elif response_json["prediction"] == "PAPER":
        return 1, gesture_image_url
    elif response_json["prediction"] == "SCISSORS":
        return 2, gesture_image_url
    elif response_json["prediction"] == "NOTHING":
        return -1, gesture_image_url
    else:
        return -2, gesture_image_url
