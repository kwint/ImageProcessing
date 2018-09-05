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


cv2.namedWindow('slider', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('slider', 640, 0)
cv2.resizeWindow('slider', 560, 400)
cv2.createTrackbar('B', 'slider', 0, 255, nothing)
cv2.createTrackbar('C', 'slider', 0, 255, nothing)


# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# camera.GetDeviceInfo().SetPropertyValue("Expose time", "8")
# cam.properties['ExposureTime'] = 1000

converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(20, pylon.TimeoutHandling_ThrowException)  # Change number for speed

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('normal', cv2.WINDOW_NORMAL)
        cv2.namedWindow('edited', cv2.WINDOW_NORMAL)
        cv2.imshow('normal', img)
        cv2.imshow('edited', change_brightness_contrast(img, cv2.getTrackbarPos('B', 'slider'), cv2.getTrackbarPos('C', 'slider')))
        k = cv2.waitKey(1)
        if k == 27:
            break
    grabResult.Release()

# Releasing the resource
camera.StopGrabbing()

cv2.destroyAllWindows()
