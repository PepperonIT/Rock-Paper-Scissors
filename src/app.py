import qi
from connection import Connection


def main():
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))

    motions = Connection(session)

    motions.startTracking()

    gesture = motions.select_gesture()
    motions.shake_arm()
    motions.do_gesture(gesture)
    motions.say_result()

    motions.stopTracking()


if __name__ == "__main__":
    main()
