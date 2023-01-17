import qi
import sys
from controller import Controller


def main(language, RPS_server_address):
    session = qi.Session()
    session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))
    motions = Controller(session, RPS_server_address, language)
    motions.game_loop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python app.py [LANGUAGE] [RPS_SERVER_ADDRESS]")
        print("\nExample:")
        print("  python app.py English \"http://192.168.1.10\"")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
