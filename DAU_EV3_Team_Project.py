#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pyhuskylens import *

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.

ev3 = EV3Brick()

grab_moter=Motor(Port.A)
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

left_cs =ColorSensor(Port.S3)
right_cs =ColorSensor(Port.S4)

ultra=UltrasonicSensor(Port.S2)

hl=HuskyLens(Port.S1, debug=False)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# BLACK = 9
# WHITE = 85=4
BLACK=8 #4
WHITE = 63  #60
threshold = (BLACK + WHITE) / 2

DRIVE_SPEED = 250

PROPORTIONAL_GAIN = 0.7

global garbage
garbage = 1

def startLine():
    while True:
        robot.drive(DRIVE_SPEED, 0)
        if(right_cs.color()==Color.BLACK and left_cs.color()!=Color.GREEN and right_cs.color()!=Color.GREEN):
            #robot.stop()
            break
    wait(10)
    while True:
        deviation = threshold-left_cs.reflection()
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED, -turn_rate)        
        if(right_cs.color()!=Color.BLACK):
            #robot.stop()
            break
    wait(10)
    return

def lineOut(num1):
    while True:
        if(num1==0):
            if(right_cs.color()==Color.BLACK and left_cs.color()==Color.BLACK):
                robot.drive(20, 0)
            else:
                break
        elif(num1==1):
            if(right_cs.color()==Color.BLACK):
                robot.drive(20, 0)
            else:
                break
        
        else:
            if(left_cs.color()==Color.BLACK):
                robot.drive(20, 0)
            else:
                break
    wait(10)
    return

def lineOut2():
    while True:
        if(left_cs.reflection()<threshold):
            robot.drive(30, 0)
        else:
            break
    wait(10)

def lineBackOut(num):
    while True:
        if(right_cs.color()!=Color.BLACK and num == 0):
            robot.stop()
            break
        elif(left_cs.color()!=Color.BLACK and num == 1):
            robot.stop()
            break
        robot.drive(-DRIVE_SPEED, 0)   
    wait(10)

def turnLine():
    while True:
        if(right_cs.color()==Color.BLACK and left_cs.color()==Color.BLACK):
            robot.stop()
            break
        robot.drive(-DRIVE_SPEED, 0)
    wait(10)
    return

def turnLineWhite():
    while True:
        if((right_cs.color()==Color.WHITE or left_cs.color()==Color.WHITE) and left_cs.color()!=Color.BLUE and right_cs.color()!=Color.BLUE):
        #if(right_cs.reflection()>40 or left_cs.reflection()>40):
            robot.stop()
            break
        robot.drive(-DRIVE_SPEED, 0)#스피드 200
    wait(10)
    return

def backRobotLine(speed):
    savePoint=0
    countCheck=0
    while True:
        robot.drive(-DRIVE_SPEED*speed, 0)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()==Color.WHITE and countCheck==1):
            countCheck=0
        if(savePoint==2):
            robot.stop()
            break
    robot.turn(90)
    wait(10)

def backRobotLineL(speed, num):
    savePoint=0
    countCheck=0
    while True:
        robot.drive(-DRIVE_SPEED*speed, 0)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()==Color.WHITE and countCheck==1):
            countCheck=0
        if(savePoint==num):
            robot.stop()
            break
    wait(10)

def goLeft(num, speed):

    savePoint=0
    countCheck=0
    while True:
        deviation = left_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
            ev3.speaker.beep()
        if(savePoint==num and countCheck == 0):
            robot.stop()
            break
    wait(10)

def goBackLeft(num, speed):
    savePoint=0
    countCheck=0
    threshold=20
    while True:
        deviation = threshold-left_cs.reflection()
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(-DRIVE_SPEED*speed, turn_rate)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        
        if(savePoint==num):
            robot.stop()
            break
    wait(10)

def goLeftR(num, speed):
    savePoint=0
    countCheck=0
    while True:
        
        deviation = threshold-left_cs.reflection() 
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()!=Color.BLACK and countCheck==1):
            wait(5)
            countCheck=0
        if(savePoint==num and countCheck == 0):
            robot.stop()
            break
    wait(10)

def goRight(num, speed):
    savePoint=0
    countCheck=0
    while True:
        deviation = threshold-right_cs.reflection()
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            ev3.speaker.beep()
            countCheck=0
        if(savePoint==num and countCheck == 0):
            robot.stop()
            break
    wait(10)

