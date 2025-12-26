import cv2
import numpy as np
import hand_tracking_module as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Audio Setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol, max_vol = vol_range[0], vol_range[1]

# Init Detector
cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detection_con=0.8)

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)

    if len(lm_list) != 0:
        # Distance between Thumb (4) and Index (8)
        length, img, line_info = detector.get_distance(4, 8, img)
        
        # Mapping volume
        vol = np.interp(length, [50, 250], [min_vol, max_vol])
        volume.SetMasterVolumeLevel(vol, None)

        # Visual Volume Bar
        vol_bar = np.interp(length, [50, 250], [400, 150])
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
