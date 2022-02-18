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
# End keypress()------------------------------------------------------------ #


def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse
    from pynput.mouse import Controller  # Added for reading pointer
    mouse_pos = Controller()

    def on_move(x, y):
        global last_position
        global last_dir
        # Read pointer position
        print('The current pointer position is {0}'.format(mouse_pos.position))

        up_threshold = (5, 5)
        down_threshold = (5, 5)
        left_threshold = (5, 5)
        right_threshold = (5, 5)
        # up_threshold = (1360, 820)
        # down_threshold = (1315, 972)
        # left_threshold = (1119, 820)
        # right_threshold = (1405, 826)
        x_pos_dis = 0
        y_pos_dis = 0

        if not all(last_position):  # Check if tuple has any 'None' value
            # Set x and y values in last_position to the current location
            last_position = (x, y)
        else:
            # find the difference between the old x & y positions
            # ie zip( Last position, Current Position)
            current_location = mouse_pos.position  # Read pointer position
            difference = tuple(
                x-y for x, y in zip(last_position, current_location))
            x_pos_dis = difference[0]
            y_pos_dis = difference[1]

        if (x_pos_dis > left_threshold[0]):
            if x_pos_dis < 0 and last_dir != "left":
                pyautogui.press('left')
                # print("left")
                last_dir = "left"
                last_position = (x, y)
        if (y_pos_dis > up_threshold[1]):
            if y_pos_dis < 0 and last_dir != "up":
                pyautogui.press('up')
                # print("up")
                last_dir = "up"
                last_position = (x, y)
        if (x_pos_dis > right_threshold[0]):
            if x_pos_dis > 0 and last_dir != "right":
                pyautogui.press('right')
                # print("right")
                last_dir = "right"
                last_position = (x, y)
        if (y_pos_dis > down_threshold[1]):
            if y_pos_dis > 0 and last_dir != "down":
                pyautogui.press('down')
                # print("down")
                last_dir = "down"
                last_position = (x, y)
        # Mouse movement; negative or positive

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
# End color_tracker()------------------------------------------------------- #


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
# End finger_tracking()----------------------------------------------------- #


def unique_control():
    # put your code here
    pass
# End unique_control()------------------------------------------------------ #


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
# End main()---------------------------------------------------------------- #
