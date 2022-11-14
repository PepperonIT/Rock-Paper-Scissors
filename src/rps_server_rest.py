import requests
import base64
import json
import numpy as np
import serialize_image as si


def serialize_image_array(image):
    """
    Serialize an image stored as an array as a base64 encoded string.

    Parameters
    ----------
    image : numpy.ndarray or list
        Image array to serialize.

    Returns
    -------
    str
        Serialized image.
    """
    image_bytes = si.serialize_image_array(image)
    image_str = base64.b64encode(image_bytes).decode("utf8")
    return image_str


def make_http_request_to_ai(image):
    """
    Send a request to the server.

    Parameters
    ----------
    image : numpy.ndarray
        The image to send to the server
    """
    request_headers = {"Content-Type": "application/json"}
    request_body = json.dumps({
        "image": serialize_image_array(image),
        "dtype": np.uint8.__name__,
        "shape": [1, 100, 100, 1]
    })

    URL = "https://pepper.lillbonum.se/predict/hand"
    response = requests.get(URL, data=request_body, headers=request_headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"AI Prediction: Something went wrong.")
        print(f"               Status code: {response.status_code}")
        print(f"               Response: {response.text}")
