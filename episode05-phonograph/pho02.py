#
# Description:  Program for the second Edison in the phonograph
#               The second Edison waits for signal from the first Edison, reads inner circle values and plays tones.
# Notes:        You can see result here: https://www.youtube.com/watch?v=xdm1bHvwAnA
#               If you want to build the phonograph yourself, check this video: https://www.youtube.com/watch?v=JZ6SFBxVJKQ
#               You should use robot with full batteries.
#               You should prepare clean and smooth table for playing.

import Ed

Ed.EdisonVersion = Ed.V2

Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_FAST
Ed.LineTrackerLed(Ed.ON)

DENSITY_COUNT = 6
density = Ed.List(6, [0, 0, 0, 0, 0, 0])
interval = Ed.List(4, [0, 0, 0, 0])
#                     C7     D7     E7     F7     G7     A7    B7    C8    R
tones = Ed.List(9, [15289, 13622, 12135, 11457, 10207, 9090, 8099, 7644, 100])

MESSAGE_EMPTY = 0
MESSAGE_CALIBRATE = 1
MESSAGE_LOW = 2
MESSAGE_HIGH = 3
MESSAGE_PAUSE = 4


def endOfCalibrationSound():
    # crrrrr
    count = 0;
    while count < 10:
        Ed.PlayTone(5000, 80)
        Ed.PlayTone(100, 50)
        count = count + 1


def calibrateDensities():
    global densityIndex, density
    if densityIndex >= DENSITY_COUNT:
        return
    tracker = Ed.ReadLineTracker()
    density[densityIndex] = tracker
    Ed.PlayTone(tones[0], 200);
    densityIndex = densityIndex + 1


def convertDensitiesToInterval():
    global interval

    # calibration is independent of starting point, we need to find the lowest shade
    lowerDensity = 32000
    index = 0
    startIndex = 0
    while index < DENSITY_COUNT:
        if density[index] < lowerDensity:
            lowerDensity = density[index]
            startIndex = index
        index = index + 1

    int = 0
    while int < DENSITY_COUNT - 2:  # we have two white on calibration disc (second will be ignored)
        firstIndex = int + startIndex
        secondIndex = int + startIndex + 1
        if firstIndex > DENSITY_COUNT - 1:
            firstIndex = firstIndex - DENSITY_COUNT
        if secondIndex > DENSITY_COUNT - 1:
            secondIndex = secondIndex - DENSITY_COUNT
        interval[int] = (density[firstIndex] + density[secondIndex]) / 2
        int = int + 1


def readMessage():
    global processingLock
    message = Ed.ReadIRData();
    if processingLock == 0:  # lock and ignore messages during processing
        processingLock = 1  # /
        if message == MESSAGE_EMPTY:  # ignore no message
            pass
        elif message == MESSAGE_PAUSE:  # pause playing, than user can change disc
            Ed.PlayTone(100, 1)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 1)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 1)
        elif message == MESSAGE_CALIBRATE:
            calibrateDensities()
        else:
            Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 1)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 1)
            tr = Ed.ReadLineTracker()
            if tr > interval[3]:
                if message == MESSAGE_LOW:
                    new_tone = 4
                else:
                    new_tone = 9
            else:
                if tr > interval[1]:
                    if tr > interval[2]:
                        if message == MESSAGE_LOW:
                            new_tone = 3
                        else:
                            new_tone = 8
                    else:
                        if message == MESSAGE_LOW:
                            new_tone = 2
                        else:
                            new_tone = 7
                else:
                    if tr > interval[0]:
                        if message == MESSAGE_LOW:
                            new_tone = 1
                        else:
                            new_tone = 6
                    else:
                        if message == MESSAGE_LOW:
                            new_tone = 0
                        else:
                            new_tone = 5
            if new_tone < 9:
                Ed.PlayTone(100, 1)
                Ed.TimeWait(30, Ed.TIME_MILLISECONDS);
                Ed.PlayTone(tones[new_tone], 30000);
            else:  # tone 9 = extend tone from last play = do nothing
                Ed.TimeWait(30, Ed.TIME_MILLISECONDS);
            Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0)
            Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 0)
        Ed.ReadIRData()
        Ed.ReadIRData()
        processingLock = 0  # release lock


Ed.RegisterEventHandler(Ed.EVENT_IR_DATA, "readMessage");
processingLock = 0

# calibration
densityIndex = 0
while densityIndex < DENSITY_COUNT:
    pass
endOfCalibrationSound()

# convert densities to intervals
convertDensitiesToInterval();

Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 1)
Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 1)

# wait to message
while True:
    pass
