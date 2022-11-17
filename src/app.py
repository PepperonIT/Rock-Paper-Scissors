import qi
from connection import Connection


def main():
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))

    motions = Connection(session)

    human_gesture = motions.capture_gesture()
    print("Capture gesture is {}".format(human_gesture))
    return
    motions.startTracking()

    computer_gesture = motions.select_gesture()
    motions.shake_arm()
    motions.do_gesture(computer_gesture)
    human_gesture = motions.capture_gesture()
    motions.say_result(human_gesture)

    motions.stopTracking()


if __name__ == "__main__":
    main()
