import random
import cv2
import numpy


class Camera:
    def __init__(self, session):
        """
        Initialize the camera service.

        Parameters
        ----------
        session : qi.Session
            The session to use to initialize the camera service.
        """
        self.camera_service = session.service("ALVideoDevice")
        self.camera_link = None

    def subscribe(self, camera_index, resolution, color_space, fps):
        """
        Subscribe to the camera. Only one camera can be subscribed at a time.

        For a complete list of possible values for the parameters, see the [pepper specifications](http://doc.aldebaran.com/2-4/family/pepper_technical/video_pep.html).

        Parameters
        ----------
        camera_index : int
            The index of the camera to subscribe to.
        resolution : int
            The resolution of the camera.
        color_space : int
            The color space of the camera.
        fps : int
            The fps of the camera.

        Raises
        ------
        RuntimeError
            If the camera is already subscribed.

        Examples
        --------
        The following code will subscribe to the top camera with resolution 
        1280x960px, color space kBGR, and 30 fps.
        >>> camera.camera_subscribe(0, 3, 13, 30)
        """
        cameraStreamName = "CameraStream" + str(random.random())
        self.camera_link = self.camera_service.subscribeCamera(
            cameraStreamName, camera_index, resolution, color_space, fps)

        if not self.camera_link:
            raise RuntimeError("Could not subscribe to camera")

    def unsubscribe(self):
        """
        Unsubscribe from the camera.
        """
        self.camera_service.unsubscribe(self.camera_link)

    def capture_frame(self, channels=3):
        """
        Get one frame from pepper.

        To use this method, you must first subscribe to the camera.

        Parameters
        ----------
        channels : int
            The number of color channels in the image.

        Raises:
        -------
        RuntimeError
            If the camera is not subscribed, or if the camera is not available.

        Returns
        -------
        image : numpy.ndarray
            The image frame in form of a numpy array. The shape of array 
            is the same as the resolution specified when subscribing to the camera.
        """
        image_stream = self.camera_service.getImageRemote(self.camera_link)
        if image_stream is None:
            raise RuntimeError("Could not get image from camera")

        # print(type(image_stream))
        # print("len list: ", len(image_stream))

        image_arr = numpy.frombuffer(image_stream[6], numpy.uint8).reshape(
            image_stream[1], image_stream[0], channels)
        return image_arr

    def save_image_frame(self, imagePath):
        """
        Get one RGB image frame from pepper.

        This method will subscribe to the camera, capture one frame, unsubscribe
        from the camera, and save the image to the specified path.

        Parameters
        ----------
        imagePath : str
            The path to save the image frame.

        Examples
        --------
        The following code will save an image frame named `image.png` to the 
        current directory.
        >>> camera.save_image_frame("image.png")
        """
        self.subscribe(0, 3, 13, 30)
        image = self.capture_frame()
        self.unsubscribe()
        cv2.imwrite(imagePath, image)
