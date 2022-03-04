'''
    File name: game_controls.py
    Authors: Naveen Kumar Rajesh, Blaine Coleman, Cameron Williams
    Date created: 02/08/2022
    Date last modified: 03/03/2022
    Python Version: 3.9.4
'''
# --------------------------------- #
import pyautogui
# --------------------------------- #

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

    # --------------------------------- #
    from pynput import mouse
    from pynput.mouse import Controller  # Added for reading pointer
    mouse_pos = Controller()
    # --------------------------------- #

    def on_move(x, y):
        global last_position
        global last_dir
        num_threshold = (200, 300)
        # difference = ()
        x_pos_dis = 0
        y_pos_dis = 0

        if not all(last_position):  # Check if tuple has any 'None' value
            # Set x and y values in last_position to the current location
            last_position = (x, y)
        else:
            # find the difference between the old x & y positions

            x_pos_dis = abs(x - last_position[0])
            y_pos_dis = abs(y - last_position[1])

            if (x_pos_dis > num_threshold[0]):
                if (x_pos_dis > 0 and last_dir != "left"):
                    pyautogui.press('left')
                    # print("left\n") # Testing
                    last_dir = "left"
                    last_position = (x, y)
                else:
                    pyautogui.press('right')
                    # print("right\n") # Testing
                    last_dir = "right"
                    last_position = (x, y)

            elif (y_pos_dis > num_threshold[1]):
                if (y_pos_dis > 0 and last_dir != "up"):
                    pyautogui.press('up')
                    # print("up\n") # Testing
                    last_dir = "up"
                    last_position = (x, y)
                else:
                    pyautogui.press('down')
                    # print("down\n") # Testing
                    last_dir = "down"
                    last_position = (x, y)

    with mouse.Listener(on_move=on_move) as listener:
        listener.join()

# End trackpad_mouse()------------------------------------------------------ #


