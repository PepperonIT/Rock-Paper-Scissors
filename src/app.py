import qi
import sys
from connection import Connection


def main(lang):
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))
    motions = Connection(session, lang)
    motions.game_loop()


if __name__ == "__main__":
    main(sys.argv[1])
