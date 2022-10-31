import random
import cv2
import numpy


class Camera:
    def __init__(self, session):
        self.camera_service = session.service("ALVideoDevice")
        self.camera_link = None

    def camera_subscribe(self, camera_index, resolution, color_space, fps):
        """
        Subscribe to the camera.
        """
        cameraStreamName = "CameraStream" + str(random.random())
        self.camera_link = self.camera_service.subscribeCamera(
            cameraStreamName, camera_index, resolution, color_space, fps)

        if not self.camera_link:
            raise RuntimeError("Could not subscribe to camera")

    def camera_unsubscribe(self):
        self.camera_service.unsubscribe(self.camera_link)

    def capture_frame(self):
        """
        Get one image frame from pepper.
        """
        self.camera_subscribe(0, 3, 13, 30)

        # Get a camera image.
        image_stream = self.camera_service.getImageRemote(self.camera_link)
        image_arr = numpy.frombuffer(image_stream[6], numpy.uint8).reshape(
            image_stream[1], image_stream[0], 3)

        # Process image
        self.camera_unsubscribe()
        cv2.imwrite("image.png", image_arr)
