# coding=utf-8

import datetime
import random
import time
import cv2
from threading import Thread
from threading import Event
from camera import Camera
from ai_rest import predict_on_images

verbal_feedback_se = {
    # General
    "welcome": "Oh hej",
    "instructions": "SKRIV INSTRUKTIONER HÄR",

    "rock_paper_scissors": [
        "sten",
        "sax",
        "påse"
    ],

    # Result messages
    "human_victory": [
        "Grattis, du vann!",
        "Nybörjartur, nästa gång vinner jag!"
    ],
    "computer_victory": [
        "Jag vann",
        "En vinst för mig"
    ],
    "tie": [
        "Oavgjort, vi kör igen",
        "Det blev lika, vi kör igen"
    ],

    # Errors
    "error_general": "Jag är lite förvirrad, kan försöka vara lite tydligare?",
    "error_hand_not_found": "Jag kunde inte hitta din hand. Kan du hålla den lite högre upp så kör vi igen?",
    "error_no_gesture": "Jag kunde inte förstå dig. Vi prövar igen",
}

# image_paths_from_pepper = {
#     "bag": "/data/home/nao/pepperonit/rps/images/RPS_bag.jpg",
#     "rock": "/data/home/nao/pepperonit/rps/images/RPS_rock.jpg",
#     "paper": "/data/home/nao/pepperonit/rps/images/RPS_paper.jpg",
#     "scissor": "/data/home/nao/pepperonit/rps/images/RPS_scissor.jpg",
# }

