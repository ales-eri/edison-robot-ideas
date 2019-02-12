#
# Description:  Edison robot plays "Turkish March" by Wolfgang Amadeus Mozart.
# Notes:        You can listen result here: https://www.youtube.com/watch?v=1Cfpv6s_xrY
#               You can upload program to Edison robot by online EdPy environment http://edpyapp.com/#
#               This is the first voice only. I wrote three programs (one for every voice),
#               but I had to modify it for every my robot, because they run program in different speed. I do not know why.
#               If you have some questions, ask me in comments of the video: https://www.youtube.com/watch?v=1Cfpv6s_xrY
#

import Ed

Ed.EdisonVersion = Ed.V2

Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_FAST

tones = Ed.List(46, [
    32396,  # 00   B5   987.767 Hz
    30578,  # 01   C6  1046.502 Hz
    28862,  # 02  #C6  1108.731 Hz
    27242,  # 03   D6  1174.659 Hz
    25713,  # 04  #D6  1244.508 Hz
    24270,  # 05   E6  1318.510 Hz
    22908,  # 06   F6  1396.913 Hz
    21622,  # 07  #F6  1479.978 Hz
    20408,  # 08   G6  1567.982 Hz
    19263,  # 09  #G6  1661.219 Hz
    18181,  # 10   A6  1760.000 Hz
    17161,  # 11  #A6  1864.655 Hz
    16202,  # 12   B6  1975.533 Hz
    15289,  # 13   C7  2093.005 Hz
    14431,  # 14  #C7  2217.461 Hz
    13622,  # 15   D7  2349.318 Hz
    12856,  # 16  #D7  2489.016 Hz
    12135,  # 17   E7  2637.021 Hz
    11457,  # 18   F7  2793.826 Hz
    10811,  # 19  #F7  2959.956 Hz
    10207,  # 20   G7  3135.964 Hz
    9631,  # 21  #G7  3322.438 Hz
    9090,  # 22   A7  3520.000 Hz
    8581,  # 23  #A7  3729.310 Hz
    8099,  # 24   B7  3951.066 Hz
    7645,  # 25   C8  4186.009 Hz
    7215,  # 26  #C8  4434.922 Hz
    6810,  # 27   D8  4698.637 Hz
    6428,  # 28  #D8  4978.032 Hz
    6067,  # 29   E8  5274.042 Hz
    5727,  # 30   F8  5587.652 Hz
    5405,  # 31  #F8  5919.912 Hz
    5102,  # 32   G8  6271.928 Hz
    4816,  # 33  #G8  6644.876 Hz
    4545,  # 34   A8  7040.000 Hz
    4290,  # 35  #A8  7458.620 Hz
    4050,  # 36   B8  7902.133 Hz
    3822,  # 37   C9  8372.019 Hz
    3608,  # 38  #C9  8869.845 Hz
    3405,  # 39   D9  9397.273 Hz
    3214,  # 40  #D9  9956.064 Hz
    3034,  # 41   E9 10548.083 Hz
    2863,  # 42   F9 11175.305 Hz
    2703,  # 43  #F9 11839.823 Hz
    2551,  # 44   G9 12543.855 Hz
    2408])  # 45  #G9 13289.752 Hz

# transpose music up or down
#TRANSPOSITION = -6
TRANSPOSITION = -10

# tone length constants (duration + action)
LENGTH_0 = 0
LENGTH_1 = 1 | 128
LENGTH_2 = 2 | 128
LENGTH_4 = 4 | 128
LENGTH_8 = 8 | 128
LENGTH_16 = 16 | 128


# This method must be called eighth time in every 2/4 measure or twelve time in 3/4 measure
#
# Inputs:
#   - length: LENGTH_0 - do not play any tone and do not interrupt previous tone
#             LENGTH_1 - sixteenth
#             LENGTH_2 - eighth
#             LENGTH_4 - quarter
#             LENGTH_8 - half
#             LENGTH_16 - whole
#   - tone: index to table above.
#
# Time consumption of this method must be same for every input!
# We must not use IFs or conditions - it is compiled as conditional jump and breaks time synchronization between robots
# We also must use internal methods, because public methods use IFs
def playTone(length, tone):
    # turn on or off LEDs
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, length >> 7)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, length >> 7)
    # transpose and set tone
    Ed.WriteModuleRegister16Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_FREQ_16, tones[tone + TRANSPOSITION])
    # real duration (1,2,4,8,16) is separate from input by masked upper bits
    # expression ((length & 127) * A + B) must be changed carefully together with length of empty cycle and with new commands
    Ed.WriteModuleRegister16Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_DURATION_16, (length & 127) * 7 + 1)
    # length constant for playing (LENGTH_1 .. LENGTH_16) has 7th bit == 1, LENGTH_0 has 7th bit == 0
    # we convert it by shift to 2 (for playing) or 0 (for do nothing)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_ACTION_8, length >> 6)

    t = 0
    # turn off LEDs
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 0)
    # empty cycle for decreasing tempo
    while t < 5:
        t = t + 1

