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
        
        if keyboard.is_pressed('a'):
            pyautogui.press('left')
        elif keyboard.is_pressed('d'):
            pyautogui.press('right')
        elif keyboard.is_pressed('s'):
            pyautogui.press('down')
        elif keyboard.is_pressed('w'):
            pyautogui.press('up')
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
        # while True:
        #     print('The current pointer position is {0}'.format(mouse_pos.position))

        # num_threshold = (2150, 1400)
        up_threshold = (1360, 820)
        down_threshold = (1315, 972)
        left_threshold = (1119, 820)
        right_threshold = (1405, 826)
        
        difference = ()
        x_pos_dis = 0
        y_pos_dis = 0

        if not all(last_position):  # Check if tuple has any 'None' value
            # Set x and y values in last_position to the current location
            last_position = (x, y)
        else:
            # find the difference between the old x & y positions
            # ie zip( Last position, Current Position)
            current_location = mouse_pos.position  # Read pointer position
            difference = tuple(map(abs, tuple(
                x-y for x, y in zip(last_position, current_location))))

            x_pos_dis = difference[0]
            y_pos_dis = difference[1]

        # Left Threshold
        if (x_pos_dis > left_threshold[0] or y_pos_dis > left_threshold[1]):
            if (x_pos_dis > y_pos_dis and last_dir != "left"):
                pyautogui.press('left')
                print("left")
                last_dir = "left"
                last_position = (x, y)

        if (x_pos_dis > right_threshold[0] or y_pos_dis > right_threshold[1]):
            if (x_pos_dis > y_pos_dis and last_dir != "right"):
                pyautogui.press('right')
                print("right")
                last_dir = "right"
                last_position = (x, y)
        
        if (x_pos_dis > up_threshold[0] or y_pos_dis > up_threshold[1]):
            if (x_pos_dis > y_pos_dis and last_dir != "up"):
                pyautogui.press('up')
                print("up")
                last_dir = "up"
                last_position = (x, y)
        
        if (x_pos_dis > down_threshold[0] or y_pos_dis > down_threshold[1]):
            if (x_pos_dis > y_pos_dis and last_dir != "down"):
                pyautogui.press('down')
                print("down")
                last_dir = "down"
                last_position = (x, y)

                




        #         if last_dir != "left":
        #             # pyautogui.press('left')
        #             print("left")
        # elif (difference > num_threshold):
        #     if x_pos_dis > y_pos_dis:
        #         if last_dir != "up":
        #             print("up")
        #             last_dir = "up"
        #             last_position = (x, y)
        # elif (difference > num_threshold):
        #     if x_pos_dis > y_pos_dis:
        #         if last_dir != "right":
        #             # pyautogui.press('right')
        #             print("right")
        #             last_dir = "right"
        #             last_position = (x, y)
        # elif (difference > do num_threshold):
        #     if x_pos_dis > y_pos_dis:
        #         if last_dir != "down":
        #             # pyautogui.press('down')
        #             print("down")
        #             last_dir = "down"
        #             last_position = (x, y)

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
        #You will first get the frame by reading the frame from the video stream:
        vs.read()

        
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
    import speech_recognition as sr
    
    r = sr.Recognizer()
    
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
            except:
                print('Did not get that try Again')
                text = ''
            if text == "go up":
                pyautogui.press('up')
                #print(text)
            elif text == "go down":
                pyautogui.press('down')
                #print(text)
            elif text == "go left":
                pyautogui.press('left')
               #print(text)
            elif text == "go right":
                pyautogui.press('right')
                #print(text)



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
# x_pos_dis < 0 and
# y_pos_dis < 0 and
# x_pos_dis > 0 and
# y_pos_dis > 0 and