def goRight2(num, speed):
    savePoint=0
    countCheck=0
    while True:
        if(left_cs.reflection()>threshold):
            deviation = threshold-right_cs.reflection()
            turn_rate = PROPORTIONAL_GAIN * deviation
            robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(left_cs.reflection()<=threshold):
            robot.drive(DRIVE_SPEED*speed, 0)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            ev3.speaker.beep()
            countCheck=0
        if(savePoint==num):
            break
    robot.stop()

def goRightR(num, speed):
    savePoint=0
    countCheck=0
    while True:
        deviation = right_cs.reflection()-threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==num and countCheck == 0):
            robot.stop()
            break
    wait(10)



def goRed(speed):
    goLeft(1, 1)
    robot.turn(90)
    while True:
        deviation = left_cs.reflection() - threshold#왼쪽으로 바꿔봐야함
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(right_cs.color()==Color.RED):
            robot.stop()
            ev3.speaker.beep()
            break
    wait(50)
    grap(-1)
    wait(10)

def goBlue(speed):
    goLeft(2, 1)
    robot.turn(90)
    while True:
        deviation = left_cs.reflection() - threshold#왼쪽으로 바꿔봐야함
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(right_cs.color()==Color.BLUE):
            robot.stop()
            ev3.speaker.beep()
            break
    wait(50)
    grap(-1)
    wait(10)

def goStart():
    turnLineWhite()
    robot.turn(90)
    if(garbage==1):
        goLeftR(1, 1)
        robot.turn(90)
        lineOut(1)
        return
    elif(garbage==2):
        goLeftR(2, 1)
        robot.turn(90)
        lineOut(1)
        return
    wait(10)

def grap(num):
    grab_moter.run_until_stalled(num*200, then=Stop.COAST, duty_limit=50)

# def goGarbageLeft():
#     while True:
#         distance=ultra.distance()
#         deviation = left_cs.reflection() - threshold
#         turn_rate = PROPORTIONAL_GAIN * deviation
#         speedX=DRIVE_SPEED*distance/80
#         if(speedX>DRIVE_SPEED):
#             speedX=DRIVE_SPEED
#         robot.drive(speedX, turn_rate)
#         print(distance)
#         if distance<55:
#             robot.straight(40)
#             robot.stop()
#             print("거리확인")
#             break
#     grap(1)

def goGarbageLeft():
    countCheck=0
    savePoint=0
    saveSpeed=300
    while True:
        distance=ultra.distance()
        speedX=DRIVE_SPEED*distance/100
        if(saveSpeed>speedX):
            saveSpeed=speedX
        if(saveSpeed>DRIVE_SPEED):
            saveSpeed=DRIVE_SPEED
        deviation = left_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(saveSpeed, turn_rate)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(right_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==1 and countCheck == 0):
            robot.stop()
            break
    grap(1)
    wait(10)

def goGarbageRight():
    countCheck=0
    savePoint=0
    saveSpeed=300
    while True:
        distance=ultra.distance()
        speedX=DRIVE_SPEED*distance/100
        if(saveSpeed>speedX):
            saveSpeed=speedX
        if(saveSpeed>DRIVE_SPEED):
            saveSpeed=DRIVE_SPEED
        deviation = threshold-right_cs.reflection()
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(saveSpeed, turn_rate)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            savePoint+=1
            countCheck=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==1 and countCheck == 0):
            robot.stop()
            break
    robot.straight(40)
    wait(20)
    grap(1)

# def goGarbageLeft():
#     savePoint=0
#     countCheck=0
#     while True:
#         deviation = left_cs.reflection() - threshold
#         turn_rate = PROPORTIONAL_GAIN * deviation
#         robot.drive(DRIVE_SPEED, turn_rate)
#         print(right_cs.color())
#         if(right_cs.color()==Color.BLACK):
#             robot.stop()
#             break
#     grap(1)
#     while True:
#         deviation = threshold-left_cs.reflection()
#         turn_rate = PROPORTIONAL_GAIN * deviation
#         robot.drive(-DRIVE_SPEED, turn_rate)
#         if(right_cs.color()==Color.WHITE):
#             robot.stop()
#             break

def objectDetection():
    time=0
    distance=ultra.distance()
    if distance<500:
        print("물체인식")
        print(distance)
        seeGarbage()
        return 1
    # elif distance>500 and time<10:
    #     time+=1
    #     print("재시도")
    else :
        print("물체없음")
        print(distance)
        return 0
        
