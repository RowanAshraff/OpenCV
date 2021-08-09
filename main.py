# Click on any colour in the video to subtract it from the video, you can change the VarThreshold, history, and Kernel as you please
## Havee fun!!

import cv2
import numpy as np
fgbg = []


def trackbar_callback(x):
    global fgbg
    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=cv2.getTrackbarPos('VarThreshold', 'img'), history=cv2.getTrackbarPos('History', 'img'))


def backgroundSubtraction(frame, fgbg):
    fmask = fgbg.apply(frame)
    res = cv2.bitwise_and(frame, frame, mask=fmask)
    return res


def morphologicalTransformations(m, frame, kernel):
    # case 'w'
    if m == 1:
        image = cv2.erode(frame, kernel, iterations=1)
    # case 'x'
    elif m == 2:
        image = cv2.dilate(frame, kernel, iterations=1)
    # case 'y'
    elif m == 3:
        image = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    # case 'z'
    elif m == 4:
        image = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    else:
        image = frame
    return image


if __name__ == "__main__":
    m = 0
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('img')
    cv2.resizeWindow('img', 400, 150)
    img = np.zeros((512, 100, 3), np.uint8)

    cv2.createTrackbar('VarThreshold', 'img', 0, 300, trackbar_callback)
    cv2.createTrackbar('Kernel', 'img', 0, 15, trackbar_callback)
    cv2.createTrackbar('History', 'img', 0, 3000, trackbar_callback)
    cv2.setTrackbarPos('VarThreshold', 'img', 16)
    cv2.setTrackbarPos('History', 'img', 400)
    fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=16, history=400)
    print(fgbg)
    while 1:
        _, frame = cap.read()
        kernel = np.ones((cv2.getTrackbarPos('Kernel', 'img'), cv2.getTrackbarPos('Kernel', 'img')), np.float32) / 25
        frame = morphologicalTransformations(m, frame, kernel)
        frame = backgroundSubtraction(frame, fgbg)
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1) & 0xff
        if k == ord('w'):
            m = 1
        elif k == ord('x'):
            m = 2
        elif k == ord('y'):
            m = 3
        elif k == ord('z'):
            m = 4
        elif k == ord('a'):
            m = 0
        if k == 27:
            break
cv2.destroyAllWindows()
cap.release()
