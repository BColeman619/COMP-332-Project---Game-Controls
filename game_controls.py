import pyautogui

last_position = (None, None)
last_dir = ''


def keypress():
    ''' 
    Choose any four keys that a user can press to control the game.
    Update this doc string with your choices. 
    '''

    import keyboard

    # put your code here
    while True:
        # function works according to terminal, but not sure on how to test with the games
        if keyboard.is_pressed('a'):
            pyautogui.press('left')
            # print("left")----- Testing
        elif keyboard.is_pressed('d'):
            pyautogui.press('right')
            # print("right")----- Testing
        elif keyboard.is_pressed('s'):
            pyautogui.press('down')
            # print("down")----- Testing
        elif keyboard.is_pressed('w'):
            pyautogui.press('up')
            # print("up")----- Testing


def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        # put your code here
        # if last_position[0] == None and last_position[1] == None:
        #last_position = (pyautogui.position())

        if not all(last_position):  # Check if tuple has any 'None' value
            # Set x and y values in last_position to the current location
            last_position(x, y)
        else:
            # find the difference between the old x & y positions
            difference = tuple(
                x-y for x, y in zip(last_position,  last_position(x, y)))

            x_pos_dis = difference[0]
            y_pos_dis = difference[1]
            """ TODO
            THIS IS NEXT THE TOP SHOULD WORK
            Given that there will always be some small movement with your hand when you are holding still, you need to check to see if the absolute differences are greater than some threshold. You should choose this threshold by trying out different numbers and see what works for your group. Only if the x difference or y difference is greater than the threshold should you try to use it for a direction. We use this threshold to prevent trying to move left 30 times for a single movement. Instead we only update our direction and position if we have moved far enough.
            
             """

        # print("None")
        pass

    with mouse.Listener(on_move=on_move) as listener:
        listener.join()

# End trackpad_mouse()------------------------------------------------------ #


def color_tracker():
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = None
    colorUpper = None

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen=buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    # Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    # Start video capture
    vs = mw.WebcamVideoStream().start()

    while True:
        # your code here
        continue


def finger_tracking():
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    # Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    # Start video capture
    vs = mw.WebcamVideoStream().start()

    # put your code here


def unique_control():
    # put your code here
    pass


def main():
    control_mode = input("How would you like to control the game? ")
    if control_mode == '1':
        keypress()
    elif control_mode == '2':
        trackpad_mouse()
    elif control_mode == '3':
        color_tracker()
    elif control_mode == '4':
        finger_tracking()
    elif control_mode == '5':
        unique_control()


if __name__ == '__main__':
    main()