# def objectDetection():
#     time=10
#     while True:
#         distance=ultra.distance()
#         time-=1
#     if distance<500:
#         print("물체인식")
#         print(distance)
#         seeGarbage()
#         return 1
#     # elif distance>500 and time<10:
#     #     time+=1
#     #     print("재시도")
#     else :
#         print("물체없음")
#         print(distance)
#         return 0


# def seeGarbage():
#     while True:
#         blocks=hl.get_blocks()
#         if len(blocks) > 0:
#             ID =blocks[0].ID
#         if ID==1:
#             ev3.speaker.beep()
#             garbage=1
#             print(garbage)
#             return garbage
#         elif ID==2:
#             ev3.speaker.beep()
#             garbage=2
#             print(garbage)
#             return garbage

def seeGarbage():
    global garbage
    garbage=2
    print(garbage)
    return garbage

def noLineAct(speed):
    saveLine=0
    savePoint=0
    countCheck=0
    saveSpeed=300
    while True:
        distance=ultra.distance()
        speedX=DRIVE_SPEED*distance/100
        if(saveSpeed>speedX):
            saveSpeed=speedX
        if(saveSpeed>DRIVE_SPEED):
            saveSpeed=DRIVE_SPEED
        saveLine+=1
        robot.drive(saveSpeed, 0)
        if distance<45:
            robot.straight(30)
            robot.stop()
            print("거리확인")
            break
    grap(1)
    #lineSet()
    lineBackOut(0)
    wait(10)
    while True:
        saveLine-=1
        robot.drive(-DRIVE_SPEED*speed, 0)
        if(right_cs.color()==Color.BLACK and countCheck==0):
            countCheck=1
            savePoint=1
        if(right_cs.color()!=Color.BLACK and countCheck==1):
            countCheck=0
        if(savePoint==1 and countCheck == 0):
            robot.stop()
            print('잡기 끝')
            break
    wait(10)
    return

def tuenBack():
    pass

def onePointCan():
    goRight(1, 1)
    robot.turn(90)

def noLineStright(speed):
    countCheck=0
    while True:
        robot.drive(DRIVE_SPEED*speed, 0)
        if(left_cs.color()==Color.BLACK):
            countCheck=1
        if(left_cs.color()==Color.WHITE and countCheck==1):
            robot.stop()
            break
    wait(10)

def noLineStright2(speed):
    countCheck=0
    savePoint=0
    while True:
        robot.drive(DRIVE_SPEED*speed, 0)
        if(left_cs.color()==Color.BLACK and countCheck==0):
            countCheck=1
            savePoint+=1
        if(left_cs.color()!=Color.BLACK and countCheck==1):
            ev3.speaker.beep()
            countCheck=0
        if(savePoint==1 and countCheck==0):
            robot.stop()
            break
    wait(10)
    robot.straight(40)

def noLineStrightR(speed):
    countCheck=0
    while True:
        robot.drive(DRIVE_SPEED*speed, 0)
        if(right_cs.color()==Color.BLACK):
            countCheck=1
        if(right_cs.color()==Color.WHITE and countCheck==1):
            robot.stop()
            break
    wait(10)

def goRed1(speed):
    countCheck=0
    PROPORTIONAL_GAIN_1=PROPORTIONAL_GAIN*1.2
    print('브레이크')
    # while True:
    #     robot.drive(DRIVE_SPEED*speed, 0)
    #     if(right_cs.color()==Color.RED):
    #         robot.stop()
    #         ev3.speaker.beep()
    #         break
    
    redSecondary(speed)
    grap(-1)

def redSecondary(speed):
    while True:
        deviation = threshold-right_cs.reflection()
        #deviation = threshold-right_cs.reflection()
        turn_rate = PROPORTIONAL_GAIN_1 * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(left_cs.color()==Color.BLACK):
            #robot.stop()
            ev3.speaker.beep()
            break
    while True:
        robot.drive(DRIVE_SPEED*speed, 0)
        if(left_cs.color()==Color.RED):
            ev3.speaker.beep()
            robot.stop()
            break
    wait(10)

