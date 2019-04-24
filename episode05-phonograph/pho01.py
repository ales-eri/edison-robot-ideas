#
# Description:  Program for the first Edison in the phonograph
#               The first Edison moves paper disc, reads outer circle values and sends signal to the second Edison.
# Notes:        You can see result here: https://www.youtube.com/watch?v=xdm1bHvwAnA
#               If you want to build the phonograph yourself, check this video: https://www.youtube.com/watch?v=JZ6SFBxVJKQ
#               You should use robot with full batteries.
#               You should prepare clean and smooth table for playing.

import Ed

Ed.EdisonVersion = Ed.V2

Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_FAST
Ed.LineTrackerLed(Ed.ON)

MESSAGE_CALIBRATE = 1
MESSAGE_LOW = 2
MESSAGE_HIGH = 3
MESSAGE_PAUSE = 4

slowingPause = 200

density0 = 0
density1 = 0
density2 = 0

inter0 = 0
inter1 = 0


def readAndCalibrate(validationStep):
    global previousTracker, density0, density1, density2
    Ed.Drive(Ed.FORWARD_LEFT, 1, 20)
    currentTracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    if validationStep > 0:
        Ed.SendIRData(MESSAGE_CALIBRATE)  # \
        Ed.SendIRData(MESSAGE_CALIBRATE)  # send three messages, because one message per 20 is lost
        Ed.SendIRData(MESSAGE_CALIBRATE)  # /
    if validationStep == 1:  # start from 1 (second calibration reading), we reduce the possibility of reading value from border
        density0 = currentTracker
    elif validationStep == 2:
        density1 = currentTracker
    elif validationStep == 3:
        density2 = currentTracker
    previousTracker = currentTracker
    Ed.TimeWait(250, Ed.TIME_MILLISECONDS)
    Ed.DriveRightMotor(Ed.FORWARD, 1, Ed.DISTANCE_UNLIMITED)


def sendPlayMessage(previousColor, currentColor):
    testButton()
    if currentColor == 0:
        message = MESSAGE_LOW
    elif currentColor == 1:
        if previousColor == 0:
            message = MESSAGE_LOW
        else:
            message = MESSAGE_HIGH
    else:
        message = MESSAGE_HIGH
    if previousColor > -1:
        Ed.SendIRData(message)  # \
        Ed.SendIRData(message)  # send three messages, because one message per 20 is lost
        Ed.SendIRData(message)  # /
    Ed.TimeWait(slowingPause, Ed.TIME_MILLISECONDS)
    Ed.DriveRightMotor(Ed.FORWARD, 1, Ed.DISTANCE_UNLIMITED)


# pause playing and change speed
# - test if round button is pressed, than wait to triangle button is pressed
# - test if triangle button is pressed, than change playing speed
def testButton():
    global slowingPause;
    keypad = Ed.ReadKeypad()
    if keypad == Ed.KEYPAD_ROUND:
        Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 1)
        Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 1)
        Ed.SendIRData(MESSAGE_PAUSE)  # \
        Ed.SendIRData(MESSAGE_PAUSE)  # send three messages, because one message from 20 is lost
        Ed.SendIRData(MESSAGE_PAUSE)  # /
        while Ed.ReadKeypad() != Ed.KEYPAD_TRIANGLE:
            pass
        Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0)
        Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 0)
    elif keypad == Ed.KEYPAD_TRIANGLE:
        if slowingPause == 350:
            slowingPause = 200
        elif slowingPause == 200:
            slowingPause = 80
        elif slowingPause == 80:
            slowingPause = 350
        i = 0
        while i < 3:
            Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 1)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 1)
            Ed.TimeWait(20, Ed.TIME_MILLISECONDS)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 0)
            Ed.TimeWait(20, Ed.TIME_MILLISECONDS)
            i = i + 1


# calibration phase
previousTracker = 9999
validationStep = 0
Ed.DriveRightMotor(Ed.FORWARD, 1, Ed.DISTANCE_UNLIMITED)
while validationStep < 7:
    tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    if tracker > previousTracker:
        if tracker - previousTracker > 150:
            Ed.DriveRightMotor(Ed.STOP, 1, Ed.DISTANCE_UNLIMITED)
            Ed.TimeWait(400, Ed.TIME_MILLISECONDS)
            readAndCalibrate(validationStep)
            validationStep = validationStep + 1
    else:
        if previousTracker - tracker > 150:
            Ed.DriveRightMotor(Ed.STOP, 1, Ed.DISTANCE_UNLIMITED)
            Ed.TimeWait(400, Ed.TIME_MILLISECONDS)
            readAndCalibrate(validationStep)
            validationStep = validationStep + 1
Ed.DriveRightMotor(Ed.STOP, 1, Ed.DISTANCE_UNLIMITED)

# convert densities to interval
# calibration is independent of starting point, we need find the lowest shade
if density2 > density0:
    inter0 = (density0 + density1) / 2
    inter1 = (density1 + density2) / 2
    inter0plus = inter0 + (density1 - density0) / 5
    inter0minus = inter0 - (density1 - density0) / 5
    inter1plus = inter1 + (density2 - density1) / 5
    inter1minus = inter1 - (density2 - density1) / 5
elif density0 > density1:
    inter0 = (density1 + density2) / 2
    inter1 = (density2 + density0) / 2
    inter0plus = inter0 + (density2 - density1) / 5
    inter0minus = inter0 - (density2 - density1) / 5
    inter1plus = inter1 + (density0 - density2) / 5
    inter1minus = inter1 - (density0 - density2) / 5
else:
    inter0 = (density2 + density0) / 2
    inter1 = (density0 + density1) / 2
    inter0plus = inter0 + (density0 - density2) / 5
    inter0minus = inter0 - (density0 - density2) / 5
    inter1plus = inter1 + (density1 - density0) / 5
    inter1minus = inter1 - (density1 - density0) / 5

# wait to press triangle
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 1)
Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 1)
while Ed.ReadKeypad() != Ed.KEYPAD_TRIANGLE:
    pass
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0)
Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 0)

# playing
previousColor = -1
# this ugly while-if-while construction is for speed up Edison reaction time
# we need 32 shades per disk on A4 paper, because it is typical kid song length, but it is on Edison limits
while True:
    Ed.DriveRightMotor(Ed.FORWARD, 1, Ed.DISTANCE_UNLIMITED)
    tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    if tracker < inter0:
        tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
        while tracker < inter0plus:
            tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    elif tracker < inter1:
        tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
        while tracker > inter0minus and tracker < inter1plus:
            tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    else:
        tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
        while tracker > inter1minus:
            tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    Ed.TimeWait(10, Ed.TIME_MILLISECONDS)  # wait to move from border to full shade
    Ed.DriveRightMotor(Ed.STOP, 1, Ed.DISTANCE_UNLIMITED)
    tracker = Ed.ReadModuleRegister16Bit(Ed.MODULE_LINE_TRACKER, Ed.REG_LT_LEVEL_16)
    if tracker < inter0:
        currentColor = 0
    elif tracker < inter1:
        currentColor = 1
    else:
        currentColor = 2
    sendPlayMessage(previousColor, currentColor)
    previousColor = currentColor
