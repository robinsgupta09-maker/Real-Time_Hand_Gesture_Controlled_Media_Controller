
import cv2
import time
import numpy as np
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()  # Returns (-65.25, 0.0, 0.03125)
min_vol, max_vol = vol_range[0], vol_range[1]

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
           
            lm_list = []
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
            
            if lm_list:
                x1, y1 = lm_list[4][1], lm_list[4][2]
                x2, y2 = lm_list[8][1], lm_list[8][2]
                
   
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                
               
                length = math.hypot(x2 - x1, y2 - y1)
                
                
                vol = np.interp(length, [50, 300], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol, None)
                
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