def blueSecondary(speed):
    while True:
        deviation = left_cs.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        robot.drive(DRIVE_SPEED*speed, turn_rate)
        if(right_cs.color()==Color.BLACK):
            ev3.speaker.beep()
            #ev3.speaker.beep()
            break
    while True:
        robot.drive(DRIVE_SPEED*speed, 0)
        if(left_cs.color()==Color.BLUE):
            ev3.speaker.beep()
            robot.stop()
            break
    wait(10)

def goBlue1(speed):
    countCheck=0
    while True:
        robot.drive(DRIVE_SPEED*speed, 0)
        if(right_cs.color()==Color.BLACK):
            countCheck=1
        if(right_cs.color()==Color.WHITE and countCheck==1):
            robot.stop()
            break
    print('브레이크')
    # while True:
    #     robot.drive(DRIVE_SPEED*speed, 0)
    #     if(right_cs.color()==Color.RED):
    #         robot.stop()
    #         ev3.speaker.beep()
    #         break
    robot.straight(70)
    robot.turn(-90)
    goLeft(1, 1)
    robot.turn(90)
    blueSecondary(speed)
    grap(-1)
    wait(10)

def onePointAct():
    wait(50)
    print('1번액트')
    startLine()

    goLeft(1, 1)
    if(objectDetection()==0):
        goLeft(1, 1)
        twoPointAct()
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        lineOut(2)
        goRight(1, 1)
        robot.straight(40)
        robot.turn(-90)

        lineOut(1)

        if(garbage==1):

            goRed(0.5)
            backRobotLine(0.5)
            goLeftR(1,1)
            robot.turn(90)
            goLeft(1, 1)
            twoPointAct()
            # goStart()
            # goLeft(2, 1)
            # twoPointAct()
        elif(garbage==2):
            goBlue(0.5)
            backRobotLine(0.5)
            goLeftR(1,1)
            robot.turn(90)
            goLeft(1, 1)
            twoPointAct()
            # goStart()
            # goLeft(2, 1)
            # twoPointAct()

# def onePointAct():
#     print('1번액트')
#     startLine()
#     goLeft(1, 1.5)
#     if(objectDetection()==0):
#         goLeft(1, 1.5)
#         twoPointAct()
#         return
#     elif(objectDetection()==1):
#         seeGarbage()
#         goGarbageLeft()
#         #lineBackOut()
        
#         goBackLeft(1,1.5)
#         robot.straight(20)
#         robot.turn(90)

#         lineOut(1)

#         if(garbage==1):

#             goRed(1)
#             goStart()
#             goLeft(2, 1)
#             twoPointAct()
#         elif(garbage==2):
#             goBlue(1)
#             goStart()
#             goLeft(2, 1)
#             twoPointAct()

def twoPointAct():
    wait(50)
    print('2번액트')
    if(objectDetection()==0):
        goLeft(1, 1)
        threePointAct()
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        lineOut(2)
        goRight(2, 1)
        robot.straight(40)
        robot.turn(-90)
        lineOut(1)

        if(garbage==1):
            # goRed(0.5)
            # goStart()
            # goLeft(3, 1)
            # threePointAct()

            goRed(0.5)
            backRobotLine(0.5)
            goLeftR(1,1)
            robot.turn(90)
            goLeft(2, 1)
            threePointAct()
        elif(garbage==2):
            # goBlue(0.5)
            # goStart()
            # goLeft(3, 1)
            # threePointAct()

            goBlue(0.5)
            
            backRobotLine(0.5)
            goLeftR(1,1)
            robot.turn(90)
            goLeft(2, 1)
            threePointAct()

# def twoPointAct():
#     print('2번액트')
#     if(objectDetection()==0):
#         goLeft(1, 1)
#         threePointAct()
#         return
#     elif(objectDetection()==1):
#         seeGarbage()
#         goGarbageLeft()

#         goBackLeft(2,1.5)
#         robot.straight(20)
#         robot.turn(90)
#         lineOut(1)

