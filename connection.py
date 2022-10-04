import fractions
import naoqi
from naoqi import ALProxy
import qi
import time

def main():
    session = qi.Session()
    connection = session.connect("tcp://{0}:{1}".format("130.240.238.32", 9559))
    # tts = ALProxy("ALTextToSpeech", "130.240.238.32", 9559)

    motion_service = session.service("ALMotion")

    shakeArm(motion_service)

    # names = ["RWristYaw", "RElbowRoll", "RElbowYaw"]
    # angles = [0, 1.4, 1.57]
    # fractionMaxSpeed = 0.2
    # motion_service.setAngles(names, angles, fractionMaxSpeed)


    # motion_service.closeHand('RHand')
    # tts.say("Hello there")
    # tts.say("Obiwan Kenobi")
    # tts.say("Goodbye")

def shakeArm(motion_service):
    # names = ["RElbowRoll"]
    names = ["RShoulderPitch", "RElbowRoll"]
    angle1 = [0.5, 1]
    angle2 = [1, 0.5]
    fractionMaxSpeed = 0.2
    motion_service.closeHand('RHand')

    for i in range(3):
        print(i)
        time.sleep(0.5)
        motion_service.setAngles(names, angle1, fractionMaxSpeed)
        time.sleep(0.5)
        motion_service.setAngles(names, angle2, fractionMaxSpeed)

main()