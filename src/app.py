import qi
from connection import Connection

motions = None


def main(session):
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))
    global motions
    motions = Connection(session, 'Swedish')
    motions.run_game()

    human_gesture = motions.capture_gesture()
    print("Capture gesture is {}".format(human_gesture))
    return


if __name__ == "__main__":
    main()
