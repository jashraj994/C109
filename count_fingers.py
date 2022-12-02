import cv2
import mediapipe as mp 
from pynput.keyboard import Key,Controller
#import pyautogui 
keyboard = Controller()
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence = 0.8,min_tracking_confidence = 0.5)

tipIds = [4,8,12,16,20]
state = None
cap = cv2.VideoCapture(0)

def countFingers(image,hand_landmarks,handNo = 0):
    global state

    if hand_landmarks:
        landmarks = hand_landmarks[handNo.landmark]
        fingers = []

        for lm_index in tipIds:
                # Get Finger Tip and Bottom y Position Value
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Check if ANY FINGER is OPEN or CLOSED
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # print("FINGER with id ",lm_index," is Open")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # print("FINGER with id ",lm_index," is Closed")

        totalFingers = fingers.count(1)

        if totalFingers == 4:
            state = "Play"

        if totalFingers == 0 and state == "Play":
            state = "Pause"
        
def drawHandLanmarks(image, hand_landmarks):
        
    # Darw connections between landmark points
    if hand_landmarks:
     for landmarks in hand_landmarks:
        mp_drawing.draw_landmarks(image,landmarks,mp_hands.HAND_CONNECTIONS)
 
 
while True:
     success, image = cap.read()
    
     image = cv2.flip(image,1)
     result = hands.process(image)
     hand_landmarks = result.multi_hand_landmarks
     drawHandLanmarks(image,hand_landmarks)
     countFingers(image,hand_landmarks)
     cv2.imshow("Media Controller", image)
    
     key = cv2.waitKey(1)
     if key == 27:
        break

cv2.destroyAllWindows()

