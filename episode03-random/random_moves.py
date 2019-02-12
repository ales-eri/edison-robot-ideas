#
# Description:  Robot Edison moves quickly in random directions, then he slows down, stops and waits to next clap
# Notes:        You can see result here: https://www.youtube.com/watch?v=LJejM69_9aY
#               You can upload program to Edison robot by online EdPy environment http://edpyapp.com/#
#               I use internal methods, because they are faster than public methods and I avoid linking public method source.
#               public method example -  Ed.DriveLeftMotor(Ed.FORWARD, speed, Ed.DISTANCE_UNLIMITED)
#               internal method example - Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_MOTOR, Ed.REG_MOTOR_CONTROL_8, 64 | speed)
#               If you have some questions, ask me in comments of the video: https://www.youtube.com/watch?v=LJejM69_9aY
#


import Ed

Ed.EdisonVersion = Ed.V2

Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_MEDIUM

CYCLE_DURATION = 60
SLOWING_DURATION = 12
START_SLOWING = CYCLE_DURATION - SLOWING_DURATION
slowed_speed = Ed.List(12, [7, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1])
wait_before_stop = Ed.List(12, [0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1])  # in centisecond
wait_after_stop = Ed.List(12,
                          [0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 1])  # in numbers of calculation random value for one step

random_tone = Ed.List(60, [17760, 23702, 19728, 12610, 29920, 15091, 22218, 30597, 24572, 28980,
                           13945, 26002, 27356, 11480, 29480, 30795, 7709, 21920, 27717, 16533,
                           17680, 17448, 18267, 24537, 21275, 12184, 14040, 29837, 19640, 21484,
                           18761, 11112, 4543, 11516, 16146, 16742, 27671, 19214, 30124, 26473,
                           25378, 16269, 17322, 15099, 17302, 21210, 17089, 30756, 25741, 20141,
                           8506, 15029, 7337, 16583, 26826, 23275, 28513, 5391, 13426,
                           32000])  # last lowest tone

# 128 - drive FORWARD, 64 - drive BACKWARD
random_left_motor = Ed.List(60, [128, 128, 64, 64, 128, 64, 64, 128, 128, 64,
                                 128, 64, 64, 64, 64, 64, 128, 128, 128, 64,
                                 128, 128, 128, 64, 64, 128, 64, 128, 128, 64,
                                 64, 64, 64, 64, 128, 128, 64, 64, 128, 64,
                                 128, 128, 128, 128, 128, 64, 128, 64,
                                 # in slowing phase I want to change direction in every step
                                 128, 128,
                                 128, 64, 64, 64, 128, 64, 128, 128, 64, 128])

# 128 - drive FORWARD, 64 - drive BACKWARD
random_right_motor = Ed.List(60, [64, 128, 64, 128, 128, 64, 128, 128, 64, 128,
                                  64, 128, 64, 64, 128, 128, 128, 64, 64, 128,
                                  64, 128, 128, 64, 128, 64, 64, 128, 64, 128,
                                  64, 128, 64, 128, 64, 64, 128, 128, 128, 64,
                                  64, 128, 64, 128, 64, 128, 128, 128,
                                  # in slowing phase I want to change direction in every step
                                  128, 64,
                                  128, 128, 64, 128, 64, 128, 64, 128, 64, 64])


def chaos():
    index = 0
    slowing_index = 0
    speed = Ed.SPEED_FULL
    while True:
        Ed.WriteModuleRegister16Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_FREQ_16, random_tone[index])
        Ed.WriteModuleRegister16Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_DURATION_16, 7)
        Ed.WriteModuleRegister8Bit(Ed.MODULE_BEEPER, Ed.REG_BEEP_ACTION_8, 2)
        # convert numbers 128/64 to 0/1 and use it to OFF/ON LEDs
        Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, random_left_motor[index] >> 7)
        Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, random_right_motor[index] >> 7)
        Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_MOTOR, Ed.REG_MOTOR_CONTROL_8, random_left_motor[index] | speed)
        Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_MOTOR, Ed.REG_MOTOR_CONTROL_8, random_right_motor[index] | speed)
        index += 1
        if index > START_SLOWING:
            speed = slowed_speed[slowing_index]
            if wait_before_stop[slowing_index] > 0:
                Ed.WriteModuleRegister16Bit(Ed.MODULE_TIMERS, Ed.REG_TIMER_PAUSE_16, wait_before_stop[slowing_index])
                Ed.WriteModuleRegister8Bit(Ed.MODULE_TIMERS, Ed.REG_TIMER_ACTION_8, 2)
            if wait_after_stop[slowing_index] > 0:
                Ed.Drive(Ed.STOP, Ed.SPEED_1, 1)
                # off LEDs
                Ed.WriteModuleRegister8Bit(Ed.MODULE_LEFT_LED, Ed.REG_LED_OUTPUT_8, 0)
                Ed.WriteModuleRegister8Bit(Ed.MODULE_RIGHT_LED, Ed.REG_LED_OUTPUT_8, 0)
                # slow by calculating random values for next cycles
                wait = 0
                while wait < wait_after_stop[slowing_index]:
                    wait += 1
                    rewrite_random()
            slowing_index += 1
            if index == CYCLE_DURATION:
                return index


random_index = 0
random_value = 111


# generate random values for sound and changing left/right motor state
# initial random values are in lists immediately after downloading program
def rewrite_random():
    global random_value, random_index, random_tone, random_left_motor, random_right_motor
    # linear congruential generator
    random_value = (random_value * 35) % 509
    # convert bit 0,1 to 128 - drive FORWARD, 64 - drive BACKWARD
    rnd_left = (2 - random_value % 2) << 6
    rnd_right = (2 - (random_value / 2) % 2) << 6
    # in slowing phase I want to change direction in every step
    if random_index >= START_SLOWING and rnd_left == random_left_motor[random_index - 1] and \
                    rnd_right == random_right_motor[random_index - 1]:
        return
    random_left_motor[random_index] = rnd_left
    random_right_motor[random_index] = rnd_right
    if random_index == CYCLE_DURATION - 1:
        # in the last step I want to play the lowest tone
        random_tone[random_index] = 32000
    else:
        random_tone[random_index] = random_value * 50 + 4000
    random_index += 1
    if random_index == CYCLE_DURATION:
        random_index = 0


while True:
    # wait 200 milliseconds to avoid triggering clap sensor by play button
    Ed.WriteModuleRegister16Bit(Ed.MODULE_TIMERS, Ed.REG_TIMER_PAUSE_16, 20)
    Ed.WriteModuleRegister8Bit(Ed.MODULE_TIMERS, Ed.REG_TIMER_ACTION_8, 2)
    # clean clap sensor
    Ed.ReadClapSensor()
    while Ed.ReadClapSensor() != Ed.CLAP_DETECTED:
        # calculate random values during waiting to clap
        rewrite_random()
    chaos()
