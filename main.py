# Choose 2 points in an image to extract the foreground
# Have fun!!
import cv2
import numpy as np


refPt = []
new = []


def foregroundExtraction(img):
    mask = np.zeros(img.shape[:2], np.uint8)    # mask with dimensions (rows, cols)
    print(img.shape)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # (x,y, cols, rows)
    rect = (min(refPt[0][0], refPt[1][0]), min(refPt[0][1], refPt[1][1]), abs(refPt[0][0] - refPt[1][0]), abs(refPt[0][1] - refPt[1][1]))       # try to automate this part with mouse events

    # this modifies mask with 0,1,2,3 and the 5 param is the no. of iterations
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 8, cv2.GC_INIT_WITH_RECT)
    # 0,2 are foreground, 1,3 are background
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    return img


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Put the clicks coordinates in a variable
        print(1)
        refPt.append([x, y])
        if len(refPt) >= 2:
            new.append([x, y])
            if len(new) == 2:
                flag = 0
                refPt.clear()
                refPt.append([new[0][0], new[0][1]])
                refPt.append([new[1][0], new[1][1]])
                new.clear()


if __name__ == "__main__":
    while 1:
        img = cv2.imread('picture.jpg')
        if len(refPt) > 1:
            img = foregroundExtraction(img)
        cv2.imshow("pic", img)
        cv2.setMouseCallback("pic", click_event)
        k = cv2.waitKey(1)
        if k == 27:
            break
