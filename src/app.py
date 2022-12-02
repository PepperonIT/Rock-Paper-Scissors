import qi
from connection import Connection


def main(session):
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))
    motions = Connection(session)
    motions.run_game()

if __name__ == "__main__":
    main()
