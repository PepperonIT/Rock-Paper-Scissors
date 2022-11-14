import qi
from connection import Connection
from camera import Camera


def main():
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))


    motions = Connection(session)
    camera = Camera(session)

    # camera.save_image_frame("test.jpg")
    # camera.capture_frame()

    motions.startTracking()

    gesture = motions.select_gesture()
    motions.shake_arm()
    motions.do_gesture(gesture)

    motions.stopTracking()
main()