def color_tracker():
    # --------------------------------- #
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw
    # --------------------------------- #

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = (29, 86, 6)  # green
    colorUpper = (64, 255, 255)  # darkish green

    # Set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen=buffer)

    # Store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    num_threshold = (100, 100)  # Threshold for direction

    # Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    # Start video capture
    video_stream = mw.WebcamVideoStream().start()
    # video_stream = cv2.VideoCapture(0) import the crap

    while True:
        # Reading the frame from the video stream
        frame = video_stream.read()
        # Using that frame, you will flip it
        frame = cv2.flip(frame, 1)
        # You will then resize the frame
        frame = imutils.resize(frame, width=600)
        # You then want to blur the image the reduce the noise in it
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        # Finally, you need to convert the colors to HSV:
        hsv_format = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        green_mask = cv2.inRange(hsv_format, colorLower, colorUpper)
        green_mask = cv2.erode(green_mask, None, iterations=2)
        green_mask = cv2.dilate(green_mask, None, iterations=2)

        # Finding the contours; Function will return a tuple or two items. We will only need the first:
        contours, ext = cv2.findContours(
            green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Track the center
        center = None

        # If we found any contours; if > 0:

        if(len(contours) > 0):
            largest_contour = max(contours, key=cv2.contourArea)
            # Returns a tuple-the radius, the second of the tuple values:
            radius = cv2.minEnclosingCircle(largest_contour)[1]

            M = cv2.moments(largest_contour)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Only if the radius is larger than 10; add the center
            if radius > 10:
                pts.appendleft(center)

        if num_frames >= 10 and len(pts) >= 10:
            # In `dX` and `dY`, store the difference between the x and y values
            x_diff = pts[9][0] - pts[0][0]  # 1st frame
            y_diff = pts[9][1] - pts[0][1]  # 2nd frame
            (dX, dY) = (x_diff, y_diff)

        if (abs(dX) > num_threshold[0] or abs(dY) > num_threshold[1]):
            # setting direction
            if(abs(dX) > abs(dY)):
                if ((dX < 0) and (last_dir != "right")):
                    direction = "right"
                elif ((dX > 0) and (last_dir != "left")):
                    direction = "left"
            # up and down
            elif (abs(dX) < abs(dY)):
                if ((dY < 0) and (last_dir != "down")):
                    direction = "down"
                elif ((dY > 0) and (last_dir != "up")):
                    direction = "up"

            # Show Direction
            cv2.putText(frame, direction, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            if (direction == "left"):
                last_dir = "left"
                pyautogui.press("left")
                # print("left") # Testing
            elif (direction == "right"):
                last_dir = "right"
                pyautogui.press("right")
                # print("right") # Testing
            elif (direction == "up"):
                last_dir = "up"
                pyautogui.press("up")
                # print("up") # Testing
            elif (direction == "down"):
                last_dir = "down"
                pyautogui.press("down")
                # print("down") # Testing

        # Show the frame on screen
        cv2.imshow('Game Control Window', frame)
        cv2.waitKey(1)
        num_frames += 1

# End color_tracker()------------------------------------------------------- #


def finger_tracking():
    # --------------------------------- #
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp
    # --------------------------------- #

    # Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)

    video_stream = mw.WebcamVideoStream().start()

    # hand detection
    one_hand = mp.solutions.hands

    # getting basic info
    hands = one_hand.Hands(static_image_mode=False, max_num_hands=2,
                           min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # draw
    mpDraw = mp.solutions.drawing_utils

    # track last direction
    global last_dir

    while True:

        finger_count = 0
        landmark_list = []

        # Reading the frame from the video stream
        frame = video_stream.read()
        # Using that frame, you will flip it
        frame = cv2.flip(frame, 1)
        # Resize the frame
        frame = imutils.resize(frame, width=600)
        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # print(results.multi_hand_landmarks)

        # Results from processing the image for hands
        results = hands.process(rgb)

        landmarks = results.multi_hand_landmarks

        # Loop though all of the "multi_hand_landmarks"
        if landmarks != None:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w = rgb.shape[0:2]  # getting dimensions
                    cx, cy = int(lm.x * w), int(lm.y*h)
                    cv2.circle(rgb, (cx, cy), 3, (255, 0, 255),
                               cv2.FILLED)  # see on frame
                    landmark_list.append((id, cx, cy))
                mpDraw.draw_landmarks(
                    frame, handLms, one_hand.HAND_CONNECTIONS)  # draw

            if landmark_list != None:
                thumb = landmark_list[4][1] < landmark_list[3][1]
                index = landmark_list[8][2] < landmark_list[6][2]
                middle = landmark_list[12][2] < landmark_list[10][2]
                ring = landmark_list[16][2] < landmark_list[14][2]
                little = landmark_list[20][2] < landmark_list[18][2]

            if thumb == True:  # keeping track of the number of fingers held up
                finger_count += 1
            if index == True:
                finger_count += 1
            if middle == True:
                finger_count += 1
            if ring == True:
                finger_count += 1
            if little == True:
                finger_count += 1

            if finger_count != 0:  # Mapping controls for finger value
                if finger_count == 1 and last_dir != "up":
                    pyautogui.press("up")
                    # print("up") # Testing
                    finger_count = 1
                    last_dir = "up"
                if finger_count == 2 and last_dir != "down":
                    pyautogui.press("down")
                    # print("down") # Testing
                    finger_count = 2
                    last_dir = "down"
                if finger_count == 3 and last_dir != "left":
                    pyautogui.press("left")
                    # print("left") # Testing
                    finger_count = 3
                    last_dir = "left"
                if finger_count == 4 and last_dir != "right":
                    pyautogui.press("right")
                    # print("right") # Testing
                    finger_count = 4
                    last_dir = "right"

        # display finger counts on screen
        cv2.putText(frame, str(int(finger_count)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", frame)
        cv2.waitKey(1)

# End finger_tracking()----------------------------------------------------- #


def unique_control():
    # --------------------------------- #
    import speech_recognition as sr
    # --------------------------------- #

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
                # print(text)
            elif text == "go down":
                pyautogui.press('down')
                # print(text)
            elif text == "go left":
                pyautogui.press('left')
                # print(text)
            elif text == "go right":
                pyautogui.press('right')
                # print(text)

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
