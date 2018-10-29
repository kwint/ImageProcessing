'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)
'''
# from pypylon import pylon
import cv2
import numpy as np

def change_brightness_contrast(img, b, c): # Adds brightness and contrast
    return cv2.addWeighted(img, 1. + c / 127., img, 0, b - c)


def noisefilter(img): # Removes noise
    for i in range(0, len(img) - 1):
        for j in range(0, len(img[0]) - 1):
            if all(img[i, j] == [255, 255, 255]) or all(img[i, j] == [0, 255, 0]) or all(
                    img[i, j] == [0, 0, 255]) or all(img[i, j] == [255, 0, 0]) or all(img[i, j] <= [0, 0, 0]):
                surrounding = np.array([])
                if not (all(img[i + 1, j] == [255, 255, 255]) or all(img[i + 1, j] == [0, 255, 0]) or all(
                    img[i + 1, j] == [0, 0, 255]) or all(img[i + 1, j] == [255, 0, 0]) or all(img[i + 1, j] <= [0, 0, 0])):
                    surrounding = np.append(surrounding, img[i+1, j])

                if not (all(img[i - 1, j] == [255, 255, 255]) or all(img[i - 1, j] == [0, 255, 0]) or all(
                    img[i - 1, j] == [0, 0, 255]) or all(img[i - 1, j] == [255, 0, 0]) or all(img[i - 1, j] <= [0, 0, 0])):
                    surrounding = np.append(surrounding, img[i-1, j])

                if not (all(img[i, j+1] == [255, 255, 255]) or all(img[i, j+1] == [0, 255, 0]) or all(
                        img[i, j+1] == [0, 0, 255]) or all(img[i, j+1] == [255, 0, 0]) or all(img[i, j+1] <= [0, 0, 0])):
                    surrounding = np.append(surrounding, img[i, j+1])

                if not (all(img[i, j-1] == [255, 255, 255]) or all(img[i, j-1] == [0, 255, 0]) or all(
                        img[i, j-1] == [0, 0, 255]) or all(img[i, j-1] == [255, 0, 0]) or all(img[i, j-1] <= [0, 0, 0])):
                    surrounding = np.append(surrounding, img[i, j-1])

                surrounding_added = 0
                surrounding = np.reshape(surrounding, [len(surrounding) // 3, 3])
                print(surrounding)

                for ii in range(0, len(surrounding)):
                    surrounding_added = surrounding_added + surrounding[ii] // len(surrounding)
                print(surrounding_added)
                img[i, j] = surrounding_added
                print(img[i, j])
    return img


img = cv2.imread('pixerror.png', 1) # Read Image

cv2.namedWindow('normal', cv2.WINDOW_NORMAL)
cv2.namedWindow('nonoise', cv2.WINDOW_NORMAL)
cv2.imshow('normal', img) # show original image
cv2.imshow('nonoise', change_brightness_contrast(noisefilter(img), 50, 0)) # Filter image and add brightness, and show it

cv2.waitKey(0)
