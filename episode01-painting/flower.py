#
# Description:  Edison robot draws/paints flower, grass and sun.
# Notes:        You can see result here: https://www.youtube.com/watch?v=-j4arUWRhj8
#               You can upload program to Edison robot by online EdPy environment http://edpyapp.com/#
#               You need paper A3 size.
#               You should use robot with good gears and full batteries
#               You must move robot to the right place after every part and press round button.
#               You must attach pen/brush to the back of robot for flower and to the front for rest of the picture.
#               If you have some questions, ask me in comments of the video: https://www.youtube.com/watch?v=-j4arUWRhj8
#

import Ed
Ed.EdisonVersion = Ed.V2
Ed.DistanceUnits = Ed.CM
Ed.Tempo = Ed.TEMPO_VERY_FAST

random_grass_length = Ed.List(23, [10,17,15,24,15,11,12,28,17,11,14,20,18,10,17,15,28,13,18,20,11,24,15])
random_grass_distance = Ed.List(23, [1,2,1,2,2,1,2,2,2,1,1,2,1,2,2,2,2,1,1,2,2,1])

round_button = False
PAUSE_LENGTH = 2

def buttonEvent():
    global round_button
    round_button = True

def waitToRoundButton():
    global round_button
    round_button = False
    Ed.PlayTone(15289,100)
    while round_button == False:
        pass
    Ed.PlayTone(7644,100)
    Ed.TimeWait(PAUSE_LENGTH, Ed.TIME_SECONDS);

Ed.RegisterEventHandler(Ed.EVENT_KEYPAD_ROUND, "buttonEvent");

#flower
Ed.PlayTone(7644,100)
Ed.TimeWait(PAUSE_LENGTH, Ed.TIME_SECONDS);
i = 0
while i<10:
    Ed.Drive(Ed.SPIN_LEFT,1,35);
    Ed.Drive(Ed.BACKWARD,1,5);
    Ed.Drive(Ed.FORWARD,1,5);
    Ed.TimeWait(2000, Ed.TIME_MILLISECONDS);
    i = i + 1;
waitToRoundButton()

#stalk
Ed.Drive(Ed.BACKWARD,3,5);
i = 0
while i<2:
    Ed.Drive(Ed.FORWARD_RIGHT ,3,50);
    Ed.Drive(Ed.BACKWARD_RIGHT ,3,50);
    Ed.Drive(Ed.BACKWARD,3,4);
    Ed.Drive(Ed.FORWARD_LEFT ,3,50);
    Ed.Drive(Ed.BACKWARD_LEFT ,3,50);
    Ed.Drive(Ed.BACKWARD,3,4);
    i = i + 1;
waitToRoundButton()

#grass
i = 0
while i<22:
    Ed.Drive(Ed.BACKWARD ,2,random_grass_distance[i])
    Ed.Drive(Ed.FORWARD_RIGHT ,2,random_grass_length[i])
    Ed.Drive(Ed.BACKWARD_RIGHT ,2,random_grass_length[i])
    i=i+1
waitToRoundButton()

#sun
i=0
while i<4:
    Ed.Drive(Ed.SPIN_RIGHT ,5, 25)
    Ed.Drive(Ed.FORWARD ,3, 3)
    Ed.Drive(Ed.BACKWARD ,3, 3)
    i = i + 1
Ed.Drive(Ed.SPIN_RIGHT ,5, 25)
waitToRoundButton()
