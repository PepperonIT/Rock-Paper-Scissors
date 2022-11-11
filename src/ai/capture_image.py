import sys
sys.path.append("./src")

from camera import Camera
import qi


def capture_image():
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))

    camera = Camera(session)

    if len(sys.argv) != 2:
        print("Usage: python ./src/ai/image_capture.py [path to image]")
        sys.exit(1)

    camera.save_image_frame(sys.argv[1])


capture_image()