# ------ Main Program --------

# wait 200 milliseconds to avoid triggering clap sensor by play button
Ed.WriteModuleRegister16Bit(Ed.MODULE_TIMERS, Ed.REG_TIMER_PAUSE_16, 20)
Ed.WriteModuleRegister8Bit(Ed.MODULE_TIMERS, Ed.REG_TIMER_ACTION_8, 2)

Ed.ClearModuleRegisterBit(Ed.MODULE_BEEPER, Ed.REG_BEEP_STATUS_8, Ed.CLAP_DETECTED_BIT)
while Ed.ReadModuleRegister8Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_STATUS_8) != 4:
    pass

#PAUSE IS 26, we can choose any value, but it must be between 0-46 after transposition
playTone(LENGTH_0, 26)#r
playTone(LENGTH_0, 26)
playTone(LENGTH_0, 26)
playTone(LENGTH_0, 26)

playTone(LENGTH_0, 26)#r
playTone(LENGTH_0, 26)
playTone(LENGTH_0, 26)
playTone(LENGTH_0, 26)

repeat = 0
while repeat < 2:
    playTone(LENGTH_1, 24)#b7
    playTone(LENGTH_1, 22)#a7
    playTone(LENGTH_1, 21)##g7
    playTone(LENGTH_1, 22)#a7
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_4, 25)#c8
    playTone(LENGTH_0, 25)
    playTone(LENGTH_0, 25)
    playTone(LENGTH_0, 25)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_1, 27)#d8
    playTone(LENGTH_1, 25)#c8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_1, 24)#b7
    playTone(LENGTH_1, 25)#c8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_4, 29)#e8
    playTone(LENGTH_0, 29)
    playTone(LENGTH_0, 29)
    playTone(LENGTH_0, 29)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_1, 30)#f8
    playTone(LENGTH_1, 29)#e8
    playTone(LENGTH_1, 28)##d8
    playTone(LENGTH_1, 29)#e8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_1, 36)#b8
    playTone(LENGTH_1, 34)#a8
    playTone(LENGTH_1, 33)##g8
    playTone(LENGTH_1, 34)#a8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_1, 36)#b8
    playTone(LENGTH_1, 34)#a8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_1, 33)##g8
    playTone(LENGTH_1, 34)#a8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_4, 37)#c9
    playTone(LENGTH_0, 37)
    playTone(LENGTH_0, 37)
    playTone(LENGTH_0, 37)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_2, 34)#a8
    playTone(LENGTH_0, 34)
    playTone(LENGTH_2, 37)#c9
    playTone(LENGTH_0, 37)#
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_2, 36)#b8
    playTone(LENGTH_0, 36)
    playTone(LENGTH_2, 34)#a8
    playTone(LENGTH_0, 34)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_2, 32)#g8
    playTone(LENGTH_0, 32)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_2, 34)#a8
    playTone(LENGTH_0, 34)#a8
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_2, 36)#b8
    playTone(LENGTH_0, 36)
    playTone(LENGTH_2, 34)#a8
    playTone(LENGTH_0, 34)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_2, 32)#g8
    playTone(LENGTH_0, 32)
    playTone(LENGTH_2, 34)#a8
    playTone(LENGTH_0, 34)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_2, 36)#b8
    playTone(LENGTH_0, 36)
    playTone(LENGTH_2, 34)#a8
    playTone(LENGTH_0, 34)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_2, 32)#g8
    playTone(LENGTH_0, 32)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    playTone(LENGTH_2, 31)##f8
    playTone(LENGTH_0, 31)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

    playTone(LENGTH_4, 29)#e8
    playTone(LENGTH_0, 29)
    playTone(LENGTH_0, 29)
    playTone(LENGTH_0, 29)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
    repeat = repeat + 1

#--------------------------------------------------------------

