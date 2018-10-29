'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)
'''
from pypylon import pylon
import cv2


def nothing(x):
    pass


def change_brightness_contrast(img, b, c):
    return cv2.addWeighted(img, 1. + c / 127., img, 0, b - c)


def noisefilter(img):
    for i in range(0, len(img)):
        for j in range(0, len(img[0])):
            # if img[i, j] == [255, 255, 255] or img[i, j] == [0, 255, 0] or img[i, j] == [0, 0, 255] or img[i, j] == [
            #     255, 0, 0]:
            if filter (lambda x : x >= 225, img[i, j]):
                surrounding = img[i + 1, j] + img[i - 1, j] + img[i, j + 1] + img[i, j - 1]
                img[i, j] = surrounding / 4
    return img

cv2.namedWindow('slider', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('slider', 640, 0)
cv2.resizeWindow('slider', 560, 400)
cv2.createTrackbar('templateWindow', 'slider', 0, 255, nothing)
cv2.createTrackbar('searchWindow', 'slider', 0, 255, nothing)
cv2.createTrackbar('h', 'slider', 0, 255, nothing)
cv2.createTrackbar('hColor', 'slider', 0, 255, nothing)

img = cv2.imread('pixerror.png', 1)

while True:
    cv2.namedWindow('normal', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('edited', cv2.WINDOW_NORMAL)
    cv2.namedWindow('nonoise', cv2.WINDOW_NORMAL)
    templateWindow = cv2.getTrackbarPos('templateWindow', 'slider')
    searchWindow = cv2.getTrackbarPos('searchWindow', 'slider')
    h = cv2.getTrackbarPos('h', 'slider')
    hColor = cv2.getTrackbarPos('hColor', 'slider')
    # dst = cv2.fastNlMeansDenoisingColored(img, None, templateWindow, searchWindow, h, hColor)
    cv2.imshow('nonoise', noisefilter(img))
    cv2.imshow('normal', img)
    cv2.imshow('edited',
               change_brightness_contrast(img, cv2.getTrackbarPos('B', 'slider'), cv2.getTrackbarPos('C', 'slider')))
    k = cv2.waitKey(1)
    print("loop")
    if k == 27:
        break

cv2.destroyAllWindows()