#         if(garbage==1):
#             goRed(1)
#             goStart()
#             goLeft(3, 1)
#             threePointAct()
#         elif(garbage==2):
#             goBlue(1)
#             goStart()
#             goLeft(3, 1)
#             threePointAct()
def threePointAct():
    #ev3.speaker.beep()
    print('3번액트')
    if(objectDetection()==0):
        lineOut(2)
        goLeft(1, 1)
        wait(20)
        fourPointAct()
        return
    elif(objectDetection()==1):
        seeGarbage()
        goGarbageLeft()
        robot.turn(180)
        lineOut(2)
        goRight(3, 1)
        robot.straight(40)
        robot.turn(-90)
        lineOut(1)
        if(garbage==1):
            # goRed(1)
            # goStart()
            # goLeft(4, 1)
            # fourPointAct()

            goRed(0.5)
            backRobotLine(0.5)
            goLeftR(1,1)
            robot.turn(90)
            goLeft(3, 1)
            fourPointAct()
        elif(garbage==2):
            # goBlue(1)
            # goStart()
            # goLeft(4, 1)
            # fourPointAct()

            goBlue(0.5)
            backRobotLine(0.5)
            goLeftR(1,1)
            robot.turn(90)
            goLeft(3, 1)
            fourPointAct()

def fourPointAct():
    #ev3.speaker.beep()
    #wait(50)
    print('4번액트')
    if(objectDetection()==0):
        # #다음줄
        robot.turn(180)
        wait(10)
        fivePointAct1()
    elif(objectDetection()==1):
        print('마지막')
        seeGarbage()
        noLineAct(1)
        robot.turn(180)
        lineOut(2)
        goRight(3, 1)
        robot.straight(40)
        robot.turn(-90)
        lineOut(1)
        if(garbage==1):
            print('1번 실행함 ㅋㅋ')
            # goRed(1)
            # goStart()
            # goLeft(5, 1)
            # fourPointAct()
            goRed(1)
            backRobotLineL(0.5, 2)
            robot.turn(180)
            fivePointAct2()
        elif(garbage==2):
            print('2번 실행함 ㅋㅋ')
            # goBlue(1)
            # goStart()
            # goLeft(5, 1)
            goBlue(0.6)
            backRobotLineL(0.5, 2)
            robot.straight(60)
            robot.turn(90)
            lineOut(2)
            goRight(1,1)
            robot.turn(90)
            fivePointAct2()

def fivePointAct1():
    print('5-1번액트')
    # robot.turn(180)
    # lineOut(2)
    goRight(2, 1)
    wait(30)
    robot.turn(-90)
    goGarbageRight()
    robot.turn(90)
    wait(10)
    if(garbage==1):
        goRed3()
        sixPointAct()
    elif(garbage==2):
        goBlue3()
        sixPointAct()

def goRed3():
    lineOut(0)
    wait(30)
    noLineStright(0.6)
    goRed1(0.4)
    backRobotLineL(0.5, 3)
    robot.turn(180)
    wait(10)

def goBlue3():
    lineOut(0)
    goBlue1(0.5)
    backRobotLineL(0.5, 2)
    #robot.straight(50)
    noLineStrightR(0.5)
    robot.turn(90)
    goRight(1, 1)
    robot.turn(90)
    noLineStright(0.6)
    wait(10)

def fivePointAct2():
    print('5-2번액트')
    wait(10)
    if(objectDetection()==0):
        noLineStrightR(0.6)
    elif(objectDetection()==1):
        seeGarbage()
        noLineAct(0.6)
        if(garbage==1):
            robot.turn(180)
            redSecondary(0.6)
            wait(10)
            grap(-1)
            backRobotLineL(0.5, 3)
            robot.turn(180)
            sixPointAct()
        elif(garbage==2):
            noLineStrightR(0.5)
            robot.turn(90)
            goLeft(1, 1)
            robot.turn(90)
            blueSecondary(0.6)
            grap(-1)
            backRobotLineL(0.5, 2)
            #noLineStrightR(0.5)
            robot.straight(60)
            robot.turn(90)
            lineOut(2)
            goRight(1, 1)
            robot.straight(-40)
            robot.turn(90)
            wait(10)
            lineOut(0)
            noLineStrightR(0.6)
            sixPointAct()

def goBlue4():
    robot.turn(-90)
    goLeft(1, 1)
    robot.turn(90)
    blueSecondary(0.6)
    grap(-1)
    backRobotLineL(0.5, 2)
    #noLineStrightR(0.5)
    robot.straight(60)
    robot.turn(90)
    lineOut(2)
    goRight(1, 1)
    robot.straight(-25)
    robot.turn(90)
    wait(10)
    lineOut(0)
    noLineStrightR(0.6)

def goRed4():
    redSecondary(0.6)
    wait(10)
    grap(-1)
    backRobotLineL(0.5, 3)
    robot.turn(180)

