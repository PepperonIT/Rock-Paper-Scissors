import random
import time


class Connection:
    """
    Docstring 1
    """

    def __init__(self, motion_service, tablet_service, camera_service):
        self.motion_service = motion_service
        self.tablet_service = tablet_service
        self.camera_service = camera_service
        self.tablet_service.preLoadImage(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Logan_Rock_Treen_closeup.jpg/1200px-Logan_Rock_Treen_closeup.jpg")
        self.tablet_service.preLoadImage(
            "https://kronofogden.se/images/18.338e6d8417768af37a81509/1613482649765/bilder%20grafisk%20manual%20web43.png")
        self.tablet_service.preLoadImage(
            "https://www.tingstad.com/fixed/images/Main/1536253379/4003801725307.png")

    def shake_arm(self):
        """
        Docstring 1
        """
        # names = ["RElbowRoll"]
        names = ["RShoulderPitch", "RElbowRoll"]
        angle1 = [0.5, 1]  # Up
        angle2 = [1, 0.5]  # Down
        fraction_max_speed = 0.2

        self.motion_service.setAngles(names, angle1, fraction_max_speed)

        for i in range(3):
            time.sleep(0.5)
            self.motion_service.setAngles(names, angle1, fraction_max_speed)
            time.sleep(0.5)
            self.motion_service.setAngles(names, angle2, fraction_max_speed)
        time.sleep(0.5)
        self.motion_service.setAngles(names, angle1, fraction_max_speed)

    def select_gesture(self):
        """
        Docstring 1
        """
        gesture_id = random.randint(0, 2)
        print(gesture_id)
        return gesture_id

    def do_gesture(self, gesture_id):
        """
        Docstring 1
        """

        # 0 == rock, 1 == paper, 2 == scissors
        if gesture_id == 0:
            self.tablet_service.showImage(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Logan_Rock_Treen_closeup.jpg/1200px-Logan_Rock_Treen_closeup.jpg"
            )
            self.motion_service.closeHand('RHand')
        elif gesture_id == 1:
            self.tablet_service.showImage(
                "https://kronofogden.se/images/18.338e6d8417768af37a81509/1613482649765/bilder%20grafisk%20manual%20web43.png")
            self.motion_service.openHand('RHand')
        elif gesture_id == 2:
            self.tablet_service.showImage(
                "https://www.tingstad.com/fixed/images/Main/1536253379/4003801725307.png")
        self.tablet_service.hideImage()

    def capture_gesture(self):
        """
        Capture a gesture from the player.
        """