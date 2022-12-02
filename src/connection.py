# coding=utf-8

import datetime
import random
import time
import platform
from threading import Thread
from threading import Event
from camera import Camera
from ai_rest import predict_on_images
from PIL import Image
from memoize import Memoize

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

        # Determine if environment is running on a real robot or using an extrernal computer
        self.running_on_pepper = "aldebaran" in platform.release()

        # Preload all images
        # for key in image_paths:
        # self.tablet_service.preLoadImage(image_paths[key])

    def run_game(self, changeTracking=True):
        """
        Main driver function for allowing Pepper to play rock-paper-scissors.

        Parameters
        -----------
        changeTracking: boolean
            Is Pepper already tracking or should 
            Pepper try to find a new target
        """
        stop_video_event = Event()
        picture_thread = Thread(target=self.send_video, args=(stop_video_event, 15))
        picture_thread.start()

        if changeTracking:
            self.startTracking()

        computer_gesture = self.select_gesture()
        self.shake_arm()
        stop_video_event.set()
        picture_thread.join()
        self.do_gesture(computer_gesture)

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
        Pepper shakes her arm and says rock paper scissors.
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
        memo = Memoize.get_instance()
        gesture_id = Memoize.memoized_random(memo)
        # random.seed(datetime.datetime.now())
        # gesture_id = random.randint(0, 2)
        return gesture_id

    def do_gesture(self, gesture_id):
        """
        Pepper performs a gesture based on parameter.

        Parameters
        ------------
        gesture_id: int
            Which gesture Pepper should do.
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

    def send_video(self, event, fps):
        """
        Continously takes pictures and sends them to pepper to display on the 
        tablet until event is set.

        This function requires the environment to be pepper, e.g. `self.running_on_pepper == True`. 
        Otherwise it will return immediately and do nothing.

        Parameters
        ------------
        event: Thread.event 
            An event that tells the process when to stop
        """
        if not self.running_on_pepper:
            print("Not running on pepper, skipping video")
            return

        self.camera.subscribe(0, 1, 11, fps)
        while True:
            if event.is_set():
                break
            image = self.camera.capture_frame()
            time.sleep(1 / fps)
            Image.fromarray(image).save("/home/nao/.local/share/ota/rps/latest.jpg", "JPEG")
            self.tablet_service.showImageNoCache("http://198.18.0.1/ota_files/rps/latest.jpg")

        self.tablet_service.hideImage()

    def capture_gesture(self):
        """
        Capture a gesture from the player.
        Returns
        -------
        int:
            Returns the gesture id. If no gesture is found, returns -1. If no 
            hand was found, returns -2. If an error occured, returns -3.
        """
        if self.camera.camera_link is None:
            self.camera.subscribe(0, 1, 11, 30)

        # Capture images
        gesture_images = []
        for _ in range(0, 2):
            gesture = self.camera.capture_frame()
            gesture_images.append(gesture)
        self.camera.unsubscribe()

        # Process images
        prediction = predict_on_images(gesture_images)

        return prediction

    def startTracking(self):
        """
        Pepper goes into neutral position and then looks for 
        a face to track. When found Pepper will verbally respond
        and track that face until interrupted.
        """

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
        """
        Function to interrupt Pepper's face tracking
        and set Pepper into a neutral position.
        """
        # Stop tracker
        self.tracker_service.stopTracker()
        self.tracker_service.unregisterAllTargets()
        self.face.unsubscribe("Face")
        self.posture_service.goToPosture("StandInit", 0.8)

        print("ALTracker stopped.")

    def say_result(self, humanGesture, computerGesture):
        """
        Pepper announces the result of the game and plays again
        if the game was a tie or an error occurs.

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

        winner = Connection.get_winner(humanGesture, computerGesture)
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

    @staticmethod
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

        Raises
        ------
        ValueError
            If either humanGesture or computerGesture is not an integer between 0 and 2.
        """
        valid_gestures = [0, 1, 2]
        if humanGesture not in valid_gestures or computerGesture not in valid_gestures:
            raise ValueError("Invalid gesture")

        if (computerGesture + 1) % len(valid_gestures) == humanGesture:
            return 0
        elif humanGesture == computerGesture:
            return 2
        else:
            return 1
