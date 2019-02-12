#
# Description:  Robot Edison is used as a musical instrument. He plays tones by shades on paper.
# Notes:        You can see result here: https://www.youtube.com/watch?v=iucFzno07uA
#               You can upload program to Edison robot by online EdPy environment http://edpyapp.com/#
#               Here is PDF for printing: https://github.com/ales-eri/edison-robot-ideas/raw/master/episode04-piano/piano_for_edison_robot.pdf
#               If you have some questions, ask me in comments of the video: https://www.youtube.com/watch?v=iucFzno07uA
#

import Ed

Ed.EdisonVersion = Ed.V2

Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_FAST
Ed.LineTrackerLed(Ed.ON)

TONE_COUNT = 12
density = Ed.List(12, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
interval = Ed.List(11, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#                     G6     A6     B6     C7     D7     E7     F7     G7     A7    B7    C8    R
tones = Ed.List(12, [20408, 18181, 16202, 15289, 13622, 12135, 11457, 10207, 9090, 8099, 7644, 100])


def scanAndPlayNewTone():
    Ed.PlayTone(100, 1)
    tr = Ed.ReadLineTracker()
    if tr > interval[3]:
        if tr > interval[7]:
            if tr > interval[9]:
                if tr > interval[10]:
                    new_tone = 11
                else:
                    new_tone = 10
            else:
                if tr > interval[8]:
                    new_tone = 9
                else:
                    new_tone = 8
        else:
            if tr > interval[5]:
                if tr > interval[6]:
                    new_tone = 7
                else:
                    new_tone = 6
            else:
                if tr > interval[4]:
                    new_tone = 5
                else:
                    new_tone = 4
    else:
        if tr > interval[1]:
            if tr > interval[2]:
                new_tone = 3
            else:
                new_tone = 2
        else:
            if tr > interval[0]:
                new_tone = 1
            else:
                new_tone = 0
    Ed.TimeWait(50, Ed.TIME_MILLISECONDS);
    Ed.PlayTone(tones[new_tone], 30000);


def endOfCalibrationSound():
    # crrrrr
    count = 0;
    while count < 6:
        Ed.PlayTone(5000, 80)
        Ed.PlayTone(100, 50)
        count = count + 1


def calibrateTone():
    global tone, density
    if tone >= TONE_COUNT:
        return
    tracker = Ed.ReadLineTracker()
    density[tone] = tracker
    Ed.PlayTone(tones[tone], 300);
    tone = tone + 1


# ---------- Main Program -------------

# calibration
tone = 0
Ed.RegisterEventHandler(Ed.EVENT_KEYPAD_TRIANGLE, "calibrateTone");
while tone < TONE_COUNT:
    pass
endOfCalibrationSound()

# convert densities to intervals
int = 0
while int < TONE_COUNT - 1:
    interval[int] = (density[int + 1] + density[int]) / 2
    int = int + 1

# playing tones
Ed.RegisterEventHandler(Ed.EVENT_KEYPAD_ROUND, "scanAndPlayNewTone");
while True:
    pass
