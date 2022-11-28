import numpy as np
import base64
import io
from PIL import Image


def serialize_image_array(arr, dtype=np.uint8):
    """
    Serialize an image stored as an array.

    Parameters
    ----------
    arr : numpy.ndarray or list
        Image array to serialize.
    dtype : type
        Data type of the array. Default value is `np.uint8`.

    Returns
    -------
    bytes
        Serialized image.
    """
    if isinstance(arr, list):
        arr = np.array(arr, dtype=dtype)
    return bytes(arr.tostring())


def serialize_image_as_dataurl(arr):
    """
    Serialize an image stored as an array into a dataurl of mimetype 
    `image/png`, e.g. `data:image/png;base64,<image_data>`.

    Parameters
    ----------
    arr : numpy.ndarray or list
        Image array to serialize.

    Returns
    -------
    str
        Serialized image as a dataurl.
    """
    buffer = io.BytesIO()
    image = Image.fromarray(arr)
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue())
    data_url = "data:image/png;base64," + img_str
    return data_url


def deserialize_image_from_dataurl(dataurl):
    """
    Deserialize an image stored as a dataurl into a `numpy.ndarray`. The image 
    must be of mimetype `image/png` and base64 encoded.

    Parameters
    ----------
    dataurl : str
        Dataurl to deserialize and must begin with `data:image/png;base64,`.

    Raises
    ------
    ValueError
        If the dataurl is not of mimetype `image/png` or is not base64 encoded.

    Returns
    -------
    numpy.ndarray
        Deserialized image from dataurl.

    """
    dataurl_prefix = "data:image/png;base64,"
    if not dataurl.startswith(dataurl_prefix):
        raise ValueError("dataurl must start with '{}'".format(dataurl_prefix))

    img_str = dataurl[len(dataurl_prefix):]  # Remove dataurl prefix
    image = Image.open(io.BytesIO(base64.b64decode(img_str)))
    return np.array(image)


def deserialize_image(arr, dtype=np.uint8, shape=None):
    """
    Deserialize an byte array into an `numpy.ndarray`.

    Parameters
    ----------
    arr : bytes
        Byte array to deserialize.
    dtype : type
        Data type of the array. Default value is `np.uint8`.
    shape : tuple
        Shape of the array. Default value is `None` and the array dimension will be 1D.

    Returns
    -------
    numpy.ndarray
        Deserialized array.

    Examples
    --------
    Deserialize an RGB image of size 2x2px stored as a byte array into a `numpy.ndarray`.

    >>> import numpy as np
    >>> deserialize_image(b'$\x1c\xedL\xb1"\xe8\xa2\x00\xff\xff\xff', np.uint8, (2, 2, 3))
    array([[[ 36,  28, 237],
            [ 76, 177,  34]],

            [[232, 162,   0],
            [255, 255, 255]]], dtype=uint8)
    """
    image = np.frombuffer(arr, dtype)
    if shape is not None:
        if not isinstance(shape, tuple):
            raise TypeError("shape must be a tuple")
        image = image.reshape(shape)

    return image
