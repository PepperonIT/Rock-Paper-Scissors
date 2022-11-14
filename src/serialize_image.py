import cv2
import numpy as np


def serialize_image(fid, grayscale=False):
    """
    Serialize an image from a file.

    Parameters
    ----------
    fid : str
        Path to the image file to serialize.
    grayscale : bool
        If true, the image will be read as grayscale single channel image. Otherwise, 
        the image will be read as an RGB image. Default value is `False`.

    Returns
    -------
    bytes
        Serialized image.

    Examples
    --------
    Serialize an image stored in a file will generate a `bytes` object.

    >>> serialize_image("rgbw.png")
    b'$\x1c\xedL\xb1"\xe8\xa2\x00\xff\xff\xff'
    """
    colormode = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
    im = cv2.imread(fid, colormode)
    return np.array(im.tolist(), dtype=np.uint8).tobytes()


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
    return arr.tobytes()


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
