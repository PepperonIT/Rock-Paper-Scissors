import qi
from connection import Connection


def main():
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))

    motion_service = session.service("ALMotion")
    tablet = session.service("ALTabletService")
    camera_service = session.service("ALVideoDevice")
    speech_service = session.service("ALTextToSpeech")

    motions = Connection(motion_service, tablet, camera_service, speech_service)

    gesture = motions.select_gesture()
    motions.shake_arm()
    motions.do_gesture(gesture)
    motions.say_result()


main()