playTone(LENGTH_2,29)#e8
playTone(LENGTH_0,29)
playTone(LENGTH_2,30)#f8
playTone(LENGTH_0,30)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_2, 32)#g8
playTone(LENGTH_0, 32)
playTone(LENGTH_2, 32)#g8
playTone(LENGTH_0, 32)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 34)#a8
playTone(LENGTH_1, 32)#g8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 30)#f8
playTone(LENGTH_1, 29)#e8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 27)#d8
playTone(LENGTH_0, 27)
playTone(LENGTH_0, 27)
playTone(LENGTH_0, 27)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 29)#e8
playTone(LENGTH_0, 29)
playTone(LENGTH_2, 30)#f8
playTone(LENGTH_0, 30)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_2, 32)#g8
playTone(LENGTH_0, 32)
playTone(LENGTH_2, 32)#g8
playTone(LENGTH_0, 32)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 34)#a8
playTone(LENGTH_1, 32)#g8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 30)#f8
playTone(LENGTH_1, 29)#e8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 27)#d8
playTone(LENGTH_0, 27)
playTone(LENGTH_0, 27)
playTone(LENGTH_0, 27)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 25)#c8
playTone(LENGTH_0, 25)
playTone(LENGTH_2, 27)#d8
playTone(LENGTH_0, 27)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_2, 29)#e8
playTone(LENGTH_0, 29)
playTone(LENGTH_2, 29)#e8
playTone(LENGTH_0, 29)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 30)#f8
playTone(LENGTH_1, 29)#e8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 27)#d8
playTone(LENGTH_1, 25)#c8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 24)#b7
playTone(LENGTH_0, 24)
playTone(LENGTH_0, 24)
playTone(LENGTH_0, 24)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 25)#c8
playTone(LENGTH_0, 25)
playTone(LENGTH_2, 27)#d8
playTone(LENGTH_0, 27)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_2, 29)#e8
playTone(LENGTH_0, 29)
playTone(LENGTH_2, 29)#e8
playTone(LENGTH_0, 29)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 30)#f8
playTone(LENGTH_1, 29)#e8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 27)#d8
playTone(LENGTH_1, 25)#c8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 24)#b7
playTone(LENGTH_0, 24)
playTone(LENGTH_0, 24)
playTone(LENGTH_0, 24)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 24)#b7
playTone(LENGTH_1, 22)#a7
playTone(LENGTH_1, 21)# #g7
playTone(LENGTH_1, 22)#a7
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 25)#c8
playTone(LENGTH_0, 25)
playTone(LENGTH_0, 25)
playTone(LENGTH_0, 25)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 27)#d8
playTone(LENGTH_1, 25)#c8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 24)#b7
playTone(LENGTH_1, 25)#c8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 29)#e8
playTone(LENGTH_0, 29)
playTone(LENGTH_0, 29)
playTone(LENGTH_0, 29)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 30)#f8
playTone(LENGTH_1, 29)#e8
playTone(LENGTH_1, 28)# #d8
playTone(LENGTH_1, 29)#e8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_1, 36)#b8
playTone(LENGTH_1, 34)#a8
playTone(LENGTH_1, 33)# #g8
playTone(LENGTH_1, 34)#a8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 36)#b8
playTone(LENGTH_1, 34)#a8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 33)# #g8
playTone(LENGTH_1, 34)#a8
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 37)#c9
playTone(LENGTH_0, 37)
playTone(LENGTH_0, 37)
playTone(LENGTH_0, 37)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 34)#a8
playTone(LENGTH_0, 34)
playTone(LENGTH_2, 36)#b8
playTone(LENGTH_0, 36)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_2, 37)#c9
playTone(LENGTH_0, 37)
playTone(LENGTH_2, 36)#b8
playTone(LENGTH_0, 36)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 34)#a8
playTone(LENGTH_0, 34)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 33)# #g8
playTone(LENGTH_0, 33)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_2, 34)#a8
playTone(LENGTH_0, 34)
playTone(LENGTH_2, 29)#e8
playTone(LENGTH_0, 29)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 30)#f8
playTone(LENGTH_0, 30)
playTone(LENGTH_2, 27)#d8
playTone(LENGTH_0, 27)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 25)#c8
playTone(LENGTH_0, 25)
playTone(LENGTH_0, 25)
playTone(LENGTH_0, 25)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_2, 24)#b7
playTone(LENGTH_0, 24)
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync
playTone(LENGTH_1, 22)#a7
playTone(LENGTH_1, 24)#b7
Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0) #compensation of some unexplained unsync

playTone(LENGTH_4, 22)#a7
playTone(LENGTH_0, 22)
playTone(LENGTH_0, 22)
playTone(LENGTH_0, 22)
