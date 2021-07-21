import numpy as np
import cv2


cap = cv2.VideoCapture("uvc_test.avi")



while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("read", frame)
    cv2.waitKey(1)