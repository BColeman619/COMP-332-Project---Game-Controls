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
    # --------------------------------- #
    import keyboard
    # --------------------------------- #

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
    # --------------------------------- #

    def on_move(x, y):
        global last_position
        global last_dir
        num_threshold = (200, 300)
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
    colorLower = (255, 64, 103)  # Redish - #ff4067
    colorUpper = (255, 64, 171)  # Pinkish - #ff40ab

    # Set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen=buffer)

    # Store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    # Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    # Start video capture
    video_stream = mw.WebcamVideoStream().start()

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

        redish_mask = cv2.inRange(hsv_format, colorLower, colorUpper)
        redish_mask = cv2.erode(redish_mask, None, iterations=2)
        redish_mask = cv2.dilate(redish_mask, None, iterations=2)

        # Finding the contours; Function will return a tuple or two items. We will only need the first:
        contours = cv2.findContours(redish_mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        # Track the center
        center = None

        # If we found any contours; if > 0:

        if(len(contours) > 0):
            largest_contour = max(contours, key=cv2.contourArea)
            # Returns a tuple-the radius, the second of the tuple values:
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            M = cv2.moments(largest_contour)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Only if the radius is larger than 10; add the center
            if radius > 10:
                pts.appendleft(center)

        if num_frames >= 10 and len(pts) >= 10:
            # In `dX` and `dY`, store the difference between the x and y values
            x_diff = (x - pts[0])  # 1st frame
            y_diff = (y - pts[9])  # 2nd frame
            (dX, dY) = (x_diff, y_diff)

        continue

# End color_tracker()------------------------------------------------------- #


def finger_tracking():
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    cap = cv2.VideoCapture(0)
    # TODO: change this and am
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                          max_num_hands=2,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y*h)
                    # if id ==0:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                #Thumb: landmarkList[4][1] < landmarkList[3][1]
                # Index finger: landmarkList[8][2] < landmarkList[6][2]
                # Middle finger: landmarkList[12][2] < landmarkList[10][2]
                # Ring finger: landmarkList[16][2] < landmarkList[14][2]
                # Little finger: landmarkList[20][2] < landmarkList[18][2]

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    # put your code here


# End finger_tracking()----------------------------------------------------- #


def unique_control():
    import speech_recognition as sr
    # need to install speechreconition

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

    """   
        KEEP UNTIL
        frame = vs.read()
        frame = cv2.flip(frame, 1)
        # TODO: Maybe the parameters need to be changed.
        frame = imutils.resize(frame, width=600)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_green = cv2.inRange(frame, colorLower, colorUpper)
        mask_gold = cv2.inRange(frame, colorLower, colorUpper)

        mask_green = cv2.erode(mask_green, None, iterations=2)
        mask_gold = cv2.erode(mask_gold, None, iterations=2)

        mask_green = cv2.dilate(mask_green, None, iterations=2)
        mask_gold = cv2.dilate(mask_gold, None, iterations=2)

        # bit_mask = cv2.bitwise_not(mask_green, mask_gold)

        # List of all of pts. Function will return a tuple or two items. We will only need the first:
        contours = cv2.findContours(
            mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Center of our object to find its location
        center = None

        # This next part we will only do if we found any contours (the list returned is greater than 0).
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            radius = cv2.minEnclosingCircle(
                largest_contour)  
            # ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)# keep until sure
            M = cv2.moments(largest_contour)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            if radius[1] > 10:
                pts.appendleft(center)

        # Next, we will find the direction. We will only find the direction if we have seen at least 10frames (`num_frames`) and there are at least 10 contours in `pts'
        # TODO - Here Cameron
        if num_frames >= 10 and len(pts) >= 10:
            difference = pts[10] - pts[0]

        continue
 """