def sixPointAct():
    print('6번액트')
    if(objectDetection()==0):
        lineOut(1)
        goLeft(1,1)
        sevenPointAct()
    elif(objectDetection()==1):
        lineOut(1)
        seeGarbage()
        goGarbageLeft()
        robot.turn(-180)
        wait(10)
        goRight2(1, 1)
        lineOut(0)
        wait(10)
        if(garbage==1):
            noLineStright2(0.6)
            goRed4()
            lineOut(1)
            goLeft(1,1)
            sevenPointAct()
        elif(garbage==2):
            noLineStright2(0.6)
            goBlue4()
            lineOut(1)
            goLeft(1,1)
            sevenPointAct()

def sevenPointAct():
    print('6번액트')
    if(objectDetection()==0):
        lineOut(1)
        goLeft(1,1)
        eightPointAct()
    elif(objectDetection()==1):
        lineOut(1)
        seeGarbage()
        goGarbageLeft()
        robot.turn(-180)
        wait(10)
        lineOut(2)
        goRight2(2, 1)
        lineOut(0)
        if(garbage==1):
            wait(10)
            noLineStright2(0.6)
        
            lineOut(2)
            goRed4()
            lineOut(1)
            goLeft(2,1)
            eightPointAct()
        elif(garbage==2):
            wait(10)
            noLineStright2(0.6)
            lineOut(2)
            goBlue4()
            lineOut(1)
            goLeft(2,1)
            eightPointAct()

def eightPointAct():
    print('8번액트')
    if(objectDetection()==0):
        robot.turn(180)
        wait(10)
        return
    elif(objectDetection()==1):
        print('마지막')
        seeGarbage()
        noLineAct(1)
        robot.turn(180)
        lineOut(2)
        goRight2(2, 1)
        wait(10)
        if(garbage==1):
            print('1번 실행함 ㅋㅋ')
            noLineStright2(0.6)
        
            lineOut(2)
            goRed4()
            lineOut(1)
            goLeft(2,1)
            eightPointAct()
        elif(garbage==2):
            print('2번 실행함 ㅋㅋ')
            noLineStright2(0.6)
            lineOut(2)
            goBlue4()
            lineOut(1)
            goLeft(2,1)
            eightPointAct()
            
# b=0
# while True:
#     b+=1
#     right_motor.run(300)
#     if(b==1000):
#         print('스탑')
#         robot.stop()
#         break
# while True:
#     print(ultra.distance())
#ev3.speaker.beep()

def rateSet():
    while True:
        print(left_cs.reflection())
        print(right_cs.reflection())
        #if(left_cs.reflection() <15 or right_cs.reflection() <15):
        if(left_cs.color()==WHITE or right_cs.color()==WHITE):
            robot.stop()
            break
        robot.drive(DRIVE_SPEED*0.1, 0)
    while True:
        print(left_cs.reflection())
        print(right_cs.reflection())
        if(left_cs.reflection()-right_cs.reflection()>30):
            left_motor.run(20)
            right_motor.run(-20)
        elif(left_cs.reflection()-right_cs.reflection()<30):
            right_motor.run(20)
            left_motor.run(-20)
        else :
            print('완벽')
            break


def lineSet():
    while True:
        print(left_cs.color())
        print(right_cs.color())
        
        if(left_cs.color()==Color.BLACK and right_cs.color()==Color.BLACK):
            #robot.drive(-DRIVE_SPEED, 0)
            robot.stop()
            break
        if(left_cs.color()==Color.WHITE and right_cs.color()==Color.WHITE):
            robot.drive(DRIVE_SPEED, 0)
        if(left_cs.color()==Color.WHITE and right_cs.color()==Color.BLACK):
            robot.turn(5)
        if(left_cs.color()==Color.BLACK and right_cs.color()==Color.WHITE):
            robot.turn(-5)
    return

# backRobotLine(0.5)
# while True:
#     print(left_cs.reflection())
#     print(right_cs.reflection())
#     if(left_cs.reflection()-right_cs.reflection()>4):78  
#         #left_motor.run(-20)
#         right_motor.run(20)
#         pass
#     elif(left_cs.reflection()-right_cs.reflection()<4):
#         #right_motor.run(-20)
#         left_motor.run(20)
#         pass
#     else :
#         robot.stop()
#         print('완벽')
#         break
#rateSet()
# while True:
#     left_motor.run(400)
#     wait(2000)
#     break
grap(-1)
#onePointAct()
fivePointAct2()
#goRight2(1, 1)