image_paths = {
    "bag": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Brown_bag.jpg/250px-Brown_bag.jpg",
    "rock": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Logan_Rock_Treen_closeup.jpg/1200px-Logan_Rock_Treen_closeup.jpg",
    "paper": "https://kronofogden.se/images/18.338e6d8417768af37a81509/1613482649765/bilder%20grafisk%20manual%20web43.png",
    "scissor": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Standard_household_scissors.jpg/640px-Standard_household_scissors.jpg",
}


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
        self.speech_service = session.service("ALTextToSpeech")
        self.mem = session.service("ALMemory")
        self.face = session.service("ALFaceDetection")
        self.camera = Camera(session)

        # Preload all images
        # for key in image_paths:
        # self.tablet_service.preLoadImage(image_paths[key])

    def run_game(self, changeTracking=True):
        if changeTracking:
            self.startTracking()

        event = Event()
        thread = Thread(target=self.showVideo, args=(event,))
        thread.start()


        computer_gesture = self.select_gesture()
        self.shake_arm()
        self.do_gesture(computer_gesture)
        event.set()
        time.sleep(1)

        human_gesture = self.capture_gesture()
        print("humangesture: {}".format(human_gesture))
        print("robotgesture: {}".format(computer_gesture))
        self.say_result(human_gesture, computer_gesture)
        time.sleep(3)
        self.tablet_service.hideImage()

        if changeTracking:
            self.stopTracking()

    def shake_arm(self):
        """
        Shake arm and say rock paper scissors.
        """
        names = ["RShoulderPitch", "RElbowRoll"]
        angleUp = [0.5, 1]  # Up
        angleDown = [1, 0.5]  # Down
        fraction_max_speed = 0.2
        motion_delay = 0.3

        # Rest to down position
        self.motion_service.setAngles(names, angleDown, fraction_max_speed)
        time.sleep(2 * motion_delay)

        for i in range(3):
            self.motion_service.setAngles(names, angleUp, fraction_max_speed)
            time.sleep(motion_delay)
            self.motion_service.setAngles(names, angleDown, fraction_max_speed)
            self.speech_service.say(verbal_feedback_se["rock_paper_scissors"][i])
            time.sleep(0.3 * motion_delay)

        self.motion_service.setAngles(names, angleUp, fraction_max_speed)

    def select_gesture(self):
        """
        Docstring 1
        """
        random.seed(datetime.datetime.now())
        gesture_id = random.randint(0, 2)
        return gesture_id

    def do_gesture(self, gesture_id):
        """
        Docstring 1
        """
        # self.tablet_service.hideImage()
        # 0 == rock, 1 == paper, 2 == scissors
        if gesture_id == 0:
            self.tablet_service.showImage(image_paths["rock"])
            # self.motion_service.closeHand('RHand')
        elif gesture_id == 1:
            self.tablet_service.showImage(image_paths["bag"])
            # self.motion_service.openHand('RHand')
        elif gesture_id == 2:
            self.tablet_service.showImage(image_paths["scissor"])

    def showVideo(self, event):
        """
        Docstring 1
        """
        self.camera.subscribe(0, 1, 13, 30)
        while True:
            # img = self.select_gesture()
            if event.is_set():
                self.tablet_service.hideImage()
                break
            image = self.camera.capture_frame()
            cv2.imwrite('image0.png', image)

            # self.do_gesture(img)
        self.camera.unsubscribe()
        

    def capture_gesture(self):
        """
        Capture a gesture from the player.

        Returns
        -------
        int:
            Returns the gesture id. If no gesture is found, returns -1. If no 
            hand was found, returns -2. If an error occured, returns -3.

        """
        # Capture images
        gesture_images = []
        self.camera.subscribe(0, 1, 13, 30)
        for _ in range(0, 2):
            gesture = self.camera.capture_frame()
            gesture_images.append(gesture)
        self.camera.unsubscribe()

        # Process images
        prediction = predict_on_images(gesture_images)

        return prediction

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

        self.speech_service.say(
            'Jag letar efter någon att spela med')

        try:
            while self.mem.getData('FaceDetected') == None or self.mem.getData('FaceDetected') == []:
                time.sleep(2)

            self.speech_service.say(verbal_feedback_se["welcome"])
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

    def say_result(self, humanGesture, computerGesture):
        """
        Docstring 1

        Parameters
        ----------
        humanGesture : int
            The gesture the human player chose.
        computerGesture : int
            The gesture the computer chose.

        Returns
        -------
        None.
        """
        if humanGesture == -1:
            self.speech_service.say(verbal_feedback_se["error_no_gesture"])
            self.run_game(False)
        elif humanGesture == -2:
            self.speech_service.say(verbal_feedback_se["error_hand_not_found"])
            self.run_game(False)

        winner = get_winner(humanGesture, computerGesture)
        if winner == 0:
            victory_saying_index = random.randint(0, len(verbal_feedback_se["human_victory"]) - 1)
            self.speech_service.say(verbal_feedback_se["human_victory"][victory_saying_index])
        elif winner == 1:
            victory_saying_index = random.randint(0, len(verbal_feedback_se["computer_victory"]) - 1)
            self.speech_service.say(verbal_feedback_se["computer_victory"][victory_saying_index])
        elif winner == 2:
            victory_saying_index = random.randint(0, len(verbal_feedback_se["tie"]) - 1)
            self.speech_service.say(verbal_feedback_se["tie"][victory_saying_index])
            self.run_game(False)


def get_winner(humanGesture, computerGesture):
    """
    Determine the winner of the game.

    A gesture is an integer between 0 and 2, where 0 is rock, 1 is paper and 2 is scissors.

    Parameters
    ----------
    humanGesture : int
        The gesture the human player chose.
    computerGesture : int
        The gesture the computer chose.

    Returns
    -------
    int
        0 if human wins, 1 if computer wins, 2 if tie.
    """
    if humanGesture == 0:  # rock
        if computerGesture == 0:
            return 2
        if computerGesture == 1:
            return 1
        if computerGesture == 2:
            return 0
    elif humanGesture == 1:  # paper
        if computerGesture == 0:
            return 0
        if computerGesture == 1:
            return 2
        if computerGesture == 2:
            return 1
    elif humanGesture == 2:  # scissors
        if computerGesture == 0:
            return 1
        if computerGesture == 1:
            return 0
        if computerGesture == 2:
            return 2
