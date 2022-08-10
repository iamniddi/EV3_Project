from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pyhuskylens import * 

ev3 = EV3Brick()

grab_moter=Motor(Port.A)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

left_cs =ColorSensor(Port.S3)
right_cs =ColorSensor(Port.S4)

ultra=UltrasonicSensor(Port.S2)


robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2

DRIVE_SPEED = 100

PROPORTIONAL_GAIN = 1.2

garbage=0

def goLeft(num):
    savePoint=0
    countCheck=0
    while True:
        deviation = left_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, turn_rate)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==num and countCheck == 0):
            robot.stop()
            break
    wait(10)

def goRight(num):
    savePoint=0
    countCheck=0
    while True:
        deviation = right_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, turn_rate)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==num and countCheck == 0):
            robot.stop()
            break
    wait(10)

def grap(num):
    grab_moter.run_until_stalled(num*200, then=Stop.COAST, duty_limit=50)

def goGarbageLeft():
    while True:
        distance=ultra.distance()
        deviation = left_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, turn_rate)
        if distance<120:
            grap(1)
            print("거리확인")
            break
    wait(10)


def seeGarbage():
    a=0
    while True:
        blocks=hl.get_blocks()
        if len(blocks) > 0:
            ID =blocks[0].ID
        if ID==1:
            ev3.speaker.beep()
            a=1
            print(a)
            return a
        elif ID==2:
            ev3.speaker.beep()
            a=2
            print(a)
            return a
        wait(10)

def tuenBack():
    pass

while True:
    # Calculate the deviation from the threshold.
    deviation = left_cs.reflection() - threshold

    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * deviation

    # Set the drive base speed and turn rate.
    robot.drive(DRIVE_SPEED, turn_rate)

    # You can wait for a short time or do other things in this loop.
    wait(10)
