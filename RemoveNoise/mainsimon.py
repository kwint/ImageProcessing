import cv2
import numpy as np

# PLZ GIT WORK v2
def change_brightness_contrast(img, b, c):  # Adds brightness and contrast
    return cv2.addWeighted(img, 1. + c / 127., img, 0, b - c)


def check_high_value(pixel):
    if all(pixel == [255, 255, 255]) or all(pixel == [0, 255, 0]) or all(pixel == [0, 0, 255]) or all(
            pixel == [255, 0, 0]) or all(pixel <= [0, 0, 0]):
        return True
    else:
        return False


def noisefilter(img):  # Removes noise
    for i in range(0, len(img) - 1):
        for j in range(0, len(img[0]) - 1):
            if check_high_value(img[i, j]):
                surrounding = np.array([])
                if not check_high_value(img[i + 1, j]):
                    surrounding = np.append(surrounding, img[i + 1, j])

                if not check_high_value(img[i - 1, j]):
                    surrounding = np.append(surrounding, img[i - 1, j])

                if not check_high_value(img[i, j + 1]):
                    surrounding = np.append(surrounding, img[i, j + 1])

                if not check_high_value(img[i, j - 1]):
                    surrounding = np.append(surrounding, img[i, j - 1])

                if not check_high_value(img[i + 1, j + 1]):
                    surrounding = np.append(surrounding, img[i + 1, j + 1])

                if not check_high_value(img[i - 1, j - 1]):
                    surrounding = np.append(surrounding, img[i - 1, j - 1])

                if not check_high_value(img[i - 1, j + 1]):
                    surrounding = np.append(surrounding, img[i - 1, j + 1])

                if not check_high_value(img[i + 1, j - 1]):
                    surrounding = np.append(surrounding, img[i + 1, j - 1])

                surrounding_added = 0
                surrounding = np.reshape(surrounding, [len(surrounding) // 3, 3])
                # print(surrounding)

                for ii in range(0, len(surrounding)):
                    surrounding_added = surrounding_added + surrounding[ii] // len(surrounding)
                # print(surrounding_added)
                img[i, j] = surrounding_added
                # print(img[i, j])
    return img


img = cv2.imread('pixerror.png', 1)  # Read Image

cv2.namedWindow('normal', cv2.WINDOW_NORMAL)
cv2.namedWindow('nonoise', cv2.WINDOW_NORMAL)
cv2.imshow('normal', img)  # show original image
cv2.imshow('nonoise',
           change_brightness_contrast(noisefilter(img), 50, 0))  # Filter image and add brightness, and show it

cv2.imwrite("result.png", img)
cv2.waitKey(0)
