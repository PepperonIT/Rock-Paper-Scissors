import qi
from connection import Connection
from camera import Camera


def main():
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))

    motion_service = session.service("ALMotion")
    tablet = session.service("ALTabletService")
    camera_service = session.service("ALVideoDevice")

    motions = Connection(motion_service, tablet, camera_service)
    camera = Camera(session)

    camera.save_image_frame("test.jpg")
    motions.capture_frame()

    gesture = motions.select_gesture()
    motions.shake_arm()
    motions.do_gesture(gesture)


main()
