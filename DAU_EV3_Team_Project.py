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

hl=HuskyLens(Port.S1, debug=False)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2

DRIVE_SPEED = 100

PROPORTIONAL_GAIN = 1.2

global garbage
garbage = 0

def startLine():
    while True:
        robot.straight(50)
        if(right_cs.color()==Color.BLACK):
            robot.stop()
            break
    while True:
        deviation = left_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, turn_rate)        
        if(right_cs.color()!=Color.BLACK):
            robot.stop()
            break
    return

def lineOut(a):#0은 양쪽 아웃 1은 오른쪽 2는 왼쪽 아웃
    while True:
        if(a==0):
            if(right_cs.color()!=Color.BLACK and left_cs.color()!=Color.BLACK):
                robot.stop()
                break
            robot.straight(10)
        elif(a==1):
            if(right_cs.color()!=Color.BLACK):
                robot.stop()
                break
            robot.straight(10)
        else:
            if(left_cs.color()!=Color.BLACK):
                robot.stop()
                break
            robot.straight(10)
    return
    # left_motor.run(180) 한쪽 모터만 쓰는 예제
    # while True:
    #     if(a==0):
    #         if(right_cs.color()!=Color.BLACK and left_cs.color()!=Color.BLACK):
    #             robot.stop()
    #             break
    #         robot.straight(10)
    #     elif(a==1):
    #         if(right_cs.color()!=Color.BLACK):
    #             right_motor.stop(Stop.BRAKE)
    #             break
    #         right_motor.run(10)
    #     else:
    #         if(left_cs.color()!=Color.BLACK):
    #             left_motor.stop(Stop.BRAKE)
    #             break
    #         left_motor.run(10)
    # return

def turnLine():
    while True:
        if(right_cs.color()==Color.BLACK and left_cs.color()==Color.BLACK):
            robot.stop()
            break
        robot.straight(-5)
    return

def turnLineWhite():
    while True:
        if(right_cs.color()==Color.WHITE or left_cs.color()==Color.WHITE):
            robot.stop()
            break
        robot.straight(-5)
    return

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

def goLeftR(num):
    savePoint=0
    countCheck=0
    while True:
        deviation = threshold-left_cs.reflection() 
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

def goRed(num):
    goLeft(1)
    robot.turn(90)
    while True:
        deviation = left_cs.reflection() - threshold#왼쪽으로 바꿔봐야함
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, turn_rate)
        if(right_cs.color()==Color.RED):
            robot.straight(80)
            grap(-1)
            robot.straight(-80)
            grap(1)
            break
    wait(10)

def goBlue(num):
    goLeft(2)
    robot.turn(90)
    while True:
        deviation = left_cs.reflection() - threshold#왼쪽으로 바꿔봐야함
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, turn_rate)
        if(right_cs.color()==Color.BLUE):
            robot.straight(80)
            grap(-1)
            robot.straight(-80)
            grap(1)
            break
    wait(10)

def goStart():
    turnLineWhite()
    robot.turn(90)
    if(garbage==1):
        goLeftR(1)
        robot.turn(90)
        lineOut(1)
        return
    elif(garbage==2):
        goLeftR(2)
        robot.turn(90)
        lineOut(1)
        return

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

def objectDetection():
    distance=ultra.distance()
    if distance<500:
        print("물체인식")
        seeGarbage()
        return 1
    else:
        print("물체없음")
        return 0



def seeGarbage():
    while True:
        blocks=hl.get_blocks()
        if len(blocks) > 0:
            ID =blocks[0].ID
        if ID==1:
            ev3.speaker.beep()
            garbage=1
            print(garbage)
            return garbage
        elif ID==2:
            ev3.speaker.beep()
            garbage=2
            print(garbage)
            return garbage

def noLineAct():
    saveLine=0
    savePoint=0
    countCheck==0
    while True:
        saveLine+=1
        distance=ultra.distance()
        robot.drive(DRIVE_SPEED, 0)
        if distance<120:
            grap(1)
            print("거리확인")
            break
        wait(10)
    robot.turn(180)
    while True:
        saveLine-=1
        distance=ultra.distance()
        robot.drive(DRIVE_SPEED, 0)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            countCheck=1
            savePoint=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==1 and countCheck == 0):
            robot.stop()
            break
        wait(10)
    return

def tuenBack():
    pass

def onePointCan():
    goRight(1)
    robot.turn(90)

def onePointAct():
    startLine()
    goLeft(1)
    if(objectDetection()==0):
        goLeft(1)
        twoPointAct()
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        goRight(1)
        robot.turn(-90)
        lineOut(1)
        if(garbage==1):
            goRed()
            goStart()
            goLeft(1)
            twoPointAct()
        elif(garbage==2):
            goBlue()
            goStart()
            goLeftR(1)
            twoPointAct()

def twoPointAct():
    if(objectDetection()==0):
        goLeft(1)
        threePointAct()
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        goRight(2)
        robot.turn(-90)
        lineOut(1)
        if(garbage==1):
            goRed()
            goStart()
            goLeft(3)
            threePointAct()
        elif(garbage==2):
            goBlue()
            goStart()
            goLeft(3)
            threePointAct()

def threePointAct():
    if(objectDetection()==0):
        goLeft(1)
        fourPointAct()
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        goRight(3)
        robot.turn(-90)
        lineOut(1)
        if(garbage==1):
            goRed()
            goStart()
            goLeft(4)
            fourPointAct()
        elif(garbage==2):
            goBlue()
            goStart()
            goLeft(4)
            fourPointAct()

def fourPointAct():
    if(objectDetection()==0):
        #다음줄
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        goRight(3)
        robot.turn(-90)
        lineOut(1)
        if(garbage==1):
            goRed()
            goStart()
            goLeft(4)
            fourPointAct()
        elif(garbage==2):
            goBlue()
            goStart()
            goLeft(4)
            fourPointAct()


