# coding=utf-8

import random
import time


class Connection:
    """
    Docstring 1
    """

    def __init__(self, session):
        self.motion_service = session.service("ALMotion")
        self.tablet_service = session.service("ALTabletService")
        self.camera_service = session.service("ALVideoDevice")
        self.tracker_service = session.service("ALTracker")
        self.posture_service = session.service("ALRobotPosture")
        self.text_to_speech_service = session.service("ALTextToSpeech")
        self.mem = session.service("ALMemory")
        self.face = session.service("ALFaceDetection")

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

        moves = ["Sten", "Sax", "Påse"]

        for i in range(3):
            # time.sleep(0.5)
            self.motion_service.setAngles(names, angle1, fraction_max_speed)
            time.sleep(0.5)
            self.motion_service.setAngles(names, angle2, fraction_max_speed)
            self.text_to_speech_service.say(moves[i])
        self.motion_service.setAngles(names, angle1, fraction_max_speed)

    def select_gesture(self):
        """
        Docstring 1
        """
        gesture_id = random.randint(0, 2)
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

    def startTracking(self):

        # First, wake up.
        self.motion_service.wakeUp()

        fractionMaxSpeed = 0.8

        # Go to posture stand
        self.posture_service.goToPosture("StandInit", fractionMaxSpeed)

        # Add target to track.
        targetName = "Face"
        faceWidth = 0.25
        self.tracker_service.registerTarget(targetName, faceWidth)

        # Set target to track.
        self.tracker_service.track(targetName)
        self.face.subscribe("Face")

        print("ALTracker successfully started.")
        print("Use Ctrl+c to stop this script.")

        self.text_to_speech_service.say(
            'Jag letar efter någon att spela med')

        try:
            while self.mem.getData('FaceDetected') == None or self.mem.getData('FaceDetected') == []:
                time.sleep(2)

            self.text_to_speech_service.say("Oh hej")
        except KeyboardInterrupt:
            print
            print("Interrupted by user")
            print("Stopping...")
            self.stopTracking()

    def stopTracking(self):
        # Stop tracker
        self.tracker_service.stopTracker()
        self.tracker_service.unregisterAllTargets()
        self.face.unsubscribe("Face")
        self.posture_service.goToPosture("StandInit", 0.8)

        print("ALTracker stopped.")
